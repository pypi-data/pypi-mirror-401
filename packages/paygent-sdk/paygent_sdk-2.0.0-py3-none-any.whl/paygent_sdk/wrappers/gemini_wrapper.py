"""
Google Gemini wrapper for automatic usage tracking with Paygent.
This wrapper intercepts Gemini API calls and automatically sends usage data to Paygent.

Usage is identical to the standard google-genai SDK, with only the addition of tracking parameters.
"""

import json
from typing import Any

try:
    from google import genai
except ImportError:
    raise ImportError(
        "google-genai package is a peer-dependency. To use the Paygent wrapper around google-genai "
        "you're assumed to already have google-genai package installed."
    )

from ..client import Client
from ..models import UsageData, UsageDataWithStrings


class PaygentGemini:
    """Main wrapper class for Google Gemini that provides automatic usage tracking."""

    def __init__(self, gemini_client: genai.Client, paygent_client: Client):
        """
        Create a new PaygentGemini wrapper.
        
        Args:
            gemini_client: The GoogleGenAI client instance from google-genai
            paygent_client: The Paygent client instance for usage tracking
        """
        self.gemini = gemini_client
        self.paygent_client = paygent_client

    @property
    def models(self) -> 'ModelsWrapper':
        """Access to models API with automatic usage tracking."""
        return ModelsWrapper(self.gemini, self.paygent_client)


class ModelsWrapper:
    """Wrapper for Gemini models API."""

    def __init__(self, gemini_client: genai.Client, paygent_client: Client):
        self.gemini = gemini_client
        self.paygent_client = paygent_client

    def generate_content(
        self,
        *,
        model: str,
        contents: Any,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> Any:
        """
        Generate content with automatic usage tracking.
        
        Args:
            model: The model to use
            contents: The content to generate from
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional Gemini parameters
            
        Returns:
            The generation response from Gemini
        """
        # Make the Gemini API call using the standard SDK method
        response = self.gemini.models.generate_content(
            model=model,
            contents=contents,
            **kwargs
        )

        # Extract usage data from response with robust fallback mechanism
        has_valid_usage = (
            hasattr(response, 'usage_metadata') and
            response.usage_metadata and
            (response.usage_metadata.prompt_token_count > 0 or
             response.usage_metadata.candidates_token_count > 0)
        )

        if has_valid_usage:
            # Primary path: Use usage metadata from API response
            usage_data = UsageData(
                service_provider=model,
                model=model,
                prompt_tokens=response.usage_metadata.prompt_token_count or 0,
                completion_tokens=response.usage_metadata.candidates_token_count or 0,
                total_tokens=response.usage_metadata.total_token_count or 0
            )

            self.paygent_client.send_usage(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data
            )
        else:
            # Fallback path: Calculate tokens from actual strings
            prompt_string = json.dumps(contents) if not isinstance(contents, str) else contents
            output_string = ''
            
            if hasattr(response, 'candidates') and response.candidates:
                if len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        if len(candidate.content.parts) > 0:
                            part = candidate.content.parts[0]
                            if hasattr(part, 'text'):
                                output_string = part.text or ''

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

    def start_chat(
        self,
        *,
        model: str,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> 'ChatSessionWrapper':
        """
        Start a chat session with automatic usage tracking.
        
        Args:
            model: The model to use
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional chat configuration
            
        Returns:
            A wrapped chat session with automatic tracking
        """
        # Start chat session using the standard SDK
        chat_session = self.gemini.models.start_chat(model=model, **kwargs)

        return ChatSessionWrapper(
            chat_session,
            self.paygent_client,
            model,
            indicator,
            external_agent_id,
            external_customer_id
        )

    def generate_image(
        self,
        *,
        model: str,
        prompt: str,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str,
        **kwargs
    ) -> Any:
        """
        Generate images with automatic usage tracking.
        
        Args:
            model: The model to use (e.g., "imagen-3.0-generate-001")
            prompt: The prompt for image generation
            indicator: Indicator for the usage event
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
            **kwargs: Additional image generation parameters
            
        Returns:
            The image generation response
        """
        # Make the image generation API call
        response = self.gemini.models.generate_content(
            model=model,
            contents=prompt,
            **kwargs
        )

        # Extract usage data from response with robust fallback mechanism
        has_valid_usage = (
            hasattr(response, 'usage_metadata') and
            response.usage_metadata and
            (response.usage_metadata.prompt_token_count > 0 or
             response.usage_metadata.candidates_token_count > 0)
        )

        if has_valid_usage:
            # Primary path: Use usage metadata from API response
            usage_data = UsageData(
                service_provider=model,
                model=model,
                prompt_tokens=response.usage_metadata.prompt_token_count or 0,
                completion_tokens=response.usage_metadata.candidates_token_count or 0,
                total_tokens=response.usage_metadata.total_token_count or 0
            )

            self.paygent_client.send_usage(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data
            )
        else:
            # Fallback path: Calculate tokens from prompt string
            usage_data_with_strings = UsageDataWithStrings(
                service_provider=model,
                model=model,
                prompt_string=prompt,
                output_string=''  # Image generation doesn't have text output
            )

            self.paygent_client.send_usage_with_token_string(
                external_agent_id,
                external_customer_id,
                indicator,
                usage_data_with_strings
            )

        return response


class ChatSessionWrapper:
    """Wrapper for Gemini ChatSession."""

    def __init__(
        self,
        chat_session: Any,
        paygent_client: Client,
        model_name: str,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str
    ):
        self.chat_session = chat_session
        self.paygent_client = paygent_client
        self.model_name = model_name
        self.indicator = indicator
        self.external_agent_id = external_agent_id
        self.external_customer_id = external_customer_id

    def send_message(self, message: str) -> Any:
        """
        Send a message in the chat with automatic usage tracking.
        
        Args:
            message: The message to send
            
        Returns:
            The chat response from Gemini
        """
        # Make the Gemini API call
        response = self.chat_session.send_message(message)

        # Extract usage data from response with robust fallback mechanism
        has_valid_usage = (
            hasattr(response, 'usage_metadata') and
            response.usage_metadata and
            (response.usage_metadata.prompt_token_count > 0 or
             response.usage_metadata.candidates_token_count > 0)
        )

        if has_valid_usage:
            # Primary path: Use usage metadata from API response
            usage_data = UsageData(
                service_provider=self.model_name,
                model=self.model_name,
                prompt_tokens=response.usage_metadata.prompt_token_count or 0,
                completion_tokens=response.usage_metadata.candidates_token_count or 0,
                total_tokens=response.usage_metadata.total_token_count or 0
            )

            self.paygent_client.send_usage(
                self.external_agent_id,
                self.external_customer_id,
                self.indicator,
                usage_data
            )
        else:
            # Fallback path: Calculate tokens from message and response
            output_string = ''
            if hasattr(response, 'candidates') and response.candidates:
                if len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        if len(candidate.content.parts) > 0:
                            part = candidate.content.parts[0]
                            if hasattr(part, 'text'):
                                output_string = part.text or ''

            usage_data_with_strings = UsageDataWithStrings(
                service_provider=self.model_name,
                model=self.model_name,
                prompt_string=message,
                output_string=output_string
            )

            self.paygent_client.send_usage_with_token_string(
                self.external_agent_id,
                self.external_customer_id,
                self.indicator,
                usage_data_with_strings
            )

        return response

    def get_history(self) -> Any:
        """
        Get the chat history.
        
        Returns:
            The chat history
        """
        return self.chat_session.get_history()
