from django.shortcuts import render, redirect
import calendar
from django.http import JsonResponse
from datetime import date
from orm.models import Appointment
from ..forms import AppointmentForm
from django.contrib import messages
from django.urls import reverse

def appoint_list(request):
    return render(request, 'trainer/appointments/appointment_list.html', {})
def appoint_add(request):
# If coming from a calendar click, we might have a date in the URL
    initial_date = request.GET.get('date') 
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # The Save method will trigger the Database UniqueConstraint check
            try:
                # Set end_date manually before saving since it's required in your model
                appointment = form.save(commit=False)
                appointment.end_date = appointment.start_date
                appointment.save()
                messages.success(request, "Appointment scheduled successfully!")
                return redirect('calendar')
            except Exception:
                form.add_error(None, "This slot is already booked for this client or trainer.")
    else:
        form = AppointmentForm(initial={'start_date': initial_date})

    return render(request, 'trainer/appointments/appointment_add.html', {'form': form})
def appoint_edit(request):
    return render(request, 'trainer/appointments/appointment_edit.html', {})
def appoint_delete(request):
    return render(request, 'trainer/appointments/appointment_delete.html', {})


def calendar_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # FIX: Use monthdayscalendar instead of monthcalendar
    cal = calendar.Calendar(firstweekday=6)
    matrix = cal.monthdayscalendar(year, month) 

    # Keep all other logic exactly the same
    appointments = Appointment.objects.filter(start_date__year=year, start_date__month=month)
    
    appt_dict = {}
    for appt in appointments:
        day_num = appt.start_date.day
        if day_num not in appt_dict:
            appt_dict[day_num] = []
        appt_dict[day_num].append(appt)

    # Navigation Logic
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1

    context = {
        'matrix': matrix,
        'appt_dict': appt_dict,
        'year': year,
        'month': month,
        'today': today,
        'target_date': date(year, month, 1),
        'prev_month': prev_month,
        'next_month': next_month,
    }
    return render(request, 'trainer/appointments/calendar.html', context)

def calendar_json_view(request):
    # Fetch appointments for the trainer (or all for now)
    appointments = Appointment.objects.all().select_related('client')
    
    events = []
    for appt in appointments:
        # 1. Map your 'scheduled_time' to a color
        if appt.scheduled_time == 'Morning':
            color = '#0dcaf0' # info
        elif appt.scheduled_time == 'Afternoon':
            color = '#0d6efd' # primary
        else:
            color = '#212529' # dark
            
        # 2. Build the event object
        events.append({
            'id': str(appt.id),
            'title': f"{appt.scheduled_time[0]} | {appt.client.name}",
            'start': appt.start_date.isoformat(), # Must be YYYY-MM-DD
            'end': appt.end_date.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'allDay': True, # Since you only have dates, not times
            'url': reverse('appointment_edit', kwargs={'pk': appt.id}),
        })
        
    return JsonResponse(events, safe=False)

def calendar_full_view(request):
    """Simple view to render the new FullCalendar template"""
    return render(request, 'trainer/appointments/calendar_full.html')