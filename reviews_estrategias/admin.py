# reviews_estrategias/admin.py
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import CampoReview

class CampoReviewInline(GenericTabularInline):
    model = CampoReview
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 0
    readonly_fields = ("reviewed_at",)
    fields = ("reviewer", "field_name", "is_valid", "justification", "reviewed_at")

admin.site.register(CampoReview)  # Para gestión directa, si lo deseas
