import os
from django.http import JsonResponse
from utilities.trainer_ai_gen import TrainerGeminiAI

trainer_ai = TrainerGeminiAI(model_name="gemini-2.5-flash", api_key=os.environ['GOOGLE_API_KEY'])

def generate(request, prompt):
    res = trainer_ai.ask(prompt)

    return JsonResponse(res, safe=False)

def generate_workout(request, prompt):
    pass