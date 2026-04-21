from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from ..schemas import WorkoutPlanSchema
from ..prompts.instructions import SYSTEM_PROMPT
from ..tools.db_tools import get_client_profile, search_exercise_library

from langchain_openai import ChatOpenAI


# agents/constants.py or directly in your agent.py

WORKOUT_ARCHITECT_SYSTEM_PROMPT = """
You are a professional strength and conditioning expert (TrainForge Workout Architect).

CORE PROTOCOLS:
1. Call 'get_client_profile' to understand the client's goals, age, height, and weight.
2. Call 'search_exercise_library' get a list of available exercises.
3. SELECT exactly the number of  exercises from the list provided by the tool based on the user prompt.
4. ONLY use exercises that exist in the database (returned by the tool).

PLANNING RULES:
- You may adjust sets, reps, weight, or duration from the defaults to better suit the client's profile.
- Reference the 'instructions' field to provide specific coaching cues in the 'trainer_notes'.

OUTPUT:
- Provide the selected exercises and a brief overall explanation for the recommendation.
- You must conform to the provided WorkoutPlanSchema.
"""

class WorkoutArchitectAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            api_key="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",
            base_url="https://openrouter.ai/api/v1",
            model_kwargs={"tool_choice": "auto"} 
        )

        self.tools = [get_client_profile, search_exercise_library]
        self.llm_with_tools = self.llm.bind_tools(self.tools, tool_choice="auto")
        
        # This is the 2026 'Stable' way to force the loop AND the schema
        # Inject the count into the instructions once

        self.app = create_agent(
            model=self.llm_with_tools,
            tools=self.tools,
            system_prompt=WORKOUT_ARCHITECT_SYSTEM_PROMPT, # In create_agent, 'prompt' takes your system string
            response_format=WorkoutPlanSchema
        )

    def run(self, client_id: int, trainer_id: int, exercise_count: int):
        query = (
            f"Build a workout for client_id {client_id} with "
            f"exactly {exercise_count} exercises. I am trainer_id {trainer_id}. "
            f"You MUST use 'get_client_profile' for client info to select the appropriate exercises"
        )
        
        # Invoke the graph
        result = self.app.invoke({"messages": [("user", query)]})
        
        # Result is a dict. The structured output lives here:
        structured_data = result.get("structured_response")
        
        if structured_data:
            return structured_data.model_dump()
        
        return {"error": "Agent failed to generate structured output"}