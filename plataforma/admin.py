from django.contrib import admin
from .models import StrategicAxis, UserAxisSelection

@admin.register(StrategicAxis)
class StrategicAxisAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)

@admin.register(UserAxisSelection)
class UserAxisSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_axes', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

    def get_axes(self, obj):
        return ", ".join([str(axis) for axis in obj.selected_axes.all()])
    get_axes.short_description = 'Ejes Seleccionados'
