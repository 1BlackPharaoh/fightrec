from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from events.models import Event, Bout, models
from .models import Fighter, WeightClass
from django.db.models import Q, IntegerField
from django.db.models.functions import Cast

def home(request):
    featured_fighters = Fighter.objects.all()[:6]
    total_fighters = Fighter.objects.count()
    
    return render(request, 'fighters/home.html', {
        'featured_fighters': featured_fighters,
        'total_fighters': total_fighters,
    })

def fighter_list(request):
    fighters = Fighter.objects.all().order_by('name')
    
    # Advanced search functionality
    query = request.GET.get('q')
    state = request.GET.get('state')
    weight_class_id = request.GET.get('weight_class')
    stance = request.GET.get('stance')
    min_wins = request.GET.get('min_wins')
    max_losses = request.GET.get('max_losses')
    
    if query:
        fighters = fighters.filter(
            Q(name__icontains=query) |
            Q(state_of_origin__icontains=query) |
            Q(biography__icontains=query)
        )
    
    if state:
        fighters = fighters.filter(state_of_origin__icontains=state)
    
    if weight_class_id:
        fighters = fighters.filter(weight_class_id=weight_class_id)
    
    if stance:
        fighters = fighters.filter(stance=stance)
    
    if min_wins:
        fighters = fighters.filter(total_wins__gte=int(min_wins))
    
    if max_losses:
        fighters = fighters.filter(total_losses__lte=int(max_losses))
    
    # Get filter options
    states = Fighter.objects.values_list('state_of_origin', flat=True).distinct()
    weight_classes = WeightClass.objects.all()
    
    context = {
        'fighters': fighters,
        'states': states,
        'weight_classes': weight_classes,
        'total_fighters': Fighter.objects.count(),
        'search_query': query or '',
        'selected_state': state or '',
    }
    
    # If it's an advanced search with multiple criteria, use search template
    if any([query, state, weight_class_id, stance, min_wins, max_losses]):
        return render(request, 'fighters/search.html', context)
    
    return render(request, 'fighters/fighter_list.html', context)

def fighter_detail(request, fighter_id):
    fighter = get_object_or_404(Fighter, id=fighter_id)
    return render(request, 'fighters/fighter_detail.html', {'fighter': fighter})

def events_dashboard(request):
    # Your events dashboard logic here
    return render(request, 'fighters/events_dashboard.html')

def rankings(request):
    weight_classes = WeightClass.objects.all()
    rankings_data = {}
    
    for wc in weight_classes:
        # Get fighters in this weight class and calculate points
        fighters = Fighter.objects.filter(weight_class=wc)
        
        # Simple ranking algorithm based on wins, KO ratio, and experience
        ranked_fighters = []
        for fighter in fighters:
            # Calculate points: wins are most important, then KO ratio, then fewer losses
            total_fights = fighter.total_wins + fighter.total_losses + fighter.total_draws
            if total_fights > 0:
                ko_ratio = fighter.kos / total_fights
            else:
                ko_ratio = 0
                
            points = (
                fighter.total_wins * 10 +          # 10 points per win
                fighter.kos * 5 +                  # 5 extra points per KO
                (ko_ratio * 100) +                 # KO ratio percentage
                (fighter.total_wins - fighter.total_losses) * 2  # Win-loss differential
            )
            ranked_fighters.append((fighter, points))
        
        # Sort by points descending and take top 10
        ranked_fighters.sort(key=lambda x: x[1], reverse=True)
        rankings_data[wc] = [fighter for fighter, points in ranked_fighters[:10]]
    
    return render(request, 'fighters/rankings.html', {'rankings_data': rankings_data})

def statistics(request):
    # Basic statistics
    total_fighters = Fighter.objects.count()
    total_events = Event.objects.count()
    total_bouts = Bout.objects.count()
    
    # State statistics
    states_stats = Fighter.objects.values('state_of_origin').annotate(
        count=models.Count('id'),
        total_wins=models.Sum('total_wins'),
        total_kos=models.Sum('kos')
    ).order_by('-count')
    
    # Weight class statistics
    weight_class_stats = WeightClass.objects.annotate(
        fighter_count=models.Count('fighter'),
        total_wins=models.Sum('fighter__total_wins'),
        total_kos=models.Sum('fighter__kos')
    )
    
    # Champion (fighter with most wins)
    try:
        champion = Fighter.objects.order_by('-total_wins', 'total_losses').first()
    except:
        champion = None
    
    return render(request, 'fighters/statistics.html', {
        'total_fighters': total_fighters,
        'total_events': total_events,
        'total_bouts': total_bouts,
        'states_stats': states_stats,
        'weight_class_stats': weight_class_stats,
        'champion': champion,
    })