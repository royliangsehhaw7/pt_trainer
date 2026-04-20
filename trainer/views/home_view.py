from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from orm.models import Trainer, Tag, Exercise, Client, Workout

def home(request):
    #
    trainer = get_object_or_404(Trainer, pk = request.user.id)
    # stepper purposes
    request.session['module'] = None

    # -- 1    
    clients_count = Client.objects.filter(trainer=trainer).count()
    tag_count = Tag.objects.filter(trainer=trainer).count()
    exe_count = Exercise.objects.filter(trainer=trainer).count()

    # -- 2
    workouts = Workout.objects.filter(trainer=trainer)
    workouts = workouts.aggregate(
        total=Count(id),
        completed=Count(id, filter=Q(is_completed=True)),
        pending=Count(id, filter=Q(is_completed=False))
    )

    # -- 3
    # annotate - will gives us a group by client
    workout_agg = {"high": 0, "medium": 0, "low": 0}

    clients_workouts = Client.objects.annotate(
        total=Count('workouts')
    )                                       # left outer join
    for client in clients_workouts:
        if client.total >= 5:
            workout_agg['high'] = workout_agg["high"] + 1
        elif client.total >= 1:
            workout_agg["medium"] = workout_agg["medium"] + 1
        else:
            workout_agg["low"] = workout_agg["low"] + 1

 
    # -- 4
    pending_workouts = Workout.objects.filter(trainer = trainer, is_completed = 0) \
                        .annotate(
                            exe_count=Count('exercises', distinct=True),
                            exe_done=Count(id, filter=Q(exercises__is_done = True), distinct=True),
                        ).select_related('client')


    # ---https://hakibenita.com/django-group-by-sql
    # --- https://hakibenita.com/django-group-by-sql
    # workouts group by count
    # workout_by_clients = Client.objects.annotate(total=Count('exercises'))



    # clients = Client.objects.filter(trainer=trainer)
    # clients = clients.aggregate(
    #     total=Count('id'),
    #     completed=Count('id', filter=Q(workouts__is_completed=True), distinct=True),
    #     pending=Count('id', filter=Q(workouts__is_completed=False), distinct=True)
    # )


    
    summary = {
        'tag_count': tag_count, 
        'exe_count': exe_count, 
        'clients_count': clients_count,
        'workout_agg': workout_agg,
        'workouts': workouts,
        'pending_workouts': pending_workouts
    }

    return render(request, 'trainer/home.html', {'summary': summary})