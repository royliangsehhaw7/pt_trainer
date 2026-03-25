# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from orm.models import Workout, Exercise, Tag, Trainer
from ..forms import WorkoutForm, ExerciseFormSet



def workout_list(request):
    workouts = Workout.objects.all().select_related('client', 'trainer')
    return render(request, 'trainer/workouts/workout_list.html', {'workouts': workouts})

def workout_add(request):
    # Saas tenant check
    trainer = get_object_or_404(Trainer, pk=request.user.id)    
    
    exercises = Exercise.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        form = WorkoutForm(request.POST)
        formset = ExerciseFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    workout = form.save(commit=False)
                    workout.trainer = trainer
                    workout.save()

                    formset.instance = workout
                    formset.save()

                messages.success(request, "Workout created!")
                return redirect('workout_list')
            except Exception as e:
                messages.error(request, f"Database Error: {e}")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"Workout {field}: {errors[0]}")
            for i, f_errors in enumerate(formset.errors):
                for field, errors in f_errors.items():
                    messages.error(request, f"Exercise {i+1} {field}: {errors[0]}")
    else:
        form = WorkoutForm()
        formset = ExerciseFormSet()

    return render(request, 'trainer/workouts/workout_add.html', {'form': form, 'formset': formset, 'exercises': exercises, 'tags': tags})

def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        formset = ExerciseFormSet(request.POST, instance=workout)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Workout updated!")
            return redirect('workout_list')
    else:
        form = WorkoutForm(instance=workout)
        formset = ExerciseFormSet(instance=workout)
    return render(request, 'trainer/workouts/workout_edit.html', {'form': form, 'formset': formset, 'workout': workout})

def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == "POST":
        workout.delete()
        return redirect('workout_list')
    return render(request, 'trainer/workouts/workout_delete.html', {'workout': workout})