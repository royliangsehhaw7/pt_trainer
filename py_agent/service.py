# ============================================================
# services.py  —  Business logic layer. Orchestrates, doesn't implement.
# This is the only layer your views/APIs should import.
# ============================================================
import asyncio
from .agents import _workout_agent
from .schemas import WorkoutPlan
from .dependencies import WorkoutDeps


class WorkoutService:
    """
    Thin orchestration layer between your web layer and the AI agent.

    Responsibilities (SRP):
    - Build the dependency container
    - Invoke the agent
    - Return the typed result

    NOT responsible for: ORM queries, prompt content, LLM config.
    """

    def generate_workout(
        self,
        trainer_id: int,
        client_id: int,
        exe_count: int,
    ) -> WorkoutPlan:
        """
        Synchronous entry point — wraps the async agent for Django views.
        Use generate_workout_async() if you're in an async context (ASGI/DRF async views).
        """
        deps = WorkoutDeps(
            trainer_id=trainer_id,
            client_id=client_id,
            exe_count=exe_count,
        )
        # run_sync is pydantic-ai's blocking wrapper — equivalent to asyncio.run()
        result = _workout_agent.run_sync(
            f"Build a workout plan with exactly {exe_count} exercises.",
            deps=deps,
        )
        usage = result.usage()
        
        # log token usage
        # logger.info(
        #     "Agent run complete | trainer=%s client=%s "
        #     "input_tokens=%s output_tokens=%s total_tokens=%s",
        #     trainer_id, client_id,
        #     usage.request_tokens,
        #     usage.response_tokens,
        #     usage.total_tokens,
        # )
        # # log all messages including CoT steps
        # for message in result.all_messages():
        #     logger.debug("Message | %s", message)

        return {
            "plan": result.output.model_dump(),
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "total_tokens": usage.total_tokens,
        }


    async def generate_workout_async(
        self,
        trainer_id: int,
        client_id: int,
        exe_count: int,
    ) -> WorkoutPlan:
        """Async version for ASGI Django or Celery async tasks."""
        deps = WorkoutDeps(
            trainer_id=trainer_id,
            client_id=client_id,
            exe_count=exe_count,
        )
        result = await _workout_agent.run(
            f"Build a workout plan with exactly {exe_count} exercises.",
            deps=deps,
        )
        return result.data