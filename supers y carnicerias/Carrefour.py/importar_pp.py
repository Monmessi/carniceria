import csv
import mysql.connector
from datetime import datetime

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",  # Cambia 'tu_usuario' por tu usuario de MySQL
    password="44273842",  # Cambia 'tu_contraseña' por tu contraseña de MySQL
    database="carnes"
)

cursor = conexion.cursor()

# Inserción en la tabla Supermercados
cursor.execute(
    """
    INSERT INTO Supermercados (Nombre_Supermercado, Contacto, Pagina_web, Negocio)
    VALUES (%s, %s, %s, %s) 
    """,
    ('Carrefour', 'https://www.carrefour.com.ar/Carnes-y-Pescados?page=1','Si','Super'  )
)

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción en la tabla Sucursales
cursor.execute(
    """
    INSERT INTO Sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (id_supermercado, 'Av. Recta Martinolli 5021', 'Córdoba Capital', 'Córdoba', 'Argüello')
)

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

conexion.commit()  # Confirmar las inserciones

def insertar_datos_csv(archivo_csv, conexion, id_supermercado):
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
        for row in reader:
            # Limpiar y convertir el precio a int (ya que ya está limpio)
            precio = int(row['Precio'])

            # Insertar los datos en la tabla Productos
            cursor.execute(
                """
                INSERT INTO Productos (Nombre_Producto, Categoria, Fecha_Carga, Precio, Descuento, ID_Supermercado)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (row['Nombre_Producto'], 'Desconocida', datetime.now().strftime('%Y-%m-%d'), precio, 0, 15)
            )

    conexion.commit()
    print(f"Datos del archivo {archivo_csv} insertados en la base de datos correctamente.")

# Llama a la función para insertar datos desde el archivo CSV
insertar_datos_csv('cas.csv', conexion, id_supermercado)

# Cerrar conexión
cursor.close()
conexion.close()
