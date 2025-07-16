from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ObjetivoSet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='objetivo_set')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Objetivos de {self.user.username}'

class Objetivo(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    nombre = models.CharField(max_length=256)
    set = models.ForeignKey(ObjetivoSet, related_name='objetivos', on_delete=models.CASCADE)

class Estrategia(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    nombre = models.CharField(max_length=256)
    objetivo = models.ForeignKey(Objetivo, related_name='estrategias', on_delete=models.CASCADE)

class Linea(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    text = models.TextField()
    estrategia = models.ForeignKey(Estrategia, related_name='lineas', on_delete=models.CASCADE)


class FeedbackAvance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_avances")
    clave = models.CharField(
        max_length=120,
        help_text='Identificador de la sección, ej: EG01-propuesta-1_1_EG01'
    )
    acuerdo = models.CharField(
        max_length=10,
        choices=[('yes', 'Sí'), ('no', 'No')]
    )
    comoDecir = models.TextField()
    justificacion = models.TextField()
    envio_final = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'clave')  # Un feedback por usuario/sección
        verbose_name = "Feedback de Avance"
        verbose_name_plural = "Feedbacks de Avance"

    def __str__(self):
        return f"{self.user.username} - {self.clave}"