import os

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from utilities.trainer_ai_gen import TrainerGeminiAI

from orm.models import Trainer, Client

trainer_ai = TrainerGeminiAI()

# --- testing 
def generate(request, prompt):
    res = trainer_ai.ask(prompt)
    return JsonResponse(res, safe=False)

def generate_workout_unstructured(request):
    res = trainer_ai.ai_workout_unstructured(2,1)
    return JsonResponse(res, safe=False)



# --- actual
# -- pk here is the client id
def generate_workout_structured(request, client_id, exe_count):
    # -- make sure client belongs to current logged in trainer
    trainer = get_object_or_404(Trainer, pk = request.user.id)
    client = get_object_or_404(Client, trainer=trainer, id=client_id)

    # res is a dict
    res = trainer_ai.ai_workout_structured(trainer.id, client.id, exe_count)
    return JsonResponse(res, safe=False)

