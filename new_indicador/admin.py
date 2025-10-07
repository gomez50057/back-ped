from django.contrib import admin
from .models import NewIndicadorProposal

@admin.register(NewIndicadorProposal)
class NewIndicadorProposalAdmin(admin.ModelAdmin):
    list_display = ("indicator_name", "user", "created_at")
    search_fields = ("indicator_name", "user__username")
    list_filter = ("created_at",)
