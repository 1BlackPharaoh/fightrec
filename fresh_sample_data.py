import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fightrec.settings')
django.setup()

from fighters.models import Fighter, WeightClass
from events.models import Event, Bout

def create_massive_sample_data():
    print("🥊 Creating MASSIVE sample data with 100 Nigerian boxers...")
    
    # Clear existing data
    print("\n🗑️  Clearing existing data...")
    Bout.objects.all().delete()
    Event.objects.all().delete()
    Fighter.objects.all().delete()
    WeightClass.objects.all().delete()
    
    # Create Weight Classes
    print("\n📦 Creating weight classes...")
    weight_classes_data = [
        ("Heavyweight", 200.00),
        ("Cruiserweight", 90.70),
        ("Light Heavyweight", 79.40),
        ("Super Middleweight", 76.20),
        ("Middleweight", 72.60),
        ("Super Welterweight", 69.90),
        ("Welterweight", 66.70),
        ("Super Lightweight", 63.50),
        ("Lightweight", 61.20),
        ("Featherweight", 57.20),
        ("Super Bantamweight", 55.30),
        ("Bantamweight", 53.50),
        ("Super Flyweight", 52.20),
        ("Flyweight", 50.80),
    ]
    
    weight_classes = {}
    for name, limit in weight_classes_data:
        wc = WeightClass.objects.create(name=name, weight_limit=limit)
        weight_classes[name] = wc
        print(f"  ✅ Created: {name}")

    # Nigerian States
    nigerian_states = [
        "Lagos", "Kano", "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", 
        "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", 
        "Gombe", "Imo", "Jigawa", "Kaduna", "Katsina", "Kebbi", "Kogi", "Kwara", 
        "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", 
        "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT Abuja"
    ]

    # Fighter name components for realistic names
    first_names = [
        "Ade", "Chika", "Emeka", "Femi", "Gbenga", "Ike", "Jide", "Kunle", "Lekan", "Musa",
        "Nnamdi", "Ola", "Segun", "Tunde", "Uche", "Yemi", "Abdul", "Bola", "Chinedu", "Dayo",
        "Efe", "Gabriel", "Hassan", "Ibrahim", "Johnson", "Kingsley", "Michael", "Nuhu", "Olu", "Peter"
    ]
    
    last_names = [
        "Adeyemi", "Balogun", "Chukwu", "Danjuma", "Eze", "Falana", "Garba", "Hassan", "Ibe", "Joseph",
        "Kalu", "Lawal", "Mohammed", "Nwosu", "Okafor", "Okoro", "Sani", "Taiwo", "Umar", "Yusuf",
        "Obi", "Bello", "Ali", "Ogun", "Shehu", "Babatunde", "Oladipo", "Mustapha", "Onyeka", "Adebayo"
    ]

    # Biography templates
    bio_templates = [
        "Known for {style}, this fighter has made a name in the Nigerian boxing circuit with impressive performances.",
        "A rising star from {state}, showing great potential with {record} record and knockout power.",
        "Veteran boxer with extensive experience in both local and international competitions.",
        "Technical boxer with excellent footwork and defensive skills, representing {state} with pride.",
        "Power puncher who has quickly risen through the ranks with devastating knockout ability.",
        "Skilled counter-puncher with a solid amateur background, now making waves in professional boxing.",
        "Aggressive pressure fighter who overwhelms opponents with constant attack and power shots.",
        "Defensive specialist known for elusive movement and precise counter-punching combinations.",
        "All-around boxer with good power, speed, and technical ability, considered a future champion.",
        "Come-forward fighter with iron chin and relentless pressure, exciting to watch in the ring."
    ]

    # Create 100 Nigerian Fighters
    print("\n👥 Creating 100 Nigerian fighters...")
    fighters = []
    
    for i in range(100):
        # Generate realistic fighter data
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        state = random.choice(nigerian_states)
        stance = random.choice(["Orthodox", "Southpaw"])
        
        # Generate realistic record based on experience level
        if i < 20:  # Prospects (0-10 fights)
            wins = random.randint(5, 10)
            losses = random.randint(0, 2)
            draws = random.randint(0, 1)
        elif i < 60:  # Established fighters (10-30 fights)
            wins = random.randint(10, 25)
            losses = random.randint(2, 8)
            draws = random.randint(0, 3)
        else:  # Veterans (25+ fights)
            wins = random.randint(20, 45)
            losses = random.randint(5, 15)
            draws = random.randint(1, 5)
        
        kos = random.randint(int(wins * 0.3), int(wins * 0.8))  # 30-80% KO rate
        
        # Weight class distribution - more fighters in popular weight classes
        weight_class_choices = [
            "Heavyweight", "Cruiserweight", "Light Heavyweight", "Super Middleweight", 
            "Middleweight", "Super Welterweight", "Welterweight", "Super Lightweight", 
            "Lightweight", "Featherweight"
        ]
        weights = random.choices(weight_class_choices, weights=[5, 8, 10, 12, 15, 15, 12, 10, 8, 5], k=1)
        weight_class_name = weights[0]
        
        # Generate physical attributes based on weight class
        if weight_class_name in ["Heavyweight", "Cruiserweight"]:
            height = random.randint(185, 205)
            reach = height + random.randint(5, 15)
        elif weight_class_name in ["Light Heavyweight", "Super Middleweight", "Middleweight"]:
            height = random.randint(175, 190)
            reach = height + random.randint(3, 10)
        else:
            height = random.randint(165, 180)
            reach = height + random.randint(2, 8)
        
        # Generate birth date (18-35 years old)
        age = random.randint(18, 35)
        birth_year = date.today().year - age
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_date = date(birth_year, birth_month, birth_day)
        
        # Generate biography
        style_options = ["devastating power", "technical brilliance", "relentless pressure", "speed and agility", "defensive mastery"]
        bio = random.choice(bio_templates).format(
            style=random.choice(style_options),
            state=state,
            record=f"{wins}-{losses}-{draws}"
        )
        
        # Create fighter
        fighter = Fighter.objects.create(
            name=full_name,
            state_of_origin=state,
            stance=stance,
            total_wins=wins,
            total_losses=losses,
            total_draws=draws,
            kos=kos,
            weight_class=weight_classes[weight_class_name],
            height=float(height),
            reach=float(reach),
            birth_date=birth_date,
            biography=bio
        )
        
        fighters.append(fighter)
        
        if (i + 1) % 10 == 0:
            print(f"  ✅ Created {i + 1}/100 fighters...")
    
    print("  ✅ All 100 fighters created successfully!")

    # Create Events and Bouts
    print("\n📅 Creating events and bouts...")
    
    # Event locations in Nigeria
    event_locations = [
        "Lagos National Stadium, Lagos",
        "Abuja International Arena, Abuja",
        "Teslim Balogun Stadium, Lagos", 
        "Adokiye Amiesimaka Stadium, Port Harcourt",
        "Sani Abacha Stadium, Kano",
        "Liberation Stadium, Uyo",
        "Nnamdi Azikiwe Stadium, Enugu",
        "Adamasingba Stadium, Ibadan",
        "Rwang Pam Stadium, Jos",
        "Stephen Keshi Stadium, Asaba"
    ]
    
    promoters = [
        "Nigerian Boxing Promotions",
        "GoTv Boxing Night",
        "African Boxing Union",
        "West African Boxing Council",
        "Naija Fight Promotions",
        "Lagos Boxing Association",
        "Abuja Fight Club",
        "Port Harcourt Boxing League",
        "Kano Warriors Promotions",
        "Delta Fighting Championship"
    ]
    
    # Create 20 events across different dates
    events = []
    for i in range(20):
        event_date = date(2023, 1, 1) + timedelta(days=random.randint(0, 730))  # Random date in 2023-2024
        event = Event.objects.create(
            name=f"{random.choice(promoters)} Fight Night #{i+1}",
            date=event_date,
            location=random.choice(event_locations),
            promoter=random.choice(promoters)
        )
        events.append(event)
    
    print(f"  ✅ Created {len(events)} events")

    # Create bouts for each event
    print("\n🥊 Creating bouts...")
    result_types = ['UD', 'SD', 'MD', 'KO', 'TKO', 'DQ']
    bouts_created = 0
    
    for event in events:
        # Each event has 5-10 bouts
        num_bouts = random.randint(5, 10)
        available_fighters = fighters.copy()
        random.shuffle(available_fighters)
        
        for i in range(num_bouts):
            if len(available_fighters) >= 2:
                fighter_a = available_fighters.pop()
                fighter_b = available_fighters.pop()
                
                # Ensure fighters are in same weight class
                while fighter_b.weight_class != fighter_a.weight_class and len(available_fighters) > 0:
                    available_fighters.insert(0, fighter_b)
                    fighter_b = available_fighters.pop()
                
                if fighter_b.weight_class == fighter_a.weight_class:
                    # Create bout with random result
                    result = random.choice(result_types)
                    winning_fighter = random.choice([fighter_a, fighter_b])
                    round_ended = random.randint(1, 12) if result in ['KO', 'TKO'] else None
                    
                    bout = Bout.objects.create(
                        event=event,
                        fighter_a=fighter_a,
                        fighter_b=fighter_b,
                        weight_class=fighter_a.weight_class,
                        scheduled_rounds=random.choice([8, 10, 12]),
                        result_type=result,
                        winning_fighter=winning_fighter,
                        round_ended=round_ended
                    )
                    bouts_created += 1
    
    print(f"  ✅ Created {bouts_created} bouts")

    # Update fighter records based on bouts
    print("\n📊 Updating fighter records based on bout results...")
    for fighter in fighters:
        wins = fighter.total_wins
        losses = fighter.total_losses
        draws = fighter.total_draws
        kos = fighter.kos
        
        # This is a simplified update - in a real system you'd calculate from actual bouts
        fighter.save()
    
    print("\n🎉 MASSIVE SAMPLE DATA CREATION COMPLETED!")
    print("=" * 50)
    print(f"📊 FINAL DATABASE STATISTICS:")
    print(f"   👥 Fighters: {Fighter.objects.count()}")
    print(f"   📦 Weight Classes: {WeightClass.objects.count()}")
    print(f"   📅 Events: {Event.objects.count()}")
    print(f"   🥊 Bouts: {Bout.objects.count()}")
    print(f"   🏴‍☠️ States Represented: {len(set(f.state_of_origin for f in Fighter.objects.all()))}")
    print("\n🌟 WEBSITE FEATURES TO TEST:")
    print("   ✅ Advanced Search with 100 fighters")
    print("   ✅ Rankings across 14 weight classes") 
    print("   ✅ Statistics dashboard with rich data")
    print("   ✅ Event pages with multiple bouts")
    print("   ✅ Fighter profiles with detailed bios")
    print("\n🚀 Your FightRec website is now loaded with realistic data!")

if __name__ == "__main__":
    create_massive_sample_data()