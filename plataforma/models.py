from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

# Regex: EG01, EG02, ..., ET01, ET02, etc.
CODE_VALIDATOR = RegexValidator(
    regex=r'^(EG|ET)\d{2}$',
    message='El código debe tener el formato EG01, EG02, ET01, ET02, etc.'
)

class StrategicAxis(models.Model):
    code = models.CharField(
        'Clave del Eje',
        max_length=10,
        unique=True,
        validators=[CODE_VALIDATOR],
        help_text='Formato: EG01, ET02, etc.'
    )
    name = models.CharField('Nombre del Eje', max_length=120)

    class Meta:
        verbose_name = 'Eje Estratégico'
        verbose_name_plural = 'Ejes Estratégicos'

    def __str__(self):
        return f"{self.code} - {self.name}"

class UserAxisSelection(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Usuario')
    selected_axes = models.ManyToManyField(StrategicAxis, verbose_name='Ejes Seleccionados')
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Selección de Ejes del Usuario'
        verbose_name_plural = 'Selecciones de Ejes de Usuarios'
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_axis_selection')
        ]

    def __str__(self):
        return f"Selección de ejes de {self.user.username}"

