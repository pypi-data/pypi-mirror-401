"""
Mistral wrapper for automatic usage tracking with Paygent.
This wrapper intercepts Mistral API calls and automatically sends usage data to Paygent.
"""

import json
from typing import Any

try:
    from mistralai import Mistral
except ImportError:
    raise ImportError(
        "mistralai package is a peer-dependency. To use the Paygent wrapper around mistralai "
        "you're assumed to already have mistralai package installed."
    )

from ..client import Client
from ..models import UsageData, UsageDataWithStrings


class PaygentMistral:
    """Main wrapper class for Mistral that provides automatic usage tracking."""

    def __init__(self, mistral_client: Mistral, paygent_client: Client):
        """
        Create a new PaygentMistral wrapper.
        
        Args:
            mistral_client: The Mistral client instance
            paygent_client: The Paygent client instance for usage tracking
        """
        self.mistral = mistral_client
        self.paygent_client = paygent_client

    @property
    def chat(self) -> 'ChatWrapper':
        """Access to chat API with automatic usage tracking."""
        return ChatWrapper(self.mistral, self.paygent_client)


class ChatWrapper:
    """Wrapper for Mistral chat API."""

    def __init__(self, mistral_client: Mistral, paygent_client: Client):
        self.mistral = mistral_client
        self.paygent_client = paygent_client

    def complete(
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
            **kwargs: Additional Mistral parameters
            
        Returns:
            The chat completion response from Mistral
        """
        # Make the Mistral API call
        response = self.mistral.chat.complete(
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
            prompt_string = json.dumps(messages)
            output_string = ''
            if hasattr(response, 'choices') and response.choices:
                if len(response.choices) > 0:
                    choice = response.choices[0]
                    if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                        output_string = choice.message.content or ''

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
