from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.prediction_list, name='list'),
    path('create/', views.create_prediction, name='create'),
    path('api/data/', views.get_prediction_data, name='api_data'),
    path('detail/<int:pk>/', views.PredictionDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.PredictionUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
] 