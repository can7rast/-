from django.contrib import admin
from .models import Meal

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'meal_type', 'calories')
    list_filter = ('user', 'meal_type', 'date')
    search_fields = ('user__username', 'meal_type', 'notes') 