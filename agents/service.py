from pydantic_ai import Agent
from .models import WorkoutStrategy, WorkoutPlan
from .tools import db_tools
from .deps import AgentDeps

class WorkoutOrchestrator:
    def __init__(self):
        # Specialist 1
        self.analyst = Agent(
            'google-gla:gemini-1.5-flash', 
            result_type=WorkoutStrategy,
            system_prompt="""
                You are a Senior Physiological Analyst. Analyze the client's biometrics (age, weight, goals) 
                and define a high-level workout strategy. Output the intensity level 
                and focus areas (tags) that should be used
            """
        )
        self.analyst.tool(db_tools.get_client_profile)

        # Specialist 2
        self.selector = Agent(
            'google-gla:gemini-1.5-flash', 
            result_type=WorkoutPlan,
            system_prompt="""
                You are a Personal Trainer. You will be given a workout strategy and a list of available exercises. 
                Select exactly {no_of_exercises} exercises that match the strategy. 
                You may adjust sets, reps, and weight to fit the strategy.
            """
        )
        self.selector.tool(db_tools.get_available_exercises)

    async def generate_workout(self, trainer_id: int, client_id: int):
        deps = AgentDeps(trainer_id=trainer_id, client_id=client_id)

        # TURN 1: The Analyst
        # We don't need to pass {client_info} because the agent calls get_client_profile(deps)
        analysis = await self.analyst.run("Please analyze the current client.", deps=deps)
        strategy = analysis.data

        # TURN 2: The Selector
        # We pass the strategy and the count into the 'Human' prompt (the .run call)
        selection = await self.selector.run(
            f"Select exactly 4 exercises based on this strategy: "
            f"{strategy.model_dump_json()}",
            deps=deps
        )

        return selection.data