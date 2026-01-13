"""
Voice client implementation for STT and TTS usage tracking.
"""

import logging
from typing import Dict
from urllib.parse import urljoin

import requests

from .constants import (
    DeepgramSTTModels,
    MicrosoftAzureSpeechSTTModels,
    GoogleCloudSpeechSTTModels,
    AssemblyAISTTModels,
    AmazonPollyTTSModels,
    MicrosoftAzureSpeechTTSModels,
    GoogleCloudTextToSpeechTTSModels,
    DeepgramTTSModels,
)
from .models import SttModelPricing, TtsModelPricing


# STT model pricing (cost per hour in USD)
STT_MODEL_PRICING: Dict[str, SttModelPricing] = {
    # Deepgram Models
    DeepgramSTTModels.FLUX: SttModelPricing(cost_per_hour=0.462),  # $0.462 per hour
    DeepgramSTTModels.NOVA_3_MONOLINGUAL: SttModelPricing(cost_per_hour=0.462),  # $0.462 per hour
    DeepgramSTTModels.NOVA_3_MULTILINGUAL: SttModelPricing(cost_per_hour=0.552),  # $0.552 per hour
    DeepgramSTTModels.NOVA_1: SttModelPricing(cost_per_hour=0.348),  # $0.348 per hour
    DeepgramSTTModels.NOVA_2: SttModelPricing(cost_per_hour=0.348),  # $0.348 per hour
    DeepgramSTTModels.ENHANCED: SttModelPricing(cost_per_hour=0.99),  # $0.99 per hour
    DeepgramSTTModels.BASE: SttModelPricing(cost_per_hour=0.87),  # $0.87 per hour
    DeepgramSTTModels.REDACTION: SttModelPricing(cost_per_hour=0.12),  # $0.12 per hour (add-on)
    DeepgramSTTModels.KEYTERM_PROMPTING: SttModelPricing(cost_per_hour=0.072),  # $0.072 per hour (add-on)
    DeepgramSTTModels.SPEAKER_DIARIZATION: SttModelPricing(cost_per_hour=0.12),  # $0.12 per hour (add-on)

    # Microsoft Azure Speech Service Models
    MicrosoftAzureSpeechSTTModels.STANDARD: SttModelPricing(cost_per_hour=1.0),  # $1.0 per hour
    MicrosoftAzureSpeechSTTModels.CUSTOM: SttModelPricing(cost_per_hour=1.2),  # $1.2 per hour

    # Google Cloud Speech-to-Text Models
    GoogleCloudSpeechSTTModels.STANDARD: SttModelPricing(cost_per_hour=0.96),  # $0.96 per hour

    # AssemblyAI Models
    AssemblyAISTTModels.UNIVERSAL_STREAMING: SttModelPricing(cost_per_hour=0.15),  # $0.15 per hour
    AssemblyAISTTModels.UNIVERSAL_STREAMING_MULTILANG: SttModelPricing(cost_per_hour=0.15),  # $0.15 per hour
    AssemblyAISTTModels.KEYTERMS_PROMPTING: SttModelPricing(cost_per_hour=0.04),  # $0.04 per hour
}


