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

# Función para insertar datos desde un archivo CSV en la tabla Productos
def insertar_datos_productos(archivo_csv, conexion, id_supermercado):
    """
    Inserta datos de un archivo CSV en la tabla Productos en la base de datos MySQL.
    
    :param archivo_csv: Ruta del archivo CSV a leer.
    :param conexion: Objeto de conexión a la base de datos MySQL.
    :param id_supermercado: ID del supermercado al que pertenecen los productos.
    """
    cursor = conexion.cursor()

    # Leer el archivo CSV
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Verifica las columnas disponibles en el archivo CSV
        if 'Precio_Limpio' not in reader.fieldnames or 'Nombre_Producto' not in reader.fieldnames or 'Categoria' not in reader.fieldnames:
            raise KeyError("El archivo CSV no contiene las columnas necesarias: 'Precio_Limpio', 'Nombre_Producto', 'Categoria'.")
        
        for row in reader:
            # Obtener los valores del CSV
            nombre_producto = row['Nombre_Producto']
            categoria = row['Categoria']
            try:
                # Limpiar y convertir el precio a int
                precio = int(row['Precio_Limpio'])
            except ValueError as e:
                print(f"Error al convertir el precio '{row['Precio_Limpio']}': {e}")
                continue  # Saltar este registro en caso de error

            # Insertar los datos en la tabla Productos
            cursor.execute(
                """
                INSERT INTO Productos (Nombre_Producto, Categoria, Fecha_Carga, Precio, Descuento, ID_Supermercado)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (nombre_producto, categoria, datetime.now().strftime('%Y-%m-%d'), precio, 0, id_supermercado)
            )

    # Confirmar los cambios en la base de datos
    conexion.commit()
    print(f"Datos del archivo {archivo_csv} insertados en la tabla 'Productos' correctamente.")
    cursor.close()

# Llama a la función para insertar datos desde el archivo CSV
try:
    insertar_datos_productos('Supermami_limpio.csv', conexion, 17)  # Asegúrate de que el ID del supermercado es correcto
finally:
    # Cerrar la conexión
    conexion.close()
