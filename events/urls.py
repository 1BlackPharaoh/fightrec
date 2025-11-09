from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('bouts/<int:bout_id>/', views.bout_detail, name='bout_detail'),
    
    # Event management
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    
    # Bout management
    path('events/<int:event_id>/bouts/create/', views.create_bout, name='create_bout'),
    path('bouts/<int:bout_id>/edit/', views.edit_bout, name='edit_bout'),
    path('bouts/<int:bout_id>/delete/', views.delete_bout, name='delete_bout'),
    
    # Dashboard
    # Path('events/dashboard/', views.events_dashboard, name='events_dashboard'),
]