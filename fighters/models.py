from django.db import models

class WeightClass(models.Model):
    name = models.CharField(max_length=50)
    weight_limit = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name

class Fighter(models.Model):
    STANCE_CHOICES = [
        ('Orthodox', 'Orthodox'),
        ('Southpaw', 'Southpaw'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    state_of_origin = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, default='Nigerian')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    reach = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Reach in cm")
    stance = models.CharField(max_length=10, choices=STANCE_CHOICES)
    
    # Career Stats
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    total_draws = models.IntegerField(default=0)
    kos = models.IntegerField(default=0, help_text="Knockout wins")
    
    # Media & Bio
    biography = models.TextField(blank=True, help_text="Fighter biography and career highlights")
    photo = models.ImageField(upload_to='fighters/photos/', null=True, blank=True, help_text="Fighter profile photo")
    
    # Weight Class
    weight_class = models.ForeignKey(WeightClass, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def record(self):
        return f"{self.total_wins}-{self.total_losses}-{self.total_draws}"
    
    @property
    def knockout_ratio(self):
        total_fights = self.total_wins + self.total_losses + self.total_draws
        if total_fights > 0 and self.kos > 0:
            return f"{(self.kos / total_fights * 100):.1f}%"
        return "0%"
    
    class Meta:
        ordering = ['name']