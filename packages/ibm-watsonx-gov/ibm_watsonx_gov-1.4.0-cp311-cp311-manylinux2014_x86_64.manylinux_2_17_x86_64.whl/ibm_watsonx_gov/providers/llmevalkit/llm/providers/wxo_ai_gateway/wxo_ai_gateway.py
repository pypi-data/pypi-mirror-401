# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
import os
from typing import Any, Dict, List, Optional, Type, Union

from llmevalkit.llm.base import Hook, LLMClient, register_llm
from llmevalkit.llm.output_parser import ValidatingLLMClient
from llmevalkit.llm.types import GenerationMode, LLMResponse, ParameterMapper

from .wxo_ai_gateway_inference import WxoAIGatewayInference

SchemaType = Union[Dict[str, Any], Type["BaseModel"], Type]


@register_llm("wxo_ai_gateway.output_val")
class WxoAIGatewayClientOutputVal(ValidatingLLMClient):

    def __init__(self, api_key: Optional[str] = None, url: Optional[str] = None, hooks: Optional[List[Hook]] = None, **kwargs):
        provider_kwargs = {"api_key": api_key, "url": url}
        super().__init__(
            client=None, client_needs_init=True, hooks=hooks, **provider_kwargs
        )

    @classmethod
    def provider_class(cls) -> Type:
        """
        Underlying client class: WxoAIGatewayInference.
        """
        return WxoAIGatewayInference

    def _register_methods(self) -> None:
        """
        Register how to call wxo ai gateway methods for validation:
          - 'chat'       -> ModelInference.chat
          - 'chat_async' -> ModelInference.achat
        """
        self.set_method_config(GenerationMode.CHAT.value, "chat", "messages")
        self.set_method_config(
            GenerationMode.CHAT_ASYNC.value, "achat", "messages")

    def _parse_llm_response(self, raw: Any) -> str:
        """
        Extract the assistant-generated text from a wxo ai gateway response.

        Same logic as non-validating client.
        """
        if isinstance(raw, dict) and "results" in raw:
            results = raw["results"]
            if isinstance(results, list) and results:
                first = results[0]
                return first.get("generated_text", "")
        if isinstance(raw, dict) and "choices" in raw:
            choices = raw["choices"]
            if isinstance(choices, list) and choices:
                first = choices[0]
                msg = first.get("message")
                if isinstance(msg, dict) and "content" in msg:
                    return msg["content"]
                if "text" in first:
                    return first["text"]
        raise ValueError(raw.get("message", "Invalid response format"))

    def generate(
        self,
        prompt: Union[str, List[Dict[str, Any]]],
        *,
        schema: SchemaType,
        retries: int = 3,
        generation_args: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Synchronous chat generation with validation + retries.

        Args:
            prompt: Either a string or a list of chat messages.
            schema: JSON Schema dict, Pydantic model class, or built-in Python type.
            retries: Maximum attempts (including the first).
            generation_args: GenerationArgs to map to provider parameters.
            **kwargs: Passed to the underlying ModelInference call (e.g., temperature).
        """
        mode = "chat"

        # Normalize prompt to chat-messages
        if isinstance(prompt, str):
            prompt = [{"role": "user", "content": prompt}]

        return super().generate(
            **{
                "prompt": prompt,
                "schema": schema,
                "retries": retries,
                "mode": mode
            }
        )

    async def generate_async(
        self,
        prompt: Union[str, List[Dict[str, Any]]],
        *,
        schema: SchemaType,
        retries: int = 3,
        generation_args: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Asynchronous chat generation with validation + retries.

        Args:
            prompt: Either a string or a list of chat messages.
            schema: JSON Schema dict, Pydantic model class, or built-in Python type.
            retries: Maximum attempts.
            generation_args: GenerationArgs to map to provider parameters.
            **kwargs: Passed to the underlying ModelInference call.
        """
        mode = "chat_async"

        if isinstance(prompt, str):
            prompt = [{"role": "user", "content": prompt}]

        return await super().generate_async(
            **{
                "prompt": prompt,
                "schema": schema,
                "retries": retries,
                "mode": mode
            }
        )
