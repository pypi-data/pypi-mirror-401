import asyncio
import json
import aiohttp
from typing import Union, List, Optional

from sycommon.config.Config import SingletonMeta
from sycommon.config.EmbeddingConfig import EmbeddingConfig
from sycommon.config.RerankerConfig import RerankerConfig
from sycommon.logging.kafka_log import SYLogger


class Embedding(metaclass=SingletonMeta):
    def __init__(self):
        # 1. 并发限制
        self.max_concurrency = 20
        # 保留默认模型名称
        self.default_embedding_model = "bge-large-zh-v1.5"
        self.default_reranker_model = "bge-reranker-large"

        # 初始化默认模型的基础URL
        self.embeddings_base_url = EmbeddingConfig.from_config(
            self.default_embedding_model).baseUrl
        self.reranker_base_url = RerankerConfig.from_config(
            self.default_reranker_model).baseUrl

        # 并发信号量
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        # 全局默认超时：永不超时（None）
        self.default_timeout = aiohttp.ClientTimeout(total=None)

    async def _get_embeddings_http_async(
        self,
        input: Union[str, List[str]],
        encoding_format: str = None,
        model: str = None,
        timeout: aiohttp.ClientTimeout = None,
        **kwargs
    ):
        async with self.semaphore:
            # 优先使用传入的超时，无则用全局默认
            request_timeout = timeout or self.default_timeout

            # 优先使用传入的模型名，无则用默认值
            target_model = model or self.default_embedding_model
            target_base_url = EmbeddingConfig.from_config(target_model).baseUrl
            url = f"{target_base_url}/v1/embeddings"

            request_body = {
                "model": target_model,
                "input": input,
                "encoding_format": encoding_format or "float"
            }
            request_body.update(kwargs)

            try:
                async with aiohttp.ClientSession(timeout=request_timeout) as session:
                    async with session.post(url, json=request_body) as response:
                        if response.status != 200:
                            error_detail = await response.text()
                            SYLogger.error(
                                f"Embedding request failed (model: {target_model}): {error_detail}")
                            return None
                        return await response.json()
            except asyncio.TimeoutError:
                SYLogger.error(
                    f"Embedding request timeout (model: {target_model})")
                return None
            except Exception as e:
                SYLogger.error(
                    f"Embedding request unexpected error (model: {target_model}): {str(e)}")
                return None

    async def _get_reranker_http_async(
        self,
        documents: List[str],
        query: str,
        top_n: Optional[int] = None,
        model: str = None,
        max_chunks_per_doc: Optional[int] = None,
        return_documents: Optional[bool] = True,
        return_len: Optional[bool] = True,
        timeout: aiohttp.ClientTimeout = None,
        **kwargs
    ):
        async with self.semaphore:
            # 优先使用传入的超时，无则用全局默认
            request_timeout = timeout or self.default_timeout

            # 优先使用传入的模型名，无则用默认值
            target_model = model or self.default_reranker_model
            target_base_url = RerankerConfig.from_config(target_model).baseUrl
            url = f"{target_base_url}/v1/rerank"

            request_body = {
                "model": target_model,
                "documents": documents,
                "query": query,
                "top_n": top_n or len(documents),
                "max_chunks_per_doc": max_chunks_per_doc,
                "return_documents": return_documents,
                "return_len": return_len,
                "kwargs": json.dumps(kwargs),
            }
            request_body.update(kwargs)

            try:
                async with aiohttp.ClientSession(timeout=request_timeout) as session:
                    async with session.post(url, json=request_body) as response:
                        if response.status != 200:
                            error_detail = await response.text()
                            SYLogger.error(
                                f"Rerank request failed (model: {target_model}): {error_detail}")
                            return None
                        return await response.json()
            except asyncio.TimeoutError:
                SYLogger.error(
                    f"Rerank request timeout (model: {target_model})")
                return None
            except Exception as e:
                SYLogger.error(
                    f"Rerank request unexpected error (model: {target_model}): {str(e)}")
                return None

    async def get_embeddings(
        self,
        corpus: List[str],
        model: str = None,
        timeout: Optional[Union[int, float]] = None
    ):
        """
        获取语料库的嵌入向量，结果顺序与输入语料库顺序一致

        Args:
            corpus: 待生成嵌入向量的文本列表
            model: 可选，指定使用的embedding模型名称，默认使用bge-large-zh-v1.5
            timeout: 可选，超时时间（秒）：
                     - 传int/float：表示总超时时间（秒）
                     - 不传/None：使用默认永不超时配置
        """
        request_timeout = None
        if timeout is not None:
            if isinstance(timeout, (int, float)):
                request_timeout = aiohttp.ClientTimeout(total=timeout)
            else:
                SYLogger.warning(
                    f"Invalid timeout type: {type(timeout)}, must be int/float, use default timeout")

        SYLogger.info(
            f"Requesting embeddings for corpus: {corpus} (model: {model or self.default_embedding_model}, max_concurrency: {self.max_concurrency}, timeout: {timeout or 'None'})")

        # 给每个异步任务传入模型名称和超时配置
        tasks = [self._get_embeddings_http_async(
            text, model=model, timeout=request_timeout) for text in corpus]
        results = await asyncio.gather(*tasks)

        vectors = []
        for result in results:
            if result is None:
                zero_vector = [0.0] * 1024
                vectors.append(zero_vector)
                SYLogger.warning(
                    f"Embedding request failed, append zero vector (1024D)")
                continue
            for item in result["data"]:
                vectors.append(item["embedding"])

        SYLogger.info(
            f"Embeddings for corpus: {corpus} created (model: {model or self.default_embedding_model})")
        return vectors

    async def get_reranker(
        self,
        top_results: List[str],
        query: str,
        model: str = None,
        timeout: Optional[Union[int, float]] = None
    ):
        """
        对搜索结果进行重排序

        Args:
            top_results: 待重排序的文本列表
            query: 排序参考的查询语句
            model: 可选，指定使用的reranker模型名称，默认使用bge-reranker-large
            timeout: 可选，超时时间（秒）：
                     - 传int/float：表示总超时时间（秒）
                     - 不传/None：使用默认永不超时配置
        """
        request_timeout = None
        if timeout is not None:
            if isinstance(timeout, (int, float)):
                request_timeout = aiohttp.ClientTimeout(total=timeout)
            else:
                SYLogger.warning(
                    f"Invalid timeout type: {type(timeout)}, must be int/float, use default timeout")

        SYLogger.info(
            f"Requesting reranker for top_results: {top_results} (model: {model or self.default_reranker_model}, max_concurrency: {self.max_concurrency}, timeout: {timeout or 'None'})")

        data = await self._get_reranker_http_async(
            top_results, query, model=model, timeout=request_timeout)
        SYLogger.info(
            f"Reranker for top_results: {top_results} completed (model: {model or self.default_reranker_model})")
        return data
