# ============================================================
# agent.py  —  AI layer. No ORM imports, no Django, no views.
# Factory Pattern: build_workout_agent() is your agent factory.
# ============================================================
from pydantic_ai import Agent, RunContext

from .schemas import WorkoutPlan
from .dependencies import WorkoutDeps
from .repositories import ClientRepository, ExerciseRepository

from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# provider = GoogleProvider(api_key='AIzaSyBXR1Bv3XXEsoh9LGpx7brI_iVLjnsL1oI')
# model = GoogleModel('gemini-2.5-flash-lite', provider=provider)
provider = OpenAIProvider(
    base_url='https://openrouter.ai/api/v1', # Your custom URL
    api_key='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'
)
model = OpenAIModel(
    "nvidia/nemotron-3-super-120b-a12b:free",  provider=provider
    )

def build_workout_agent(client_repo: ClientRepository | None = None, exercise_repo: ExerciseRepository | None = None) -> Agent:
    """
    Factory function — returns a fully wired Agent.

    Why a factory and not a module-level singleton?
    - Testability: inject mock repos in tests (Open/Closed principle)
    - Flexibility: swap model or repos without touching agent logic
    - Explicitness: dependencies are declared, not hidden

    In C# terms: this is your IServiceCollection.AddScoped<IWorkoutAgent>()
    """
    _client_repo = client_repo or ClientRepository()
    _exercise_repo = exercise_repo or ExerciseRepository()

    # The agent is stateless — safe to reuse across requests (like a singleton service)
    agent = Agent(
        # model="google-gla:gemini-2.5-flash-lite",  # provider:model-name format
        model = model,
        output_type=WorkoutPlan,
        deps_type=WorkoutDeps,
        system_prompt="""
            You are an expert personal trainer building customised workout plans.
            Retrieve the client profile and available exercises, then select 
            exactly the number of exercises requested.
            ONLY select from the provided exercise list. Never invent exercises.
            Match exercises to the client's goals, fitness level, age, and weight.
            For each exercise, specify sets/reps/weight appropriate for the client.
        """,
    )

    # ----------------------------------------------------------------
    # Tools — these are the agent's only bridge to your data layer.
    # Each tool has a single responsibility and is independently testable.
    # The docstring IS the tool description the LLM reads — write it well.
    # ----------------------------------------------------------------

    @agent.tool
    def get_client_info(ctx: RunContext[WorkoutDeps]) -> dict:
        """
        Retrieve the client's profile: age, height, weight, goals, fitness level.
        Always call this first before selecting exercises.
        """
        # ctx.deps is your injected WorkoutDeps — analogous to this._service in C#
        return _client_repo.get_client_info(ctx.deps.client_id)

    @agent.tool
    def get_exercise_list(ctx: RunContext[WorkoutDeps]) -> list[dict]:
        """
        Retrieve all exercises available for this trainer.
        Each exercise includes name, instructions, default sets/reps/weight,
        duration, and tags (muscle groups, goals, training styles).
        Select from this list only.
        """
        exercises = _exercise_repo.get_exercises_for_trainer(ctx.deps.trainer_id)
        # Serialise to dicts — the LLM receives plain JSON, not Pydantic instances
        # return [e.model_dump() for e in exercises]
        return exercises

    return agent


# Module-level singleton — created once at import time (like a scoped service)
# If you need per-request agents (e.g. different models per trainer), call the
# factory in the service layer instead.
_workout_agent = build_workout_agent()