# -*- coding: UTF-8 -*-
# @Time : 2026/1/8 00:04 
# @Author : 刘洪波

import httpx
import asyncio
import logging
from types import TracebackType
from typing import List, Dict, Union, Optional, Any
from tenacity import Retrying, AsyncRetrying, stop_after_attempt, wait_random_exponential, retry_if_exception_type
from llmskit._types import RerankerResponse


__all__ = ["Reranker", "AsyncReranker"]


def should_retry(exc: Exception) -> bool:
    """Retry on network errors and server-side 5xx errors only."""
    if isinstance(exc, RerankerRequestError):
        msg = str(exc).lower()
        # 不重试客户端错误 4xx
        if "400" in msg or "401" in msg or "403" in msg or "404" in msg or "422" in msg:
            return False
        return True
    # httpx 网络错误也可重试
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return True
    return False

# =========================
# Exceptions
# =========================

class RerankerError(Exception):
    """Base exception for Reranker SDK."""


class RerankerRequestError(RerankerError):
    """Raised when the rerank API request fails."""


class RerankerResponseError(RerankerError):
    """Raised when the rerank API response is invalid."""

class RerankerClientError(RerankerError):
    """Raised when the rerank client request fails."""


class BaseReranker:
    """Base class for Reranker SDK.

    This class contains shared logic between synchronous and asynchronous
    Reranker implementations, such as input validation and response parsing.
    """

    def __init__(
        self,
        base_url: str,
        model_name: str
    ):
        if not base_url:
            raise ValueError("base_url must not be empty")
        if not model_name:
            raise ValueError("model_name must not be empty")

        self.base_url = base_url.rstrip("/")
        self.model_name = model_name

    @staticmethod
    def _validate_inputs(
        query: str,
        documents: List[str],
        top_n: int,
        threshold: float
    ) -> None:
        """Validate rerank input parameters.

        Args:
            query: Search query string.
            documents: List of documents.
            top_n: Number of results to return.
            threshold: Minimum relevance score.

        Raises:
            ValueError: If any input is invalid.
        """
        if not query:
            raise ValueError("query must not be empty")
        if not documents:
            raise ValueError("documents must not be empty")
        if top_n <= 0:
            raise ValueError("top_n must be greater than 0")
        if threshold < 0:
            raise ValueError("threshold must be >= 0")

    @staticmethod
    def _parse_response(response_data: Dict, threshold: float) -> RerankerResponse:
        """Parse and filter rerank API response.

        Args:
            response_data: Raw JSON response.
            threshold: Minimum score threshold.

        Returns:
            Filtered and sorted rerank results.

        Raises:
            RerankerResponseError: If response format is invalid.
        """
        if "results" not in response_data:
            raise RerankerResponseError(
                "Invalid rerank API response: missing 'results'"
            )

        results = []
        for item in response_data["results"]:
            document = item.get("document")
            score = float(item.get("relevance_score", 0.0))

            if score < threshold:
                continue

            if document:
                doc = document.get('text', '')
            else:
                doc = ''
            results.append({
                "idx": item.get("index"),
                "relevance_score": score,
                "document": doc
            })

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return RerankerResponse(results=results, usage=response_data["usage"])


