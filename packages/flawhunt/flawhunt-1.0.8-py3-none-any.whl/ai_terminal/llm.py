"""
LLM wrapper for FlawHunt CLI.
Handles Gemini and Groq API integration and model management.
"""
import os
from typing import Optional, Literal

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

from rich.console import Console

console = Console()

# Default to Groq provider and specified model
DEFAULT_MODEL = "moonshotai/kimi-k2-instruct-0905"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")
GROQ_API_KEY = os.getenv("GROQ_API_KEY","")
GROQ_FALLBACK_MODEL = os.getenv("GROQ_FALLBACK_MODEL", "meta-llama/llama-4-maverick-17b-128e-instruct")

# Available models for each provider
GEMINI_MODELS = [
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash"
]

GROQ_MODELS = [
    "deepseek-r1-distill-llama-70b",
    "moonshotai/kimi-k2-instruct-0905 ",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "llama-3.1-8b-instant",
    "moonshotai/kimi-k2-instruct-0905"
]

class LLM:
    """Wrapper class for LLM interactions."""
    
    def __init__(self, model: str = DEFAULT_MODEL, provider: str = "groq", gemini_api_key: str = None, groq_api_key: str = None):
        self.model = model
        self.provider = provider
        self.langchain_mode = False
        self.lc_model = None
        self.sdk_model = None
        
        # Use provided API keys or fall back to environment
        gemini_key = gemini_api_key or GEMINI_API_KEY
        groq_key = groq_api_key or GROQ_API_KEY
        
        if provider == "groq":
            if not groq_key:
                console.print(f"[red]Groq API key not provided. Please set GROQ_API_KEY environment variable.[/red]")
            elif ChatGroq is None:
                console.print(f"[red]langchain_groq not installed. Run: pip install langchain-groq[/red]")
            else:
                # Try primary model first, then fallback
                for candidate_model in [model, GROQ_FALLBACK_MODEL]:
                    try:
                        self.lc_model = ChatGroq(
                            model=candidate_model,
                            api_key=groq_key,
                            temperature=0,
                            max_tokens=None,
                            timeout=None,
                            max_retries=2
                        )
                        # Track actual model in use
                        self.model = candidate_model
                        self.langchain_mode = True
                        if candidate_model != model:
                            console.print(f"[yellow]Using fallback Groq model: {candidate_model}[/yellow]")
                        break
                    except Exception as e:
                        # Try next candidate
                        self.lc_model = None
                        continue
                if self.lc_model is None:
                    console.print(f"[red]Groq API init failed for both primary '{model}' and fallback '{GROQ_FALLBACK_MODEL}'.[/red]")
                    console.print(f"[yellow]Please check your API key at: https://console.groq.com/keys[/yellow]")
        
        elif provider == "gemini":
            if ChatGoogleGenerativeAI is not None and gemini_key:
                try:
                    self.lc_model = ChatGoogleGenerativeAI(
                        model=model, 
                        google_api_key=gemini_key, 
                        temperature=0.2
                    )
                    self.langchain_mode = True
                except Exception as e:
                    console.print(f"[yellow]LangChain Google GenAI init failed: {e}. Falling back to direct SDK.[/yellow]")
            
            if not self.langchain_mode and genai is not None and gemini_key:
                genai.configure(api_key=gemini_key)
                try:
                    self.sdk_model = genai.GenerativeModel(model_name=model)
                except Exception as e:
                    console.print(f"[red]Gemini SDK init failed: {e}[/red]")
                    self.sdk_model = None
        
        if not self.langchain_mode and self.sdk_model is None:
            console.print(f"[red]Failed to initialize {provider} provider with model {model}[/red]")

    def invoke(self, prompt: str) -> str:
        """Generate response from the LLM."""
        if self.langchain_mode and self.lc_model is not None:
            try:
                resp = self.lc_model.invoke(prompt)
                return getattr(resp, "content", str(resp))
            except Exception as e:
                # Attempt runtime fallback for Groq if invocation fails
                if self.provider == "groq" and self.model != GROQ_FALLBACK_MODEL and ChatGroq is not None:
                    try:
                        self.lc_model = ChatGroq(
                            model=GROQ_FALLBACK_MODEL,
                            api_key=os.getenv("GROQ_API_KEY", ""),
                            temperature=0,
                            max_tokens=None,
                            timeout=None,
                            max_retries=2
                        )
                        self.model = GROQ_FALLBACK_MODEL
                        console.print(f"[yellow]Switched to fallback Groq model due to error: {e}[/yellow]")
                        resp = self.lc_model.invoke(prompt)
                        return getattr(resp, "content", str(resp))
                    except Exception:
                        pass
                raise
        
        if self.sdk_model is not None:
            resp = self.sdk_model.generate_content(prompt)
            return getattr(resp, "text", str(resp))
        
        raise RuntimeError("No LLM available. Set GEMINI_API_KEY and install deps.")

    def generate_command_help(self, command: str) -> str:
        """Generate helpful documentation for a command."""
        prompt = f"""
        Generate comprehensive help for the command: {command}
        
        Include:
        1. Brief description (1-2 sentences)
        2. Common usage examples (3-5 examples)
        3. Important flags and options
        4. Related commands
        5. Common pitfalls to avoid
        
        Format as a clear, practical guide.
        """
        return self.invoke(prompt)

    def explain_error(self, command: str, error_output: str) -> str:
        """Explain an error and provide solutions."""
        prompt = f"""
        Command: {command}
        Error: {error_output}
        
        Explain what went wrong and provide:
        1. Clear explanation of the error
        2. 2-3 possible solutions
        3. How to prevent this in the future
        4. Alternative commands if applicable
        
        Keep it concise and actionable.
        """
        return self.invoke(prompt)
