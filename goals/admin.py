from django.contrib import admin
from .models import Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'goal_type', 'status', 'start_date', 'target_date')
    list_filter = ('goal_type', 'status', 'start_date', 'target_date')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'start_date' 