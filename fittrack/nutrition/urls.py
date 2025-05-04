from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.meal_list, name='list'),
    path('create/', views.meal_create, name='create'),
    path('<int:pk>/', views.meal_detail, name='detail'),
    path('<int:pk>/update/', views.meal_update, name='update'),
    path('<int:pk>/delete/', views.meal_delete, name='delete'),
] 