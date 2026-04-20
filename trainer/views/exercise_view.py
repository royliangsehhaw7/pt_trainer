from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from django.core.exceptions import ValidationError


from orm.models import Exercise
from orm.models import UserTrainer as Trainer
from ..forms.exercise_form import ExerciseForm

# - simulate logged in trainer
# logged_in_trainer = 1


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def exercise_list(request):
    # stepper highlight
    request.session['module'] = "exercise"

    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    search = request.GET.get('search', '')
    if search:
        exercises = Exercise.objects.filter(trainer=trainer, name__icontains=search).order_by('name')
    else:
        exercises = Exercise.objects.filter(trainer=trainer).order_by('name')
    
    exercises = exercises.annotate(tags_count=Count('tags'))

    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(exercises, 6)
    page_number = request.GET.get('page')

    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/exercise/exercise_list.html', {'exercises': pager, 'search': search, 'page_obj': pager})


def exercise_add(request):
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, trainer=trainer)
        if form.is_valid():
            try:
                with transaction.atomic():                    # better have this
                    exercise = form.save(commit=False)      # dont save first
                    exercise.trainer = trainer

                    # exercise.full_clean()
                    exercise.save()
                    # this is a must for the manytomany junctioan table
                    form.save_m2m() # Django handles the hidden junction table automatically.

                messages.success(request, f"Exercise '{exercise.name}' added.")
                return redirect('exercise_list')
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = ExerciseForm(trainer=trainer)

    return render(request, 'trainer/exercise/exercise_add.html', {'form': form})


def exercise_edit(request, pk):
    # Ensure SaaS security: exercise must belong to the trainer
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    exercise = get_object_or_404(Exercise, pk=pk, trainer=trainer)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise, trainer=trainer)

        if form.is_valid():
            try:
                with transaction.atomic():        # better have this
                    exercise = form.save(commit=False)
                    exercise.save()

                    # save_m2m() identifies which tags were removed and which were added.
                    form.save_m2m()

                messages.success(request, f"Exercise '{exercise.name}' updated.")

                return redirect('exercise_list')
            except ValidationError as e:
                form.add_error(None, str(e))                    
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        # pre-selects the tags currently linked to this exercise.
        form = ExerciseForm(instance=exercise, trainer=trainer)

    return render(request, 'trainer/exercise/exercise_edit.html', {'form': form})


def exercise_delete(request, pk):
    # Ensure SaaS security: the exercise must belong to the logged-in trainer
    exercise = get_object_or_404(Exercise, pk=pk, trainer_id=request.user.id)

    if request.method == 'POST':
        try:
            exercise_name = exercise.name
            exercise.delete()               # junction table related record
            messages.success(request, f"Exercise '{exercise_name}' has been deleted.")

            return redirect('exercise_list')
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")

    return render(request, 'trainer/exercise/exercise_delete.html', {'exercise': exercise})


def get_exercises_by_tags(request):
    trainer = get_object_or_404(Trainer, id=request.user.id)

    selected_tags = request.GET.getlist('tags_filter')
    exercises = Exercise.objects.filter(trainer=trainer, tags__id__in = selected_tags)

    return render(request, 'trainer/partials/_exercises_partial.html', {'exercises': exercises})













# =================================== WHEN NOT USING HTMX, ONLY AJAX =================================== #
# def get_exercises_by_tags(request, tag_ids):
#     # Saas tenant - get logged in trainer for data filtering
#     trainer = get_object_or_404(Trainer, pk=request.user.id)
#     # 2. Split the path string "9,11" into ['9', '11']
#     # We use a list comprehension to strip whitespace and remove empty strings
#     tag_ids = [tid.strip() for tid in tag_ids.split(',') if tid.strip()]
#     # exercises = ExerciseTag.objects.filter(tag_id__in=tag_ids)
#     #                 .values('exercise__id', 'exercise__name').distinct()
#     # distinct as some tags have the same exercises - we only display the exercise once for selection
#     exercises = Exercise.objects.filter(tags__id__in=tag_ids, trainer=trainer).distinct()

