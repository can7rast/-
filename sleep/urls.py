from django.urls import path
from . import views

app_name = 'sleep'

urlpatterns = [
    path('', views.SleepListView.as_view(), name='list'),
    path('add/', views.SleepCreateView.as_view(), name='add'),
    path('add/', views.SleepCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SleepDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.SleepUpdateView.as_view(), name='edit'),
    path('<int:pk>/edit/', views.SleepUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SleepDeleteView.as_view(), name='delete'),
] 