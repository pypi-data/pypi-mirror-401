"""
LangChain callback handler for automatic usage tracking with Paygent.
This callback intercepts LangChain LLM calls and automatically sends usage data to Paygent.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

try:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.outputs import LLMResult
except ImportError:
    raise ImportError(
        "LangChain is required for this integration. "
        "Install it with: pip install langchain-core"
    )

from ..client import Client
from ..models import UsageData, UsageDataWithStrings


class PaygentLangChainCallback(BaseCallbackHandler):
    """
    LangChain callback handler that automatically tracks usage with Paygent.
    
    Usage example:
    ```python
    from paygent_sdk import Client, PaygentLangChainCallback
    from langchain_openai import ChatOpenAI
    
    paygent_client = Client("your-api-key")
    callback = PaygentLangChainCallback(
        paygent_client,
        indicator="chat_completion",
        external_agent_id="agent-123",
        external_customer_id="customer-456"
    )
    
    llm = ChatOpenAI(callbacks=[callback])
    response = llm.invoke("Hello!")
    # Usage automatically tracked!
    ```
    """
    
    def __init__(
        self,
        paygent_client: Client,
        indicator: str,
        external_agent_id: str,
        external_customer_id: str
    ):
        """
        Create a new PaygentLangChainCallback.
        
        Args:
            paygent_client: The Paygent client instance for usage tracking
            indicator: Indicator for the usage event (e.g., "chat_completion")
            external_agent_id: External agent identifier
            external_customer_id: External customer identifier
        """
        super().__init__()
        self.paygent_client = paygent_client
        self.indicator = indicator
        self.external_agent_id = external_agent_id
        self.external_customer_id = external_customer_id
        self.run_info: Dict[UUID, Dict[str, str]] = {}
    
    def _extract_provider(self, serialized: Dict[str, Any]) -> str:
        """Extract the service provider from the serialized LLM data."""
        if not serialized:
            return "unknown"
        
        # Check id field
        if "id" in serialized:
            id_list = serialized["id"]
            if isinstance(id_list, list):
                id_str = " ".join(id_list).lower()
            else:
                id_str = str(id_list).lower()
            
            if "openai" in id_str:
                return "openai"
            if "anthropic" in id_str:
                return "anthropic"
            if "mistral" in id_str:
                return "mistral"
            if "cohere" in id_str:
                return "cohere"
            if "google" in id_str or "gemini" in id_str:
                return "gemini"
            if "huggingface" in id_str:
                return "huggingface"
            if "azure" in id_str:
                return "azure"
        
        # Check name field
        if "name" in serialized:
            name = str(serialized["name"]).lower()
            if "openai" in name:
                return "openai"
            if "anthropic" in name:
                return "anthropic"
            if "mistral" in name:
                return "mistral"
            if "gemini" in name or "google" in name:
                return "gemini"
        
        return "unknown"
    
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM starts running."""
        try:
            provider = self._extract_provider(serialized)
            model_name = metadata.get("ls_model_name", "unknown") if metadata else "unknown"
            
            # Store the run info for use in on_llm_end
            self.run_info[run_id] = {
                "provider": provider,
                "model_name": model_name
            }
        except Exception as e:
            print(f"Error in on_llm_start: {e}")
    
    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM ends running."""
        try:
            # Get the stored run info
            info = self.run_info.get(run_id, {})
            provider = info.get("provider", "unknown")
            model_name = info.get("model_name", "unknown")
            
            # Extract usage information from LangChain's LLMResult
            llm_output = response.llm_output or {}
            
            prompt_tokens = 0
            completion_tokens = 0
            total_tokens = 0
            
            # OpenAI-style usage (in llm_output["token_usage"])
            if "token_usage" in llm_output:
                token_usage = llm_output["token_usage"]
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)
                total_tokens = token_usage.get("total_tokens", 0)
            
            # Anthropic-style usage (in llm_output["usage"])
            elif "usage" in llm_output:
                usage = llm_output["usage"]
                prompt_tokens = usage.get("input_tokens", usage.get("prompt_tokens", 0))
                completion_tokens = usage.get("output_tokens", usage.get("completion_tokens", 0))
                total_tokens = prompt_tokens + completion_tokens
            
            # Gemini-style usage (in generations[0].message.usage_metadata)
            elif (response.generations and 
                  len(response.generations) > 0 and 
                  len(response.generations[0]) > 0):
                gen = response.generations[0][0]
                if hasattr(gen, "message") and hasattr(gen.message, "usage_metadata"):
                    usage_metadata = gen.message.usage_metadata
                    prompt_tokens = getattr(usage_metadata, "input_tokens", 0)
                    completion_tokens = getattr(usage_metadata, "output_tokens", 0)
                    total_tokens = getattr(usage_metadata, "total_tokens", 0)
            
            # Try to extract model name from response if not already set
            if model_name == "unknown":
                if "model_name" in llm_output:
                    model_name = llm_output["model_name"]
                elif (response.generations and 
                      len(response.generations) > 0 and 
                      len(response.generations[0]) > 0):
                    gen = response.generations[0][0]
                    if hasattr(gen, "message") and hasattr(gen.message, "response_metadata"):
                        model_name = gen.message.response_metadata.get("model_name", "unknown")
            
            # Send usage data if we have token information
            if total_tokens > 0:
                usage_data = UsageData(
                    service_provider=provider,
                    model=model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens
                )
                
                self.paygent_client.send_usage(
                    self.external_agent_id,
                    self.external_customer_id,
                    self.indicator,
                    usage_data
                )
            else:
                # Fallback: use string-based tracking
                # Extract prompt and output strings
                prompt_string = ""
                if response.generations and len(response.generations) > 0:
                    # Get the first generation's text
                    if len(response.generations[0]) > 0:
                        prompt_string = str(response.generations[0][0].text)
                
                output_string = ""
                if response.generations and len(response.generations) > 0:
                    outputs = [gen.text for gen in response.generations[0]]
                    output_string = " ".join(outputs)
                
                usage_data_with_strings = UsageDataWithStrings(
                    service_provider=provider,
                    model=model_name,
                    prompt_string=prompt_string,
                    output_string=output_string
                )
                
                self.paygent_client.send_usage_with_token_string(
                    self.external_agent_id,
                    self.external_customer_id,
                    self.indicator,
                    usage_data_with_strings
                )
            
            # Clean up the run info
            if run_id in self.run_info:
                del self.run_info[run_id]
                
        except Exception as e:
            print(f"Error tracking LangChain usage with Paygent: {e}")
            if run_id in self.run_info:
                del self.run_info[run_id]
    
    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM encounters an error."""
        print(f"LLM error: {error}")
        # Clean up the run info
        if run_id in self.run_info:
            del self.run_info[run_id]
