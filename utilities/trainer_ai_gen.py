from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

from django.http import JsonResponse
from orm.models import Trainer, Tag, Exercise, Client

from .structured_model import WorkoutPlan


# """
# --- https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai
# --- https://medium.com/@pbaliyan1992/the-ultimate-guide-to-langchain-prompts-mastering-prompt-templates-messages-and-chat-history-926dcdac0e07
# --- https://latenode.com/blog/ai-frameworks-technical-infrastructure/langchain-setup-tools-agents-memory/langchain-prompt-templates-complete-guide-with-examples
# """

class TrainerGeminiAI:
    # initialize the gemini
    def __init__(self):

        # should be private to class

        # 1. gemini
        self._llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key="AIzaSyCzqEQzKJtvRqaUJ4AKdBE5rOeGAH6YCdE",
        )
        
        # # 2. openrouter
        # model="nvidia/nemotron-3-super-120b-a12b:free"
        # # model="google/gemma-4-31b-it:free"        
        # self._llm = ChatOpenAI(
        #     model=model,
        #     api_key="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",
        #     base_url="https://openrouter.ai/api/v1",
        # )


    # ============================ testing ===============================
    # simple - no templates
    def ask(self, prompt: str) -> JsonResponse:
        response = self._llm.invoke(prompt)

        # -- ================================ process results
        # additional metadata infiormation
        usage = response.usage_metadata
        return {
            "content": response.content,
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens")
        }
    
    # prompt template
    def ask_templated(self, prompt: str):
        prompt_template = PromptTemplate.from_template("""
            I need to understand about this science topic {topic} in simple bullet form.
            Just provide {bullet_count} answers.

        """)

        # option 1
        # formatted_string = prompt_template.format(
        #     topic = "DNA", bullet_count = 3
        # )
        # self._llm.invoke(formatted_string);

        # option 2
        chain = prompt_template | self._llm
        response = chain.invoke({'topic': 'DNA', 'bullet_count': '3'})


        # -- ================================ process results
        # additional metadata infiormation
        usage = response.usage_metadata
        return {
            "content": response.content,
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens")
        }

    # --- chat prompt template (unstructured)
    # --- dont think can use this, have to write a function to extract and format the output
    def ai_workout_unstructured(self, trainer_id: int, client_id: int):
        prompt = self._get_prompt_template()

        # get exercises with tags for the trainer
        data = self._get_data(trainer_id, client_id)

        # chain and execute
        chain = prompt | self._llm
        response = chain.invoke({
            'no_of_exercises': 4, 
            'exercise_list': data.get('exercise_list'),
            'client_info': data.get('client_info')
        })

        # --- process results # additional metadata infiormation
        usage = response.usage_metadata # just curious about this !!!
        return {
            "content": response.content,
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens")
        }
    
    
    
    # ===================== actual implementation ========================
    # --- execute promppt (structured output based pydantic model)
    def ai_workout_structured(self, trainer_id:int, client_id: int, exe_count: int):
        try:
            prompt = self._get_prompt_template()
            data = self._get_data(trainer_id, client_id)

            # --- https://medium.com/@gaurav_hoskote/getting-structured-output-from-llms-using-langchain-bedrock-614efe19a6aa
            # --- https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI/with_structured_outputs
            structured_llm = self._llm.with_structured_output(WorkoutPlan, include_raw = True)
            chain = prompt | structured_llm
            response = chain.invoke({
                'no_of_exercises': exe_count, 
                'exercise_list': data.get('exercise_list'),
                'client_info': data.get('client_info')
            })

            # --- process results # additional metadata infiormation
            workout_data = response.get('parsed')           # using with_structure_output only
            usage = response.get('raw').usage_metadata      # just curious about this !!!
        except Exception as e:
            raise Exception(f"AI Exception : {str(e)}") from e

        # --- for checking
        # return {
        #     "content": workout_data.model_dump(),
        #     "input_tokens": usage.get("input_tokens"),
        #     "output_tokens": usage.get("output_tokens")
        # }   
        
        # workout_data is actually a pydantic model, so have to convert to dict
        # python cannot convert custom classes to json
        return workout_data.model_dump()    


    # --- chatPromptTemplate content for generating exercises based on client info and exercises
    # - list of tuples
    def _get_prompt_template(self):
        chat_prompt = ChatPromptTemplate.from_messages([
            (
                "system", """
                You are a personal trainer.

                You will receive a client info
                - age, height, weight, goals

                You will receive a list of exercises. Each exercise includes:
                - name, instructions, default sets/reps/weight or duration
                - tags (representing muscle groups or workout goals, training styles but NOT equipment)
                - you may refer to the exercises tag for selection

                Task:
                - Select exactly {no_of_exercises} exercises based on the client goals, age, height, weight
                - ONLY use exercises from the list

                You may adjust sets, reps, weight, or duration

                Just return the selected exercises data. no other instructions or explanation required.

                Finally, a brief overall explanation on why the workout was recommended
                """
            ),
            (
                "human", """
                Client: {client_info}
                Exercises: {exercise_list}
                """
            ),
        ])

        return chat_prompt
    # --- get client info and exercises with tags
    def _get_data(self, trainer_id: int, client_id: int):
        # 
        # exercises = Exercise.objects.filter(trainer__id=trainer_id).values()
        # return exercises
    
        # --- get trainer exercisses / tags
        exercises = Exercise.objects.filter(trainer__id=trainer_id).prefetch_related("tags")
        # have to get seperately, annotate also wony help here
        ex_list = []        
        for ex in exercises:
            ex_dict = {
                "id": ex.id,
                "name": ex.name,
                "instructions": ex.instructions,
                "def_sets": ex.def_sets,
                "def_reps": ex.def_reps,
                "def_weight": ex.def_weight,
                "def_duration": ex.def_duration,
                "tags": [t.name for t in ex.tags.all()]
            }
            ex_list.append(ex_dict)       

        # --- get client info        
        client_info = Client.objects.filter(id=client_id).values('goals', 'age', 'height', 'weight')

        data = {
            'exercise_list': ex_list,
            'client_info': client_info
        }

        return data
