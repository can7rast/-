from django.urls import path
from . import views

app_name = 'sleep'

urlpatterns = [
    path('', views.sleep_list, name='list'),
    path('create/', views.sleep_create, name='create'),
    path('<int:pk>/', views.sleep_detail, name='detail'),
    path('<int:pk>/update/', views.sleep_update, name='update'),
    path('<int:pk>/delete/', views.sleep_delete, name='delete'),
] 