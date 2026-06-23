from django.core.management.base import BaseCommand
from productos.models import TipoProducto, VariedadProducto, CategoriaProducto


VARIEDADES_POR_TIPO = {
    # ==========================================
    # TUBÉRCULOS Y RAÍCES
    # ==========================================
    "Papa": [
        "Criolla amarilla", "Pastusa", "Sabanera", "Superior",
        "Tuquerreña", "R12", "Roja", "Parda", "Tocarré",
        "Betina", "Única", "Capiro",
    ],
    "Cubio": [
        "Blanco", "Amarillo", "Rojo", "Negro", "Morado",
    ],
    "Arracacha": [
        "Amarilla", "Blanca", "Morada", "Roja", "Rayada",
    ],
    "Hibia": [
        "Blanca", "Amarilla", "Morada", "Roja", "Negra",
    ],
    "Ruba": [
        "Blanca", "Amarilla", "Roja", "Morada", "Negra",
    ],
    "Batata": [
        "Amarilla", "Morada", "Blanca", "Naranja", "Criolla",
    ],

    # ==========================================
    # HORTALIZAS Y VERDURAS DE CLIMA FRÍO
    # ==========================================
    "Lechuga": [
        "Crespa", "Romana", "Iceberg", "Lollo Rosso",
        "Batavia", "Orgánica", "Baby",
    ],
    "Repollo": [
        "Blanco", "Morado", "Saboyano", "Milan", "Corazón de buey",
    ],
    "Coliflor": [
        "Blanca", "Morada", "Verde", "Naranja", "Amarilla",
    ],
    "Brócoli": [
        "Verde", "Morado", "Baby", "Romanesco", "Orgánico",
    ],
    "Espinaca": [
        "Santa Fe", "Viroflay", "Baby", "Crespa", "Redonda",
    ],
    "Acelga": [
        "Verde", "Penca blanca", "Penca roja", "Arcoíris", "Baby",
    ],
    "Apio": [
        "Verde", "Dorado", "Rojo", "Tallo grueso", "Baby",
    ],
    "Zanahoria": [
        "Naranja", "Morada", "Amarilla", "Blanca", "Baby",
    ],
    "Remolacha": [
        "Roja", "Amarilla", "Blanca", "Rayada", "Baby",
    ],
    "Habichuela": [
        "Verde", "Roja", "Criolla", "Larga", "Baby",
    ],
    "Arveja": [
        "Verde", "Partida", "Tirabeque", "Dulce", "Criolla",
    ],
    "Haba": [
        "Verde", "Blanca", "Roja", "Criolla", "Pelada",
    ],
    "Ajo": [
        "Blanco", "Morado", "Criollo", "Chino", "Elefante",
    ],
    "Cebolla cabezona": [
        "Roja", "Blanca", "Amarilla", "Morada", "Dulce",
    ],
    "Cebolla junca": [
        "Junca", "Larga", "Cebollín", "Puerro", "Criolla",
    ],
    "Pepino": [
        "Cojín", "Largo", "Inglés", "Pickle", "Armenio",
    ],
    "Calabacín": [
        "Verde", "Amarillo", "Redondo", "Raya", "Baby",
    ],
    "Maíz": [
        "Blanco", "Amarillo", "Morado", "Criollo", "Mazorca tierna",
    ],

    # ==========================================
    # FRUTAS DE CLIMA FRÍO
    # ==========================================
    "Fresa": [
        "Albión", "Monterey", "San Andreas", "Camarosa",
        "Ventana", "Sabrosa", "Cristalina", "Diamante",
    ],
    "Mora": [
        "Castilla", "Brasilera", "Sansón", "Negra", "Roja",
    ],
    "Uchuva": [
        "Dorada", "Naranja", "Colombiana", "Keniana", "Gigante",
    ],
    "Curuba": [
        "Verde", "Amarilla", "Roja", "Dulce", "Ácida",
    ],
    "Feijoa": [
        "Coolidge", "Apollo", "Gemini", "Mammoth", "Unique",
    ],
    "Durazno": [
        "Diamante", "Rubro", "Jarillo", "Criollo", "Dorado",
    ],
    "Manzana": [
        "Red Delicious", "Granny Smith", "Fuji", "Gala",
        "Golden", "Anna", "Criolla",
    ],
    "Pera": [
        "Williams", "Abate Fétel", "Conference", "Packham", "Criolla",
    ],
    "Ciruela": [
        "Roja", "Amarilla", "Horcones", "Criolla", "Dulce",
    ],
    "Tomate de árbol": [
        "Rojo", "Amarillo", "Dulce", "Ácido", "Criollo",
    ],
    "Gulupa": [
        "Morada", "Naranja", "Dulce", "Ácida", "Gigante",
    ],
    "Frambuesa": [
        "Roja", "Negra", "Dorada", "Dulce", "Silvestre",
    ],
    "Arándano": [
        "Bluecrop", "Duke", "Elliot", "Legacy", "Chandler",
    ],
    "Cereza": [
        "Criolla", "Dulce", "Ácida", "Roja", "Negra",
    ],
    "Granadilla": [
        "Dulce", "Ácida", "Gigante", "Criolla", "Orgánica",
    ],

    # ==========================================
    # CEREALES Y GRANOS
    # ==========================================
    "Arroz": [
        "Blanco", "Integral", "Paddy", "Parbolizado",
        "Rojal", "Cachaza",
    ],
    "Trigo": [
        "Sabanero", "Criollo", "Duro", "Blando", "Orgánico",
    ],
    "Cebada": [
        "Forrajera", "Cervecera", "Criolla", "Maltera", "Sabanera",
    ],
    "Avena": [
        "En grano", "En hojuelas", "Forrajera", "Criolla", "Orgánica",
    ],
    "Quinua": [
        "Real", "Blanca", "Roja", "Negra", "Orgánica",
    ],
    "Amaranto": [
        "Rojo", "Verde", "Dorado", "Criollo", "Orgánico",
    ],

    # ==========================================
    # LÁCTEOS Y DERIVADOS
    # ==========================================
    "Leche": [
        "Entera", "Semidescremada", "Descremada", "Orgánica",
        "Criolla", "Pasteurizada",
    ],
    "Queso": [
        "Campesino", "Doble crema", "Cuajada", "Mozzarella",
        "Parmesano", "Ricotta", "Quesillo", "Costeño",
    ],
    "Yogur": [
        "Natural", "Griego", "De fresa", "De mora",
        "De uchuva", "Arequipe",
    ],
    "Arequipe": [
        "Tradicional", "Ligero", "Artesanal", "Con nueces",
        "Con café", "Con coco",
    ],
    "Mantequilla": [
        "Salada", "Sin sal", "Orgánica", "Criolla", "Clarificada",
    ],

    # ==========================================
    # PROCESADOS Y ARTESANALES
    # ==========================================
    "Miel": [
        "Multifloral", "De eucalipto", "De cítricos",
        "Orgánica", "De abejorro", "De acacia",
    ],
    "Mermelada": [
        "De fresa", "De mora", "De uchuva", "De durazno",
        "De feijoa", "Light",
    ],
    "Almojábana": [
        "Tradicional", "De maíz", "De yuca", "Dulce",
        "Salada", "Sin gluten",
    ],
    "Masato": [
        "Arroz", "Maíz", "Tradicional", "Dulce", "Fermentado",
    ],
    "Panela": [
        "Blanca", "Morena", "Orgánica", "Dulce", "En polvo",
    ],
    "Café": [
        "Arábica", "Robusta", "Caturra", "Castillo",
        "Colombia", "Supremo", "Excelso", "Orgánico",
    ],
    "Chocolate": [
        "Amargo", "Dulce", "De leche", "Blanco",
        "Artesanal", "Orgánico",
    ],

    # ==========================================
    # HIERBAS AROMÁTICAS Y MEDICINALES
    # ==========================================
    "Cilantro": [
        "Común", "Sabanero", "Europeo", "Thai", "Vietnamita",
    ],
    "Perejil": [
        "Liso", "Crespo", "Italiano", "Chino", "Orgánico",
    ],
    "Hierbabuena": [
        "Común", "Menta", "Piperita", "Tradicional", "Silvestre",
    ],
    "Tomillo": [
        "Común", "Limón", "Naranja", "Criollo", "Seco",
    ],
    "Romero": [
        "Común", "Tuscan blue", "Prostratus", "Criollo", "Seco",
    ],

    # ==========================================
    # FLORES DE CORTE (Sabana de Bogotá)
    # ==========================================
    "Rosa": [
        "Roja", "Blanca", "Amarilla", "Naranja",
        "Fucsia", "Vendela", "Equator", "Freedom",
    ],
    "Clavel": [
        "Rojo", "Blanco", "Rosado", "Amarillo",
        "Naranja", "Miniatura",
    ],
    "Crisantemo": [
        "Amarillo", "Blanco", "Morado", "Rosado",
        "Pompón", "Spider",
    ],
    "Gerbera": [
        "Roja", "Naranja", "Amarilla", "Rosada",
        "Blanca", "Doble",
    ],
    "Astromelia": [
        "Roja", "Blanca", "Rosada", "Naranja",
        "Morada", "Amarilla",
    ],
    "Lirio": [
        "Blanco", "Rosado", "Morado", "Amarillo",
        "Naranja", "Tigre",
    ],
}

