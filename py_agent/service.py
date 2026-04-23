from dependencies import AppDeps
from agents import workout_agent

class WorkoutService:
    async def create_workout(self, c_id: int, t_id: int):
        # Exactly like the 'Anne' example in the docs
        deps = AppDeps(client_id=c_id, trainer_id=t_id)
        
        # The agent chooses the tools based on the instructions
        return await workout_agent.run("Build a plan for my client", deps=deps)