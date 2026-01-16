# In sutram_services/llm/llm_service.py
import json
from typing import Dict, Any, Optional, Type, TypeVar

from guardianhub import get_logger
from guardianhub.clients import LLMClient
from guardianhub.utils.json_utils import parse_structured_response, extract_json_from_text
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel
from guardianhub.config.settings import settings

logger = get_logger(__name__)
T = TypeVar('T', bound=BaseModel)


class LLMService:
    """Service for managing LLM interactions."""

    def __init__(self):
        self.llm_client = LLMClient(settings.endpoints.LLM_URL, "NO_API_KEY")
        self.llm = self.llm_client  # For backward compatibility
        self.eval_llm = self.llm_client
        self.logger = logger

    async def invoke_unstructured_model(
            self,
            model: str,
            user_input: str,
            system_prompt: str,
            model_key: str = "default",
            temperature: float = 0.7,
            langfuse_trace_id: Optional[str] = None,
            parent_span_id: Optional[str] = None,
            # Additional context can be passed here if needed, but keeping it simple for text generation
    ) -> str:
        """
        Invokes the LLM to generate a natural language, unstructured text response.

        This method is suitable for final synthesis, summarization, or dialogue.

        Returns:
            str: The raw text content of the LLM's response.
        """
        try:
            self.logger.info(f"🌐 Calling LLM for unstructured text generation (Model: {model})")

            # 1. Build simple message list
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]

            # 2. Call the LLM (without JSON enforcement)
            response = await self.llm_client.chat_completion(
                messages=messages,
                model=model_key,
                temperature=temperature,
                # Crucial: No response_format={"type": "json_object"}
                langfuse_trace_id=langfuse_trace_id,
                otel_trace_id=parent_span_id,
                max_tokens=4048,
                response_model_name=None,
                response_model=None
            )

            # 3. Extract and return the raw text content
            response_text = response
            self.logger.debug(f"Raw unstructured LLM response: {response_text[:100]}...")
            self.logger.info(f"Raw unstructured LLM response: {response_text[:100]}...")

            return response_text

        except Exception as e:
            self.logger.error(f"Error in invoke_unstructured_model: {str(e)}", exc_info=True)
            # Provide a non-empty, safe fallback string instead of raising a generic RuntimeError
            raise RuntimeError(f"Unstructured LLM invocation failed: {str(e)}") from e

    async def invoke_structured_model(
            self,
            user_input: str,
            system_prompt_template: str,
            response_model: Optional[Type[T]] = None,
            response_model_name: Optional[str] = None,
            model_key: str = "default",
            langfuse_trace_id: Optional[str] = None,
            parent_span_id: Optional[str] = None,
    ) -> T:
        """
        Invoke the LLM with a structured response format.

        Args:
            user_input: The user's input text
            system_prompt_template: System prompt template for the LLM
            response_model: Pydantic model for response validation
            response_model_name: Name of the response model (for logging)
            model_key: Key to identify the model to use
            langfuse_trace_id: Optional trace ID for Langfuse
            parent_span_id: Optional parent span ID for tracing

        Returns:
            Validated response as an instance of the response_model

        Raises:
            RuntimeError: If the LLM request fails
        """
        try:
            # Prepare the messages for the LLM
            messages = [
                {"role": "system", "content": system_prompt_template},
                {"role": "user", "content": user_input}
            ]

            # Call the LLM with the response model for schema validation
            self.logger.debug(f"Sending request to LLM with model: {model_key}")
            response = await self.llm_client.chat_completion(
                messages=messages,
                model=model_key,
                temperature=0.1,  # Lower temperature for more deterministic output
                response_model=response_model,
                response_model_name=response_model_name,
                langfuse_trace_id=langfuse_trace_id,
                otel_trace_id=parent_span_id,
                max_tokens=4048
            )

            # If we get here, the response is already validated by the client
            self.logger.info("Successfully got response from LLM")
            return response

        except Exception as e:
            self.logger.error(f"LLM request failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"LLM request failed: {str(e)}") from e
