from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from orm.models import Trainer, Tag, Exercise, Client, Workout

def home(request):
    #
    trainer = get_object_or_404(Trainer, pk = request.user.id)
    # stepper purposes
    request.session['module'] = None

    
    # ---https://hakibenita.com/django-group-by-sql
    tag_count = Tag.objects.filter(trainer=trainer).count()
    exe_count = Exercise.objects.filter(trainer=trainer).count()

    # workouts = Workout.objects.values('is_completed').annotate(total=Count('id'))

    workouts = Workout.objects.filter(trainer=trainer)
    workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        pending=Count('id', filter=Q(is_completed=False))
    )

    # --- https://hakibenita.com/django-group-by-sql
    # workouts group by count
    # workout_by_clients = Client.objects.annotate(total=Count('exercises'))

    # left outer join
    workout_by_clients = Client.objects.annotate(
        total=Count('workouts')
    ).values('id', 'total')

    workout_agg = {"high": 0, "medium": 0, "low": 0}
    for workout in workout_by_clients:
        if workout['total'] >= 5:
            workout_agg['high'] = workout_agg["high"] + 1
        elif workout['total'] > 1:
            workout_agg["medium"] = workout_agg["medium"] + 1
        else:
            workout_agg["low"] = workout_agg["low"] + 1


    

    # clients = Client.objects.filter(trainer=trainer)
    # clients = clients.aggregate(
    #     total=Count('id'),
    #     completed=Count('id', filter=Q(workouts__is_completed=True), distinct=True),
    #     pending=Count('id', filter=Q(workouts__is_completed=False), distinct=True)
    # )

    pending_workouts = Workout.objects.filter(trainer = trainer, is_completed = 0)\
                        .annotate(name='client__name', total_exe=Count(<<filter here>>))
    

    pending_workouts = pending_workouts.values(
        'client__name', 'workout'
    )

    summary = {
        'tag_count': tag_count, 
        'exe_count': exe_count, 
        'workout_agg': workout_agg,
        'workouts': workouts,
        'pending_workouts': pending_workouts
    }

    return render(request, 'trainer/home.html', {'summary': summary})