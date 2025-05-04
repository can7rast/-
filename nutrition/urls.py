from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.MealListView.as_view(), name='list'),
    path('add/', views.MealCreateView.as_view(), name='add'),
    path('add/', views.MealCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MealDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MealUpdateView.as_view(), name='edit'),
    path('<int:pk>/edit/', views.MealUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MealDeleteView.as_view(), name='delete'),
] 