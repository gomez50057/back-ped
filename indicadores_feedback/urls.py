from django.urls import path
from .views import IndicadoresFeedbackUserView

urlpatterns = [
    path('feedback/', IndicadoresFeedbackUserView.as_view(), name='indicadores-feedback'),
]
