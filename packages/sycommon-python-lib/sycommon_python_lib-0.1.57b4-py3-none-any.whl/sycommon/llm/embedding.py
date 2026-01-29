import asyncio
import aiohttp
import atexit
from typing import Union, List, Optional, Dict
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

        # [修复] 缓存配置URL，避免高并发下重复读取配置文件
        self._embedding_url_cache: Dict[str, str] = {
            self.default_embedding_model: self.embeddings_base_url
        }
        self._reranker_url_cache: Dict[str, str] = {
            self.default_reranker_model: self.reranker_base_url
        }

        # [修复] 缓存模型的向量维度，用于生成兜底零向量
        self._model_dim_cache: Dict[str, int] = {}

        # 并发信号量
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.default_timeout = aiohttp.ClientTimeout(total=None)

        # 核心优化：创建全局可复用的ClientSession（连接池复用）
        self.session = None
        # 重试配置（可根据需要调整）
        self.max_retry_attempts = 3  # 最大重试次数
        self.retry_wait_base = 0.5   # 基础等待时间（秒）

        # [修复] 注册退出钩子，确保程序结束时关闭连接池
        atexit.register(self._sync_close_session)

    async def init_session(self):
        """初始化全局ClientSession（仅创建一次）"""
        if self.session is None or self.session.closed:
            # 配置连接池参数，适配高并发
            connector = aiohttp.TCPConnector(
                limit=self.max_concurrency * 2,  # 连接池最大连接数（建议是并发数的2倍）
                limit_per_host=self.max_concurrency,  # 每个域名的最大连接数
                ttl_dns_cache=300,  # DNS缓存时间
                enable_cleanup_closed=True  # 自动清理关闭的连接
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.default_timeout
            )

    async def close_session(self):
        """关闭全局Session（程序退出时调用）"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _sync_close_session(self):
        """同步关闭Session的封装，供atexit调用"""
        # 注意：atexit在主线程运行，如果当前没有事件循环，这个操作可能会受限
        # 但它能捕获大多数正常退出的场景。对于asyncio程序，建议显式调用cleanup
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果loop还在跑，创建一个任务去关闭
                loop.create_task(self.close_session())
            else:
                # 如果loop已经停止，尝试运行一次
                loop.run_until_complete(self.close_session())
        except Exception:
            # 静默处理清理失败，避免退出报错
            pass

    async def _retry_request(self, func, *args, **kwargs):
        """
        原生异步重试封装函数
        Args:
            func: 待重试的异步函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        Returns:
            函数执行结果，重试失败返回None
        """
        attempt = 0
        while attempt < self.max_retry_attempts:
            try:
                return await func(*args, **kwargs)
            except (aiohttp.ClientConnectionResetError, asyncio.TimeoutError, aiohttp.ClientError) as e:
                attempt += 1
                if attempt >= self.max_retry_attempts:
                    SYLogger.error(
                        f"Request failed after {attempt} retries: {str(e)}")
                    return None
                # 指数退避等待：0.5s → 1s → 2s（最大不超过5s）
                wait_time = min(self.retry_wait_base * (2 ** (attempt - 1)), 5)
                SYLogger.warning(
                    f"Retry {func.__name__} (attempt {attempt}/{self.max_retry_attempts}): {str(e)}, wait {wait_time}s")
                await asyncio.sleep(wait_time)
            except Exception as e:
                # 非重试类异常直接返回None
                SYLogger.error(
                    f"Non-retryable error in {func.__name__}: {str(e)}")
                return None
        return None

    def _get_embedding_url(self, model: str) -> str:
        """获取Embedding URL（带缓存）"""
        if model not in self._embedding_url_cache:
            self._embedding_url_cache[model] = EmbeddingConfig.from_config(
                model).baseUrl
        return self._embedding_url_cache[model]

    def _get_reranker_url(self, model: str) -> str:
        """获取Reranker URL（带缓存）"""
        if model not in self._reranker_url_cache:
            self._reranker_url_cache[model] = RerankerConfig.from_config(
                model).baseUrl
        return self._reranker_url_cache[model]

    async def _get_embeddings_http_core(
        self,
        input: Union[str, List[str]],
        encoding_format: str = None,
        model: str = None,
        timeout: aiohttp.ClientTimeout = None,
        **kwargs
    ):
        """embedding请求核心逻辑（剥离重试，供重试封装调用）"""
        await self.init_session()  # 确保Session已初始化
        async with self.semaphore:
            request_timeout = timeout or self.default_timeout
            target_model = model or self.default_embedding_model

            # [修复] 使用缓存获取URL
            target_base_url = self._get_embedding_url(target_model)
            url = f"{target_base_url}/v1/embeddings"

            request_body = {
                "model": target_model,
                "input": input,
                "encoding_format": encoding_format or "float"
            }
            request_body.update(kwargs)

            # 复用全局Session
            async with self.session.post(
                url,
                json=request_body,
                timeout=request_timeout
            ) as response:
                if response.status != 200:
                    error_detail = await response.text()
                    SYLogger.error(
                        f"Embedding request failed (model: {target_model}): {error_detail}")
                    return None
                return await response.json()

    async def _get_embeddings_http_async(
        self,
        input: Union[str, List[str]],
        encoding_format: str = None,
        model: str = None,
        timeout: aiohttp.ClientTimeout = None, ** kwargs
    ):
        """对外暴露的embedding请求方法（包含重试）"""
        return await self._retry_request(
            self._get_embeddings_http_core,
            input, encoding_format, model, timeout, ** kwargs
        )

    async def _get_reranker_http_core(
        self,
        documents: List[str],
        query: str,
        top_n: Optional[int] = None,
        model: str = None,
        max_chunks_per_doc: Optional[int] = None,
        return_documents: Optional[bool] = True,
        return_len: Optional[bool] = True,
        timeout: aiohttp.ClientTimeout = None, ** kwargs
    ):
        """reranker请求核心逻辑（剥离重试，供重试封装调用）"""
        await self.init_session()  # 确保Session已初始化
        async with self.semaphore:
            request_timeout = timeout or self.default_timeout
            target_model = model or self.default_reranker_model

            # [修复] 使用缓存获取URL
            target_base_url = self._get_reranker_url(target_model)
            url = f"{target_base_url}/v1/rerank"

            request_body = {
                "model": target_model,
                "documents": documents,
                "query": query,
                "top_n": top_n or len(documents),
                "max_chunks_per_doc": max_chunks_per_doc,
                "return_documents": return_documents,
                "return_len": return_len,
            }
            request_body.update(kwargs)

            # 复用全局Session
            async with self.session.post(
                url,
                json=request_body,
                timeout=request_timeout
            ) as response:
                if response.status != 200:
                    error_detail = await response.text()
                    SYLogger.error(
                        f"Rerank request failed (model: {target_model}): {error_detail}")
                    return None
                return await response.json()

    async def _get_reranker_http_async(
        self,
        documents: List[str],
        query: str,
        top_n: Optional[int] = None,
        model: str = None,
        max_chunks_per_doc: Optional[int] = None,
        return_documents: Optional[bool] = True,
        return_len: Optional[bool] = True,
        timeout: aiohttp.ClientTimeout = None, ** kwargs
    ):
        """对外暴露的reranker请求方法（包含重试）"""
        return await self._retry_request(
            self._get_reranker_http_core,
            documents, query, top_n, model, max_chunks_per_doc,
            return_documents, return_len, timeout, **kwargs
        )

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

        actual_model = model or self.default_embedding_model

        SYLogger.info(
            f"Requesting embeddings for corpus: {len(corpus)} items (model: {actual_model}, max_concurrency: {self.max_concurrency}, timeout: {timeout or 'None'})")

        all_vectors = []

        # [修复] 增加 Chunk 处理逻辑，防止 corpus 过大导致内存溢出或协程过多
        # 每次最多处理 max_concurrency * 2 个请求，避免一次性创建几十万个协程
        batch_size = self.max_concurrency * 2

        for i in range(0, len(corpus), batch_size):
            batch_texts = corpus[i: i + batch_size]

            # 给每个异步任务传入模型名称和超时配置
            tasks = [self._get_embeddings_http_async(
                text, model=model, timeout=request_timeout) for text in batch_texts]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result is None:
                    # [修复] 尝试获取真实维度或使用配置兜底，不再硬编码 1024
                    dim = self._model_dim_cache.get(actual_model)

                    # 如果缓存中没有维度，尝试从配置对象获取（假设Config类有dimension属性）
                    if dim is None:
                        try:
                            config = EmbeddingConfig.from_config(actual_model)
                            if hasattr(config, 'dimension'):
                                dim = config.dimension
                            else:
                                # 最后的兜底：如果配置也没有，必须有一个默认值防止崩溃
                                # bge-large 通常是 1024
                                dim = 1024
                                SYLogger.warning(
                                    f"Cannot get dimension from config for {actual_model}, use default 1024")
                        except Exception:
                            dim = 1024

                    zero_vector = [0.0] * dim
                    all_vectors.append(zero_vector)
                    SYLogger.warning(
                        f"Embedding request failed, append zero vector ({dim}D) for model {actual_model}")
                    continue

                # 从返回结果中提取向量并更新维度缓存
                # 正常情况下 result["data"] 是一个列表
                try:
                    for item in result["data"]:
                        embedding = item["embedding"]
                        # [修复] 动态学习并缓存维度
                        if actual_model not in self._model_dim_cache:
                            self._model_dim_cache[actual_model] = len(
                                embedding)
                        all_vectors.append(embedding)
                except (KeyError, TypeError) as e:
                    SYLogger.error(f"Failed to parse embedding result: {e}")
                    # 解析失败也补零
                    dim = self._model_dim_cache.get(actual_model, 1024)
                    all_vectors.append([0.0] * dim)

        SYLogger.info(
            f"Embeddings for corpus created: {len(all_vectors)} vectors (model: {actual_model})")
        return all_vectors

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

        actual_model = model or self.default_reranker_model
        SYLogger.info(
            f"Requesting reranker for top_results: {top_results} (model: {actual_model}, max_concurrency: {self.max_concurrency}, timeout: {timeout or 'None'})")

        data = await self._get_reranker_http_async(
            top_results, query, model=model, timeout=request_timeout)
        SYLogger.info(
            f"Reranker for top_results completed (model: {actual_model})")
        return data
