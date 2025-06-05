from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.meal_list, name='list'),
    path('add/', views.meal_add, name='add'),
    path('<int:pk>/', views.meal_detail, name='detail'),
    path('<int:pk>/edit/', views.meal_edit, name='edit'),
    path('<int:pk>/delete/', views.meal_delete, name='delete'),
] 