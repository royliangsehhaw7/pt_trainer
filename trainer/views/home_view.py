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

    clients = Client.objects.filter(trainer=trainer)
    clients = clients.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(workouts__is_completed=True), distinct=True),
        pending=Count('id', filter=Q(workouts__is_completed=False), distinct=True)
    )

    pending_workouts = Workout.objects.filter(trainer = trainer, is_completed = 0)
    pending_workouts = pending_workouts.values(
        'client__name'
    )

    summary = {
        'tag_count': tag_count, 
        'exe_count': exe_count, 
        'clients' : clients,
        'workouts': workouts,
        'pending_workouts': pending_workouts
    }

    return render(request, 'trainer/home.html', {'summary': summary})