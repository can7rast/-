from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressListView.as_view(), name='list'),
    path('add/', views.ProgressCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProgressDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProgressUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProgressDeleteView.as_view(), name='delete'),
    # URL-маршруты для личных рекордов
    path('pr/add/', views.PersonalRecordCreateView.as_view(), name='create_pr'),
    path('pr/<int:pk>/edit/', views.PersonalRecordUpdateView.as_view(), name='update_pr'),
    path('pr/<int:pk>/delete/', views.PersonalRecordDeleteView.as_view(), name='delete_pr'),
] 