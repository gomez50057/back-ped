# otro_apartados/admin.py

from django.contrib import admin
from .models import Elemento

@admin.register(Elemento)
class ElementoAdmin(admin.ModelAdmin):
    list_display = ('id', 'sectionName', 'page', 'user', 'fecha_creacion')
    search_fields = ('sectionName', 'asIs', 'shouldBe', 'user__username')
    list_filter = ('fecha_creacion', 'user')
