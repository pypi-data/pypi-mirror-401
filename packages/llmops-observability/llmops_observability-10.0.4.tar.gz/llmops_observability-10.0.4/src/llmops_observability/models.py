"""
Data models for LLMOps Observability
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class TraceConfig:
    """
    Configuration for starting a trace.
    Handles trace naming, project identification, and environment tracking.
    """
    name: str  # Operation/trace name (e.g., "chat_message", "document_analysis")
    project_id: Optional[str] = None  # Project identifier, defaults to PROJECT_ID env var
    environment: Optional[str] = None  # Environment (e.g., "development", "production"), defaults to ENV env var
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        """Auto-populate from environment variables if not provided"""
        # Default project_id from environment
        if self.project_id is None:
            self.project_id = os.getenv("PROJECT_ID", "unknown_project")
        
        # Default environment from environment
        if self.environment is None:
            self.environment = os.getenv("ENV", "development")
        
        # Initialize metadata if None
        if self.metadata is None:
            self.metadata = {}
        
        # Add environment to metadata
        self.metadata["environment"] = self.environment
        self.metadata["project_id"] = self.project_id
        
        # Debug: Log loaded values (can be disabled in production)
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"TraceConfig initialized - PROJECT_ID: {self.project_id}, ENV: {self.environment}")
    
    @property
    def trace_name(self) -> str:
        """Generate the Langfuse trace name: project_id"""
        return self.project_id or "unknown_project"


@dataclass
class SpanContext:
    """
    Context holder for span execution.
    Provides all necessary data for span creation and finalization.
    """
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    start_time: float
    span_name: str
    span_type: str = "span"  # "span" or "generation"
    tags: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Captured inputs/outputs
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Optional[Any] = None
    error: Optional[Exception] = None
    
    @property
    def duration_ms(self) -> int:
        """Calculate duration in milliseconds"""
        return int((time.time() - self.start_time) * 1000)
