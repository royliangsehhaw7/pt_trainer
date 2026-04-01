from django.contrib.auth.models import Group

from django.db.models import Count


from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..forms import SubscriptionForm
from orm.models import UserTrainer as Trainer


def sub_list(request):
    search = request.GET.get('search', '')
    subType = request.GET.get('subscriptionType', '')

    if search:
        trainers = Trainer.objects.filter(is_trainer = 1, first_name__icontains=search).order_by('first_name')
    else:     
        trainers = Trainer.objects.filter(is_trainer = 1).order_by('first_name')

    if subType:
        trainers = trainers.filter(groups__name = subType)

    # annotate client count
    trainers =  trainers.annotate(client_count = Count('clients'))

    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(trainers, 3)
    page_number = request.GET.get('page')

    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'backend/subscriptions/subscription_list.html', {'trainers': pager, 'search': search, 'page_obj': pager})


def sub_add(request):
    if request.method == "POST":
        # set form to request.POST data from client
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            try:
                trainer = form.save()
                
                new_group = form.cleaned_data['group']
                # NOTE: must clear trainer group before updating the one from form
                trainer.groups.clear() 
                trainer.groups.add(new_group)

                messages.success(request, "Record updated successfully.")
                return redirect('subscription_list')
            except Exception as e:
                messages.error(request, f"Persistence Error: {str(e)}")
    else:
        form = SubscriptionForm()

    return render(request, 'backend/subscriptions/subscription_add.html', {'form': form})

def sub_edit(request, pk):
    # 1. Fetch the Model Instance (The Entity)
    trainer = get_object_or_404(Trainer, pk=pk)

    # a container to pass for editing on non fields
    initial_state = {}

    current_group = trainer.groups.first()      # this is the trainer groups (currently on one group per trainer)
    if current_group:
        initial_state['group'] = current_group.id

    if request.method == "POST":
        # set form to request.POST data from client
        form = SubscriptionForm(request.POST, instance=trainer)

        if form.is_valid():
            try:
                trainer = form.save()
                
                new_group = form.cleaned_data['group']
                # NOTE: must clear trainer group before updating the one from form
                trainer.groups.clear() 
                trainer.groups.add(new_group)

                messages.success(request, "Record updated successfully.")
                return redirect('subscription_list')
            except Exception as e:
                messages.error(request, f"Persistence Error: {str(e)}")
    else:
        #must pass in the previous group of the trainer for editing
        form = SubscriptionForm(instance=trainer, initial=initial_state)

    return render(request, 'backend/subscriptions/subscription_edit.html', {'form': form})

def sub_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk = pk)

    if request.method == "POST":
        try:
            trainer_email = trainer.email

            trainer.delete()
            messages.success(request, f"Trainer {trainer_email} deleted")
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")

            messages.error('subscription_list')

    return render(request, 'backend/subscriptions/subscription_delete.html', {'trainer': trainer})
