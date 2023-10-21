from django.db import models
from django.utils import timezone

class ManejadorImagen(models.Model):
    capacidad_normal = models.IntegerField(default=10)
    capacidad_alta_demanda = models.IntegerField(default=150)
    alta_demanda_horas_inicio = models.TimeField(null=True, blank=True)
    alta_demanda_horas_fin = models.TimeField(null=True, blank=True)

    def __str__(self):
        return "Manejador de Imágenes"

    def esta_en_alta_demanda(self):
        now = timezone.now().time()
        if self.alta_demanda_horas_inicio and self.alta_demanda_horas_fin:
            return self.alta_demanda_horas_inicio <= now <= self.alta_demanda_horas_fin
        return False


