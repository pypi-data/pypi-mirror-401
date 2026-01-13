"""
Paygent SDK for Python

A Python SDK for integrating with the Paygent API to track usage and costs for AI models.

For the Go SDK equivalent, see: https://github.com/paygent/paygent-sdk-go
"""

from .client import Client
from .models import (
    UsageData, UsageDataWithStrings, APIRequest, ModelPricing, MODEL_PRICING,
    SttUsageData, TtsUsageData, SttModelPricing, TtsModelPricing
)
from .voice_client import send_stt_usage, send_tts_usage  # Import to attach methods to Client

# Import wrappers with optional LangChain support
try:
    from .wrappers import (
        PaygentOpenAI,
        PaygentAnthropic,
        PaygentMistral,
        PaygentGemini,
        PaygentLangChainCallback
    )
    _has_langchain = True
except ImportError:
    from .wrappers import (
        PaygentOpenAI,
        PaygentAnthropic,
        PaygentMistral,
        PaygentGemini
    )
    _has_langchain = False
from .constants import (
    ServiceProvider,
    OpenAIModels,
    AnthropicModels,
    GoogleDeepMindModels,
    MetaModels,
    AWSModels,
    MistralAIModels,
    CohereModels,
    DeepSeekModels,
    DeepgramSTTModels,
    MicrosoftAzureSpeechSTTModels,
    GoogleCloudSpeechSTTModels,
    AssemblyAISTTModels,
    AmazonPollyTTSModels,
    MicrosoftAzureSpeechTTSModels,
    GoogleCloudTextToSpeechTTSModels,
    DeepgramTTSModels,
    is_model_supported
)

__version__ = "1.0.0"
__all__ = [
    # Core classes
    "Client",
    "UsageData", 
    "UsageDataWithStrings", 
    "APIRequest", 
    "ModelPricing",
    "MODEL_PRICING",
    
    # Voice data models
    "SttUsageData",
    "TtsUsageData",
    "SttModelPricing",
    "TtsModelPricing",
    
    # Wrappers
    "PaygentOpenAI",
    "PaygentAnthropic",
    "PaygentMistral",
    "PaygentGemini",
    
    # Constants
    "ServiceProvider",
    "OpenAIModels",
    "AnthropicModels", 
    "GoogleDeepMindModels",
    "MetaModels",
    "AWSModels",
    "MistralAIModels",
    "CohereModels",
    "DeepSeekModels",
    
    # STT/TTS Model constants
    "DeepgramSTTModels",
    "MicrosoftAzureSpeechSTTModels",
    "GoogleCloudSpeechSTTModels",
    "AssemblyAISTTModels",
    "AmazonPollyTTSModels",
    "MicrosoftAzureSpeechTTSModels",
    "GoogleCloudTextToSpeechTTSModels",
    "DeepgramTTSModels",
    
    # Utility functions
    "is_model_supported"
]
