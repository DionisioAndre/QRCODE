from django.db import models

class Evento(models.Model):
    id = models.AutoField(primary_key=True)  # Campo id auto-incremental
    morador = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=100)
    data_evento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    local = models.CharField(max_length=255)
    convidado = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.morador} - {self.tipo_evento} em {self.data_evento}"
