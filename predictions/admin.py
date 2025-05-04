from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'prediction_type', 'current_value', 'predicted_value', 'prediction_date', 'target_date', 'confidence')
    list_filter = ('user', 'prediction_type', 'prediction_date')
    search_fields = ('user__username', 'prediction_type', 'notes') 