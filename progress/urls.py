from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressListView.as_view(), name='list'),
    path('add/', views.ProgressCreateView.as_view(), name='add'),
    path('add/', views.ProgressCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProgressDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProgressUpdateView.as_view(), name='edit'),
    path('<int:pk>/edit/', views.ProgressUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProgressDeleteView.as_view(), name='delete'),
    path('pr/add/', views.ProgressCreateView.as_view(), name='create_pr'),
    path('pr/<int:pk>/edit/', views.ProgressUpdateView.as_view(), name='update_pr'),
    path('pr/<int:pk>/delete/', views.ProgressDeleteView.as_view(), name='delete_pr'),
] 