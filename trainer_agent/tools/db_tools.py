from langchain.tools import tool
from orm.models import Client, Exercise

@tool
def get_client_profile(client_id: int) -> str:
    """
    Fetches the physical profile and goals for a specific client.
    Matches the schema: goals, age, height, weight.
    """
    try:
        # Matching your .values() call columns
        client = Client.objects.filter(id=client_id).values(
            'goals', 'age', 'height', 'weight'
        ).first()

        if not client:
            return "Error: Client not found."

        return (
            f"Client Profile - Goals: {client['goals']}, Age: {client['age']}, "
            f"Height: {client['height']}cm, Weight: {client['weight']}kg"
        )
    except Exception as e:
        return f"Error accessing client data: {str(e)}"

@tool
def search_exercise_library(trainer_id: int) -> str:
    """
    Searched trainer exercises using specific tags. 
    Returns: id, name, instructions, sets, reps, weight, duration, and tags.
    """
    # Matching your prefetch_related and manual dictionary construction
    exercises = Exercise.objects.filter(trainer__id=trainer_id).prefetch_related("tags")

    ex_list = []        
    for ex in exercises:
        # Matching your exact column names from _get_data
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
        
        # Format as string for LLM readability
        ex_list.append(
            f"ID: {ex_dict['id']} | Name: {ex_dict['name']} | "
            f"Tags: {ex_dict['tags']} | Sets: {ex_dict['def_sets']} | "
            f"Reps: {ex_dict['def_reps']} | Weight: {ex_dict['def_weight']} | "
            f"Duration: {ex_dict['def_duration']} | Instructions: {ex_dict['instructions']}"
        )
    
    return "\n---\n".join(ex_list)