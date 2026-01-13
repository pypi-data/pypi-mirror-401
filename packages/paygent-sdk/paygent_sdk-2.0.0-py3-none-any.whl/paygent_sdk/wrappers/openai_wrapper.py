"""
OpenAI wrapper for automatic usage tracking with Paygent.
This wrapper intercepts OpenAI API calls and automatically sends usage data to Paygent.
"""

import json
from typing import Any, Optional

try:
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "openai package is a peer-dependency. To use the Paygent wrapper around openai "
        "you're assumed to already have openai package installed."
    )

from ..client import Client
from ..models import UsageData, UsageDataWithStrings


class PaygentOpenAI:
    """Main wrapper class for OpenAI that provides automatic usage tracking."""

    def __init__(self, openai_client: OpenAI, paygent_client: Client):
        """
        Create a new PaygentOpenAI wrapper.
        
        Args:
            openai_client: The OpenAI client instance
            paygent_client: The Paygent client instance for usage tracking
        """
        self.openai = openai_client
        self.paygent_client = paygent_client

    @property
    def chat(self) -> 'ChatWrapper':
        """Access to chat API with automatic usage tracking."""
        return ChatWrapper(self.openai, self.paygent_client)

    @property
    def embeddings(self) -> 'EmbeddingsWrapper':
        """Access to embeddings API with automatic usage tracking."""
        return EmbeddingsWrapper(self.openai, self.paygent_client)

    @property
    def images(self) -> 'ImagesWrapper':
        """Access to images API with automatic usage tracking."""
        return ImagesWrapper(self.openai, self.paygent_client)


class ChatWrapper:
    """Wrapper for OpenAI chat API."""

    def __init__(self, openai_client: OpenAI, paygent_client: Client):
        self.openai = openai_client
        self.paygent_client = paygent_client

    @property
    def completions(self) -> 'ChatCompletionsWrapper':
        """Access to chat completions API with automatic usage tracking."""
        return ChatCompletionsWrapper(self.openai, self.paygent_client)


class ChatCompletionsWrapper:
    """Wrapper for OpenAI chat completions API."""

    def __init__(self, openai_client: OpenAI, paygent_client: Client):
        self.openai = openai_client
        self.paygent_client = paygent_client

    def create(
        self,
        *,
        model: str,
        messages: list,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> Any:
        """
        Create a chat completion with automatic usage tracking.
        Note: Streaming is not supported with automatic tracking.
        
        Args:
            model: The model to use
            messages: The messages to send
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional OpenAI parameters
            
        Returns:
            The chat completion response from OpenAI
        """
        # Ensure streaming is disabled for automatic tracking
        kwargs['stream'] = False

        # Make the OpenAI API call (non-streaming)
        response = self.openai.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        # Extract usage data from response with robust fallback mechanism
        has_valid_usage = (
            hasattr(response, 'usage') and
            response.usage and
            response.usage.prompt_tokens > 0 and
            response.usage.completion_tokens > 0
        )

        if has_valid_usage:
            # Primary path: Use usage data from API response
            usage_data = UsageData(
                service_provider=model,
                model=model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            )

            self.paygent_client.send_usage(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data
            )
        else:
            # Fallback path: Calculate tokens from actual strings
            # This ensures we never lose billing data even if API response format changes
            prompt_string = json.dumps(messages)
            output_string = ''
            if hasattr(response, 'choices') and response.choices:
                if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                    output_string = response.choices[0].message.content or ''

            usage_data_with_strings = UsageDataWithStrings(
                service_provider=model,
                model=model,
                prompt_string=prompt_string,
                output_string=output_string
            )

            self.paygent_client.send_usage_with_token_string(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data_with_strings
            )

        return response


class EmbeddingsWrapper:
    """Wrapper for OpenAI embeddings API."""

    def __init__(self, openai_client: OpenAI, paygent_client: Client):
        self.openai = openai_client
        self.paygent_client = paygent_client

    def create(
        self,
        *,
        model: str,
        input: Any,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> Any:
        """
        Create embeddings with automatic usage tracking.
        
        Args:
            model: The model to use
            input: The input text(s) to embed
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional OpenAI parameters
            
        Returns:
            The embeddings response from OpenAI
        """
        # Make the OpenAI API call
        response = self.openai.embeddings.create(
            model=model,
            input=input,
            **kwargs
        )

        # Extract usage data from response with robust fallback mechanism
        has_valid_usage = (
            hasattr(response, 'usage') and
            response.usage and
            response.usage.prompt_tokens > 0
        )

        if has_valid_usage:
            # Primary path: Use usage data from API response
            usage_data = UsageData(
                service_provider=model,
                model=model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.prompt_tokens,  # Embeddings don't have completion tokens
                total_tokens=response.usage.total_tokens
            )

            self.paygent_client.send_usage(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data
            )
        else:
            # Fallback path: Calculate tokens from input text
            input_text = input
            if isinstance(input, list):
                input_text = ' '.join(str(i) for i in input)
            else:
                input_text = str(input)

            usage_data_with_strings = UsageDataWithStrings(
                service_provider=model,
                model=model,
                prompt_string=input_text,
                output_string=''  # Embeddings don't have output
            )

            self.paygent_client.send_usage_with_token_string(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data_with_strings
            )

        return response


class ImagesWrapper:
    """Wrapper for OpenAI images API."""

    def __init__(self, openai_client: OpenAI, paygent_client: Client):
        self.openai = openai_client
        self.paygent_client = paygent_client

    def generate(
        self,
        *,
        model: Optional[str] = None,
        prompt: str,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> Any:
        """
        Generate images with automatic usage tracking.
        Note: OpenAI's image generation API doesn't return token usage,
        so we track the request parameters instead.
        
        Args:
            model: The model to use (optional, defaults to dall-e-2)
            prompt: The prompt for image generation
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional OpenAI parameters
            
        Returns:
            The images response from OpenAI
        """
        # Make the OpenAI API call
        if model:
            response = self.openai.images.generate(
                model=model,
                prompt=prompt,
                **kwargs
            )
        else:
            response = self.openai.images.generate(
                prompt=prompt,
                **kwargs
            )
            model = 'dall-e-2'  # Default model

        # For image generation, we'll use a simplified usage tracking
        # since OpenAI doesn't provide token counts for images
        usage_data = UsageData(
            service_provider=model,
            model=model,
            prompt_tokens=0,  # Images don't use traditional tokens
            completion_tokens=0,
            total_tokens=0
        )

        # Send usage data to Paygent
        # Note: Cost calculation for images should be handled by the pricing module
        self.paygent_client.send_usage(
            external_agent_id,
            external_customer_id,
            indicator,
            usage_data
        )

        return response
