from django.db import models
from fighters.models import Fighter, WeightClass, Organization

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    promoter = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.date}"

class Bout(models.Model):
    RESULT_CHOICES = [
        ('UD', 'Unanimous Decision'),
        ('SD', 'Split Decision'),
        ('MD', 'Majority Decision'),
        ('KO', 'Knockout'),
        ('TKO', 'Technical Knockout'),
        ('DQ', 'Disqualification'),
        ('Draw', 'Draw'),
        ('NC', 'No Contest'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bouts')
    fighter_a = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='fights_as_a')
    fighter_b = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='fights_as_b')
    weight_class = models.ForeignKey(WeightClass, on_delete=models.CASCADE)
    scheduled_rounds = models.IntegerField(default=10)
    
    # Result
    result_type = models.CharField(max_length=10, choices=RESULT_CHOICES)
    winning_fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE, null=True, blank=True, related_name='wins')
    losing_fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE, null=True, blank=True, related_name='losses')
    round_ended = models.IntegerField(null=True, blank=True)
    time_ended = models.CharField(max_length=10, blank=True)  # e.g., "2:35"
    is_draw = models.BooleanField(default=False)
    
    # For title fights
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    is_title_fight = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.fighter_a} vs {self.fighter_b}" 