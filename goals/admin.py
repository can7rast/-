from django.contrib import admin
from .models import Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal_type', 'current_value', 'target_value', 'status', 'start_date', 'end_date')
    list_filter = ('user', 'goal_type', 'status')
    search_fields = ('user__username', 'goal_type', 'description', 'notes') 