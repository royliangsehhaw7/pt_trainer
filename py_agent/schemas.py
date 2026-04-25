# ============================================================
# models.py  —  Pure data contracts (no business logic here)
# Single Responsibility: only define shapes of data
# ============================================================
from pydantic import BaseModel, Field
from dataclasses import dataclass


class Exercise(BaseModel):
    """Maps 1:1 to your Exercise ORM model. Pydantic handles validation."""
    id: int
    name: str
    instructions: str
    default_sets: int | None
    default_reps: int | None
    default_weight: float | None
    duration_seconds: int | None
    tags: list[str]


class WorkoutExercise(BaseModel):
    """One exercise slot in the generated plan."""
    exercise_id: int
    name: str
    sets: int
    reps: int | None
    weight_kg: float | None
    duration_seconds: int | None


class WorkoutPlan(BaseModel):
    """
    The structured output the LLM must produce.
    Think of this as your DTO — the contract between LLM and your app.
    """
    exercises: list[WorkoutExercise]
    summary: str = Field(description="a brief explanation of the workout plan based on the selected exercises for the client")
