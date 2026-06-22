from django.core.management.base import BaseCommand
from productos.models import Producto, TipoProducto, VariedadProducto, CategoriaProducto


class Command(BaseCommand):
    help = 'Crea TipoProducto y VariedadProducto a partir de los productos existentes'

    def handle(self, *args, **options):
        nombres = Producto.objects.values_list(
            'nombre_producto', flat=True
        ).distinct()

        creados = 0
        for nombre in nombres:
            if not nombre or TipoProducto.objects.filter(nombre=nombre).exists():
                continue

            # Buscar una categoría de referencia entre los productos con ese nombre
            ref = Producto.objects.filter(nombre_producto=nombre).first()
            categoria = ref.id_categoria if ref and ref.id_categoria else None
            if not categoria:
                categoria, _ = CategoriaProducto.objects.get_or_create(
                    nombre_categoria='Sin categoría'
                )

            tipo = TipoProducto.objects.create(
                nombre=nombre,
                id_categoria=categoria,
            )

            VariedadProducto.objects.create(
                id_tipo=tipo,
                nombre='Genérica',
            )

            Producto.objects.filter(nombre_producto=nombre).update(id_tipo=tipo)

            creados += 1
            self.stdout.write(f'  Creado TipoProducto: {nombre}')

        self.stdout.write(self.style.SUCCESS(
            f'Backfill completado: {creados} tipos creados'
        ))
