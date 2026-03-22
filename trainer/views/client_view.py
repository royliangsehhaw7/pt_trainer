from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from orm.models import Trainer, Client

logged_in_trainer = 1

def client_list(request):
    trainer = get_object_or_404(Trainer, pk = logged_in_trainer)
    clients = Client.objects.filter(trainer = trainer)

    return render(request, 'trainer/client/client_list.html', {'clients': clients})

def client_add(request):
    pass

def client_edit(request):
    pass

def client_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    # Ensure the tag belongs to this trainer before deleting
    client = get_object_or_404(Client, pk=pk, trainer=trainer)

    if request.method == "POST":
        client.delete()
        messages.success(request, f"Tag deleted.")
        return redirect('tag_list')
    
    return render(request, 'trainer/client/client_delete.html', {'client': client})