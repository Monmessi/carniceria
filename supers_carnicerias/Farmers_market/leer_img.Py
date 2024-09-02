import pymysql
from datetime import datetime


'''''este codigo esta hecho a partir de diccionarios que me pasaron desde una imagen, para luego cargarlo directamente
en la base de datos'''

# Datos de conexión a la base de datos
conexion = pymysql.connect(
    host="localhost",
    user="root",
    password="44273842",
    database="carnes",
    charset="utf8mb4"
)

cursor = conexion.cursor()

# Inserta el supermercado 'Farmers Market'
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES (%s)", ('Farmers Market',))
conexion.commit()

# Obtiene el ID del supermercado 'Farmers Market'
cursor.execute("SELECT ID_Supermercado FROM supermercados WHERE Nombre_Supermercado = %s", ('Farmers Market',))
id_supermercado = cursor.fetchone()[0]

# Inserta la sucursal
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal)
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, 'Av. Carlos F. Gauss 5700', 'Córdoba Capital', 'Córdoba', 'Villa Belgrano'))
conexion.commit()

# Diccionarios de productos
productos_farmer_1 = {
    "Mollejas": 10360,
    "Molida Intermedia": 6600,
    "Molida Especial": 9320,
    "Milanesas de Carne": 9650,
    "Milanesas de Peceto": 9650,
    "Matambre": 9890,
    "Marucha": 6600,
    "Lomo": 10470,
    "Falda Deshuesada": 8390,
    "Falda": 7220,
    "Entrecot": 9560,
    "Entraña": 11980,
    "Cuadril": 9950,
    "Costilla": 9770,
    "Costeleta Ancha": 9450,
    "Colita de Cuadril": 9950,
    "Bola de Lomo": 9660,
    "Bocado Fino": 7170,
    "Bocado Ancho": 7170,
    "Bife de Chorizo": 9870,
    "Arañita": 9420,
    "Aguja Parrillera": 6470,
    "Chinchulin": 3800,
    "Riñones": 4060
}

productos_farmer_2 = {
    "Matambre De Cerdo": 13020,
    "Bondiola": 11850,
    "Salchicha Fina": 13520,
    "Solomillo de Cerdo": 11840,
    "Chorizo de Cerdo": 10530,
    "Chorizo Colorado": 11590,
    "Costeleta de Cerdo": 6300,
    "Costilla de Cerdo": 7050,
    "Pechito de Cerdo": 7050,
    "Pollo Entero": 4550,
    "Pechuga Deshuesada": 7800,
    "Pechuga": 7600,
    "Pata Muslo Deshuesada": 6320,
    "Pata Muslo": 3890,
    "Milanesas de Pollo": 8590,
    "Bifes de Pechuga": 8100,
    "Torguita": 6670,
    "Vacío": 9890,
    "Tapa de Nalga": 8300,
    "Tapa de Asado": 9250,
    "Peceto": 9990,
    "Palomita": 6470,
    "Paleta": 7470,
    "Osobuco": 6470,
    "Ojo de Bife": 9930,
    "Nalga": 9850,
    "Morcilla Vasca": 9900,
    "Morcilla Grande": 6320,
    "Morcilla Bombon": 6320,
    "Tapa de Cuadril": 9950
}

def insertar_productos(productos, categoria):
    fecha_carga = datetime.now().strftime('%Y-%m-%d')
    for producto, precio in productos.items():
        cursor.execute("""
            INSERT INTO productos (Nombre_Producto, Categoria, Fecha_Carga, Precio, ID_Supermercado)
            VALUES (%s, %s, %s, %s, %s)
        """, (producto, categoria, fecha_carga, precio, id_supermercado))
    conexion.commit()

# Inserta los productos de cada categoría
insertar_productos(productos_farmer_1, 'Vaca')
insertar_productos(productos_farmer_2, 'Cerdo')

# Cierra la conexión
cursor.close()
conexion.close()
