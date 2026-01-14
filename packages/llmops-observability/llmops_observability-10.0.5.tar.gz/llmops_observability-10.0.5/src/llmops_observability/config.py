"""
Configuration management for LLMOps Observability
Direct Langfuse client configuration + SQS event streaming
"""
import os
import logging
from typing import Optional, Dict, Any
from langfuse import Langfuse
import httpx
from dotenv import load_dotenv
import warnings

# Configure logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[llmops_observability] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Suppress OpenTelemetry errors - they don't affect SDK functionality

 

# Suppress SSL warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Load environment variables
load_dotenv()

# Global Langfuse client
_langfuse_client: Optional[Langfuse] = None


def get_langfuse_client() -> Langfuse:
    """
    Get or create the global Langfuse client.
    
    Environment variables:
        - LANGFUSE_PUBLIC_KEY: Langfuse public key
        - LANGFUSE_SECRET_KEY: Langfuse secret key
        - LANGFUSE_BASE_URL: Langfuse base URL
        - LANGFUSE_VERIFY_SSL: Whether to verify SSL (default: false)
        - ENV: Environment name (e.g., "production", "development") - mapped to LANGFUSE_TRACING_ENVIRONMENT
    
    Returns:
        Langfuse: Configured Langfuse client
    """
    global _langfuse_client
    
    if _langfuse_client is None:
        verify_ssl = os.getenv("LANGFUSE_VERIFY_SSL", "false").lower() == "false"
        
        # Set LANGFUSE_TRACING_ENVIRONMENT from ENV variable
        # This applies environment to all traces and observations automatically
        # Convert to lowercase as Langfuse requires lowercase environment names
        env_value = os.getenv("ENV", "development").lower()
        os.environ["LANGFUSE_TRACING_ENVIRONMENT"] = env_value
        
        # Create custom HTTP client with optional SSL verification
        httpx_client = httpx.Client(verify=verify_ssl) if not verify_ssl else None
        
        # Control Langfuse debug logging via LANGFUSE_DEBUG environment variable
        debug_mode = os.getenv("LANGFUSE_DEBUG", "false").lower() == "true"
        
        # Set Langfuse logger level based on debug mode
        langfuse_logger = logging.getLogger("langfuse")
        if debug_mode:
            langfuse_logger.setLevel(logging.DEBUG)
        else:
            langfuse_logger.setLevel(logging.WARNING)  # Only show warnings and errors
        
        _langfuse_client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            base_url=os.getenv("LANGFUSE_BASE_URL"),
            httpx_client=httpx_client,
            debug=debug_mode,
        )
        
        # Log the actual base URL being used
        actual_base_url = os.getenv("LANGFUSE_BASE_URL") 
        logger.info(f"Langfuse client initialized: {actual_base_url} | Environment: {env_value}")
    
    return _langfuse_client


def configure(
    public_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    base_url: Optional[str] = None,
    verify_ssl: bool = False
):
    """
    Manually configure Langfuse client.
    
    Args:
        public_key: Langfuse public key
        secret_key: Langfuse secret key
        base_url: Langfuse base URL
        verify_ssl: Whether to verify SSL certificates
    """
    global _langfuse_client
    
    httpx_client = httpx.Client(verify=verify_ssl) if not verify_ssl else None
    
    _langfuse_client = Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        base_url=base_url,
        httpx_client=httpx_client,
    )
    
    print(f"[LLMOps-Observability] Langfuse client configured: {base_url}")


# ============================================================
# SQS Configuration
# ============================================================

def get_sqs_config() -> Dict[str, Any]:
    """
    Get SQS configuration from environment variables.
    
    Environment variables:
        - AWS_SQS_URL: SQS queue URL (required to enable SQS)
        - AWS_PROFILE: AWS profile name (default: "default")
        - AWS_REGION: AWS region (default: "us-east-1")
    
    Returns:
        Dict with SQS configuration
    """
    return {
        "aws_sqs_url": os.getenv("AWS_SQS_URL"),
        "aws_profile": os.getenv("AWS_PROFILE", "default"),
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
    }

