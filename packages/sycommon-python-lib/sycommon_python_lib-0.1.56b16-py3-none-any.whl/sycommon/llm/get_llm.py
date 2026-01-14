import os
from typing import Dict, Tuple, Type, List, Optional, Callable, Any
from langfuse import Langfuse, get_client, propagate_attributes
from sycommon.config.Config import Config
from sycommon.llm.llm_logger import LLMLogger
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable, RunnableLambda, RunnableConfig
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, ValidationError, Field
from sycommon.config.LLMConfig import LLMConfig
from sycommon.llm.llm_tokens import TokensCallbackHandler
from sycommon.logging.kafka_log import SYLogger
from sycommon.tools.env import get_env_var
from langfuse.langchain import CallbackHandler


class StructuredRunnableWithToken(Runnable):
    """带Token统计的Runnable类"""

    def __init__(self, retry_chain: Runnable, langfuse: Langfuse):
        super().__init__()
        self.retry_chain = retry_chain
        self.langfuse = langfuse
        self.metadata = {"langfuse_session_id": SYLogger.get_trace_id()}

    def _adapt_input(self, input: Any) -> List[BaseMessage]:
        """适配输入格式"""
        if isinstance(input, list) and all(isinstance(x, BaseMessage) for x in input):
            return input
        elif isinstance(input, BaseMessage):
            return [input]
        elif isinstance(input, str):
            return [HumanMessage(content=input)]
        elif isinstance(input, dict) and "input" in input:
            return [HumanMessage(content=str(input["input"]))]
        else:
            raise ValueError(f"不支持的输入格式：{type(input)}")

    def _get_callback_config(self, config: Optional[RunnableConfig] = None) -> tuple[RunnableConfig, TokensCallbackHandler]:
        """构建包含Token统计的回调配置"""
        # 每次调用创建新的Token处理器实例
        token_handler = TokensCallbackHandler()

        # 初始化配置
        if config is None:
            processed_config = {"callbacks": []}
        else:
            processed_config = config.copy()
            if "callbacks" not in processed_config:
                processed_config["callbacks"] = []

        # 添加回调（去重）
        callbacks = processed_config["callbacks"]
        # 添加LLMLogger（如果不存在）
        if not any(isinstance(cb, LLMLogger) for cb in callbacks):
            callbacks.append(LLMLogger())
        # 添加Token处理器
        callbacks.append(token_handler)

        # 按类型去重
        callback_types = {}
        unique_callbacks = []
        for cb in callbacks:
            cb_type = type(cb)
            if cb_type not in callback_types:
                callback_types[cb_type] = cb
                unique_callbacks.append(cb)

        processed_config["callbacks"] = unique_callbacks

        return processed_config, token_handler

    # 同步调用
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, ** kwargs) -> Dict[str, Any]:
        try:
            with self.langfuse.start_as_current_observation(as_type="span", name="invoke") as span:
                with propagate_attributes(session_id=SYLogger.get_trace_id(), user_id=get_env_var('VERSION')):
                    processed_config, token_handler = self._get_callback_config(
                        config)
                    adapted_input = self._adapt_input(input)

                    span.update_trace(
                        input={"messages": adapted_input}
                    )

                    structured_result = self.retry_chain.invoke(
                        {"messages": adapted_input},
                        config={**processed_config, **self.metadata},
                        **kwargs
                    )

                    span.update_trace(output=structured_result)

                    token_usage = token_handler.usage_metadata
                    structured_result._token_usage_ = token_usage

                    return structured_result

        except Exception as e:
            SYLogger.error(f"同步LLM调用失败: {str(e)}", exc_info=True)
            return None

    # 异步调用
    async def ainvoke(self, input: Any, config: Optional[RunnableConfig] = None, ** kwargs) -> Dict[str, Any]:
        try:
            with self.langfuse.start_as_current_observation(as_type="span", name="ainvoke") as span:
                with propagate_attributes(session_id=SYLogger.get_trace_id(), user_id=get_env_var('VERSION')):
                    processed_config, token_handler = self._get_callback_config(
                        config)
                    adapted_input = self._adapt_input(input)

                    span.update_trace(
                        input={"messages": adapted_input}
                    )

                    structured_result = await self.retry_chain.ainvoke(
                        {"messages": adapted_input},
                        config={**processed_config, **self.metadata},
                        **kwargs
                    )

                    span.update_trace(output=structured_result)

                    token_usage = token_handler.usage_metadata
                    structured_result._token_usage_ = token_usage

                    return structured_result

        except Exception as e:
            SYLogger.error(f"异步LLM调用失败: {str(e)}", exc_info=True)
            return None


