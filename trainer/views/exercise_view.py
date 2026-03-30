from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError


from orm.models import Exercise, ExerciseTag
from orm.models import UserTrainer as Trainer
from ..forms.exercise_form import ExerciseForm


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def exercise_list(request):
    # 1. Get the trainer instance (Must exist)
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    search = request.GET.get('search', '')
    if search:
        exercises = Exercise.objects.filter(trainer=trainer, name__icontains=search).orderBy('name')
    else:
        exercises = Exercise.objects.filter(trainer=trainer).order_by('name')
    
    # pagination controls
    paginator = Paginator(exercises, 3)
    #
    page_number = request.GET.get('page')

    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/exercise/exercise_list.html', {'exercises': pager, 'search': search, 'page_obj': pager})

def exercise_add(request):
    trainer_instance = get_object_or_404(Trainer, pk=request.user.id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, trainer=trainer_instance)
        if form.is_valid():
            try:
                # to maintain data integrity, using transaction
                with transaction.atomic():
                    exercise = form.save(commit=False)
                    exercise.trainer = trainer_instance
                    exercise.save()

                    selected_tags = form.cleaned_data.get('tags')
                    # using manual loop thru tags coz we use a manual junction table
                    if selected_tags:
                        for tag in selected_tags:
                            exercise_tag = ExerciseTag(
                                trainer=trainer_instance, 
                                exercise=exercise, 
                                tag=tag
                            )
                            exercise_tag.save()

                messages.success(request, f"Exercise added.")
                return redirect('exercise_list')        # 'exercise_list' is the name of the path in urls.py
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = ExerciseForm(trainer=trainer_instance)

    return render(request, 'trainer/exercise/exercise_add.html', {'form': form})

def exercise_edit(request, pk):
    # Ensure SaaS security: exercise must belong to the trainer
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    exercise = get_object_or_404(Exercise, pk=pk, trainer=trainer)



    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise, trainer=trainer)

        if form.is_valid():
            try:
                with transaction.atomic():
                    exercise = form.save(commit=False)
                    exercise.trainer = trainer
                    exercise.save()

                    # simpler logic, remove all previous tags for this edited exercise
                    # before inserting new ones
                    ExerciseTag.objects.filter(
                        exercise=exercise,
                        trainer=trainer
                    ).delete()

                    # insert new tags
                    selected_tags = form.cleaned_data.get('tags')
                    if selected_tags:
                        for tag in selected_tags:
                            ExerciseTag.objects.create(
                                trainer=trainer,
                                exercise=exercise,
                                tag=tag
                            )

                messages.success(request, f"Exercise '{exercise.name}' updated.")
                return redirect('exercise_list')
            except ValidationError as e:
                form.add_error(None, str(e))                    
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        # IMPORTANT: we have to get the previously update tags and pass into the form to be marked since we are using a manual junction table
        # get existing tag IDs for initial display
        # selected_tags = ExerciseTag.objects.filter( exercise=exercise, trainer=trainer_instance).values_list('tag_id', flat=True)
        selected_tags = exercise.exercise_tags.values_list("tag_id", flat=True)
        form = ExerciseForm(
            instance=exercise, 
            trainer=trainer,
            initial = {'tags': selected_tags})

    return render(request, 'trainer/exercise/exercise_edit.html', {'form': form})


def exercise_delete(request, pk):
    # Ensure SaaS security: the exercise must belong to the logged-in trainer
    exercise = get_object_or_404(Exercise, pk=pk, trainer_id=request.user.id)

    if request.method == 'POST':
        try:
            exercise_name = exercise.name
            exercise.delete()       # junction table related record
            messages.success(request, f"Exercise '{exercise_name}' has been deleted.")

            return redirect('exercise_list')
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")

    return render(request, 'trainer/exercise/exercise_delete.html', {'exercise': exercise})


def get_exercises_params(request):
    trainer = get_object_or_404(Trainer, pk=request.user.id)
    print(trainer.username)
    tag_ids = request.GET.getlist('tag_id')

    # exercises = ExerciseTag.objects.filter(tag_id__in=tag_ids)
    #                 .values('exercise__id', 'exercise__name').distinct()
    # distinct as some tags have the same exercises - we only display the exercise once for selection
    exercises = Exercise.objects.filter(exercise_tags__tag_id__in=tag_ids).distinct()

    # return JsonResponse(list(exercises.values('id', 'name')), safe=False)
    return JsonResponse(list(exercises.values(
    'id',
    'name',
    'def_sets',
    'def_reps',
    'def_weight',
    'def_duration'
)), safe=False)




# ======================================================= #

# def exercise_list(request):
#     # 1. Get the trainer instance (Must exist)
#     trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

#     # Only show exercises belonging to the logged-in user
#     exercises = Exercise.objects.filter(trainer=trainer_instance)  # THIS WORKS - by object
#     # exercises = Exercise.objects.filter(trainer_id=logged_in_trainer)   # THIS WORKS - by int
    
#     return render(request, 'trainer/exercise/exercise_list.html', {'exercises': exercises})

# def exercise_add(request):
#     # 1. Get the trainer instance (Must exist)
#     trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

#     if request.method == 'POST':
#         # passing data from the form and the current logged in trainer coz in the form, there is a list tags
#         # we will use it to select tgas to select only tags belonging to the trainer (Saas)
#         form = ExerciseForm(request.POST, trainer=trainer_instance)
        
