from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list, name='list'),
    path('add/', views.add_goal, name='add'),
    path('<int:goal_id>/', views.goal_detail, name='detail'),
    path('<int:goal_id>/edit/', views.edit_goal, name='edit'),
    path('<int:goal_id>/delete/', views.delete_goal, name='delete'),
    path('<int:goal_id>/update-status/', views.update_goal_status, name='update_status'),
] 