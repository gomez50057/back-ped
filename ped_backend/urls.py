from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/plataforma/', include('plataforma.urls')),
    path('api/objetivos/', include('objetivos.urls')),
    path('api/otro_apartados/', include('otro_apartados.urls')),
    path('api/indicadores/', include('indicadores_eleccion.urls')),
    path('api/indicadores-feedback/', include('indicadores_feedback.urls')),  
    path('api/indicador/', include('new_indicador.urls')),
    path('api/', include('reviews_estrategias.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)