from django.db import models
from django.contrib.auth.models import User

class WeightClass(models.Model):
    name = models.CharField(max_length=50)
    weight_limit = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name

class Fighter(models.Model):
    STANCE_CHOICES = [
        ('Orthodox', 'Orthodox'),
        ('Southpaw', 'Southpaw'),
        ('Switch', 'Switch'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    state_of_origin = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, default='Nigerian')
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # in cm
    reach = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # in cm
    stance = models.CharField(max_length=10, choices=STANCE_CHOICES)
    
    # Career Stats (calculated fields)
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    total_draws = models.IntegerField(default=0)
    kos = models.IntegerField(default=0)
    
    # Media
    photo = models.ImageField(upload_to='fighters/', null=True, blank=True)
    biography = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def record(self):
        return f"{self.total_wins}-{self.total_losses}-{self.total_draws}"

class Organization(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name