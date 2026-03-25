# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from orm.models import Workout, Exercise, Tag, Trainer, Client, WorkoutExercise
from ..forms import WorkoutForm, ExerciseFormSet



def workout_list(request):
    workouts = Workout.objects.all().select_related('client', 'trainer')
    return render(request, 'trainer/workouts/workout_list.html', {'workouts': workouts})

def workout_add(request):
    selected_tag_ids = request.POST.getlist('tags_filter')

    if request.method == "POST":
        form = WorkoutForm(request.POST)
        formset = ExerciseFormSet(request.POST, prefix='exercises')
        
        # We need to modify POST data to add a row, so we copy it
        post_data = request.POST.copy()
        sidebar_ex_id = request.POST.get('sidebar_ex_id')
        
        if sidebar_ex_id or 'add_row' in request.POST:
            total_key = 'exercises-TOTAL_FORMS'
            current_total = int(post_data.get(total_key, 0))

            # -- check for empty rows AI::
            if 'add_row' in request.POST and current_total > 0:
                last_val = post_data.get(f'exercises-{current_total-1}-exercise')
                if not last_val or last_val == "":
                    # Just re-render the existing formset without adding +1
                    formset = ExerciseFormSet(post_data, prefix='exercises')
                    return render(request, 'trainer/workouts/workout_add.html', {
                        'form': form, 'formset': formset, 'selected_tag_ids': selected_tag_ids, 
                    })
            # --- END GUARD ---            
            
            # Manually increment the total forms
            post_data[total_key] = current_total + 1
            
            # If it's from the sidebar, inject the exercise ID into the new row
            if sidebar_ex_id:
                post_data[f'exercises-{current_total}-exercise'] = sidebar_ex_id
            
            # Re-bind with the updated post_data
            formset = ExerciseFormSet(post_data, prefix='exercises')
            
            return render(request, 'trainer/workouts/workout_add.html', {
                'form': form,
                'formset': formset,
                'selected_tag_ids': selected_tag_ids, 
            })


        # Regular save logic
        if form.is_valid() and formset.is_valid():
            try:
                workout = form.save(commit=False)
                workout.trainer = request.user
                workout.full_clean()
                workout.save()

                formset.instance = workout
                formset.full_clean()
                formset.save()

                messages.success(request, "Workout added successfully!")
                
                return redirect('workout_list')
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")            

    else:
        # 1. Create a blank, unsaved instance of the parent model
        empty_workout = Workout()
        
        # 2. Start the form
        form = WorkoutForm(instance=empty_workout)
        
        # 3. Force the formset to bind to that empty instance 
        # AND tell it the queryset is empty.
        formset = ExerciseFormSet(
            instance=empty_workout, 
            queryset=WorkoutExercise.objects.none(),
            prefix='exercises'
        )
        
        selected_tag_ids = []

    return render(request, 'trainer/workouts/workout_add.html', {
        'form': form,
        'formset': formset,
        'selected_tag_ids': selected_tag_ids,
    })
# def workout_add(request):
#     trainer = get_object_or_404(Trainer, pk=request.user.id)
    
#     # We check if we are already in the middle of adding rows
#     # by looking at the Management Form's TOTAL_FORMS
#     current_extra = int(request.POST.get('exercises-TOTAL_FORMS', 1))

#     if request.method == "POST":
#         form = WorkoutForm(request.POST)
#         formset = ExerciseFormSet(request.POST)

#         # SCENARIO A: User clicked the Sidebar or the "Add Exercise" button
#         if 'add_row' in request.POST:
#             # We don't validate yet. We just want to re-render with an extra row.
#             # If a specific exercise_id was passed from the sidebar:
#             new_exercise_id = request.POST.get('sidebar_exercise_id')
            
#             # We create a NEW formset with the existing data + 1 more empty slot
#             # Note: We don't save to the DB here.
#             return render(request, 'trainer/workouts/workout_add.html', {
#                 'form': form, 
#                 'formset': formset, 
#                 'new_exercise_id': new_exercise_id # Pass this to the template
#             })

#         # SCENARIO B: User clicked the final "Assign Workout" button
#         elif form.is_valid() and formset.is_valid():
#             try:
#                 with transaction.atomic():
#                     workout = form.save(commit=False)
#                     workout.trainer = trainer
#                     workout.save()
#                     formset.instance = workout
#                     formset.save()
#                 messages.success(request, "Workout created!")
#                 return redirect('workout_list')
#             except Exception as e:
#                 messages.error(request, f"Database Error: {e}")
#     else:
#         form = WorkoutForm()
#         formset = ExerciseFormSet()

#     return render(request, 'trainer/workouts/workout_add.html', {
#         'form': form, 
#         'formset': formset, 
#         'tags': Tag.objects.all()
#     })

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