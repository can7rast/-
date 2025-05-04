from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list, name='list'),
    path('create/', views.workout_create, name='create'),
    path('<int:pk>/', views.workout_detail, name='detail'),
    path('<int:pk>/update/', views.workout_update, name='update'),
    path('<int:pk>/delete/', views.workout_delete, name='delete'),
    path('types/', views.workout_type_list, name='type_list'),
    path('types/create/', views.workout_type_create, name='type_create'),
    path('types/<int:pk>/update/', views.workout_type_update, name='type_update'),
    path('types/<int:pk>/delete/', views.workout_type_delete, name='type_delete'),
] 