from django.contrib import admin
from .models import Fighter, WeightClass

@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_of_origin', 'weight_class', 'record', 'stance', 'created_at']
    list_filter = ['state_of_origin', 'stance', 'weight_class', 'created_at']
    search_fields = ['name', 'biography']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'birth_date', 'state_of_origin', 'nationality')
        }),
        ('Physical Attributes', {
            'fields': ('height', 'reach', 'stance', 'weight_class')
        }),
        ('Career Statistics', {
            'fields': ('total_wins', 'total_losses', 'total_draws', 'kos')
        }),
        ('Media & Biography', {
            'fields': ('photo', 'biography')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeightClass)
class WeightClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight_limit']
    search_fields = ['name']