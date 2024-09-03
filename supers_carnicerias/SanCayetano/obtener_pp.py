import os
import pandas as pd
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

# ID de la sucursal existente donde se quieren insertar los productos
id_sucursal = 13  # Reemplaza con el ID correcto de la sucursal

# Cargar el CSV limpio de productos
df = pd.read_csv('SanCayetano_limpio.csv')

# Iterar sobre cada fila del DataFrame e insertar los productos en la base de datos
for index, row in df.iterrows():
    nombre = row['Nombre']
    precio = float(row['Precio'])  # El precio ya está limpio y convertido a float
    categoria = row['Categoría']

    # Inserción de productos
    cursor.execute("""
        INSERT INTO productos (Nombre_Producto, Precio, Categoria, ID_Supermercado) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, precio, categoria, id_sucursal))

# Confirmar cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Inserción completada exitosamente desde el CSV limpio.")
