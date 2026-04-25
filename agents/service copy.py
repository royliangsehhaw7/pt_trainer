# """
# FILE: agents/service.py
# TERM: Tool Decorators
# ROLE: The Logic Layer
# DESCRIPTION: Using @self.analyst.tool to bind logic directly to the agent.
# """
# from pydantic_ai import Agent, RunContext
# from .models import WorkoutState, WorkoutStrategy, WorkflowStatus
# from .deps import AgentDeps
# from orm.models import Client, Exercise 


# # ================ SETTING UP MODELS ================= #
# from pydantic_ai.models.google import GoogleModel

# # 1. Create the model instance with the key
# custom_model = GoogleModel(
#     model_name='gemini-3-flash-preview',
#     api_key='your-actual-api-key-here'
# )
# from pydantic_ai.models.openai import OpenAIChatModel

# # Using DeepSeek via their OpenAI-compatible endpoint
# deepseek_model = OpenAIChatModel(
#     model_name='deepseek-chat',
#     base_url='https://api.deepseek.com/v1',
#     api_key='your-deepseek-key'
# )

# # =============== SYSTEM PROMPT FOR AGENT ============= #
# ANALYST_PROMPT = """
#     You are a Senior Physiological Analyst. 
#     Your goal is to interpret client data and provide a high-level strategy.
#     DO NOT pick exercises. Just define the 'flavor' of the workout.
#     Only use focus_areas that likely exist as tags in our system.
# """


# # ============= ORCHESTRATOR & AGENTS ================== #
# class WorkoutOrchestrator:
#     def __init__(self):
#         """
#         In the constructor, we define the agent. 
#         Then we use the .tool() decorator on our methods.
#         """
#         self.analyst = Agent(
#             'google-gla:gemini-1.5-flash',
#             deps_type=AgentDeps,
#             result_type=WorkoutStrategy, 
#             system_prompt=ANALYST_PROMPT
#         )

#         # To use decorators on instance methods, we wrap them like this:
        
#         @self.analyst.tool
#         async def get_client_profile(ctx: RunContext[AgentDeps]) -> dict:
#             """Fetches client biometrics and goals from the DB."""
#             client = await Client.objects.aget(id=ctx.deps.client_id)
#             return {
#                 "age": client.age,
#                 "height": client.height,
#                 "weight": client.weight,
#                 "goals": client.goals
#             }

#         @self.analyst.tool
#         async def get_available_exercises(ctx: RunContext[AgentDeps]) -> list[str]:
#             exercises = Exercise.objects.filter(trainer__id=ctx.deps.trainer_id).prefetch_related('tags')
#             ex_list = []
#             for exercise in exercises:
#                 ex_list.append({
#                     'id': exercise.id,
#                     'name': exercise.name,
#                     'instructions': exercise.instructions,
#                     'def_sets': exercise.def_sets,
#                     'def_reps': exercise.def_reps,
#                     'def_weight': exercise.def_weight,
#                     'def_duration': exercise.def_duration,
                    
#                     'tags': [{'name': t.name} for t in exercise.tags.all()]
#                 })

#             return ex_list

#         # Re-assigning to self so they can be accessed elsewhere if needed
#         self.get_client_profile = get_client_profile
#         self.get_available_tags = get_available_tags


#     async def generate_workout(self, trainer_id: int, client_id: int):
#         """Kicks off the first stage of the process."""
#         deps = AgentDeps(trainer_id=trainer_id, client_id=client_id)
#         state = WorkoutState()

#         # The Agent 'calls' the decorated tools automatically during this run.
#         result = await self.analyst.run(
#             "Please analyze the client and provide a strategy.", 
#             deps=deps
#         )

#         state.strategy = result.data
#         state.status = WorkflowStatus.SELECTING

#         return state