class LLMWithAutoTokenUsage(BaseChatModel):
    """自动为结构化调用返回token_usage的LLM包装类"""
    llm: BaseChatModel = Field(default=None)
    langfuse: Optional[Langfuse] = Field(default=None, exclude=True)

    def __init__(self, llm: BaseChatModel, langfuse: Langfuse, **kwargs):
        super().__init__(llm=llm, langfuse=langfuse, **kwargs)

    def with_structured_output(
        self,
        output_model: Type[BaseModel],
        max_retries: int = 3,
        is_extract: bool = False,
        override_prompt: ChatPromptTemplate = None,
        custom_processors: Optional[List[Callable[[str], str]]] = None,
        custom_parser: Optional[Callable[[str], BaseModel]] = None
    ) -> Runnable:
        """返回支持自动统计Token的结构化Runnable"""
        parser = PydanticOutputParser(pydantic_object=output_model)

        # 提示词模板
        accuracy_instructions = """
        字段值的抽取准确率（0~1之间），评分规则：
        1.0（完全准确）：直接从原文提取，无需任何加工，且格式与原文完全一致
        0.9（轻微处理）：数据来源明确，但需进行格式标准化或冗余信息剔除（不改变原始数值）
        0.8（有限推断）：数据需通过上下文关联或简单计算得出，仍有明确依据
        0.8以下（不可靠）：数据需大量推测、存在歧义或来源不明，处理方式：直接忽略该数据，设置为None
        """

        if is_extract:
            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="messages"),
                HumanMessage(content=f"""
                请提取信息并遵循以下规则：
                1. 准确率要求：{accuracy_instructions.strip()}
                2. 输出格式：{parser.get_format_instructions()}
                """)
            ])
        else:
            prompt = override_prompt or ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="messages"),
                HumanMessage(content=f"""
                输出格式：{parser.get_format_instructions()}
                """)
            ])

        # 文本处理函数
        def extract_response_content(response: BaseMessage) -> str:
            try:
                return response.content
            except Exception as e:
                raise ValueError(f"提取响应内容失败：{str(e)}") from e

        def strip_code_block_markers(content: str) -> str:
            try:
                return content.strip("```json").strip("```").strip()
            except Exception as e:
                raise ValueError(f"移除代码块标记失败：{str(e)}") from e

        def normalize_in_json(content: str) -> str:
            try:
                return content.replace("None", "null").replace("none", "null").replace("NONE", "null").replace("''", '""')
            except Exception as e:
                raise ValueError(f"JSON格式化失败：{str(e)}") from e

        def default_parse_to_pydantic(content: str) -> BaseModel:
            try:
                return parser.parse(content)
            except (ValidationError, ValueError) as e:
                raise ValueError(f"解析结构化结果失败：{str(e)}") from e

        # ========== 构建处理链 ==========
        base_chain = prompt | self.llm | RunnableLambda(
            extract_response_content)

        # 文本处理链
        process_runnables = custom_processors or [
            RunnableLambda(strip_code_block_markers),
            RunnableLambda(normalize_in_json)
        ]
        process_chain = base_chain
        for runnable in process_runnables:
            process_chain = process_chain | runnable

        # 解析链
        parse_chain = process_chain | RunnableLambda(
            custom_parser or default_parse_to_pydantic)

        # 重试链
        retry_chain = parse_chain.with_retry(
            retry_if_exception_type=(ValidationError, ValueError),
            stop_after_attempt=max_retries,
            wait_exponential_jitter=True,
            exponential_jitter_params={
                "initial": 0.1, "max": 3.0, "exp_base": 2.0, "jitter": 1.0}
        )

        return StructuredRunnableWithToken(retry_chain, self.langfuse)

    # ========== 实现BaseChatModel抽象方法 ==========
    def _generate(self, messages, stop=None, run_manager=None, ** kwargs):
        return self.llm._generate(messages, stop=stop, run_manager=run_manager, ** kwargs)

    @property
    def _llm_type(self) -> str:
        return self.llm._llm_type


def _init_langfuse() -> Tuple[List[CallbackHandler], Optional[Langfuse]]:
    """
    初始化 Langfuse 组件的辅助函数
    """
    callbacks = []
    langfuse = None

    # 基础日志回调
    callbacks.append(LLMLogger())
    config_dict = Config().config

    server_name = config_dict.get('Name', '')
    langfuse_configs = config_dict.get('LangfuseConfig', [])
    environment = config_dict.get('Nacos', {}).get('namespaceId', '')

    # 查找当前服务对应的 Langfuse 配置
    target_config = next(
        (item for item in langfuse_configs if item.get('name') == server_name), None
    )

    if target_config and target_config.get('enable', False):
        # 设置环境变量
        os.environ["LANGFUSE_SECRET_KEY"] = target_config.get('secretKey', '')
        os.environ["LANGFUSE_PUBLIC_KEY"] = target_config.get('publicKey', '')
        os.environ["LANGFUSE_BASE_URL"] = target_config.get('baseUrl', '')
        os.environ["LANGFUSE_TRACING_ENVIRONMENT"] = environment

        # 创建 Langfuse Handler 和 Client
        langfuse_handler = CallbackHandler(
            trace_context={"trace_id": SYLogger.get_trace_id()}
        )
        callbacks.append(langfuse_handler)
        langfuse = get_client()

    return callbacks, langfuse


def get_llm(
    model: str = None,
    streaming: bool = False
) -> LLMWithAutoTokenUsage:
    if not model:
        model = "Qwen2.5-72B"

    llmConfig = LLMConfig.from_config(model)
    if not llmConfig:
        raise Exception(f"无效的模型配置：{model}")

    callbacks, langfuse = _init_langfuse()

    llm = init_chat_model(
        model_provider=llmConfig.provider,
        model=llmConfig.model,
        base_url=llmConfig.baseUrl,
        api_key="-",
        temperature=0.1,
        streaming=streaming,
        callbacks=callbacks
    )

    if llm is None:
        raise Exception(f"初始化原始LLM实例失败：{model}")

    return LLMWithAutoTokenUsage(llm, langfuse)