# Mapa de normalización para nombres existentes mal formateados
NORMALIZAR_NOMBRES = {
    "Papa R12": "Papa",
    "Lechuga Crespa": "Lechuga",
    "manzana": "Manzana",
    "ARROZ": "Arroz",
    "cilantro": "Cilantro",
    "Miel De Abeja": "Miel",
}

# Categorías sugeridas para nuevos tipos que no existen
CATEGORIA_POR_TIPO = {
    "Papa": "Tubérculos",
    "Cubio": "Tubérculos",
    "Arracacha": "Tubérculos",
    "Hibia": "Tubérculos",
    "Ruba": "Tubérculos",
    "Batata": "Tubérculos",
    "Lechuga": "Hortalizas",
    "Repollo": "Hortalizas",
    "Coliflor": "Hortalizas",
    "Brócoli": "Hortalizas",
    "Espinaca": "Hortalizas",
    "Acelga": "Hortalizas",
    "Apio": "Hortalizas",
    "Zanahoria": "Hortalizas",
    "Remolacha": "Hortalizas",
    "Habichuela": "Hortalizas",
    "Arveja": "Hortalizas",
    "Haba": "Hortalizas",
    "Ajo": "Hortalizas",
    "Cebolla cabezona": "Hortalizas",
    "Cebolla junca": "Hortalizas",
    "Pepino": "Hortalizas",
    "Calabacín": "Hortalizas",
    "Maíz": "Cereales",
    "Fresa": "Frutas",
    "Mora": "Frutas",
    "Uchuva": "Frutas",
    "Curuba": "Frutas",
    "Feijoa": "Frutas",
    "Durazno": "Frutas",
    "Manzana": "Frutas",
    "Pera": "Frutas",
    "Ciruela": "Frutas",
    "Tomate de árbol": "Frutas",
    "Gulupa": "Frutas",
    "Frambuesa": "Frutas",
    "Arándano": "Frutas",
    "Cereza": "Frutas",
    "Granadilla": "Frutas",
    "Arroz": "Cereales",
    "Trigo": "Cereales",
    "Cebada": "Cereales",
    "Avena": "Cereales",
    "Quinua": "Cereales",
    "Amaranto": "Cereales",
    "Leche": "Lácteos",
    "Queso": "Lácteos",
    "Yogurt": "Lácteos",
    "Arequipe": "Lácteos",
    "Mantequilla": "Lácteos",
    "Miel": "Procesados",
    "Mermelada": "Procesados",
    "Almojábana": "Procesados",
    "Masato": "Procesados",
    "Panela": "Procesados",
    "Café": "Procesados",
    "Chocolate": "Procesados",
    "Cilantro": "Hierbas",
    "Perejil": "Hierbas",
    "Hierbabuena": "Hierbas",
    "Tomillo": "Hierbas",
    "Romero": "Hierbas",
    "Rosa": "Flores",
    "Clavel": "Flores",
    "Crisantemo": "Flores",
    "Gerbera": "Flores",
    "Astromelia": "Flores",
    "Lirio": "Flores",
}


