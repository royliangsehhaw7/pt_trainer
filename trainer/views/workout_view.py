# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from orm.models import Workout, Exercise, Tag, Trainer, Client, WorkoutExercise
from ..forms import WorkoutForm, ExerciseFormSet


# list view with search and pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def workout_list(request):
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    # workouts = Workout.objects.all().select_related('client', 'trainer')
    search = request.GET.get('search', '')
    if search:
        # Use icontains for a better user search experience
        workouts = Workout.objects.filter(trainer=trainer, client__name__icontains=search).order_by('client__name')
    else:     
        workouts = Workout.objects.filter(trainer=trainer).order_by('client__name')

    # pagination controls
    paginator = Paginator(workouts, 4)
    #
    page_number = request.GET.get('page')

    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/workouts/workout_list.html', {'workouts': pager, 'search': search, 'page_obj': pager})


    return render(request, 'trainer/workouts/workout_list.html', {'workouts': workouts})

def workout_add(request):

    if request.method == "POST":

        post_data = request.POST.copy()

        selected_tag_ids = post_data.getlist('tags_filter')

        form = WorkoutForm(post_data)
        formset = ExerciseFormSet(post_data, prefix='exercises')

        if form.is_valid() and formset.is_valid():
            workout = form.save(commit=False)
            workout.trainer = request.user
            workout.save()

            formset.instance = workout
            formset.save()

            return redirect('workout_list')

        return render(request, 'trainer/workouts/workout_add.html', {
            'form': form,
            'formset': formset,
            'selected_tag_ids': selected_tag_ids
        })

    form = WorkoutForm()
    formset = ExerciseFormSet(queryset=WorkoutExercise.objects.none(), prefix='exercises')

    return render(request, 'trainer/workouts/workout_add.html', {
        'form': form,
        'formset': formset,
        'selected_tag_ids': []
    })
# def workout_add(request):
#     selected_tag_ids = request.POST.getlist('tags_filter')
    
#     if request.method == "POST":
#         post_data = request.POST.copy()
#         total_key = 'exercises-TOTAL_FORMS'
        
#         # 1. DATA POPULATION LOOP
#         # This handles Sidebar clicks, Dropdown changes, and Add Row clicks.
#         # It just looks at what's in the post_data and fills blanks.
#         # try:
#         #     current_total = int(post_data.get(total_key, 0))
#         # except (ValueError, TypeError):
#         #     current_total = 0

#         # for i in range(current_total):
#         #     prefix = f'exercises-{i}'
#         #     ex_id = post_data.get(f'{prefix}-exercise')

#         #     if ex_id:
#         #         # If sets is empty or 0, we treat it as a "New Selection"
#         #         val_sets = post_data.get(f'{prefix}-pre_sets')
#         #         if not val_sets or val_sets in ['0', '']:
#         #             try:
#         #                 ex = Exercise.objects.get(id=ex_id)
#         #                 post_data[f'{prefix}-pre_sets'] = ex.def_sets
#         #                 post_data[f'{prefix}-pre_reps'] = ex.def_reps
#         #                 post_data[f'{prefix}-pre_weight'] = ex.def_weight
#         #                 post_data[f'{prefix}-pre_duration'] = ex.def_duration
#         #             except Exercise.DoesNotExist:
#         #                 pass

#         # 2. BIND THE FORMS
#         form = WorkoutForm(post_data)
#         formset = ExerciseFormSet(post_data, prefix='exercises')

#         # 3. THE SAVE GATE
#         # Only save if the user explicitly clicked the 'Save' button
#         if 'save_workout' in post_data:
#             if form.is_valid() and formset.is_valid():
#                 try:
#                     workout = form.save(commit=False)
#                     workout.trainer = request.user
#                     workout.save()
#                     formset.instance = workout
#                     formset.save()
#                     return redirect('workout_list')
#                 except ValidationError as e:
#                     form.errors.add(None, str(e))
#                 except Exception as e:
#                     messages.error(request, str(e))

#         # Otherwise, just re-render with the populated data
#         return render(request, 'trainer/workouts/workout_add.html', {
#             'form': form, 'formset': formset, 'selected_tag_ids': selected_tag_ids
#         })

#     # GET Request
#     form = WorkoutForm()
#     formset = ExerciseFormSet(queryset=WorkoutExercise.objects.none(), prefix='exercises')
#     return render(request, 'trainer/workouts/workout_add.html', {
#         'form': form, 'formset': formset, 'selected_tag_ids': selected_tag_ids
#     })



# def workout_add(request):
#     selected_tag_ids = request.POST.getlist('tags_filter')
    
#     if request.method == "POST":
#         post_data = request.POST.copy()
#         sidebar_id = post_data.get('sidebar_ex_id')
#         total_key = 'exercises-TOTAL_FORMS'
        
#         # 1. ADD ROW LOGIC
#         # Triggered by either the "Add Empty Row" button OR a Sidebar click
#         if 'add_row' in post_data or sidebar_id:
#             try:
#                 current_total = int(post_data.get(total_key, 0))
#             except (ValueError, TypeError):
#                 current_total = 0
            
#             # Increment the form count
#             post_data[total_key] = str(current_total + 1)
            
