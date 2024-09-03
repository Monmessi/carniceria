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
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES (%s)", ("Doble Pechuga",))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Av. Ambrosio Olmos 805,", "Villa Allende", "Córdoba", "Ciudad Universitaria"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {

    "Pechuga": (6700, "Pollo"),
    "Pata Muslo": (2900, "Pollo"),
    "Pata Muslo Deshuesada": (4800, "Pollo"),
    "Milanesas de Pollo": (5200, "Pollo"),
    "Hamburguesas de Pollo": (4400, "Pollo"),
    "Medallones - Patitas": (4500, "Pollo"),
    "Alitas": (2000, "Pollo"),
    "Arrollados": (5500, "Pollo"),
    "Milanesas de Carne": (6600, "Vaca"),  # Asumiendo que se puede considerar en esta categoría
    "Hamburguesa Vegetariana": (0, "Vegetariana")  # Precio no proporcionado en la imagen, ajusta según sea necesario


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
