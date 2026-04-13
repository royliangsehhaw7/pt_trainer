from google import genai
from google.genai import types

from orm.models import Trainer, Tag, Exercise, Client


"""
https://ai.google.dev/gemini-api/docs/text-generation
https://ai.google.dev/api/generate-content#v1beta.GenerationConfig
"""


def generate(prompt) -> str:
    client = genai.Client(api_key="AIzaSyDmuTRd1MLRENHIiEdDsuyhPKy7cdQ71so")

    response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1
        )
    )

    return response.text.strip()


def prepare_input(trainer_id, client_id):
    trainer = Trainer.objects.get(id=trainer_id)
    client = Client.objects.get(id=client_id)
    
    tags = Tag.objects.filter(trainer=trainer)
    exercises = Exercise.objects.filter(trainer=trainer)

    data = {}
    data