#             # If it's a sidebar click, set the ID and fetch the defaults immediately
#             if sidebar_id:
#                 new_idx = current_total
#                 post_data[f'exercises-{new_idx}-exercise'] = sidebar_id
                
#                 try:
#                     ex_obj = Exercise.objects.get(id=sidebar_id)
#                     # Use your exact DB column names: def_sets, def_reps, etc.
#                     post_data[f'exercises-{new_idx}-pre_sets'] = ex_obj.def_sets
#                     post_data[f'exercises-{new_idx}-pre_reps'] = ex_obj.def_reps
#                     post_data[f'exercises-{new_idx}-pre_weight'] = ex_obj.def_weight
#                     post_data[f'exercises-{new_idx}-pre_duration'] = ex_obj.def_duration
#                 except Exercise.DoesNotExist:
#                     pass

#         # 2. BIND FORMS
#         form = WorkoutForm(post_data)
#         formset = ExerciseFormSet(post_data, prefix='exercises')

#         # 3. SAVE LOGIC
#         if 'save_workout' in post_data:
#             if form.is_valid() and formset.is_valid():
#                 workout = form.save(commit=False)
#                 workout.trainer = request.user
#                 workout.save()
#                 formset.instance = workout
#                 formset.save()
#                 return redirect('workout_list')

#         return render(request, 'trainer/workouts/workout_add.html', {
#             'form': form, 'formset': formset, 'selected_tag_ids': selected_tag_ids
#         })

#     # GET Request
#     form = WorkoutForm()
#     formset = ExerciseFormSet(queryset=WorkoutExercise.objects.none(), prefix='exercises')
#     return render(request, 'trainer/workouts/workout_add.html', {
#         'form': form, 'formset': formset, 'selected_tag_ids': selected_tag_ids
#     })





# def workout_add(request):
    # selected_tag_ids = request.POST.getlist('tags_filter')
    
    # if request.method == "POST":
    #     post_data = request.POST.copy()
    #     form = WorkoutForm(post_data)
        
    #     total_key = 'exercises-TOTAL_FORMS'
    #     current_total = int(post_data.get(total_key, 0))

    #     # --- PRE-PROCESSING: Determine if we need to add a row ---
    #     sidebar_ex_id = post_data.get('sidebar_ex_id')
    #     if sidebar_ex_id:
    #         # Add a row for the sidebar selection
    #         prefix = f'exercises-{current_total}'
    #         post_data[total_key] = current_total + 1
    #         post_data[f'{prefix}-exercise'] = sidebar_ex_id
    #         current_total += 1 
    #     elif 'add_row' in post_data:
    #         # Add a truly empty row
    #         post_data[total_key] = current_total + 1
    #         current_total += 1

    #     # --- THE POPULATOR: Runs for EVERY row in EVERY branch ---
    #     # This ensures that whether from Sidebar, Add Row, or JS Change, 
    #     # if an exercise exists but fields are empty, we fill them.
    #     for i in range(current_total):
    #         prefix = f'exercises-{i}'
    #         ex_id = post_data.get(f'{prefix}-exercise')
            
    #         if ex_id:
    #             # Get current values from POST
    #             s = post_data.get(f'{prefix}-pre_sets')
    #             r = post_data.get(f'{prefix}-pre_reps')
    #             w = post_data.get(f'{prefix}-pre_weight')

    #             # Logic: If sets is empty/0/None, we assume it needs defaults
    #             if not s or s in ['0', '']:
    #                 try:
    #                     ex_obj = Exercise.objects.get(id=ex_id)
    #                     post_data[f'{prefix}-pre_sets'] = getattr(ex_obj, 'default_sets', 5)
    #                     post_data[f'{prefix}-pre_reps'] = getattr(ex_obj, 'default_reps', 10)
    #                     post_data[f'{prefix}-pre_weight'] = getattr(ex_obj, 'default_weight', 0)
    #                 except Exercise.DoesNotExist:
    #                     pass

    #     # Now that post_data is fully "fixed", initialize the formset ONCE
    #     formset = ExerciseFormSet(post_data, prefix='exercises')

    #     # --- BRANCHING: Decide what to return ---
    #     if 'save_workout' in post_data:
    #         if form.is_valid() and formset.is_valid():
    #             workout = form.save(commit=False)
    #             workout.trainer = request.user
    #             workout.save()
    #             formset.instance = workout
    #             formset.save()
    #             messages.success(request, "Workout saved successfully!")
    #             return redirect('workout_list')
        
    #     # For Sidebar, Add Row, or JS Change, or Failed Validation:
    #     return render(request, 'trainer/workouts/workout_add.html', {
    #         'form': form,
    #         'formset': formset,
    #         'selected_tag_ids': selected_tag_ids,
    #     })

    # else:
    #     # GET request
    #     form = WorkoutForm()
    #     formset = ExerciseFormSet(queryset=WorkoutExercise.objects.none(), prefix='exercises')

    # return render(request, 'trainer/workouts/workout_add.html', {
    #     'form': form, 'formset': formset, 'selected_tag_ids': selected_tag_ids,
    # })

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
            try:
                form.save()
                formset.save()
                messages.success(request, "Workout updated!")
                
                return redirect('workout_list')
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")            
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