# TTS model pricing (cost per 1 million characters in USD)
TTS_MODEL_PRICING: Dict[str, TtsModelPricing] = {
    # Amazon Polly Models
    AmazonPollyTTSModels.STANDARD: TtsModelPricing(cost_per_million_characters=0.4),  # $0.4 per 1 million characters
    AmazonPollyTTSModels.NEURAL: TtsModelPricing(cost_per_million_characters=16.0),  # $16 per 1 million characters
    AmazonPollyTTSModels.LONG_FORM: TtsModelPricing(cost_per_million_characters=100.0),  # $100 per 1 million characters
    AmazonPollyTTSModels.GENERATIVE: TtsModelPricing(cost_per_million_characters=30.0),  # $30 per 1 million characters

    # Microsoft Azure Speech Service TTS Models
    MicrosoftAzureSpeechTTSModels.STANDARD: TtsModelPricing(cost_per_million_characters=15.0),  # $15 per 1 million characters
    MicrosoftAzureSpeechTTSModels.CUSTOM: TtsModelPricing(cost_per_million_characters=24.0),  # $24 per 1 million characters
    MicrosoftAzureSpeechTTSModels.CUSTOM_NEURAL_HD: TtsModelPricing(cost_per_million_characters=48.0),  # $48 per 1 million characters

    # Google Cloud Text-to-Speech TTS Models
    GoogleCloudTextToSpeechTTSModels.CHIRP_3_HD: TtsModelPricing(cost_per_million_characters=30.0),  # $30 per 1 million characters
    GoogleCloudTextToSpeechTTSModels.INSTANT_CUSTOM: TtsModelPricing(cost_per_million_characters=60.0),  # $60 per 1 million characters
    GoogleCloudTextToSpeechTTSModels.WAVENET: TtsModelPricing(cost_per_million_characters=4.0),  # $4 per 1 million characters
    GoogleCloudTextToSpeechTTSModels.STUDIO: TtsModelPricing(cost_per_million_characters=160.0),  # $160 per 1 million characters
    GoogleCloudTextToSpeechTTSModels.STANDARD: TtsModelPricing(cost_per_million_characters=4.0),  # $4 per 1 million characters
    GoogleCloudTextToSpeechTTSModels.NEURAL2: TtsModelPricing(cost_per_million_characters=16.0),  # $16 per 1 million characters
    GoogleCloudTextToSpeechTTSModels.POLYGLOT_PREVIEW: TtsModelPricing(cost_per_million_characters=16.0),  # $16 per 1 million characters

    # Deepgram TTS Models
    DeepgramTTSModels.AURA_2: TtsModelPricing(cost_per_million_characters=30.0),  # $30 per 1 million characters
    DeepgramTTSModels.AURA_1: TtsModelPricing(cost_per_million_characters=15.0),  # $15 per 1 million characters
}


def _calculate_stt_cost(client_instance, model: str, audio_duration_seconds: int) -> float:
    """
    Calculate the cost based on STT model and audio duration.
    
    Args:
        client_instance: The Client instance
        model: The STT model name
        audio_duration_seconds: Audio duration in seconds
        
    Returns:
        Calculated cost in USD
    """
    pricing = STT_MODEL_PRICING.get(model)
    
    if not pricing:
        client_instance.logger.warning(f"Unknown STT model '{model}', using default pricing")
        # Use default pricing for unknown models (per hour)
        pricing = SttModelPricing(cost_per_hour=0.5)  # $0.50 per hour default
    
    # Calculate cost: (duration in seconds / 3600) * cost per hour
    # Convert seconds to hours and multiply by cost per hour
    duration_hours = audio_duration_seconds / 3600.0
    total_cost = duration_hours * pricing.cost_per_hour
    
    client_instance.logger.debug(
        f"STT cost calculation for model '{model}': "
        f"duration={audio_duration_seconds} seconds ({duration_hours:.6f} hours), "
        f"cost_per_hour={pricing.cost_per_hour:.6f}, total={total_cost:.6f}"
    )
    
    return total_cost


def _calculate_tts_cost(client_instance, model: str, character_count: int) -> float:
    """
    Calculate the cost based on TTS model and character count.
    
    Args:
        client_instance: The Client instance
        model: The TTS model name
        character_count: Number of characters
        
    Returns:
        Calculated cost in USD
    """
    pricing = TTS_MODEL_PRICING.get(model)
    
    if not pricing:
        client_instance.logger.warning(f"Unknown TTS model '{model}', using default pricing")
        # Use default pricing for unknown models (per 1 million characters)
        pricing = TtsModelPricing(cost_per_million_characters=10.0)  # $10 per 1 million characters default
    
    # Calculate cost: (character count / 1,000,000) * cost per 1 million characters
    # Convert character count to millions and multiply by cost per million
    characters_in_millions = character_count / 1000000.0
    total_cost = characters_in_millions * pricing.cost_per_million_characters
    
    client_instance.logger.debug(
        f"TTS cost calculation for model '{model}': "
        f"characters={character_count} ({characters_in_millions:.6f} millions), "
        f"cost_per_million={pricing.cost_per_million_characters:.6f}, total={total_cost:.6f}"
    )
    
    return total_cost


