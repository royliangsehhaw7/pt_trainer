from django.contrib import messages
from django.http import JsonResponse
from django.forms import ValidationError
# from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from orm.models import Client
from orm.models import UserTrainer as Trainer

from ..forms import ClientForm

# list view with search and pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def client_list(request):
    # Saas tenant requirement
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    search = request.GET.get('search', '')
    if search:
        tags = Client.objects.filter(trainer=trainer, name__icontains=search).order_by('name')
    else:     
        tags = Client.objects.filter(trainer=trainer).order_by('name')

    # pagination controls
    paginator = Paginator(tags, 3)
    page_number = request.GET.get('page')

    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/clients/client_list.html', {'clients': pager, 'search': search, 'page_obj': pager})


def client_add(request):
    # Saas tenant requirement
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():            
            try:
                client = form.save(commit=False)    # dont save first
                client.trainer = trainer            # attach trainer
                # client.preferred_times = "123"
                
                client.full_clean()                 # trigger model validation
                client.save()
                messages.success(request, 'Client updated successfully')

                return redirect('client_list')
            except ValidationError as e:
                form.add_error(None, str(e))                    
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = ClientForm()

    return render(request, 'trainer/clients/client_add.html', {'form': form})


def client_edit(request, pk):
    # Saas tenant requirement
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    # have to check if client belongs to the current logged in user
    client = get_object_or_404(Client, pk=pk, trainer = trainer)

    if request.method == "POST":
        form = ClientForm(request.POST, instance = client)
        if form.is_valid():
            try:
                client = form.save(commit=False)
                client.trainer = trainer

                client.full_clean()
                client.save()
                messages.success(request, 'Client saved successfully!')

                return redirect('client_list')
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = ClientForm(instance=client)

    return render(request, 'trainer/clientsclient_edit.html', {'form': form})
        

def client_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    # Ensure the tag belongs to this trainer before deleting
    client = get_object_or_404(Client, pk=pk, trainer=trainer)

    if request.method == "POST":
        try:
            client_name = client.name
            client.delete()
            messages.success(request, f"Client {client_name} deleted.")
            
            return redirect('client_list')
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    
    return render(request, 'trainer/clients/client_delete.html', {'client': client})


def get_client_by_id(request, pk):
    # Saas requirement, tenant
    trainer = get_object_or_404(Trainer, pk=request.user.id)
    client = Client.objects.get(id=pk, trainer=trainer)

    data = {"id": client.id, "name": client.name, "goals": client.goals }
    return JsonResponse(data)