class Command(BaseCommand):
    help = (
        'Siembra variedades predefinidas para todos los TipoProducto. '
        'Normaliza nombres existentes y crea tipos faltantes.'
    )

    def _get_o_categoria(self, nombre_tipo):
        cat_nombre = CATEGORIA_POR_TIPO.get(nombre_tipo, "Sin categoría")
        cat, _ = CategoriaProducto.objects.get_or_create(
            nombre_categoria=cat_nombre
        )
        return cat

    def handle(self, *args, **options):
        # ==========================================
        # PASO 1: Normalizar nombres existentes
        # ==========================================
        self.stdout.write("Paso 1/3: Normalizando nombres existentes...")
        for viejo, nuevo in NORMALIZAR_NOMBRES.items():
            tipo = TipoProducto.objects.filter(nombre__iexact=viejo).first()
            if tipo and tipo.nombre != nuevo:
                old = tipo.nombre
                tipo.nombre = nuevo
                tipo.save()
                self.stdout.write(f'  Renombrado: "{old}" -> "{nuevo}"')

        # ==========================================
        # PASO 2: Crear tipos faltantes
        # ==========================================
        self.stdout.write("Paso 2/3: Creando tipos faltantes...")
        creados = 0
        for nombre_tipo in VARIEDADES_POR_TIPO:
            tipo, created = TipoProducto.objects.get_or_create(
                nombre=nombre_tipo,
                defaults={
                    'id_categoria': self._get_o_categoria(nombre_tipo),
                },
            )
            if created:
                creados += 1
                self.stdout.write(f'  Creado TipoProducto: "{nombre_tipo}"')
        self.stdout.write(f'  {creados} tipos nuevos creados.')

        # ==========================================
        # PASO 3: Sembrar variedades
        # ==========================================
        self.stdout.write("Paso 3/3: Sembrando variedades...")
        total_variedades = 0
        for nombre_tipo, variedades in VARIEDADES_POR_TIPO.items():
            tipo = TipoProducto.objects.filter(nombre=nombre_tipo).first()
            if not tipo:
                self.stdout.write(
                    self.style.WARNING(
                        f'  Tipo "{nombre_tipo}" no encontrado, se omite'
                    )
                )
                continue

            for nombre_var in variedades:
                var, created = VariedadProducto.objects.get_or_create(
                    id_tipo=tipo,
                    nombre=nombre_var,
                )
                if created:
                    total_variedades += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nSeed completado: {total_variedades} variedades sembradas '
            f'en {len(VARIEDADES_POR_TIPO)} tipos de producto.'
        ))
