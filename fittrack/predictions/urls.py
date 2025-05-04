from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.prediction_list, name='list'),
    path('create/', views.prediction_create, name='create'),
    path('<int:pk>/', views.prediction_detail, name='detail'),
    path('<int:pk>/delete/', views.prediction_delete, name='delete'),
] 