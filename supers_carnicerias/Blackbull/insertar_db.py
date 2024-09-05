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
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
df = pd.read_csv('blackbull_with_category_complete.csv')
cursor = conn.cursor()

# Insertar el supermercado en la tabla 'supermercados'
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES ('Blackbull')")
conn.commit()

# Obtener el ID del supermercado recién insertado
cursor.execute("SELECT LAST_INSERT_ID()")
id_supermercado = cursor.fetchone()[0]

# Insertar la sucursal en la tabla 'sucursales'
direccion = 'Av. Gauss 5780'
departamento = 'Córdoba Capital'
provincia = 'Córdoba'
sucursal = 'Villa Belgrano'

cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal)
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, direccion, departamento, provincia, sucursal))
conn.commit()

# Obtener el ID de la sucursal recién insertada
cursor.execute("SELECT LAST_INSERT_ID()")
id_sucursal = cursor.fetchone()[0]

# Insertar productos en la tabla 'productos'
for index, row in df.iterrows():
    nombre = row['Nombre']
    precio = row['Precio']
    categoria = row['Categoría']

    cursor.execute("""
        INSERT INTO productos (ID_Supermercado, Nombre_Producto, Precio, Categoria)
        VALUES (%s, %s, %s, %s)
    """, (id_sucursal, nombre, precio, categoria))

# Confirmar todos los cambios
conn.commit()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

print("Datos insertados correctamente en la base de datos.")
