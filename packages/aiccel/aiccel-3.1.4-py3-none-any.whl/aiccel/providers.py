import os
import orjson
import requests
import asyncio
from typing import Dict, List, Any, Optional, Union, AsyncIterator
from aiohttp import ClientSession, ClientTimeout

from .logger import AILogger
from .providers_base import BaseProvider

class LLMProvider(BaseProvider):
    """
    Base class for LLM providers.
    
    This is a legacy wrapper around BaseProvider for backward compatibility.
    All concrete providers (OpenAI, Gemini, Groq) inherit from this class.
    
    The LLMProvider interface provides:
    - generate(prompt): Simple text completion
    - chat(messages): Multi-turn conversation
    - embed(text): Text embeddings
    - Async variants: generate_async, chat_async, embed_async
    """
    pass


class OpenAIProvider(LLMProvider):
    """
    OpenAI LLM Provider for GPT models.
    
    Supports GPT-4, GPT-4o, GPT-3.5-Turbo and other OpenAI models.
    Also provides text embeddings via text-embedding-3-small/large.
    
    Attributes:
        api_key: OpenAI API key. If not provided, reads from OPENAI_API_KEY env var.
        model: Model identifier (default: 'gpt-4o').
        embedding_model: Model for embeddings (default: 'text-embedding-3-small').
    
    Example:
        >>> from aiccel import OpenAIProvider
        >>> 
        >>> # Initialize with explicit key
        >>> provider = OpenAIProvider(api_key="sk-...", model="gpt-4o-mini")
        >>> 
        >>> # Or use environment variable
        >>> provider = OpenAIProvider()  # Uses OPENAI_API_KEY
        >>> 
        >>> # Generate text
        >>> response = provider.generate("Explain quantum computing")
        >>> 
        >>> # Chat with history
        >>> response = provider.chat([
        ...     {"role": "user", "content": "Hello"},
        ...     {"role": "assistant", "content": "Hi there!"},
        ...     {"role": "user", "content": "How are you?"}
        ... ])
        >>> 
        >>> # Generate embeddings
        >>> embeddings = provider.embed("Some text to embed")
    
    See Also:
        - GeminiProvider: For Google Gemini models
        - GroqProvider: For Groq-hosted models
    """
    
    ENV_KEY_PREFIX = "OPENAI"
    
    def __init__(
        self, 
        api_key: str = None, 
        model: str = "gpt-4o", 
        embedding_model: str = "text-embedding-3-small", 
        verbose: bool = False, 
        log_file: Optional[str] = None, 
        structured_logging: bool = False
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
            model: Model to use (default: 'gpt-4o').
            embedding_model: Model for embeddings (default: 'text-embedding-3-small').
            verbose: Enable verbose logging.
            log_file: Optional file path for logging.
            structured_logging: Use JSON structured logging.
        """
        super().__init__(
            api_key=api_key, 
            model=model, 
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        self.embedding_model = embedding_model
        self.http_session = None

    async def __aenter__(self):
        self.http_session = ClientSession(timeout=ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    def _generate_impl(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    async def _generate_async_impl(self, prompt: str, **kwargs) -> str:
        return await self.chat_async([{"role": "user", "content": prompt}], **kwargs)

    def _chat_impl(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("openai_chat", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            
            if not response_json.get("choices") or not response_json["choices"][0].get("message"):
                raise Exception("Invalid response format: Missing choices or message")
                
            result = response_json["choices"][0]["message"]["content"]
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
            
        except requests.exceptions.HTTPError as e:
            # Propagate for BaseProvider retry/rate-limit handling
            raise
        except Exception as e:
            self.logger.trace_error(trace_id, e, "OpenAI chat failed")
            raise

    async def _chat_async_impl(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("openai_chat_async", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        session = self.http_session or ClientSession(timeout=ClientTimeout(total=self.timeout))
        close_session = self.http_session is None
        
        try:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                response.raise_for_status()
                response_json = await response.json()
                
                if not response_json.get("choices") or not response_json["choices"][0].get("message"):
                    raise Exception("Invalid response format")
                    
                result = response_json["choices"][0]["message"]["content"]
                self.logger.trace_end(trace_id, {"response": result[:100]})
                return result
                
        except Exception as e:
            self.logger.trace_error(trace_id, e, "OpenAI async chat failed")
            raise
        finally:
            if close_session:
                await session.close()
    
    def _embed_impl(self, text: Union[str, List[str]]) -> List[float]:
        trace_id = self.logger.trace_start("openai_embed", {"text_len": len(str(text))})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.embedding_model,
            "input": text
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            
            if isinstance(text, str):
                result = response_json["data"][0]["embedding"]
            else:
                result = [item["embedding"] for item in response_json["data"]]
                
            self.logger.trace_end(trace_id, {"dim": len(result)})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Embed failed")
            raise

    async def _embed_async_impl(self, text: Union[str, List[str]]) -> List[float]:
        # Using sync for now inside async wrapper if needed, or implement async http call
        # For brevity, reusing sync logic in executor is fine as fallback, 
        # but let's do proper async http since we are here.
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.embedding_model,
            "input": text
        }
        
        session = self.http_session or ClientSession(timeout=ClientTimeout(total=self.timeout))
        close_session = self.http_session is None
        
        try:
            async with session.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=data
            ) as response:
                response.raise_for_status()
                response_json = await response.json()
                
                if isinstance(text, str):
                    result = response_json["data"][0]["embedding"]
                else:
                    result = [item["embedding"] for item in response_json["data"]]
                return result
        finally:
            if close_session:
                await session.close()


class GeminiProvider(LLMProvider):
    """
    Google Gemini LLM Provider.
    
    Supports Gemini 2.0, Gemini 1.5 Pro/Flash and other Google AI models.
    
    Note: Gemini does not provide native embeddings API. You must supply an
    embedding_provider (e.g., OpenAIProvider) for embed() calls.
    
    Attributes:
        api_key: Google AI API key. Falls back to GOOGLE_API_KEY or GEMINI_API_KEY.
        model: Model identifier (default: 'gemini-2.5-flash').
        embedding_provider: Optional provider for embeddings.
    
    Example:
        >>> from aiccel import GeminiProvider
        >>> 
        >>> # Initialize
        >>> provider = GeminiProvider(api_key="AI...", model="gemini-2.0-flash")
        >>> 
        >>> # Generate text
        >>> response = provider.generate("Write a poem about AI")
        >>> 
        >>> # Chat
        >>> response = provider.chat([
        ...     {"role": "user", "content": "Hello!"}
        ... ])
        >>> 
        >>> # For embeddings, provide embedding_provider
        >>> oai = OpenAIProvider(api_key="sk-...")
        >>> provider = GeminiProvider(api_key="AI...", embedding_provider=oai)
        >>> embeddings = provider.embed("Some text")
    
    See Also:
        - OpenAIProvider: For OpenAI models
        - GroqProvider: For ultra-fast inference
    """
    
    ENV_KEY_PREFIX = "GOOGLE"
    
    def __init__(
        self, 
        api_key: str = None, 
        model: str = "gemini-2.5-flash", 
        embedding_provider: Optional[LLMProvider] = None, 
        verbose: bool = False, 
        log_file: Optional[str] = None, 
        structured_logging: bool = False
    ):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google AI API key. Falls back to GOOGLE_API_KEY env var.
            model: Model to use (default: 'gemini-2.5-flash').
            embedding_provider: Provider for embeddings (Gemini lacks native embeddings).
            verbose: Enable verbose logging.
            log_file: Optional file path for logging.
            structured_logging: Use JSON structured logging.
        """
        super().__init__(
            api_key=api_key, 
            model=model,
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        self.embedding_provider = embedding_provider
        self.http_session = None

    async def __aenter__(self):
        self.http_session = ClientSession(timeout=ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    def _generate_impl(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    async def _generate_async_impl(self, prompt: str, **kwargs) -> str:
        return await self.chat_async([{"role": "user", "content": prompt}], **kwargs)

    def _chat_impl(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("gemini_chat", {"message_count": len(messages)})
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
        
        contents = []
        for msg in messages:
            role = "user" if msg["role"].lower() == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
                "maxOutputTokens": kwargs.get("max_tokens", 2048),
            }
        }
        
        import time
        max_retries = 3
        backoff_factor = 2
        
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(url, json=data, timeout=self.timeout)
                
                if response.status_code == 429:
                    if attempt < max_retries:
                        sleep_time = backoff_factor ** attempt
                        self.logger.warning(f"Gemini API rate limit exceeded (429). Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue
                    else:
                        response.raise_for_status()
                
                response.raise_for_status()
                response_json = orjson.loads(response.content)
                
                if not response_json.get("candidates") or not response_json["candidates"][0].get("content"):
                    raise Exception("Invalid response format")
                    
                result = response_json["candidates"][0]["content"]["parts"][0]["text"]
                self.logger.trace_end(trace_id, {"response": result[:100]})
                return result
            except Exception as e:
                # If it was a 429 that we didn't catch above (e.g. from raise_for_status)
                if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429:
                     if attempt < max_retries:
                        sleep_time = backoff_factor ** attempt
                        self.logger.warning(f"Gemini API rate limit exceeded (429). Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue
                
                self.logger.trace_error(trace_id, e, "Gemini chat failed")
                raise

    async def _chat_async_impl(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("gemini_chat_async", {"message_count": len(messages)})
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
        
        contents = []
        for msg in messages:
            role = "user" if msg["role"].lower() == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
                "maxOutputTokens": kwargs.get("max_tokens", 2048),
            }
        }
        
        session = self.http_session or ClientSession(timeout=ClientTimeout(total=self.timeout))
        close_session = self.http_session is None
        
        max_retries = 3
        backoff_factor = 2
        
        try:
            for attempt in range(max_retries + 1):
                try:
                    async with session.post(url, json=data) as response:
                        if response.status == 429:
                            if attempt < max_retries:
                                sleep_time = backoff_factor ** attempt
                                self.logger.warning(f"Gemini API rate limit exceeded (429). Retrying in {sleep_time}s...")
                                await asyncio.sleep(sleep_time)
                                continue
                            else:
                                response.raise_for_status()
                        
                        response.raise_for_status()
                        response_json = await response.json()
                        
                        if not response_json.get("candidates") or not response_json["candidates"][0].get("content"):
                            raise Exception("Invalid response format")
                            
                        result = response_json["candidates"][0]["content"]["parts"][0]["text"]
                        self.logger.trace_end(trace_id, {"response": result[:100]})
                        return result
                except Exception as e:
                    # If it was a 429 that we didn't catch above
                    # aiohttp raises ClientResponseError which has .status
                    from aiohttp import ClientResponseError
                    if isinstance(e, ClientResponseError) and e.status == 429:
                        if attempt < max_retries:
                            sleep_time = backoff_factor ** attempt
                            self.logger.warning(f"Gemini API rate limit exceeded (429). Retrying in {sleep_time}s...")
                            await asyncio.sleep(sleep_time)
                            continue
                            
                    if attempt == max_retries:
                         self.logger.trace_error(trace_id, e, "Gemini async chat failed")
                         raise
                    # For other errors, maybe retry? For now let's just fail fast on non-rate-limit
                    self.logger.trace_error(trace_id, e, "Gemini async chat failed")
                    raise
        finally:
            if close_session:
                await session.close()
                
    def _embed_impl(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            raise ValueError("No embedding provider specified")
        return self.embedding_provider.embed(text)
        
    async def _embed_async_impl(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            raise ValueError("No embedding provider specified")
        return await self.embedding_provider.embed_async(text)


class GroqProvider(LLMProvider):
    """
    Groq LLM Provider for ultra-fast inference.
    
    Groq provides extremely fast inference for open-source models like
    LLaMA, Mixtral, and Gemma using custom LPU hardware.
    
    Note: Groq does not provide embeddings. You must supply an
    embedding_provider for embed() calls.
    
    Attributes:
        api_key: Groq API key. Falls back to GROQ_API_KEY env var.
        model: Model identifier (default: 'llama3-70b-8192').
        embedding_provider: Optional provider for embeddings.
    
    Example:
        >>> from aiccel import GroqProvider
        >>> 
        >>> # Initialize with fastest LLaMA 3
        >>> provider = GroqProvider(api_key="gsk_...", model="llama3-70b-8192")
        >>> 
        >>> # Generate (very fast!)
        >>> response = provider.generate("Explain machine learning")
        >>> 
        >>> # Available models:
        >>> # - llama3-70b-8192 (best quality)
        >>> # - llama3-8b-8192 (faster)
        >>> # - mixtral-8x7b-32768 (long context)
        >>> # - gemma-7b-it (compact)
    
    See Also:
        - OpenAIProvider: For OpenAI models
        - GeminiProvider: For Google Gemini models
    """
    
    ENV_KEY_PREFIX = "GROQ"
    
    def __init__(
        self, 
        api_key: str = None, 
        model: str = "llama3-70b-8192", 
        embedding_provider: Optional[LLMProvider] = None, 
        verbose: bool = False, 
        log_file: Optional[str] = None, 
        structured_logging: bool = False
    ):
        """
        Initialize Groq provider.
        
        Args:
            api_key: Groq API key. Falls back to GROQ_API_KEY env var.
            model: Model to use (default: 'llama3-70b-8192').
            embedding_provider: Provider for embeddings (Groq lacks embeddings).
            verbose: Enable verbose logging.
            log_file: Optional file path for logging.
            structured_logging: Use JSON structured logging.
        """
        super().__init__(
            api_key=api_key, 
            model=model,
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        self.embedding_provider = embedding_provider
        self.http_session = None

    async def __aenter__(self):
        self.http_session = ClientSession(timeout=ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    def _generate_impl(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    async def _generate_async_impl(self, prompt: str, **kwargs) -> str:
        return await self.chat_async([{"role": "user", "content": prompt}], **kwargs)

    def _chat_impl(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("groq_chat", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            
            result = response_json["choices"][0]["message"]["content"]
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Groq chat failed")
            raise

    async def _chat_async_impl(self, messages: List[Dict[str, str]], **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        session = self.http_session or ClientSession(timeout=ClientTimeout(total=self.timeout))
        close_session = self.http_session is None
        
        try:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                response.raise_for_status()
                response_json = await response.json()
                result = response_json["choices"][0]["message"]["content"]
                return result
        finally:
            if close_session:
                await session.close()

    def _embed_impl(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            raise ValueError("No embedding provider specified")
        return self.embedding_provider.embed(text)

    async def _embed_async_impl(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            raise ValueError("No embedding provider specified")
        return await self.embedding_provider.embed_async(text)