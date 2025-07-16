from django.urls import path
from .views import ObjetivoSetView, ObjetivoDetailView, UserFeedbackAvanceView

urlpatterns = [
    path('mis-objetivos/', ObjetivoSetView.as_view(), name='mis-objetivos'),
    path('mis-objetivos/<str:objetivo_id>/', ObjetivoDetailView.as_view(), name='mis-objetivo-detalle'),
    path('feedback-avance/', UserFeedbackAvanceView.as_view(), name='user-feedback-avance'),
]
