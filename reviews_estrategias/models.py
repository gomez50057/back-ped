from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class CampoReview(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de objeto"
    )
    object_id = models.PositiveIntegerField(
        verbose_name="ID del objeto"
    )
    # Relación genérica al objeto revisado
    content_object = GenericForeignKey('content_type', 'object_id')

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_estrategias',
        verbose_name="Revisor"
    )
    field_name = models.CharField(
        max_length=100,
        verbose_name="Campo revisado",
        help_text="Nombre interno del campo en el modelo"
    )
    is_valid = models.BooleanField(
        verbose_name="¿Aprobado?",
        help_text="Marcar Sí (aprobado) o No (rechazado)"
    )
    justification = models.TextField(
        blank=True,
        verbose_name="Justificación"
    )
    reviewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de revisión"
    )

    class Meta:
        unique_together = (
            'content_type', 'object_id', 'reviewer', 'field_name'
        )
        verbose_name = "Revisión de Campo"
        verbose_name_plural = "Revisiones de Campo"

    def __str__(self):
        status = 'OK' if self.is_valid else 'KO'
        return (
            f"{self.content_type.app_label}.{self.content_type.model} "
            f"(ID={self.object_id}) - {self.field_name}: {status}"
        )
