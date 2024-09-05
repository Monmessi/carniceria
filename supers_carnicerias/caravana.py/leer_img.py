import os
import mysql.connector  # Importar para conectar a MySQL
from datetime import datetime  # Importar para manejar fechas
from dotenv import load_dotenv

# Especifica la ruta del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

# Cargar el archivo .env desde la ruta específica
load_dotenv(dotenv_path)

# Obtener las variables de entorno
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')

print(f"Host: {host}")
print(f"User: {user}")
print(f"Password: {password}")
print(f"Database: {database}")

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conexion.cursor()

# Inserta el supermercado 'Caravana'
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES (%s)", ('Caravana',))
conexion.commit()

# Obtiene el ID del supermercado 'Caravana'
cursor.execute("SELECT ID_Supermercado FROM supermercados WHERE Nombre_Supermercado = %s", ('Caravana',))
id_supermercado = cursor.fetchone()[0]

# Inserta la sucursal
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal)
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, 'Rafael Núñez 4328', 'Córdoba Capital', 'Córdoba', 'Cerro de las rosas'))
conexion.commit()

# Diccionarios de productos
productos_vaca = {
    "Porter House": 10698.00,
    "Tomahawk - Prime Rib": 9690.00,
    "Rack Ojo de Bife": 10698.00,
    "Tapa de Bife Ancho": 4781.00,
    "T-Bone": 10055.00,
    "Bife de Chorizo": 10383.00,
    "Ojo de Bife": 10698.00,
    "Lomo": 10698.00,
    "Costilla": 8554.00,
    "Costilla Banderita": 8554.00,
    "Asado": 7053.00,
    "Tapa de Asado": 6196.00,
    "Entraña": 11005.00,
    "Falda Deshuesada": 7546.00,
    "Matambre": 8554.00,
    "Vacío": 8554.00,
    "Bife de Vacio": 8983.00,
    "Medialuna de Vacío": 9326.00,
    "Tapa de Cuadril": 10698.00,
    "Colita de Cuadril": 10484.00,
    "Corazón de Cuadril": 8554.00,
    "Bola de Lomo Feteada": 7053.00,
    "Cuadrada Feteada": 7053.00,
    "Nalga s/ Tapa Feteada": 7696.00
}

productos_cerdo = {
    "BONDIOLA DE CERDO": 7824.62,
    "CARRE DESHUESADO": 8507.70,
    "CHORIZO COLORADO": 6101.33,
    "CHORIZO DE CERDO": 7079.39,
    "MORCILLA VASCA": 5573.48,
    "VACÍO DE CERDO": 6815.46,
    "PECHITO DE CERDO": 6520.49,
    "SOLOMILLO DE CERDO": 7886.72,
    "CHURRASCO DE BONDIOLA": 7824.62,
    "MATAMBRE DE CERDO": 9547.86,
    "COSTILLA DE CERDO": 6520.49,
    "TAPITA DE CERDO": 9026.35,
    "ENTRECOTTE DE CERDO": 4910.55,
    "MORCILLA CLASICA": 4052.02,
    "CARRÉ DE CERDO": 4041.16
}

productos_cordero = {
    "CHULETA CORDERO": 10684.06,
    "GIGOT CORDERO": 10684.06,
    "MOLIDA X KG CORDERO": 12356.92,
    "PALETA CORDERO": 9888.28,
    "PICAÑA CORDERO": 12477.73,
    "RACK CORDERO": 13022.78,
    "RIBS CORDERO": 9616.95,
    "RIÑÓN CORDERO": 8647.06,
    "T-BONE CORDERO": 12558.37
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
insertar_productos(productos_vaca, 'Vaca')
insertar_productos(productos_cerdo, 'Cerdo')
insertar_productos(productos_cordero, 'Cordero')

# Cierra la conexión
cursor.close()
conexion.close()
