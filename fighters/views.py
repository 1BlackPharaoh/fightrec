from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Fighter, WeightClass

def fighter_list(request):
    fighters = Fighter.objects.all().order_by('name')
    
    # Basic search
    query = request.GET.get('q')
    if query:
        fighters = fighters.filter(
            Q(name__icontains=query) |
            Q(state_of_origin__icontains=query)
        )
    
    return render(request, 'fighters/fighter_list.html', {'fighters': fighters})

def fighter_detail(request, fighter_id):
    fighter = get_object_or_404(Fighter, id=fighter_id)
    fights = fighter.fights_as_a.all() | fighter.fights_as_b.all()
    
    return render(request, 'fighters/fighter_detail.html', {
        'fighter': fighter,
        'fights': fights.order_by('-event__date')
    })

def rankings(request):
    weight_classes = WeightClass.objects.all()
    return render(request, 'fighters/rankings.html', {'weight_classes': weight_classes})