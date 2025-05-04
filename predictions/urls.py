from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.PredictionListView.as_view(), name='list'),
    path('add/', views.PredictionCreateView.as_view(), name='add'),
    path('add/', views.PredictionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PredictionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PredictionUpdateView.as_view(), name='edit'),
    path('<int:pk>/edit/', views.PredictionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PredictionDeleteView.as_view(), name='delete'),
] 