from pydantic_ai import Agent, RunContext
from .dependencies import AppDeps
# Import your repository logic directly
from .repositories import ClientRepo, ExerciseRepo 

workout_agent = Agent(
    'google-gla:gemini-3-flash-preview',
    deps_type=AppDeps,
    instructions="Plan a workout. Check the profile first, then get exercises."
)

@workout_agent.tool
async def get_profile(ctx: RunContext[AppDeps]) -> str:
    """Use this to see the client's injuries and goals."""
    # Just instantiate and use. Simple.
    return ClientRepo().get_by_id(ctx.deps.client_id)

@workout_agent.tool
async def get_exercises(ctx: RunContext[AppDeps], focus: str) -> str:
    """Use this to find specific exercises in the library."""
    return ExerciseRepo().search(ctx.deps.trainer_id, focus)