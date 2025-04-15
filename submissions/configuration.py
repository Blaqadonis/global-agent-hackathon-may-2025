"""Configuration module for Aza Man financial assistant.

This module defines the configurable parameters for initializing and running the Aza Man
application, including user identification, model selection, and system prompt formatting.
Supports multiple LLM providers (Groq, Together, OpenRouter) for flexible model switching.
"""

from dataclasses import dataclass, field, fields
from typing import Optional, Union
from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated
from langchain_groq import ChatGroq
from langchain_together import ChatTogether
from langchain_openai import ChatOpenAI
import os
import prompts
import tools

@dataclass(kw_only=True)
class Configuration:
    """Configuration class for the Aza Man financial assistant.

    Encapsulates settings for user identification, thread management, language model, and
    system prompt. Supports dynamic LLM provider selection (Groq, Together, OpenRouter).

    Attributes:
        user_id (str): Unique identifier for the user. Defaults to "default".
        thread_id (str): Identifier for the conversation thread. Defaults to "default".
        model (Annotated[str, dict]): Language model name with metadata. Defaults to
            "google/gemini-2.0-flash-lite-preview-02-05:free".
        provider (str): LLM provider ("groq", "together", "openrouter"). Defaults to "openrouter".
        system_prompt (str): Template for the system prompt, sourced from prompts module.
    """
    user_id: str = "default"
    thread_id: str = "default"
    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="google/gemini-2.0-flash-lite-preview-02-05:free", 
        metadata={"description": "The name of the language model to use."}
    )
    provider: str = field(
        default="openrouter",
        metadata={"description": "The LLM provider to use: 'groq', 'together', or 'openrouter'."}
    )
    system_prompt: str = prompts.SYSTEM_PROMPT

    def get_llm(self) -> Union[ChatGroq, ChatTogether, ChatOpenAI]:
        """Initialize and return the language model with bound tools based on the provider.

        Configures the appropriate LLM client (Groq, Together, or OpenRouter) using the
        specified model and provider settings, binding available financial tools.

        Returns:
            Union[ChatGroq, ChatTogether, ChatOpenAI]: Configured language model instance.

        Raises:
            ValueError: If an invalid provider is specified.
        """
        if self.provider.lower() == "groq":
            llm = ChatGroq(
                model=self.model,
                api_key=os.environ.get("GROQ_API_KEY")
            )
        elif self.provider.lower() == "together":
            llm = ChatTogether(
                model=self.model,
                api_key=os.environ.get("TOGETHER_API_KEY")
            )
        elif self.provider.lower() == "openrouter":
            llm = ChatOpenAI(
                model=self.model,
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
                default_headers={
                    #"HTTP-Referer": "http://localhost:your-port",  
                    "X-Title": "Aza Man"       
                }
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}. Use 'groq', 'together', or 'openrouter'.")
        return llm.bind_tools(tools.ALL_TOOLS)

    def format_system_prompt(self, state) -> str:
        """Format the system prompt with current state values.

        Substitutes state variables into the system prompt template. Falls back to the
        unformatted prompt if formatting fails due to missing keys.

        Args:
            state: The current state object containing user and financial data.

        Returns:
            str: The formatted system prompt string.
        """
        format_args = {
            "username": state.username or "Unknown",
            "income": float(state.income or 0.0),
            "budget_for_expenses": float(state.budget_for_expenses or 0.0),
            "expense": float(state.expense or 0.0),
            "expenses": str(state.expenses or []),
            "savings_goal": float(state.savings_goal or 0.0),
            "savings": float(state.savings or 0.0),
            "currency": state.currency or "",
            "summary": state.summary or "No prior conversation summary available."
        }
        try:
            return self.system_prompt.format(**format_args)
        except KeyError:
            # Silently fall back to unformatted prompt if state data is incomplete
            return self.system_prompt

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig or environment variables.

        Constructs a Configuration object by prioritizing values from the provided
        RunnableConfig, falling back to environment variables if not specified.

        Args:
            config (Optional[RunnableConfig]): Configuration data from LangGraph runtime.

        Returns:
            Configuration: A new instance with resolved configuration values.
        """
        configurable = config["configurable"] if config and "configurable" in config else {}
        values = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls) if f.init
        }
        return cls(**{k: v for k, v in values.items() if v is not None})