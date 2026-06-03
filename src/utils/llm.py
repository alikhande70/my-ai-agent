from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.0):
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    grok_key = os.getenv("GROK_API_KEY")

    if groq_key:
        return ChatGroq(model=model, temperature=temperature)
    elif grok_key:
        return ChatOpenAI(
            model="grok-beta",
            api_key=grok_key,
            base_url="https://api.x.ai/v1",
            temperature=temperature
        )
    elif openai_key:
        return ChatOpenAI(model=model, temperature=temperature)
    else:
        raise ValueError("No LLM API key found in environment variables!")