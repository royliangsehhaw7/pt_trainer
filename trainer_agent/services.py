from typing import Dict, Any
from .agents.workout import WorkoutArchitectAgent

class WorkoutGeneratorService:
    """
    Service Layer responsible for orchestrating the AI workout generation.
    Follows the Service Pattern to keep business logic out of Django Views.
    """
    
    def __init__(self):
        # We encapsulate the engine here. 
        # This makes it easy to swap WorkoutArchitectAgent for a PydanticAIAgent later.
        self.agent_engine = WorkoutArchitectAgent()

    def execute(self, trainer_id: int, client_id: int, exercise_count: int) -> Dict[str, Any]:
        try:
            # 1. Trigger the ReAct Loop
            result = self.agent_engine.run(
                client_id=client_id, 
                trainer_id=trainer_id, 
                exercise_count=exercise_count
            )
            
            # 2. Extract Reasoning Trace (The 'Thinking' events)
            steps = result.get("intermediate_steps", [])
            logic_events = [
                {
                    "step": i,
                    "thought": action.log.strip(),
                    "tool": action.tool,
                    "observation": observation 
                }
                for i, (action, observation) in enumerate(steps, 1)
            ]

            return {
                "status": "success",
                "workout_data": result.get("output"),
                "logic_events": logic_events
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "logic_events": []
            }