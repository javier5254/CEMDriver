import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from services.indicadores import calcular_indicadores


class Command(BaseCommand):
    help = (
        'Exporta a JSON los indicadores operativos (los mismos de GET /api/indicadores/), '
        'calculados sobre la base de datos actual.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--dias', type=int, default=30, help='Tamaño del periodo en días (1 a 365). Por defecto 30.')
        parser.add_argument('--zona', default=None, help='Texto exacto de la zona para filtrar (opcional).')
        parser.add_argument(
            '--salida', default=None,
            help='Ruta del archivo JSON a escribir. Si se omite, imprime el JSON por la salida estándar.',
        )

    def handle(self, *args, **options):
        dias = options['dias']
        if not 1 <= dias <= 365:
            raise CommandError('--dias debe ser un número entero entre 1 y 365.')

        datos = calcular_indicadores(dias=dias, zona=options['zona'] or None)
        texto = json.dumps(datos, ensure_ascii=False, indent=2)

        if not options['salida']:
            self.stdout.write(texto)
            return

        destino = Path(options['salida'])
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto + '\n', encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(
            f'Indicadores exportados a {destino} ({datos["resumen"]["servicios_total"]} servicios, {dias} días).'
        ))