#     # return JsonResponse(list(exercises.values('id', 'name')), safe=False)
#     return JsonResponse(list(exercises.values(
#         'id',
#         'name',
#         'def_sets',
#         'def_reps',
#         'def_weight',
#         'def_duration'
#     )), safe=False)


# ================================= WHEN USING MANUAL JUNCTION TABLE ==================================== #
# def exercise_add(request):
#     trainer = get_object_or_404(Trainer, pk=request.user.id)
#     if request.method == 'POST':
#         form = ExerciseForm(request.POST, trainer=trainer)
#         if form.is_valid():
#             try:
#                 # to maintain data integrity, using transaction
#                 with transaction.atomic():
#                     exercise = form.save(commit=False)
#                     exercise.trainer = trainer
#                     exercise.save()

#                     # junction table
#                     selected_tags = form.cleaned_data.get('tags')
#                     # using manual loop thru tags coz we use a manual junction table
#                     if selected_tags:
#                         for tag in selected_tags:
#                             exercise_tag = ExerciseTag(
#                                 trainer=trainer, 
#                                 exercise=exercise, 
#                                 tag=tag
#                             )
#                             exercise_tag.save()

#                 messages.success(request, f"Exercise added.")
#                 return redirect('exercise_list')        # 'exercise_list' is the name of the path in urls.py
#             except ValidationError as e:
#                 form.add_error(None, str(e))
#             except Exception as e:
#                 messages.error(request, f"Exceptions: {str(e)}")
#     else:
#         trainer_tags = Tag.objects.filter(trainer = trainer)
#         form = ExerciseForm(trainer_tags=trainer_tags)

#     return render(request, 'trainer/exercise/exercise_add.html', {'form': form})

# def exercise_edit(request, pk):
#     # Saas tenant - get logged in trainer for data filtering    
#     trainer = get_object_or_404(Trainer, pk=request.user.id)

#     # get the exercise to be edited first
#     exercise = get_object_or_404(Exercise, pk=pk, trainer=trainer)

#     if request.method == 'POST':
#         # trainer is passed in so the tags are selected by trainer in the form
#         form = ExerciseForm(request.POST, instance=exercise, trainer=trainer)

#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     exercise = form.save(commit=False)
#                     exercise.trainer = trainer
#                     exercise.save()

#                     # simpler logic, remove all previous tags for this edited exercise
#                     # before inserting new ones
#                     ExerciseTag.objects.filter(
#                         exercise=exercise,
#                         trainer=trainer
#                     ).delete()

#                     # insert new tags
#                     selected_tags = form.cleaned_data.get('tags')
#                     if selected_tags:
#                         for tag in selected_tags:
#                             ExerciseTag.objects.create(
#                                 trainer=trainer,
#                                 exercise=exercise,
#                                 tag=tag
#                             )

#                 messages.success(request, f"Exercise '{exercise.name}' updated.")
#                 return redirect('exercise_list')
#             except ValidationError as e:
#                 form.add_error(None, str(e))                    
#             except Exception as e:
#                 messages.error(request, f"Exceptions: {str(e)}")
#     else:
#         # IMPORTANT: we have to get the previously update tags and pass into the form to be marked since we are using a manual junction table
#         # get existing tag IDs for initial display
#         # selected_tags = ExerciseTag.objects.filter( exercise=exercise, trainer=trainer_instance).values_list('tag_id', flat=True)
#         selected_tags = exercise.exercise_tags.values_list("tag_id", flat=True)
#         #
#         trainer_tags = Tag.objects.filter(trainer=trainer)
#         form = ExerciseForm(
#             instance=exercise, 
#             trainer_tags=trainer_tags,
#             initial = {'tags': selected_tags})  # pass in previously selected tags here as initial

#     return render(request, 'trainer/exercise/exercise_edit.html', {'form': form})
# ======================================================================================================================
