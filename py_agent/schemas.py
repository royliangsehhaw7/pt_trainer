from pydantic import BaseModel, Field
from typing import List, Optional

# --- INPUT SCHEMAS (For Step A & B) ---

class ClientInfo(BaseModel):
    """The profile data we fetch from the DB to give context to the AI."""
    id: int
    name: str
    fitness_level: str
    goal: str
    limitations: Optional[str] = None

class ExerciseLibraryItem(BaseModel):
    """The available pool of exercises the AI can choose from."""
    id: int
    name: str
    category: str
    # We include these so the AI knows the 'baseline' it is adjusting from
    base_sets: int
    base_reps: Optional[int]
    base_weight: float

# --- OUTPUT SCHEMAS (The Contract / Step D) ---

class WorkoutExercise(BaseModel):
    # CRITICAL: We tell the AI to use the ID from our provided list
    id: int = Field(description="The exact database ID from the provided exercise library.")
    name: str = Field(description="The name of the exercise.")
    def_sets: int = Field(description="Number of sets to perform.")
    def_reps: Optional[int] = Field(None, description="Repetitions per set.")
    def_weight: float = Field(0.0, description="Suggested weight in kg.")
    def_duration: int = Field(0, description="Duration in minutes (used for cardio).")

class WorkoutPlan(BaseModel):
    exercises: List[WorkoutExercise]
    ai_explanation: str = Field(
        description="A brief overall explanation of why this workout was recommended for this specific client."
    )