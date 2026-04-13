from django.http import JsonResponse
from utilities import ai_gen


def generate(request, prompt):
    res = ai_gen.generate(prompt)

    return JsonResponse(res, safe=False)