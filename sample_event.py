import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fightrec.settings')
django.setup()

from events.models import Event, Bout
from fighters.models import Fighter, WeightClass

def create_sample_events():
    print("Creating sample events...")
    
    # Check if we have enough data
    weight_classes = WeightClass.objects.all()
    fighters = Fighter.objects.all()
    
    print(f"Available weight classes: {weight_classes.count()}")
    print(f"Available fighters: {fighters.count()}")
    
    if weight_classes.count() == 0:
        print("No weight classes found. Please create some in admin first.")
        return
    
    if fighters.count() < 4:
        print("Need at least 4 fighters. Please add more fighters in admin.")
        return
    
    # Get or create weight classes safely
    try:
        heavy = WeightClass.objects.filter(name="Heavyweight").first()
        middle = WeightClass.objects.filter(name="Middleweight").first()
        welter = WeightClass.objects.filter(name="Welterweight").first()
        
        if not heavy:
            print("Heavyweight not found, using first available weight class")
            heavy = weight_classes.first()
    except Exception as e:
        print(f"Error getting weight classes: {e}")
        return
    
    # Create sample events
    events_data = [
        {
            "name": "Lagos Boxing Championship 2024",
            "date": date(2024, 3, 15),
            "location": "Lagos National Stadium",
            "promoter": "Nigerian Boxing Promotions"
        },
        {
            "name": "Abuja Fight Night",
            "date": date(2024, 2, 10),
            "location": "Abuja International Arena", 
            "promoter": "Capital City Promotions"
        },
        {
            "name": "Port Harcourt Boxing Showdown",
            "date": date(2024, 4, 5),
            "location": "Yakubu Gowon Stadium, PH",
            "promoter": "Niger Delta Promotions"
        }
    ]
    
    events_created = 0
    bouts_created = 0
    
    for event_data in events_data:
        # Check if event already exists
        if not Event.objects.filter(name=event_data["name"]).exists():
            event = Event.objects.create(**event_data)
            events_created += 1
            print(f"Created event: {event.name}")
            
            # Create 2-3 bouts for each event
            available_fighters = list(fighters)
            
            for i in range(min(3, len(available_fighters) // 2)):
                if len(available_fighters) >= 2:
                    fighter_a = available_fighters.pop(0)
                    fighter_b = available_fighters.pop(0)
                    
                    # Choose weight class based on available classes
                    if heavy and i == 0:
                        wc = heavy
                    elif middle and i == 1:
                        wc = middle  
                    elif welter:
                        wc = welter
                    else:
                        wc = weight_classes.first()
                    
                    # Create bout with random result
                    result_types = ['UD', 'KO', 'TKO', 'SD']
                    bout = Bout.objects.create(
                        event=event,
                        fighter_a=fighter_a,
                        fighter_b=fighter_b,
                        weight_class=wc,
                        scheduled_rounds=10 if i < 2 else 8,
                        result_type=result_types[i % len(result_types)],
                        winning_fighter=fighter_a,  # Always fighter_a wins for simplicity
                        round_ended=8 if result_types[i % len(result_types)] in ['KO', 'TKO'] else None
                    )
                    bouts_created += 1
                    print(f"  Created bout: {fighter_a.name} vs {fighter_b.name}")
    
    print(f"\nSuccessfully created {events_created} events and {bouts_created} bouts!")
    print(f"Total events in database: {Event.objects.count()}")
    print(f"Total bouts in database: {Bout.objects.count()}")

if __name__ == "__main__":
    create_sample_events()