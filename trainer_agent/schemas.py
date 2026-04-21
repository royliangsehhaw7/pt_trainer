from pydantic import BaseModel, Field
from typing import List, Optional

class ClientSchema(BaseModel):
    """Reflects the data retrieved from the database for the client."""
    goals: str
    age: int
    height: int
    weight: int
    limitations: Optional[str] = Field("None", description="Any injuries or health restrictions.")

class WorkoutExerciseSchema(BaseModel):
    exercise_id: int = Field(description="The exact database ID of the exercise.")
    name: str = Field(description="The display name of the exercise.")
    sets: int = Field(description="Recommended number of sets.")
    reps: Optional[int] = Field(None, description="Recommended repetitions per set.")
    weight: float = Field(0.0, description="Suggested weight in kg.")
    duration_minutes: int = Field(0, description="Duration if it is a cardio exercise.")
    trainer_notes: str = Field(description="Specific coaching cues for this client.")

class WorkoutPlanSchema(BaseModel):
    client_summary: ClientSchema = Field(description="Snapshot of the client profile used for this plan.")
    exercises: List[WorkoutExerciseSchema] = Field(description="List of selected exercises.")
    ai_explanation: str = Field(description="A brief explanation of why this plan fits the client's goals.")