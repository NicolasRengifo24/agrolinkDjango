from django import forms
from productos.models import Producto, ImagenesProducto, ProductoFinca, CategoriaProducto, Finca
from usuarios.models import Productor


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model =Producto
        fields = [
            'id_usuario',
            'id_categoria',
            'nombre_producto',
            'descripcion_producto',
            'precio',
            'stock',
            'peso_kg',
        ]
        
        widgets={
            'id_usuario': forms.Select(attrs={'id': 'id_usuario', 'name':'id_usuario',}),
            
            'id_categoria': forms.Select(attrs={
                'id': 'categoria', 'name': 'categoria',
            }),
            'nombre_producto': forms.TextInput(attrs={
                'id': 'nombre_producto', 'placeholder': 'Ej: Café especial tostado',
            }),
            'descripcion_producto': forms.Textarea(attrs={
                'id': 'descripcion', 'placeholder': 'Describe el producto...',
                'rows': 4,
            }),
            'precio': forms.NumberInput(attrs={
                'id': 'precio', 'placeholder': '0.00', 'min': '0', 'step': '0.01',
            }),
            'stock': forms.NumberInput(attrs={
                'id': 'stock', 'placeholder': '0', 'min': '0',
            }),
            'peso_kg': forms.NumberInput(attrs={
                'id': 'peso_kg', 'placeholder': '0.00', 'min': '0', 'step': '0.01',
            }),
        }
        
        labels = {
            'id_usuario'          : 'Productor',
            'id_categoria'        : 'Categoría',
            'nombre_producto'     : 'Nombre del producto',
            'descripcion_producto': 'Descripción',
            'precio'              : 'Precio unitario (COP)',
            'stock'               : 'Stock disponible',
            'peso_kg'             : 'Peso por unidad (kg)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo muestra productores activos (ajusta el filtro a tu modelo)
        self.fields['id_usuario'].queryset = Productor.objects.all()
        self.fields['id_categoria'].queryset = CategoriaProducto.objects.all()
        # Campos opcionales según el modelo
        self.fields['descripcion_producto'].required = False
        self.fields['precio'].required  = False
        self.fields['stock'].required   = False
        self.fields['peso_kg'].required = False


class ImagenPrincipalForm(forms.ModelForm):
    """
    Subida de la imagen principal del producto.
    Se guarda en ImagenesProducto con es_principal=1.
    """

    class Meta:
        model  = ImagenesProducto
        fields = ['url_imagen']
        widgets = {
            'url_imagen': forms.ClearableFileInput(attrs={
                'id': 'imagen_producto', 'name': 'imagen_producto',
                'accept': 'image/*',
            }),
        }
        labels = {
            'url_imagen': 'Imagen del producto',
        }


class ProductoFincaForm(forms.ModelForm):
    """
    Relaciona el producto con una finca y guarda
    cantidad de producción y fecha de cosecha.
    """

    class Meta:
        model  = ProductoFinca
        fields = ['id_finca', 'cantidad_produccion', 'fecha_cosecha']
        widgets = {
            'id_finca': forms.RadioSelect(attrs={
                'name': 'finca',
            }),
            'cantidad_produccion': forms.NumberInput(attrs={
                'id': 'cantidad_produccion', 'placeholder': '0.00',
                'min': '0', 'step': '0.01',
            }),
            'fecha_cosecha': forms.DateInput(attrs={
                'id': 'fecha_cosecha', 'type': 'date',
            }),
        }
        labels = {
            'id_finca'           : 'Finca del productor',
            'cantidad_produccion': 'Cantidad de producción',
            'fecha_cosecha'      : 'Fecha de cosecha',
        }
        
    def __init__(self, *args, productor=None, validate_finca=False, **kwargs):
        super().__init__(*args, **kwargs)  # ← validate_finca ya no llega aquí
        if productor:
            self.fields['id_finca'].queryset = Finca.objects.filter(id_usuario=productor)
        elif validate_finca:
            self.fields['id_finca'].queryset = Finca.objects.all()
        else:
            self.fields['id_finca'].queryset = Finca.objects.none()
        self.fields['cantidad_produccion'].required = False
        self.fields['fecha_cosecha'].required       = False    

    
        
        