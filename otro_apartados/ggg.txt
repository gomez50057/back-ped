# otro_apartados/models.py

from django.db import models
from django.contrib.auth.models import User

class Elemento(models.Model):
    envio_final = models.BooleanField(default=False)
    asIs = models.CharField(max_length=255)
    justification = models.TextField()
    page = models.CharField(max_length=10)
    sectionName = models.CharField(max_length=255)
    shouldBe = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='elementos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sectionName} - {self.page}"
