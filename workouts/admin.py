from django.contrib import admin
from .models import Workout, WeeklyWorkoutStats, MonthlyWorkoutStats


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'workout_type', 'duration', 'intensity', 'calories_burned')
    list_filter = ('user', 'date', 'workout_type', 'intensity')
    search_fields = ('user__username', 'notes')
    date_hierarchy = 'date'


@admin.register(WeeklyWorkoutStats)
class WeeklyWorkoutStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_start', 'week_end', 'total_workouts', 'total_duration', 'total_calories')
    list_filter = ('user', 'week_start')
    search_fields = ('user__username',)
    date_hierarchy = 'week_start'


@admin.register(MonthlyWorkoutStats)
class MonthlyWorkoutStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'month', 'total_workouts', 'total_duration', 'total_calories')
    list_filter = ('user', 'year', 'month')
    search_fields = ('user__username',)
    ordering = ('-year', '-month') 