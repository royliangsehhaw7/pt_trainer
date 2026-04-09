from django.shortcuts import render, redirect, get_object_or_404
import calendar
from django.http import JsonResponse
from datetime import date
from orm.models import Appointment, Trainer, Client
from ..forms import AppointmentForm
from django.contrib import messages
from django.urls import reverse
from django.core.validators import ValidationError

# list view with search and pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def appoint_list(request):
    # stepper highlight
    request.session['module'] = "appointment"

    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    search = request.GET.get('search', '')
    if search:
        # icontains to ignore char case
        appts = Appointment.objects.filter(trainer=trainer, client__name=search).order_by('client__name')
    else:     
        appts = Appointment.objects.filter(trainer=trainer).order_by('client__name')

    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(appts, 4)
    page_number = request.GET.get('page')

    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)    

    return render(request, 'trainer/appointments/appointment_list.html', {'appointments': pager, 'search': search, 'page_obj': pager})


def appoint_add(request):
    # stepper highlight
    request.session['module'] = "appointment"

    trainer = get_object_or_404(Trainer, pk = request.user.id)

    # If coming from a calendar click, we might have a date in the URL
    initial_date = request.GET.get('date') 
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, trainer = trainer)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.trainer = trainer
                appointment.save()
                messages.success(request, "Appointment scheduled successfully!")

                return redirect('appointment_list')
            except ValidationError as e:
                form.erros.add(None, str(e))
            except Exception:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = AppointmentForm(
            trainer = trainer, 
            initial={'scheduled_date': initial_date}
        )

    return render(request, 'trainer/appointments/appointment_add.html', {'form': form })


def appoint_edit(request, pk):
    # stepper highlight
    request.session['module'] = "appointment"    
    trainer = get_object_or_404(Trainer, pk = request.user.id)

    appointment = get_object_or_404(Appointment, pk = pk, trainer = trainer)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, trainer = trainer)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.trainer = trainer
                appointment.save()
                messages.success(request, "Appointment scheduled successfully!")

                return redirect('appointment_list')
            except ValidationError as e:
                form.erros.add(None, str(e))
            except Exception:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = AppointmentForm(instance = appointment, trainer = trainer)

    return render(request, 'trainer/appointments/appointment_edit.html', {'form': form })


def appoint_delete(request, pk):
    # stepper highlight
    request.session['module'] = "appointment"

    # Ensure the tag belongs to this trainer before deleting
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == "POST":
        try:
            appointment.delete()
            messages.success(request, f"Appointment deleted.")
            
            return redirect('appointment_list')
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    
    return render(request, 'trainer/appointments/appointment_delete.html', {})


def appoint_calendar(request):
    # stepper highlight
    request.session['module'] = "appointment"
    
    return render(request, 'trainer/appointments/appointment_calendar.html')


def calendar_json_view(request):
    # Fetch appointments for the trainer (or all for now)
    appointments = Appointment.objects.all().select_related('client')
    
    events = []
    for appt in appointments:           
        # create an FullCalendar event object
        # https://fullcalendar.io/docs/event-object
        events.append({
            'id': str(appt.id),
            'title': f"{appt.scheduled_time[0]} | {appt.client.name}",
            'start': appt.scheduled_date.isoformat(),   # Must be YYYY-MM-DD

            #'url': '/appointment/edit/{appt.id}/'
            'url': reverse('appointment_edit', kwargs={'pk': appt.id}),
        })
        
    return JsonResponse(events, safe=False)

