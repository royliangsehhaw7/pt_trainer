"""
FILE: agents/models.py
TERM: Result Type / Structured Output
ROLE: The Contract
DESCRIPTION: Defines the shape of the data the agents must produce.
"""


from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class WorkflowStatus(Enum):
    """
    TERM: State Machine
    Tracks the progress of the multi-agent orchestration.
    """
    ANALYZING = "analyzing"      
    SELECTING = "selecting"      
    REFINING = "refining"        
    COMPLETE = "complete"
    FAILED = "failed"

class WorkoutStrategy(BaseModel):
    """
    TERM: Result Model
    The specific 'Contract' for the Analyst Agent.
    """
    intensity_tier: str = Field(description="e.g., Low, Moderate, High")
    focus_areas: List[str] = Field(description="Muscle groups or styles, e.g., 'Posterior Chain'")
    reasoning: str = Field(description="Brief scientific justification for the trainer")

class WorkoutState(BaseModel):
    """
    TERM: Workflow State
    The internal 'Briefcase' used by the Orchestrator to manage handoffs.
    """
    status: WorkflowStatus = WorkflowStatus.ANALYZING
    strategy: Optional[WorkoutStrategy] = None
    selected_exercise_ids: List[int] = Field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3