from django.contrib import admin
from .models import IndicadoresFeedback

@admin.register(IndicadoresFeedback)
class IndicadoresFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'envio_final', 'created_at', 'updated_at')
    search_fields = ('user__username',)