def send_stt_usage(client_instance, agent_id: str, customer_id: str, stt_usage_data) -> None:
    """
    Send STT usage data to the Paygent API.
    
    Args:
        client_instance: The Client instance
        agent_id: Unique identifier for the agent
        customer_id: Unique identifier for the customer
        stt_usage_data: SttUsageData containing model and audio duration information
        
    Raises:
        requests.RequestException: If the request fails
    """
    client_instance.logger.info(
        f"Starting send_stt_usage for agentID={agent_id}, customerID={customer_id}, "
        f"model={stt_usage_data.model}, duration={stt_usage_data.audio_duration} seconds"
    )
    
    try:
        # Calculate cost
        cost = _calculate_stt_cost(client_instance, stt_usage_data.model, stt_usage_data.audio_duration)
        client_instance.logger.info(f"Calculated STT cost: {cost:.6f} for model {stt_usage_data.model}")
        
        # Prepare API request
        api_request = {
            "agentId": agent_id,
            "customerId": customer_id,
            "indicator": "stt-usage",  # Default indicator for STT usage
            "amount": cost,
            "audioDuration": stt_usage_data.audio_duration,
            "model": stt_usage_data.model,
            "serviceProvider": stt_usage_data.service_provider,
        }
        
        # Make HTTP request
        url = urljoin(client_instance.base_url, "/api/v1/usage")
        headers = {
            "Content-Type": "application/json",
            "paygent-api-key": client_instance.api_key,
        }
        
        response = client_instance.session.post(url, json=api_request, headers=headers)
        response.raise_for_status()
        
        client_instance.logger.info(
            f"Successfully sent STT usage data for agentID={agent_id}, "
            f"customerID={customer_id}, cost={cost:.6f}"
        )
    except requests.RequestException as e:
        client_instance.logger.error(f"Failed to send STT usage data: {str(e)}")
        raise


def send_tts_usage(client_instance, agent_id: str, customer_id: str, tts_usage_data) -> None:
    """
    Send TTS usage data to the Paygent API.
    
    Args:
        client_instance: The Client instance
        agent_id: Unique identifier for the agent
        customer_id: Unique identifier for the customer
        tts_usage_data: TtsUsageData containing model and character count information
        
    Raises:
        requests.RequestException: If the request fails
    """
    client_instance.logger.info(
        f"Starting send_tts_usage for agentID={agent_id}, customerID={customer_id}, "
        f"model={tts_usage_data.model}, characters={tts_usage_data.character_count}"
    )
    
    try:
        # Calculate cost
        cost = _calculate_tts_cost(client_instance, tts_usage_data.model, tts_usage_data.character_count)
        client_instance.logger.info(f"Calculated TTS cost: {cost:.6f} for model {tts_usage_data.model}")
        
        # Prepare API request
        api_request = {
            "agentId": agent_id,
            "customerId": customer_id,
            "indicator": "tts-usage",  # Default indicator for TTS usage
            "amount": cost,
            "characterCount": tts_usage_data.character_count,
            "model": tts_usage_data.model,
            "serviceProvider": tts_usage_data.service_provider,
        }
        
        # Make HTTP request
        url = urljoin(client_instance.base_url, "/api/v1/usage")
        headers = {
            "Content-Type": "application/json",
            "paygent-api-key": client_instance.api_key,
        }
        
        response = client_instance.session.post(url, json=api_request, headers=headers)
        response.raise_for_status()
        
        client_instance.logger.info(
            f"Successfully sent TTS usage data for agentID={agent_id}, "
            f"customerID={customer_id}, cost={cost:.6f}"
        )
    except requests.RequestException as e:
        client_instance.logger.error(f"Failed to send TTS usage data: {str(e)}")
        raise


# Add methods to Client class
def _add_voice_methods_to_client():
    """Dynamically add voice methods to the Client class."""
    from .client import Client
    
    Client.send_stt_usage = send_stt_usage
    Client.send_tts_usage = send_tts_usage


# Call this function to attach methods when module is imported
_add_voice_methods_to_client()

