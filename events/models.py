from django.db import models
from fighters.models import Fighter, WeightClass

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    promoter = models.CharField(max_length=100, blank=True)
    
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
    is_draw = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.fighter_a} vs {self.fighter_b}"
    
    def save(self, *args, **kwargs):
        # Auto-set winning/losing fighters for non-draws
        if not self.is_draw and self.winning_fighter:
            if self.winning_fighter == self.fighter_a:
                self.losing_fighter = self.fighter_b
            else:
                self.losing_fighter = self.fighter_a
        super().save(*args, **kwargs)