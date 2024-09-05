import requests
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import time

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Tu clave API de OpenCage
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')  # Asegúrate de agregar esta clave a tu archivo .env

# Conexión a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Verificar si una columna existe en una tabla
def columna_existe(cursor, nombre_tabla, nombre_columna):
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_name = '{nombre_tabla}'
        AND column_name = '{nombre_columna}';
    """)
    return cursor.fetchone()[0] > 0

# Función para obtener coordenadas de OpenCage
def obtener_coordenadas_opencage(direccion):
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={direccion}&key={OPENCAGE_API_KEY}&language=es&countrycode=AR"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                lat = data['results'][0]['geometry']['lat']
                lon = data['results'][0]['geometry']['lng']
                return lat, lon
            else:
                print("No se encontraron resultados para la dirección proporcionada.")
                return None, None
        else:
            print(f"Error en la solicitud a OpenCage: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")
        return None, None

# Función para actualizar la tabla Sucursales con las coordenadas
def actualizar_coordenadas():
    conexion = conectar_db()
    if not conexion:
        return

    cursor = conexion.cursor()

    # Verificar si las columnas de latitud y longitud existen, si no, agregarlas
    if not columna_existe(cursor, 'Sucursales', 'Latitud'):
        cursor.execute("ALTER TABLE Sucursales ADD COLUMN Latitud FLOAT;")
        print("Columna 'Latitud' agregada a la tabla 'Sucursales'.")
    
    if not columna_existe(cursor, 'Sucursales', 'Longitud'):
        cursor.execute("ALTER TABLE Sucursales ADD COLUMN Longitud FLOAT;")
        print("Columna 'Longitud' agregada a la tabla 'Sucursales'.")

    # Seleccionar las direcciones, departamentos y provincias de la tabla Sucursales donde Latitud o Longitud son NULL y ID_Supermercado != 1
    cursor.execute("""
        SELECT ID_Sucursal, Direccion, Departamento, Provincia 
        FROM Sucursales 
        WHERE (Latitud IS NULL OR Longitud IS NULL) 
        AND ID_Supermercado != 1
    """)
    sucursales = cursor.fetchall()

    for sucursal in sucursales:
        id_sucursal, direccion, departamento, provincia = sucursal
        direccion_completa = f"{direccion}, {departamento}, {provincia}, Argentina"
        latitud, longitud = obtener_coordenadas_opencage(direccion_completa)
        
        if latitud and longitud:
            # Actualizar la sucursal con las coordenadas
            cursor.execute("""
            UPDATE Sucursales
            SET Latitud = %s, Longitud = %s
            WHERE ID_Sucursal = %s
            """, (latitud, longitud, id_sucursal))
            print(f"Sucursal {id_sucursal} actualizada con coordenadas: ({latitud}, {longitud})")
        
        # Añadir un retardo de 2 segundos entre solicitudes para evitar límites de API
        time.sleep(2)

    conexion.commit()
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    actualizar_coordenadas()
