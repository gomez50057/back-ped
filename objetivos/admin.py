from django.contrib import admin
from .models import ObjetivoSet, Objetivo, Estrategia, Linea, FeedbackAvance

# Inlines jerárquicos
class LineaInline(admin.TabularInline):
    model = Linea
    extra = 1

class EstrategiaInline(admin.TabularInline):
    model = Estrategia
    extra = 1

class ObjetivoInline(admin.TabularInline):
    model = Objetivo
    extra = 1

@admin.register(ObjetivoSet)
class ObjetivoSetAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_objetivos', 'creado', 'actualizado')
    search_fields = ('user__username',)
    inlines = [ObjetivoInline]

    def get_objetivos(self, obj):
        return ", ".join(o.nombre for o in obj.objetivos.all())
    get_objetivos.short_description = "Objetivos"

@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'set')
    list_filter = ('set',)
    search_fields = ('id', 'nombre')
    inlines = [EstrategiaInline]

@admin.register(Estrategia)
class EstrategiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'objetivo')
    list_filter = ('objetivo',)
    search_fields = ('id', 'nombre')
    inlines = [LineaInline]

@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'estrategia')
    list_filter = ('estrategia',)
    search_fields = ('id', 'text')



@admin.register(FeedbackAvance)
class FeedbackAvanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'clave', 'acuerdo', 'envio_final', 'created']
    search_fields = ['user__username', 'clave']
    readonly_fields = ['created', 'updated']
    list_filter = ['acuerdo', 'envio_final']

