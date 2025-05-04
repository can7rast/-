from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('workouts/', include('workouts.urls')),
    path('nutrition/', include('nutrition.urls')),
    path('progress/', include('progress.urls')),
    path('goals/', include('goals.urls')),
    path('predictions/', include('predictions.urls')),
    path('sleep/', include('sleep.urls')),
] 