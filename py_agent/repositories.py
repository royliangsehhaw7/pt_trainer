from typing import List, Dict, Any

class ClientRepository:
    def __init__(self, session: Any = None):
        self.session = session

    def get_by_id(self, client_id: int) -> str:
        """
        Fetches age, height, weight, and goals.
        Returns a string formatted for LLM consumption.
        """
        # In a real app: self.session.execute("SELECT ... WHERE id = :id", {"id": client_id})
        # For now, representing the explicit data structure you need:
        return (
            "Client Profile: Age 32, Height 180cm, Weight 85kg. "
            "Goals: Hypertrophy and improved core stability."
        )

class ExerciseRepository:
    def __init__(self, session: Any = None):
        self.session = session

    def get_by_tags(self, trainer_id: int, tags: str) -> List[Dict[str, Any]]:
        """
        Queries exercises associated with a trainer that match specific tags.
        Avoids 'magic'—uses explicit filtering.
        """
        # Logic: 
        # 1. Split tags string into a list.
        # 2. Query join table between Exercises and Tags.
        # 3. Ensure trainer_id isolation for multi-tenancy.
        
        return [
            {
                "name": "Barbell Squat",
                "instructions": "Place bar on traps, squat until thighs are parallel.",
                "default_sets": 3,
                "default_reps": "8-12",
                "tags": ["legs", "strength", "compound"]
            },
            {
                "name": "Plank",
                "instructions": "Hold a pushup position on your elbows.",
                "default_duration": "60s",
                "tags": ["core", "stability"]
            }
        ]