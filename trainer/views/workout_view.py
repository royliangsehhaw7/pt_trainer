# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from orm.models import Workout, Exercise, Tag, Trainer, Client, WorkoutExercise
from ..forms import WorkoutForm, ExerciseFormSet

# - simulate logged in trainer
# logged_in_trainer = 1

# list view with search and pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def workout_list(request):
    # stepper highlight
    request.session['module'] = "workout"


    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    # workouts = Workout.objects.all().select_related('client', 'trainer')
    search = request.GET.get('search', '')
    if search:
        # Use icontains for a better user search experience
        workouts = Workout.objects.filter(trainer=trainer, client__name__icontains=search).order_by('client__name')
    else:     
        workouts = Workout.objects.filter(trainer=trainer).order_by('client__name')

    # page controls - paginators with model data - 4 rows per page
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

def workout_add(request):
    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    if request.method == "POST":
        selected_tag_ids = request.POST.getlist('tags_filter')

        form = WorkoutForm(request.POST)
        formset = ExerciseFormSet(request.POST, prefix='exercises')

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    workout = form.save(commit=False)
                    workout.trainer = trainer       # assign current trainer
                    workout.save()

                    formset.instance = workout
                    formset.save()

                messages.success(request, "New workout created successfully!")

                return redirect('workout_list')
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

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


def workout_edit(request, pk):
    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    workout = get_object_or_404(Workout, pk=pk, trainer = trainer)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        formset = ExerciseFormSet(request.POST, instance=workout)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
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
    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    workout = get_object_or_404(Workout, pk=pk, trainer = trainer)
    if request.method == "POST":
        workout.delete()
        
        return redirect('workout_list')
    
    return render(request, 'trainer/workouts/workout_delete.html', {'workout': workout})