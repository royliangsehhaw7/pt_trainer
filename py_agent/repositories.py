# ============================================================
# repositories.py  —  Data access layer (pure ORM, no AI logic)
# Follows Repository Pattern — swap ORM for anything else here
# ============================================================
from orm.models import Exercise
from orm.models import Client, Exercise as ExerciseORM  # your Django models


class ClientRepository:
    """Thin wrapper over Django ORM. Keeps ORM coupling out of the agent."""

    def get_client_info(self, client_id: int) -> dict:
        """
        Returns a plain dict so the agent tool isn't coupled to Django model
        instances. LLMs work with serialisable data.
        """
        client = Client.objects.get(id=client_id)
        return {
            "age": client.age,
            "height_cm": client.height,
            "weight_kg": client.weight,
            "goals": client.goals
        }


class ExerciseRepository:
    """
    Fetches exercises scoped to the trainer.
    If you later add filtering (by tag, equipment), add methods here — 
    not in the agent tools.
    """

    def get_exercises_for_trainer(self, trainer_id: int) -> list[Exercise]:
        """Fetches the full catalog of exercises for selection."""
        queryset = Exercise.objects.filter(trainer__id= trainer_id).prefetch_related('tags')
            
        ex_list = []
        for exercise in queryset:
            # Django requires async iteration for M2M tags
            tags = [t.name for t in exercise.tags.all()]
            
            ex_list.append({
                'id': exercise.id,
                'name': exercise.name,
                'instructions': exercise.instructions,
                'def_sets': exercise.def_sets,
                'def_reps': exercise.def_reps,
                'tags': tags
            })
            
        return ex_list
