from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.WorkoutListView.as_view(), name='list'),
    path('add/', views.WorkoutCreateView.as_view(), name='add'),
    path('add/', views.WorkoutCreateView.as_view(), name='create'),
    path('<int:pk>/', views.WorkoutDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.WorkoutUpdateView.as_view(), name='edit'),
    path('<int:pk>/edit/', views.WorkoutUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='delete'),
] 