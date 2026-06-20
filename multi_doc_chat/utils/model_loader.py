import os
import sys
import json
from dotenv import load_dotenv
from multi_doc_chat.utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings  # <--- Clean, compiled at startup!
from multi_doc_chat.logger import GLOBAL_LOGGER as log
from multi_doc_chat.exception.custom_exception import DocumentPortalException



class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY", "GOOGLE_API_KEY"]


    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("apikeyliveclass")

        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise ValueError("API_KEYS is not a valid JSON object")
                self.api_keys = parsed
                log.info("Loaded API_KEYS from ECS secret")
            except Exception as e:
                log.warning("Failed to parse API_KEYS as JSON", error=str(e))




        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)
                if env_val:
                    self.api_keys[key] = env_val
                    log.info(f"Loaded {key} from individual env var")

        # Final check
        missing = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
        if missing:
            log.error("Missing required API keys", missing_keys=missing)
            raise DocumentPortalException("Missing API keys", sys)

        log.info("API keys loaded", keys={k: v[:6] + "..." for k, v in self.api_keys.items()})


    def get(self, key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val


class ModelLoader:
    """
    Loads embedding models and LLMs based on config and environment.
    """

    def __init__(self):
        if os.getenv("ENV", "local").lower() != "production":
            load_dotenv()
            log.info("Running in LOCAL mode: .env loaded")
        else:
            log.info("Running in PRODUCTION mode")

        self.api_key_mgr = ApiKeyManager()
        self.config = load_config()
        log.info("YAML config loaded", config_keys=list(self.config.keys()))


    def load_embeddings(self):
        """
        Load and return the configured embedding model based on provider settings.
        """
        try:
            provider = self.config["embedding_model"].get("provider", "google").lower()
            model_name = self.config["embedding_model"]["model_name"]

            if provider == "google":
                log.info("Loading Google embedding model", model=model_name)
                return GoogleGenerativeAIEmbeddings(
                    model=model_name,
                    google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY") # type: ignore
                )
            
            elif provider == "huggingface":
                log.info("Loading Hugging Face embedding model locally", model=model_name)
                return HuggingFaceEmbeddings(model_name=model_name)
            
            else:
                log.error("Unsupported embedding provider", provider=provider)
                raise ValueError(f"Unsupported embedding provider: {provider}")

        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise DocumentPortalException("Failed to load embedding model", sys)


    def load_llm(self):
        """
        Load Hugging Face as the primary LLM, with Groq and Google as automatic fallbacks
        if the API key is absent or a network request fails (e.g., Rate Limits).
        """
        llm_block = self.config["llm"]
        fallbacks = []
        primary_llm = None
        
        # 1. Initialize Groq (Fallback 1)
        groq_conf = llm_block.get("groq", {})
        groq_llm = ChatGroq(
            model=groq_conf.get("model_name", "llama3-8b-8192"),
            api_key=self.api_key_mgr.get("GROQ_API_KEY"), # type: ignore
            temperature=groq_conf.get("temperature", 0.2),
        )
        
        # 2. Initialize Google (Fallback 2)
        google_conf = llm_block.get("google", {})
        google_llm = ChatGoogleGenerativeAI(
            model=google_conf.get("model_name", "gemini-2.0-flash"),
            google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY"), # type: ignore
            temperature=google_conf.get("temperature", 0.2),
            max_output_tokens=google_conf.get("max_output_tokens", 2048)
        )
        
        # 3. Initialize Hugging Face (Primary)
        hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        hf_conf = llm_block.get("huggingface")
        
        if hf_token and hf_conf:
            try:
                from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
                log.info("Loading Hugging Face API as Primary LLM")
                
                # Setup the remote endpoint
                hf_endpoint = HuggingFaceEndpoint(
                    repo_id=hf_conf.get("model_name", "mistralai/Mistral-7B-Instruct-v0.2"),
                    temperature=hf_conf.get("temperature", 0.1),
                    max_new_tokens=hf_conf.get("max_output_tokens", 2048),
                    huggingfacehub_api_token=hf_token,
                )
                # Wrap it in ChatHuggingFace for Conversational RAG compatibility
                primary_llm = ChatHuggingFace(llm=hf_endpoint)
                
                # If HF fails during chat, try Groq, then Google
                fallbacks = [groq_llm, google_llm]
                
            except Exception as e:
                log.warning("Failed to initialize Hugging Face, falling back to Groq", error=str(e))
                primary_llm = groq_llm
                fallbacks = [google_llm]
        else:
            log.warning("Hugging Face token or config absent. Using Groq as Primary LLM.")
            primary_llm = groq_llm
            fallbacks = [google_llm]

        # Wrap the primary model with the fallback chain
        log.info("LLM configured with fallbacks", primary=primary_llm.__class__.__name__)
        return primary_llm.with_fallbacks(fallbacks)

if __name__ == "__main__":
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result}")

    # Test LLM
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")