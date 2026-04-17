"""
FILE: agents/tools/db_tools.py
ROLE: The "Hands" (Data Access Layer)
"""
from pydantic_ai import RunContext
from ..deps import AgentDeps  # Share the same Dependency type

from orm.models import Client, Exercise

async def get_client_profile(ctx: RunContext[AgentDeps]) -> dict:
    """
    Fetches client biometrics from the database. 
    The LLM uses this to understand the physical constraints of the user.
    """
    # 1. Logic: Standard Django Async ORM
    client = await Client.objects.aget(id=ctx.deps.client_id)
    
    # 2. Return: Clean, flat dictionary (JSON-friendly for the LLM)
    return {
        "age": client.age,
        "weight": client.weight,
        "goals": client.goals
    }

async def get_available_exercises(ctx: RunContext[AgentDeps]) -> list[dict]:
    """Fetches the full catalog of exercises for selection."""
    queryset = Exercise.objects.filter(trainer__id=ctx.deps.trainer_id).prefetch_related('tags')
    
    ex_list = []
    async for exercise in queryset:
        # Django requires async iteration for M2M tags
        tags = [t.name async for t in exercise.tags.all()]
        
        ex_list.append({
            'id': exercise.id,
            'name': exercise.name,
            'instructions': exercise.instructions,
            'def_sets': exercise.def_sets,
            'def_reps': exercise.def_reps,
            'tags': tags
        })
        
    return ex_list