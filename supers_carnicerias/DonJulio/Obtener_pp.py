import os
import mysql.connector  # Importar para conectar a MySQL
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

# Inserción del supermercado "Los Amigos"
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado, Contacto, Pagina_web) VALUES (%s, %s, %s)", ("Don Julio",5491141610835, "Si"))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Gurruchaga 2050", "Córdoba Capital", "Córdoba", "LaMadrid"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {
  "Vacio": (29100.00, "Piezas Enteras"),
    "Asado del centro - Costillar": (90900.00, "Piezas Enteras"),
    "Lomo": (55100.00, "Piezas Enteras"),
    "Vacio ancho": (44100.00, "Piezas Enteras"),
    "Peceto": (24700.00, "Piezas Enteras"),
    "Matambre": (22950.00, "Piezas Enteras"),
    "Ojo de bife": (11040.00, "Vaca"),
    "Bife ancho": (13900.00, "Vaca"),
    "Bife angosto": (12680.00, "Vaca"),
    "Churrasquito de cerdo": (7350.00, "Vaca"),
    "Brochtta": (18950.00, "Vaca"),
    "Asado": (18760.00, "Cortes Con Hueso"),
    "Entrecot": (27300.00, "Cortes Con Hueso"),
    "T-bone": (26100.00, "Cortes Con Hueso"),
    "Chorizo casero": (2675.00, "Cerdo"),
    "Morcilla": (1400.00, "Cerdo"),
    "Chorizo Valles Calchaquies": (5220.00, "Cerdo"),
    "Salchicha Parrillera": (2350.00, "Cerdo"),
    "Morcilla Criolla": (2900.00, "Cerdo"),
    "Mollejas": (8400.00, "Achuras"),
    "Chinchulin": (2000.00, "Achuras"),
    "Riñon": (4800.00, "Achuras"),
    "Provoleta": (3300.00, "Queso"),
    "Provoleta de Cabra": (3800.00, "Queso"),
    "SELECCIÓN FIN DE SEMANA": (45600.00, "Selecciones de Don Julio"),
    "SELECCIÓN DE SEMANA": (24800.00, "Selecciones de Don Julio")
}

# Inserción de productos
for nombre, (precio, categoria) in precios_carnes.items():
    cursor.execute("""
        INSERT INTO productos (Nombre_Producto, Precio, Categoria, ID_Supermercado) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, precio, categoria, id_sucursal))

# Confirmar cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Inserción completada exitosamente.")
