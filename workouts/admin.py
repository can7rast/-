from django.contrib import admin
from .models import WorkoutType, Workout


@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories_per_hour')
    search_fields = ('name',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_type', 'date', 'duration', 'intensity', 'calories_burned')
    list_filter = ('user', 'workout_type', 'date', 'intensity')
    search_fields = ('user__username', 'workout_type__name', 'notes')
    date_hierarchy = 'date' 