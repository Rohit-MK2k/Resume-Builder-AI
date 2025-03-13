import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialize the LLM
def get_llm():
    """Initialize and return the language model."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    return init_chat_model(
        "gpt-4o-mini", 
        model_provider="openai",
        temperature = 0.2,
    )