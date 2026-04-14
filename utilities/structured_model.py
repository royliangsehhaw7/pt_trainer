from pydantic import BaseModel, Field
from typing import List, Optional

# the output must match the workout_exercises model
class WorkoutExercise(BaseModel):
    exercise_id: int = Field(description="the id of the exercise from the provided data")
    pre_sets: int = Field(description="no of sets to be perfromed")
    pre_reps: Optional[int] = Field(None, description="reptitions per set")
    pre_weight: float = Field(0.0, description="suggested weight in kg")
    pre_duration: int = Field(0, description="duration in minutes for cardio")

class WorkoutPlan(BaseModel):
    exercises: List[WorkoutExercise]
    ai_explanation: str = Field(description="""
                                a brief explanation of why the workout was structured this way with the selection of exercises
                                """)

class ClientProfile(BaseModel):
    user_goals: str
    age: int
    weight: float
    height: float