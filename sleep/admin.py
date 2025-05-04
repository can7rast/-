from django.contrib import admin
from .models import Sleep

@admin.register(Sleep)
class SleepAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start_time', 'end_time', 'duration', 'quality', 'interruptions')
    list_filter = ('user', 'date', 'quality')
    search_fields = ('user__username', 'notes') 