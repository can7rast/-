from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list, name='list'),
    path('add/', views.workout_create, name='add'),
    path('<int:pk>/', views.workout_detail, name='detail'),
    path('<int:pk>/edit/', views.workout_update, name='edit'),
    path('<int:pk>/delete/', views.workout_delete, name='delete'),
] 