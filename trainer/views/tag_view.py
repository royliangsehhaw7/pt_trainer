
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from orm.models import Tag 
from orm.models import UserTrainer as Trainer

from ..forms.tag_form import TagForm

# - simulate logged in trainer
# logged_in_trainer = 1

# # simple list view
# def tag_list(request):
#     # Saas tenant check
#     trainer = get_object_or_404(Trainer, pk=request.user.id)
#     # filter tags 
#     tags = Tag.objects.filter(trainer=trainer)

#     # -- normal get exercises count
#     # tag = Tag.objects.get(id=1)
#     # count1 = tag.exercises.count()
#     # count2 = Exercise.objects.filter(tags__id=1).count()
    
    
#     # using annotate to create a computer property
#     # 2. Get tags for this trainer and "attach" the count
#     # 'exercises' matches the related_name we set in the ManyToManyField
#     tags = Tag.objects.filter(trainer=trainer).annotate(
#         exercise_count=Count('exercises')
#     )

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
    trainer = get_object_or_404(Trainer, pk=request.user.id)

    search = request.GET.get('search', '')
    if search:
        # Use icontains for a better user search experience
        tags = Tag.objects.filter(trainer=trainer, name__icontains=search).order_by('name')
    else:     
        tags = Tag.objects.filter(trainer=trainer).order_by('name')

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
    trainer= get_object_or_404(Trainer, pk=request.user.id)

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                tag = form.save(commit=False)   # don't save yet, get the tag model
                tag.trainer = trainer           # attach trainer here

                tag.full_clean()                # triggre model validation
                tag.save()
                messages.success(request, "Tag added successfully!")

                return redirect("tag_list")
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")

    else:
        form = TagForm()

    return render(request, "trainer/tag/tag_add.html", {"form": form})


def tag_edit(request, pk):
    # Saas tenant - get logged in tenant for data filtering
    trainer_instance = get_object_or_404(Trainer, pk=request.user.id)

    # getting data from database first
    # actually this has NO concurrency check, 
    # data from this get could have been changed before
    # STILL this is required to let django knows this is an update nor insert
    tag = get_object_or_404(Tag, pk=pk, trainer=trainer_instance)

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            try:
                tag = form.save(commit=False)
                tag.trainer = trainer_instance  # optional but safe
                
                tag.full_clean()
                tag.save()
                messages.success(request, "Tag updated successfully!")
                
                return redirect("tag_list")
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = TagForm(instance=tag)

    return render(request, "trainer/tag/tag_edit.html", {"form": form})


def tag_delete(request, pk):
    # Saas requirement, tenant
    trainer_instance = get_object_or_404(Trainer, pk=request.user.id)

    # Ensure the tag belongs to this trainer before deleting
    tag = get_object_or_404(Tag, pk=pk, trainer=trainer_instance)

    if request.method == "POST":
        try:            
            tag_name = tag.name             # Store name before deleting for the message
            tag.delete()
            messages.success(request, f"Tag '{tag_name}' deleted.")
            
            return redirect('tag_list')
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    
    # No form needed, just pass the object to the template for confirmation
    return render(request, 'trainer/tag/tag_delete.html', {'tag': tag})


def get_tags(request):
    # Saas requirement, tenant
    trainer = get_object_or_404(Trainer, pk=request.user.id)
    tags = Tag.objects.filter(trainer = trainer)

    return JsonResponse(list(tags.values()), safe=False)