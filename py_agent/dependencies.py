from pydantic import BaseModel, Field
from dataclasses import dataclass

@dataclass
class WorkoutDeps:
    """
    Dependency injection container for the agent.
    Equivalent to injecting services via constructor in C#.
    The agent receives this at runtime via RunContext — it never
    instantiates its own dependencies.
    """
    trainer_id: int
    client_id: int
    exe_count: int