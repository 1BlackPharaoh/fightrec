from django.contrib import admin
from .models import Event, Bout

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'promoter', 'bout_count']
    list_filter = ['date', 'location']
    search_fields = ['name', 'location', 'promoter']
    date_hierarchy = 'date'
    
    def bout_count(self, obj):
        return obj.bouts.count()
    bout_count.short_description = 'Bouts'

@admin.register(Bout)
class BoutAdmin(admin.ModelAdmin):
    list_display = ['fighter_a', 'fighter_b', 'event', 'weight_class', 'result_type', 'winning_fighter']
    list_filter = ['weight_class', 'result_type', 'event__date']
    search_fields = ['fighter_a__name', 'fighter_b__name', 'event__name']
    autocomplete_fields = ['fighter_a', 'fighter_b', 'winning_fighter', 'event']