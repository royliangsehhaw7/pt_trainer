from pydantic import BaseModel, Field
from typing import List, Optional


# Have to ensure result return from llm matches to workoutexercise model
# in order for easy insertion into inline formset rows

class WorkoutExercise(BaseModel):
    id: int = Field(description="the id of the exercise from the provided data")
    name: str = Field(descipriont="the name of the exercise")
    pre_sets: int = Field(description="no of sets to perfrom")
    pre_reps: Optional[int] = Field(None, description="reptitions per set")
    pre_weight: float = Field(0.0, description="suggested weight in kg")
    pre_duration: int = Field(0, description="duration in minutes for cardio")

class WorkoutPlan(BaseModel):
    exercises: List[WorkoutExercise]
    ai_explanation: str = Field(description="""
                                a brief overall explanation of why the workout was recommended
                                """)
