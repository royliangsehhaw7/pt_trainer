
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from django.conf import settings
from django.http import JsonResponse
from orm.models import Trainer, Tag, Exercise, Client


# """
# --- https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai
# --- https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI/with_structured_output
# """

class TrainerGeminiAI:
    def __init__(self, model_name: str = "gemini-1.5-flash", api_key: str = None):
        # Prefix with _ to make it "protected/private"
        self._llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3
        )

    def ask(self, prompt: str) -> JsonResponse:
        response = self._llm.invoke(prompt)
        usage = response.usage_metadata

        return {
            "content": response.content,
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens")
        }
    
    # def ask_structured(self) -> JsonResponse:
    #     # Pass the list of tuples directly
    #     prompt_template = ChatPromptTemplate.from_messages(self.trainer_prompt)
        
    #     # Bind the structured output
    #     chain = prompt_template | self._llm.with_structured_output(WorkoutPlan)
        
    #     # Run the chain
    #     return chain.invoke({
    #         "user_goal": user_goal,
    #         "library_data": library_data
    #     })


    # --- https://www.geeksforgeeks.org/artificial-intelligence/chatprompttemplate-in-langchain/
    @property
    def trainer_prompt(self):
        return [
            (
                "system", 
                "You are an elite trainer. Use the provided library to build a workout plan "
                "that strictly follows the JSON schema. Focus on the client's biometrics."
            ),
            (
                "human", 
                "CLIENT PROFILE: {user_goal}\n\n"
                "EXERCISE LIBRARY: {library_data}\n\n"
                "Select the best exercises and provide your reasoning."
            )
        ]
    



# def generate(prompt) -> str:
#     client = genai.Client(api_key="AIzaSyDmuTRd1MLRENHIiEdDsuyhPKy7cdQ71so")

#     response = client.models.generate_content(
#         model = "gemini-2.5-flash-lite",
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             temperature=0.1
#         )
#     )

#     return response.text.strip()

# def prepare_input(trainer_id, client_id):
#     trainer = Trainer.objects.get(id=trainer_id)
#     client = Client.objects.get(id=client_id)    
#     tags = Tag.objects.filter(trainer=trainer)
#     exercises = Exercise.objects.filter(trainer=trainer)

