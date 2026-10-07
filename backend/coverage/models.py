from django.db import models

DIAS_SEMANA = [
    ('LUN', 'Lunes'),
    ('MAR', 'Martes'),
    ('MIE', 'Miercoles'),
    ('JUE', 'Jueves'),
    ('VIE', 'Viernes'),
    ('SAB', 'Sabado'),
    ('DOM', 'Domingo'),
]


class Cobertura(models.Model):
    zona = models.CharField(max_length=100, unique=True)
    leadtime_dias = models.PositiveIntegerField(default=1)
    dias_disponibles = models.CharField(
        max_length=40,
        help_text='Codigos de dia separados por coma, ej: LUN,MAR,MIE',
        default='LUN,MAR,MIE,JUE,VIE',
    )
    hora_inicio = models.TimeField(default='08:00')
    hora_fin = models.TimeField(default='18:00')

    class Meta:
        verbose_name = 'Cobertura'
        verbose_name_plural = 'Coberturas'

    def __str__(self):
        return f'{self.zona} (leadtime {self.leadtime_dias}d)'

    def dias_codigos(self):
        return [d.strip().upper() for d in self.dias_disponibles.split(',') if d.strip()]
