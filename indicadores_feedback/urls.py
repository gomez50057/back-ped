from django.urls import path
from .views import IndicadoresFeedbackUserView
from .views import IndicadoresFeedbackListAPIViewFull


urlpatterns = [
    path('feedback/', IndicadoresFeedbackUserView.as_view(), name='indicadores-feedback'),
    path('feedback-full/', IndicadoresFeedbackListAPIViewFull.as_view(), name='indicadores-feedback-list-full'),

]
