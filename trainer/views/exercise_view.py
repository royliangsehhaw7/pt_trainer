from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages

from orm.models import Exercise, Trainer, ExerciseTag
from ..forms.exercise_form import ExerciseForm

# default for testing. next time will get from session user
logged_in_trainer = 1

def list(request):
    # Only show exercises belonging to the logged-in user
    exercises = Exercise.objects.filter(trainer=logged_in_trainer)
    
    return render(request, 'trainer/exercise/exercise_list.html', {'exercises': exercises})

def add(request):
    # 1. Get the trainer instance (Must exist)
    trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, trainer=trainer_instance)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    exercise = form.save(commit=False)
                    exercise.trainer = trainer_instance
                    exercise.save()

                    # 5. Junction table manual bulk insert
                    selected_tags = form.cleaned_data.get('tags')
                    if selected_tags:
                        for tag in selected_tags:
                            exercise_tag = ExerciseTag(
                                trainer=trainer_instance, 
                                exercise=exercise, 
                                tag=tag
                            )
                            exercise_tag.save()

                messages.success(request, f"Exercise '{exercise.name}' added.")
                return redirect('exercise_list')

            except Exception as e:
                messages.error(request, f"Database Error: {e}")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field.title()}: {errors[0]}")
    else:
        form = ExerciseForm(trainer=trainer_instance)

    return render(request, 'trainer/exercise/exercise_add.html', {'form': form})

def add_using_M2M(request):
    # Fetch the actual User object to pass to the form
    trainer_user = get_object_or_404(Trainer, pk=logged_in_trainer)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, trainer=trainer_user)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.trainer = trainer_user # Assign the object
            exercise.save()
            form.save_m2m() # Critical for Tags!
            return redirect('exercise_list')
    else:
        form = ExerciseForm(trainer=trainer_user)

    return render(request, 'trainer/exercise/exercise_add.html', {'form': form })

def edit(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, trainer=logged_in_trainer)
    trainer_instance = exercise.trainer

    # 🔥 get existing tag IDs for initial display
    existing_tags = ExerciseTag.objects.filter(
        exercise=exercise,
        trainer=trainer_instance
    ).values_list('tag_id', flat=True)

    if request.method == 'POST':
        form = ExerciseForm(
            request.POST,
            instance=exercise,
            trainer=trainer_instance
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    # ✅ save exercise safely
                    exercise = form.save(commit=False)
                    exercise.trainer = trainer_instance
                    exercise.save()

                    # ✅ clear old tags
                    ExerciseTag.objects.filter(
                        exercise=exercise,
                        trainer=trainer_instance
                    ).delete()

                    # ✅ insert new tags
                    selected_tags = form.cleaned_data.get('tags')
                    if selected_tags:
                        for tag in selected_tags:
                            ExerciseTag.objects.create(
                                trainer=trainer_instance,
                                exercise=exercise,
                                tag=tag
                            )

                messages.success(request, f"Exercise '{exercise.name}' updated.")
                return redirect('exercise_list')

            except Exception as e:
                messages.error(request, f"Database Error: {e}")

        else:
            # ✅ same error handling style as your add()
            for field, errors in form.errors.items():
                messages.error(request, f"{field.title()}: {errors[0]}")

    else:
        form = ExerciseForm(
            instance=exercise,
            trainer=trainer_instance,
            initial={'tags': existing_tags}   # 🔥 preload checked tags
        )

    return render(request, 'trainer/exercise/exercise_edit.html', {
        'form': form,
        'title': 'Edit Exercise'
    })

def delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, trainer=logged_in_trainer)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')

    return render(request, 'trainer/exercise/exercise_delete.html', {'exercise': exercise})