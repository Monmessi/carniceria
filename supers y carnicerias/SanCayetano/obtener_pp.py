import mysql.connector
import pandas as pd

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",  # Cambia esto si tu host es diferente
    user="root",  # Reemplaza con tu nombre de usuario de MySQL
    password="44273842",  # Reemplaza con tu contraseña de MySQL
    database="carnes"
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
