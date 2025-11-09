from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Event, Bout
from fighters.models import Fighter, WeightClass
from .forms import EventForm, BoutForm

def event_list(request):
    # Get upcoming and past events
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')
    past_events = Event.objects.filter(date__lt=today).order_by('-date')
    
    return render(request, 'events/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    bouts = event.bouts.all().select_related('fighter_a', 'fighter_b', 'weight_class')
    
    # Calculate event statistics
    total_bouts = bouts.count()
    completed_bouts = bouts.exclude(result_type='').count()
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'bouts': bouts,
        'total_bouts': total_bouts,
        'completed_bouts': completed_bouts,
    })

def bout_detail(request, bout_id):
    bout = get_object_or_404(Bout, id=bout_id)
    return render(request, 'events/bout_detail.html', {'bout': bout})

# Event Management Views
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {
        'form': form,
        'title': 'Create New Event',
        'submit_text': 'Create Event'
    })

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {
        'form': form,
        'title': f'Edit Event: {event.name}',
        'submit_text': 'Update Event'
    })

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Event "{event_name}" deleted successfully!')
        return redirect('event_list')
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# Bout Management Views
@login_required
def create_bout(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = BoutForm(request.POST)
        if form.is_valid():
            bout = form.save(commit=False)
            bout.event = event
            bout.save()
            messages.success(request, f'Bout added to "{event.name}"!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = BoutForm()
    
    return render(request, 'events/bout_form.html', {
        'form': form,
        'event': event,
        'title': f'Add Bout to {event.name}',
        'submit_text': 'Add Bout'
    })

@login_required
def edit_bout(request, bout_id):
    bout = get_object_or_404(Bout, id=bout_id)
    
    if request.method == 'POST':
        form = BoutForm(request.POST, instance=bout)
        if form.is_valid():
            bout = form.save()
            messages.success(request, 'Bout updated successfully!')
            return redirect('event_detail', event_id=bout.event.id)
    else:
        form = BoutForm(instance=bout)
    
    return render(request, 'events/bout_form.html', {
        'form': form,
        'event': bout.event,
        'title': f'Edit Bout: {bout.fighter_a} vs {bout.fighter_b}',
        'submit_text': 'Update Bout'
    })

@login_required
def delete_bout(request, bout_id):
    bout = get_object_or_404(Bout, id=bout_id)
    event_id = bout.event.id
    
    if request.method == 'POST':
        bout.delete()
        messages.success(request, 'Bout deleted successfully!')
        return redirect('event_detail', event_id=event_id)
    
    return render(request, 'events/bout_confirm_delete.html', {'bout': bout})