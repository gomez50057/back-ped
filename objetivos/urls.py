from django.urls import path
from .views import ObjetivoSetView, ObjetivoDetailView, UserFeedbackAvanceView
from .views import (
    AllObjetivoSetView,
    AllObjetivoView,
    AllEstrategiaView,
    AllLineaView,
)
from .views import AllFeedbackAvanceView


urlpatterns = [
    path('mis-objetivos/', ObjetivoSetView.as_view(), name='mis-objetivos'),
    path('mis-objetivos/<str:objetivo_id>/', ObjetivoDetailView.as_view(), name='mis-objetivo-detalle'),
    path('feedback-avance/', UserFeedbackAvanceView.as_view(), name='user-feedback-avance'),

    path('objetivo-sets/', AllObjetivoSetView.as_view(), name='all-objetivo-sets'),
    path('objetivos/', AllObjetivoView.as_view(), name='all-objetivos'),
    path('estrategias/', AllEstrategiaView.as_view(), name='all-estrategias'),
    path('lineas/', AllLineaView.as_view(), name='all-lineas'),
    path('feedback-avances-full/', AllFeedbackAvanceView.as_view(), name='all-feedback-avances'),


]
