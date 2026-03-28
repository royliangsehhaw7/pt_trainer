from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise

# # Register your models here.
# admin.site.register(Workout)
# admin.site.register(WorkoutExercise)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    search_fields = ["name"]

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1
    autocomplete_fields = ["exercise"]


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    inlines = [WorkoutExerciseInline]