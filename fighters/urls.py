from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
   # path('', include('fighters.urls')),
    path('', include('events.urls')),
     path('events/', views.events_dashboard, name='events_dashboard'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('fighters/', views.fighter_list, name='fighter_list'),
    path('fighters/<int:fighter_id>/', views.fighter_detail, name='fighter_detail'),
    path('rankings/', views.rankings, name='rankings'),
    path('statistics/', views.statistics, name='statistics'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)