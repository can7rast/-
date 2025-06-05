from django.urls import path
from . import views

app_name = 'sleep'

urlpatterns = [
    path('', views.sleep_list, name='list'),
    path('add/', views.sleep_create, name='add'),
    path('<int:pk>/', views.sleep_detail, name='detail'),
    path('<int:pk>/edit/', views.sleep_update, name='edit'),
    path('<int:pk>/delete/', views.sleep_delete, name='delete'),
] 