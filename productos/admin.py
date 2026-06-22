from django.contrib import admin
from .models import Producto, CategoriaProducto, Finca, ProductoFinca, ImagenesProducto, TipoProducto, VariedadProducto

admin.site.register(CategoriaProducto)
admin.site.register(ProductoFinca)
admin.site.register(Finca)
admin.site.register(TipoProducto)
admin.site.register(VariedadProducto)

class ImagenesProductoInline(admin.TabularInline):
    model = ImagenesProducto
    extra = 1
    fields = ('url_imagen', 'es_principal')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_tipo', 'id_variedad', 'precio', 'id_usuario', 'stock')
    list_filter = ('id_tipo', 'id_variedad', 'id_categoria')
    search_fields = ('id_tipo__nombre', 'id_variedad__nombre', 'nombre_producto')
    inlines = [ImagenesProductoInline]