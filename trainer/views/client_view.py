from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from orm.models import Client
from orm.models import UserTrainer as Trainer

from ..forms import ClientForm

logged_in_trainer = 1

def client_list(request):
    # Saas tenant requirement
    trainer = get_object_or_404(Trainer, pk = logged_in_trainer)

    clients = Client.objects.filter(trainer = trainer)

    return render(request, 'trainer/client/client_list.html', {'clients': clients })


def client_add(request):
    # Saas tenant requirement
    trainer = get_object_or_404(Trainer, pk = logged_in_trainer)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # normal save
            # tag = form.save()
            # with saas, where tenant must be supplied
            client = form.save(commit=False)
            client.trainer = trainer
            client.save()

            messages.success(request, 'Client updated successfully')
            return redirect('client_list')
    else:
        form = ClientForm()

    return render(request, 'trainer/client/client_add.html', {'form': form})


def client_edit(request, pk):
    # Saas tenant requirement
    trainer = get_object_or_404(Trainer, pk = logged_in_trainer)

    # have to check if client belongs to the current logged in user
    client = get_object_or_404(Client, pk=pk, trainer = trainer)

    if request.method == "POST":
        form = ClientForm(request.POST, instance = client)
        if form.is_valid():
            form.save()
            #newClient = form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)

    
    return render(request, 'trainer/client/client_edit.html', {'form': form})
        

    

def client_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    # Ensure the tag belongs to this trainer before deleting
    client = get_object_or_404(Client, pk=pk, trainer=trainer)

    if request.method == "POST":
        client.delete()
        messages.success(request, f"Client deleted.")
        return redirect('client_list')
    
    return render(request, 'trainer/client/client_delete.html', {'client': client})