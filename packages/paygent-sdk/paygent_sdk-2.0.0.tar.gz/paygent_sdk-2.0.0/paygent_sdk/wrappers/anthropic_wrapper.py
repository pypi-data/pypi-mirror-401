"""
Anthropic wrapper for automatic usage tracking with Paygent.
This wrapper intercepts Anthropic API calls and automatically sends usage data to Paygent.
"""

import json
from typing import Any

try:
    from anthropic import Anthropic
except ImportError:
    raise ImportError(
        "anthropic package is a peer-dependency. To use the Paygent wrapper around anthropic "
        "you're assumed to already have anthropic package installed."
    )

from ..client import Client
from ..models import UsageData, UsageDataWithStrings


class PaygentAnthropic:
    """Main wrapper class for Anthropic that provides automatic usage tracking."""

    def __init__(self, anthropic_client: Anthropic, paygent_client: Client):
        """
        Create a new PaygentAnthropic wrapper.
        
        Args:
            anthropic_client: The Anthropic client instance
            paygent_client: The Paygent client instance for usage tracking
        """
        self.anthropic = anthropic_client
        self.paygent_client = paygent_client

    @property
    def messages(self) -> 'MessagesWrapper':
        """Access to messages API with automatic usage tracking."""
        return MessagesWrapper(self.anthropic, self.paygent_client)


class MessagesWrapper:
    """Wrapper for Anthropic messages API."""

    def __init__(self, anthropic_client: Anthropic, paygent_client: Client):
        self.anthropic = anthropic_client
        self.paygent_client = paygent_client

    def create(
        self,
        *,
        model: str,
        messages: list,
        max_tokens: int,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> Any:
        """
        Create a message with automatic usage tracking.
        Note: Streaming is not supported with automatic tracking.
        
        Args:
            model: The model to use
            messages: The messages to send
            max_tokens: Maximum tokens to generate
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional Anthropic parameters
            
        Returns:
            The message response from Anthropic
        """
        # Ensure streaming is disabled for automatic tracking
        kwargs['stream'] = False

        # Make the Anthropic API call (non-streaming)
        response = self.anthropic.messages.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            **kwargs
        )

        # Extract usage data from response with robust fallback mechanism
        has_valid_usage = (
            hasattr(response, 'usage') and
            response.usage and
            response.usage.input_tokens > 0 and
            response.usage.output_tokens > 0
        )

        if has_valid_usage:
            # Primary path: Use usage data from API response
            usage_data = UsageData(
                service_provider=model,
                model=model,
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens
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
            if hasattr(response, 'content') and response.content:
                if len(response.content) > 0 and hasattr(response.content[0], 'text'):
                    output_string = response.content[0].text or ''

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
