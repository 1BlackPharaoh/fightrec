import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fightrec.settings')
django.setup()

from fighters.models import Fighter, WeightClass
from events.models import Event, Bout

def verify_data():
    print("🔍 Verifying database contents...")
    
    print(f"👥 Total Fighters: {Fighter.objects.count()}")
    print(f"📦 Total Weight Classes: {WeightClass.objects.count()}")
    print(f"📅 Total Events: {Event.objects.count()}")
    print(f"🥊 Total Bouts: {Bout.objects.count()}")
    
    # Show some sample fighters
    print("\n🎯 Sample Fighters:")
    sample_fighters = Fighter.objects.all()[:5]
    for fighter in sample_fighters:
        print(f"  • {fighter.name} ({fighter.state_of_origin}) - {fighter.record}")
    
    # Show weight class distribution
    print("\n⚖️ Weight Class Distribution:")
    for wc in WeightClass.objects.all():
        count = Fighter.objects.filter(weight_class=wc).count()
        if count > 0:
            print(f"  • {wc.name}: {count} fighters")
    
    # Show state distribution
    print("\n🏴‍☠️ Top States by Fighter Count:")
    from django.db.models import Count
    top_states = Fighter.objects.values('state_of_origin').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    for state in top_states:
        print(f"  • {state['state_of_origin']}: {state['count']} fighters")

if __name__ == "__main__":
    verify_data()