#         if form.is_valid():
#             try:
#                 # to maintain data integrity, using transaction
#                 with transaction.atomic():
#                     exercise = form.save(commit=False)
#                     exercise.trainer = trainer_instance
#                     exercise.save()

#                     selected_tags = form.cleaned_data.get('tags')
#                     # using manual loop thru tags coz we use a manual junction table
#                     if selected_tags:
#                         for tag in selected_tags:
#                             exercise_tag = ExerciseTag(
#                                 trainer=trainer_instance, 
#                                 exercise=exercise, 
#                                 tag=tag
#                             )
#                             exercise_tag.save()

#                 messages.success(request, f"Exercise '{exercise.name}' added.")
#                 return redirect('exercise_list')        # 'exercise_list' is the name of the path in urls.py

#             except Exception as e:
#                 messages.error(request, f"Database Error: {e}")
#         else:
#             for field, errors in form.errors.items():
#                 messages.error(request, f"{field.title()}: {errors[0]}")
#     else:
#         form = ExerciseForm(trainer=trainer_instance)       # presenting empty form when get
#                                                             # passing in trainer to populate the tags in the form

#     return render(request, 'trainer/exercise/exercise_add.html', {'form': form})

# def add_using_M2M(request):
#     # Fetch the actual User object to pass to the form
#     trainer_user = get_object_or_404(Trainer, pk=logged_in_trainer)

#     if request.method == 'POST':
#         form = ExerciseForm(request.POST, trainer=trainer_user)
#         if form.is_valid():
#             exercise = form.save(commit=False)
#             exercise.trainer = trainer_user # Assign the object
#             exercise.save()
#             form.save_m2m() # Critical for Tags!
#             return redirect('exercise_list')
#     else:
#         form = ExerciseForm(trainer=trainer_user)

#     return render(request, 'trainer/exercise/exercise_add.html', {'form': form })

# def exercise_edit(request, pk):
#     # exercise = get_object_or_404(Exercise, pk=pk)
#     # trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)
    
#     # for Saas, selecting by key is not enough. have to select with the logged in trainer 
#     # to ensure exercise belongs to him
#     exercise = get_object_or_404(Exercise, pk=pk, trainer_id=logged_in_trainer)
#     trainer_instance = exercise.trainer

#     # IMPORTANT: we have to get the previously update tags and pass into the form to be marked
#     # 🔥 get existing tag IDs for initial display
#     # selected_tags = ExerciseTag.objects.filter( exercise=exercise, trainer=trainer_instance).values_list('tag_id', flat=True)
#     selected_tags = exercise.tagged_items.values_list("tag_id", flat=True)

#     if request.method == 'POST':
#         form = ExerciseForm(
#             request.POST,
#             instance=exercise,
#             trainer=trainer_instance
#         )

#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     exercise = form.save(commit=False)
#                     exercise.trainer = trainer_instance
#                     exercise.save()

#                     # simpler logic, remove all previous tags for this edited exercise
#                     # before inserting new ones
#                     ExerciseTag.objects.filter(
#                         exercise=exercise,
#                         trainer=trainer_instance
#                     ).delete()

#                     # insert new tags
#                     selected_tags = form.cleaned_data.get('tags')
#                     if selected_tags:
#                         for tag in selected_tags:
#                             ExerciseTag.objects.create(
#                                 trainer=trainer_instance,
#                                 exercise=exercise,
#                                 tag=tag
#                             )

#                 messages.success(request, f"Exercise '{exercise.name}' updated.")
#                 return redirect('exercise_list')

#             except Exception as e:
#                 messages.error(request, f"Database Error: {e}")

#         else:
#             # ✅ same error handling style as your add()
#             for field, errors in form.errors.items():
#                 messages.error(request, f"{field.title()}: {errors[0]}")
#     else:
#         form = ExerciseForm(
#             instance=exercise,
#             trainer=trainer_instance,
#             initial={'tags': selected_tags}   # 🔥 preload checked tags
#         )

#     return render(request, 'trainer/exercise/exercise_edit.html', {
#         'form': form,
#         'title': 'Edit Exercise'
#     })

# def exercise_delete(request, pk):
#     exercise = get_object_or_404(Exercise, pk=pk, trainer=logged_in_trainer)
#     if request.method == 'POST':
#         exercise.delete()
#         return redirect('exercise_list')

#     return render(request, 'trainer/exercise/exercise_delete.html', {'exercise': exercise})


# import json
# def get_exercises_params(request):
#     trainer = get_object_or_404(Trainer, pk=logged_in_trainer)

#     # ASP.NET equivalent of: public JsonResult GetExercises(List<int> tag_id)
#     # .getlist() captures ALL ?tag_id=3&tag_id=4 into a Python list
#     tag_ids = request.GET.getlist('tag_id')

#     # If the list is empty, Django won't crash, it just returns nothing.
#     # If it has ['3', '4'], Django's ORM handles the conversion to INT.
#     exercises = Exercise.objects.filter(
#         trainer=trainer, 
#         tagged_items__tag_id__in=tag_ids
#     ).distinct()

#     # Just ensure you didn't name your view function 'list' or it shadows the constructor!
#     return JsonResponse(list(exercises.values('id', 'name')), safe=False)
