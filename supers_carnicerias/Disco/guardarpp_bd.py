import pandas as pd
import mysql.connector

# Leer el CSV limpio
df = pd.read_csv('cac_sin_duplicados.csv')

# Convertir la columna 'Precio' a tipo string
df['Precio'] = df['Precio'].astype(str)

# Limpiar los datos de la columna 'Precio' eliminando los puntos
df['Precio'] = df['Precio'].str.replace('.', '', regex=False)

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host='localhost',  # Cambia esto si tu base de datos no está en el localhost
    user='root',  # Reemplaza con tu nombre de usuario de MySQL
    password='44273842',  # Reemplaza con tu contraseña de MySQL
    database='carnes'  # Nombre de la base de datos
)

cursor = conexion.cursor()

# Obtener el ID del supermercado "Disco"
cursor.execute("SELECT ID_Supermercado FROM Supermercados WHERE Nombre_Supermercado = %s", ("Disco",))
id_supermercado = cursor.fetchone()[0]  # Leer el resultado inmediatamente

# Obtener el ID de la sucursal correspondiente
cursor.execute("SELECT ID_Sucursal FROM Sucursales WHERE Direccion = %s", ("Av. Rafael Núñez 4630",))
id_sucursal = cursor.fetchone()[0]  # Leer el resultado inmediatamente

# Insertar los datos en la tabla 'Productos'
for _, row in df.iterrows():
    sql = """
    INSERT INTO Productos (Nombre_Producto, Categoria, Fecha_Carga, Precio, Descuento, ID_Supermercado)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (row['Producto'], None, '2024-08-28', row['Precio'], 0, id_supermercado)  # Ajusta los valores según sea necesario

    cursor.execute(sql, valores)

# Confirmar los cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Datos guardados en la tabla 'Productos' de la base de datos 'carnes'.")
