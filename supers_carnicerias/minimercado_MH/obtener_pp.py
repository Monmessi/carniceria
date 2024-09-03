import os
import csv  # Importar para manejar CSV
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

def limpiar_precio(precio):
    # Eliminar espacios y convertir a número flotante
    precio_limpio = precio.replace(" ", "").replace(",", ".")
    try:
        return float(precio_limpio)
    except ValueError:
        return None  # O manejar el error de otra manera si es necesario

try:
    with conexion.cursor() as cursor:  # Usar 'conexion' en lugar de 'connection'
        # Insertar en la tabla Supermercados si no existe
        cursor.execute("INSERT IGNORE INTO Supermercados (Nombre_Supermercado) VALUES ('MH minimercado')")
        conexion.commit()

        # Obtener el ID del supermercado recién insertado o existente
        cursor.execute("SELECT ID_Supermercado FROM Supermercados WHERE Nombre_Supermercado='MH minimercado'")
        id_supermercado = cursor.fetchone()[0]

        # Insertar en la tabla Sucursales con los datos proporcionados
        cursor.execute("""
            INSERT IGNORE INTO Sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
            VALUES (%s, 'Av. Recta Martinolli 8024', 'Córdoba Capital', 'Córdoba', 'Argüello')
        """, (id_supermercado,))
        conexion.commit()

        # Obtener el ID de la sucursal recién insertada o existente
        cursor.execute("SELECT ID_Sucursal FROM Sucursales WHERE ID_Supermercado=%s", (id_supermercado,))
        id_sucursal = cursor.fetchone()[0]

        # Leer el archivo CSV generado y agregar los productos a la base de datos
        with open("productos.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                precio_limpio = limpiar_precio(row['Precio'])
                if precio_limpio is not None:
                    cursor.execute(
                        "INSERT INTO Productos (Nombre_Producto, Categoria, ID_Supermercado, Fecha_Carga, Precio) VALUES (%s, %s, %s, CURDATE(), %s)",
                        (row['Producto'], row['Categoría'], id_supermercado, precio_limpio)
                    )
            conexion.commit()

        print("Datos insertados correctamente en la base de datos.")

finally:
    conexion.close()  # Usar 'conexion' en lugar de 'connection'
