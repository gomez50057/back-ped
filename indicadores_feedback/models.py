from django.db import models
from django.contrib.auth import get_user_model

class IndicadoresFeedback(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='indicadores_feedback')
    envio_final = models.BooleanField(default=False)
    feedback = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Retroalimentación de Indicadores"
        verbose_name_plural = "Retroalimentaciones de Indicadores"

    def __str__(self):
        return f"Feedback de {self.user} (final: {self.envio_final})"