class Reranker(BaseReranker):
    """Synchronous Reranker SDK client using httpx."""

    def __init__(
            self,
            base_url: str,
            model_name: str,
            api_key: Optional[str] = None,
            timeout: float = 30.0,
            proxies: Optional[Union[str, Dict[str, str]]] = None,
            http_client: Optional[httpx.Client] = None,  # 同步 Client
            retry_enabled: bool = True,
            retry_max_attempts: int = 3,
            retry_delay: float = 1.0,
            max_retry_delay: int = 10,
            logger: Optional[logging.Logger] = None
    ):
        """Initialize the Reranker client.

        Args:
            base_url: Base URL of the rerank API service.
            model_name: Rerank model name.
            api_key: Optional API key for authentication.
            timeout: Request timeout in seconds.
            proxies: Optional proxies dictionary.
            http_client: Optional HTTP client to use.
            retry_enabled: Whether to enable automatic retries.
            retry_max_attempts: Maximum number of retry attempts.
            retry_delay: retry delay in seconds.
            max_retry_delay: maximum retry delay in seconds.
            logger: Optional logger.

        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        super().__init__(base_url, model_name)

        # 1. 日志配置
        self.logger = logger or logging.getLogger(__name__)

        # 2. 构造 Headers
        self._headers = {"Content-Type": "application/json"}
        if api_key and api_key != "EMPTY":
            self._headers["Authorization"] = f"Bearer {api_key}"

        # 3. Client 管理逻辑 (同步版)
        if http_client is not None:
            self._client = http_client
            self._should_close_client = False
            self.logger.info(f"✅ Initialized Reranker: using HTTP client {http_client}")
        else:
            self._client = httpx.Client(
                base_url=base_url,
                headers=self._headers,
                timeout=httpx.Timeout(timeout),
                proxies=proxies
            )
            self._should_close_client = True
            self.logger.info(f"✅ Initialized Reranker: model={model_name!r}, endpoint={base_url}")

        # 4. 重试配置 (使用同步的 Retrying)
        self.retry_enabled = retry_enabled
        if self.retry_enabled:
            self.max_retries = max(0, retry_max_attempts)
            self.retry_delay = max(0.1, retry_delay)
            self.max_retry_delay = max(1, max_retry_delay)

            self.retry_config = {
                "stop": stop_after_attempt(self.max_retries),
                "wait": wait_random_exponential(multiplier=self.retry_delay, max=self.max_retry_delay),
                "retry": retry_if_exception_type(RerankerRequestError),
                "reraise": True
            }
            self.logger.debug(
                f'retry_enabled: {retry_enabled}, max_retries: {self.max_retries}, retry_delay: {self.retry_delay}, max_retry_delay: {self.max_retry_delay}')
        else:
            self.logger.debug(f'retry_enabled: {retry_enabled}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        self.close()

    def close(self) -> None:
        """同步关闭。"""
        if self._should_close_client and not self._client.is_closed:
            self._client.close()

    def rerank(
            self,
            query: str,
            documents: List[str],
            top_n: int = 10,
            threshold: float = 0.0,
    ) -> RerankerResponse:
        """执行同步 Rerank。"""
        self._validate_inputs(query, documents, top_n, threshold)

        if self.retry_enabled:
            # 使用同步的 Retrying 迭代器
            for attempt in Retrying(**self.retry_config):
                with attempt:
                    return self._request_once(query, documents, top_n, threshold)

        return self._request_once(query, documents, top_n, threshold)

    def _request_once(self, query: str, documents: List[str], top_n: int, threshold: float) -> RerankerResponse:
        """单次同步请求执行逻辑。"""
        payload = {
            "model": self.model_name,
            "query": query,
            "documents": documents,
            "top_n": top_n
        }

        try:
            # 使用同步 post
            response = self._client.post("/rerank", json=payload)

            if response.status_code == 429:
                raise RerankerRequestError(f"Rate limited: {response.text}")
            if response.status_code >= 500:
                raise RerankerRequestError(f"Server error: {response.status_code}")

            if response.is_error:
                # 注意：同步 response 使用 .content 或 .text
                raise RerankerClientError(f"Client error {response.status_code}: {response.text}")

            data = response.json()
            result = self._parse_response(data, threshold)
            self.logger.debug(f'rerank result: {result}')
            return result

        except httpx.RequestError as exc:
            raise RerankerRequestError(f"Network error: {str(exc)}") from exc
        except (RerankerRequestError, RerankerClientError):
            raise
        except Exception as exc:
            raise RerankerRequestError(f"Unexpected error: {str(exc)}") from exc


class AsyncReranker(BaseReranker):
    """Asynchronous Reranker SDK client using aiohttp."""

    def __init__(
            self,
            base_url: str,
            model_name: str,
            api_key: Optional[str] = None,
            timeout: float = 30.0,
            proxies: Optional[Union[str, Dict[str, str]]] = None,
            http_client: Optional[httpx.AsyncClient] = None,  # 允许外部注入 client
            retry_enabled: bool = True,
            retry_max_attempts: int = 3,
            retry_delay: float = 1.0,
            max_retry_delay: int = 10,
            logger: Optional[logging.Logger] = None
    ):
        """Initialize the Reranker client.

        Args:
            base_url: Base URL of the rerank API service.
            model_name: Rerank model name.
            api_key: Optional API key for authentication.
            timeout: Request timeout in seconds.
            proxies: Optional proxies dictionary.
            http_client: Optional HTTP client to use.
            retry_enabled: Whether to enable automatic retries.
            retry_max_attempts: Maximum number of retry attempts.
            retry_delay: retry delay in seconds.
            max_retry_delay: maximum retry delay in seconds.
            logger: Optional logger.

        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        super().__init__(base_url, model_name)

        # 1. 日志配置
        self.logger = logger or logging.getLogger(__name__)

        # 2. 构造 Headers
        self._headers = {"Content-Type": "application/json"}
        if api_key and api_key !="EMPTY":
            self._headers["Authorization"] = f"Bearer {api_key}"

        # 3. 仿照 OpenAI 的 Client 管理逻辑
        if http_client is not None:
            self._client = http_client
            self._should_close_client = False  # 外部传入的 Client 由外部负责关闭
            self.logger.info(f"✅ Initialized OpenAIEmbeddings: using HTTP client {http_client}")
        else:
            # httpx.AsyncClient() 实例化是非阻塞的，可以在 __init__ 中安全执行
            self._client = httpx.AsyncClient(
                base_url=base_url,
                headers=self._headers,
                timeout=httpx.Timeout(timeout),
                proxies=proxies
            )
            self._should_close_client = True  # SDK 内部创建的，SDK 负责关闭
            self.logger.info(f"✅ Initialized OpenAIEmbeddings: model={model_name!r}, endpoint={self.base_url}")

        # 4. 重试配置
        self.retry_enabled = retry_enabled
        if self.retry_enabled:
            self.max_retries = max(0, retry_max_attempts)
            self.retry_delay = max(0.1, retry_delay)  # At least 0.1s
            self.max_retry_delay = max(1, max_retry_delay)  # At least 1s

            self.retry_config = {
                "stop": stop_after_attempt(self.max_retries),
                "wait": wait_random_exponential(multiplier=self.retry_delay, max=self.max_retry_delay),
                "retry": retry_if_exception_type(RerankerRequestError),
                "reraise": True
            }
            self.logger.debug(f'retry_enabled: {retry_enabled}, max_retries: {self.max_retries}, retry_delay: {self.retry_delay}, max_retry_delay: {self.max_retry_delay}')
        else:
            self.logger.debug(f'retry_enabled: {retry_enabled}')

    async def __aenter__(self):
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """优雅关闭。注意：如果是外部注入的 Client，此方法不执行关闭操作。"""
        if self._should_close_client and not self._client.is_closed:
            await self._client.aclose()

    async def rerank(
            self,
            query: str,
            documents: List[str],
            top_n: int = 10,
            threshold: float = 0.0,
    ) -> RerankerResponse:
        """执行 Rerank。逻辑更加线性，直接使用 self._client。"""
        self._validate_inputs(query, documents, top_n, threshold)

        if self.retry_enabled:
            async for attempt in AsyncRetrying(**self.retry_config):
                with attempt:
                    return await self._request_once(query, documents, top_n, threshold)

        return await self._request_once(query, documents, top_n, threshold)

    async def _request_once(self, query: str, documents: List[str], top_n: int, threshold: float) -> RerankerResponse:
        """单次请求执行逻辑。"""
        payload = {
            "model": self.model_name,
            "query": query,
            "documents": documents,
            "top_n": top_n
        }

        try:
            # 直接使用初始化好的 self._client
            response = await self._client.post("/rerank", json=payload)

            # OpenAI 风格的状态码检查
            if response.status_code == 429:
                raise RerankerRequestError(f"Rate limited: {response.text}")
            if response.status_code >= 500:
                raise RerankerRequestError(f"Server error: {response.status_code}")

            if response.is_error:
                # 4xx 错误通过 raise_for_status 或手动抛出
                error_msg = await response.aread()
                raise RerankerClientError(f"Client error {response.status_code}: {error_msg.decode()}")

            data = response.json()
            result = self._parse_response(data, threshold)
            self.logger.debug(f'rerank result: {result}')
            return result

        except httpx.RequestError as exc:
            # 捕获网络层错误并包装为可重试异常
            raise RerankerRequestError(f"Network error: {str(exc)}") from exc
        except asyncio.CancelledError:
            raise
        except (RerankerRequestError, RerankerClientError):
            raise
        except Exception as exc:
            raise RerankerRequestError(f"Unexpected error: {str(exc)}") from exc
