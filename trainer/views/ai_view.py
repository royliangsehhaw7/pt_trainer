import os

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from utilities.trainer_ai_gen import TrainerGeminiAI

from orm.models import Trainer

trainer_ai = TrainerGeminiAI(model_name="gemini-2.5-flash-lite", api_key=settings.G_API_KEY)

# --- testing 
def generate(request, prompt):
    res = trainer_ai.ask(prompt)
    return JsonResponse(res, safe=False)

def generate_workout_unstructured(request):
    res = trainer_ai.ai_workout_unstructured(2,1)
    return JsonResponse(res, safe=False)


# --- actual
# -- pk here is the client id
def generate_workout_structured(request, pk):
    # -- make sure client belongs to current logged in trainer
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    # res is a dict
    res = trainer_ai.ai_workout_structured(trainer.id, pk)
    return JsonResponse(res, safe=False)
