"""LangChain integration module"""

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List


def create_langchain_agent(
    api_key: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
    tools: List,
    system_prompt: str
):
    """
    Create a LangChain agent with specified configuration
    
    Args:
        api_key: Google API key
        model_name: Model name (e.g., 'gemini-2.0-flash-exp')
        temperature: Temperature for model
        max_tokens: Max tokens for response
        tools: List of tools to provide to agent
        system_prompt: System prompt for agent
    
    Returns:
        Configured LangChain agent
    """
    # Build ChatGoogleGenerativeAI model
    model = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Create agent with automatic tool looping
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
    )
    
    return agent
