import pandas as pd
import mysql.connector

# Leer el archivo CSV
df = pd.read_csv('productos_carnes_limpio.csv')

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host='localhost',  # Cambia esto si tu base de datos no está en localhost
    user='root',  # Tu usuario de MySQL
    password='44273842',  # Tu contraseña de MySQL
    database='carnes'  # Nombre de la base de datos
)

cursor = conn.cursor()

# Insertar productos en la tabla 'productos'
for index, row in df.iterrows():
    nombre = row['Nombre']
    precio = row['Precio']
    categoria = row['Categoría']

    cursor.execute("""
        INSERT INTO productos (ID_Supermercado, Nombre_Producto, Precio, Categoria)
        VALUES (%s, %s, %s, %s)
    """, (None, nombre, precio, categoria))

# Confirmar todos los cambios
conn.commit()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

print("Datos insertados correctamente en la base de datos.")
