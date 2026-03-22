
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from orm.models import Tag, Trainer
from ..forms.tag_form import TagForm

# - simulate logged in trainer
logged_in_trainer = 1

# simple list view
# def tag_list(request):
#     trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)
#     tags = Tag.objects.filter(trainer=trainer_instance)
#     return render(request, 'trainer/tag/tag_list.html', {'tags': tags})


# list view with search
"""
def tag_list(request):
    trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

    search = request.GET.get('search', '')
    if search:
        # Use icontains for a better user search experience
        tags = Tag.objects.filter(trainer=trainer_instance, name__icontains=search)
    else:     
        tags = Tag.objects.filter(trainer=trainer_instance)

    return render(request, 'trainer/tag/tag_list.html', {'tags': tags, 'search': search})
"""

# list view with search and pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def tag_list(request):
    trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

    search = request.GET.get('search', '')
    if search:
        # Use icontains for a better user search experience
        tags = Tag.objects.filter(trainer=trainer_instance, name__icontains=search).order_by('name')
    else:     
        tags = Tag.objects.filter(trainer=trainer_instance).order_by('name')

    # pagination controls
    paginator = Paginator(tags, 3)
    #
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/tag/tag_list.html', {'tags': pager, 'search': search, 'page_obj': pager})

def tag_add(request):
    # Saas tenant - get logged in tenant for data filtering
    trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)   # don't save yet
            tag.trainer = trainer_instance  # attach trainer here
            tag.save()

            messages.success(request, "Tag added successfully!")
            return redirect("tag_list")
    else:
        form = TagForm()

    return render(request, "trainer/tag/tag_add.html", {"form": form})


def tag_edit(request, pk):
    # Saas tenant - get logged in tenant for data filtering
    trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

    # getting data from database first
    # actually this has NO concurrency check, 
    # data from this get could have been changed before
    # STILL this is required to let django knows this is an update nor insert
    tag = get_object_or_404(Tag, pk=pk, trainer=trainer_instance)

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.trainer = trainer_instance  # optional but safe
            tag.save()

            messages.success(request, "Tag updated successfully!")
            return redirect("trainer:tag_list")
    else:
        form = TagForm(instance=tag)

    return render(request, "trainer/tag/tag_edit.html", {"form": form})


def tag_delete(request, pk):
    # Saas requirement, tenant
    trainer_instance = get_object_or_404(Trainer, pk=logged_in_trainer)

    # Ensure the tag belongs to this trainer before deleting
    tag = get_object_or_404(Tag, pk=pk, trainer=trainer_instance)

    if request.method == "POST":
        tag_name = tag.name  # Store name before deleting for the message
        tag.delete()
        messages.success(request, f"Tag '{tag_name}' deleted.")
        return redirect('tag_list')
    
    # No form needed, just pass the object to the template for confirmation
    return render(request, 'trainer/tag/tag_delete.html', {'tag': tag})

import json

def get_tags(request):
    # Saas requirement, tenant
    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    tags = Tag.objects.filter(trainer = trainer)

    return JsonResponse(list(tags.values()), safe=False)