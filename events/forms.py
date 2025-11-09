from django import forms
from .models import Event, Bout
from fighters.models import Fighter, WeightClass

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'promoter']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event location'}),
            'promoter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter promoter name'}),
        }
        labels = {
            'name': 'Event Name',
            'date': 'Event Date',
            'location': 'Event Location',
            'promoter': 'Promoter',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class BoutForm(forms.ModelForm):
    class Meta:
        model = Bout
        fields = ['fighter_a', 'fighter_b', 'weight_class', 'scheduled_rounds', 'result_type', 'winning_fighter', 'round_ended', 'is_draw']
        widgets = {
            'scheduled_rounds': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 15}),
            'round_ended': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 15}),
            'result_type': forms.Select(attrs={'class': 'form-control'}),
            'is_draw': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Order fighters by name
        self.fields['fighter_a'].queryset = Fighter.objects.all().order_by('name')
        self.fields['fighter_b'].queryset = Fighter.objects.all().order_by('name')
        self.fields['winning_fighter'].queryset = Fighter.objects.all().order_by('name')
        self.fields['weight_class'].queryset = WeightClass.objects.all().order_by('weight_limit')
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name != 'is_draw':
                field.widget.attrs.update({'class': 'form-control'})
            if field_name in ['fighter_a', 'fighter_b', 'winning_fighter', 'weight_class']:
                field.empty_label = "Select..."
    
    def clean(self):
        cleaned_data = super().clean()
        fighter_a = cleaned_data.get('fighter_a')
        fighter_b = cleaned_data.get('fighter_b')
        winning_fighter = cleaned_data.get('winning_fighter')
        is_draw = cleaned_data.get('is_draw')
        
        # Check if fighters are the same
        if fighter_a and fighter_b and fighter_a == fighter_b:
            raise forms.ValidationError("Fighters cannot be the same person.")
        
        # Check if winning fighter is one of the bout fighters
        if winning_fighter and not is_draw:
            if winning_fighter not in [fighter_a, fighter_b]:
                raise forms.ValidationError("Winning fighter must be one of the bout participants.")
        
        return cleaned_data