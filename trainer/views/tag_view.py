from django.http import request
from django.contrib import messages
from django.shortcuts import render, redirect

from orm.models import Tag
from ..forms.tag_form import TagForm

def list(request):
    # - simulate logged in trainer
    logged_in_trainer_id = 1
    
    tags = Tag.objects.filter(trainer_id = logged_in_trainer_id)

    return render(request, 'trainer/tag/tag_list.html', {'tags': tags})

def add(request):
    form = TagForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Author added successfully!")
            return redirect("trainer:tag_list")
    
    return render(request, "trainer/tag/tag_add.html", {"form": form})

def edit(request):
    pass

def delete(request):
    pass
