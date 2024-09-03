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
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado, Contacto, Pagina_web, Negocio) VALUES (%s,%s,%s,%s)", ("Abastecimiento San Benito",5493516482138, "No", "Carniceria"))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Javier Lascano Colodrero 2721", "Córdoba Capital", "Córdoba", "Poeta Lugones"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {
   "Parrillera": (6000, "Vaca"),
    "Osobuco": (6000, "Vaca"),
    "Bocado Fino": (6000, "Vaca"),
    "Bocado Ancho": (7800, "Vaca"),
    "Falda": (6000, "Vaca"),
    "Vacio": (8800, "Vaca"),
    "Costilla": (8500, "Vaca"),
    "Matambre": (8800, "Vaca"),
    "Tapa de Asado": (8800, "Vaca"),
    "Costeleta": (8300, "Vaca"),
    "Palomita/Paleta": (8500, "Vaca"),
    "Nalga": (9300, "Vaca"),
    "Bola de Lomo": (8800, "Vaca"),
    "Cuadril/Cuadrilero": (9300, "Vaca"),
    "Jamón Cuadrado": (8800, "Vaca"),
    "Peceto": (9500, "Vaca"),
    "Lomo": (9999, "Vaca"),
    "Molida Intermedia": (6000, "Vaca"),
    "Molida Especial": (8500, "Vaca"),
    "Milanesas": (8500, "Vaca"),
    "Hamburguesas (Clasicas)": (7500, "Vaca"),
    "Hamburguesas (Gurmet)": (8500, "Vaca"),
    "Hamburguesas (Gurmet con muzza)": (8500, "Vaca"),
    "Hamburguesas (Gurmet con roquefort)": (8500, "Vaca"),
    
    # Carne de Pollo
    "Pollo": (4100, "Pollo"),
    "Pata Muslo": (4100, "Pollo"),
    "Pechuga": (7500, "Pollo"),
    "Pechuga sin hueso": (7800, "Pollo"),
    "Milanesas de Pollo": (7000, "Pollo"),
    "Alitas": (1500, "Pollo"),
    "Alitas Rebozadas": (5000, "Pollo"),
    
    # Carne de Cerdo
    "Carre": (6500, "Cerdo"),
    "Pechito": (6500, "Cerdo"),
    "Matambre de Cerdo": (8500, "Cerdo"),
    "Vacío de Cerdo": (6500, "Cerdo"),
    "Bondiola": (7500, "Cerdo"),
    "Chorizo": (9500, "Cerdo"),
    "Morcilla": (7500, "Cerdo"),
    "Morcilla Vasca": (7000, "Cerdo"),
    "Salchichitas": (12000, "Cerdo"),
    "Pulpa": (6500, "Cerdo")
}

# Inserción de productos
for nombre, (precio, categoria) in precios_carnes.items():
    cursor.execute("""
        INSERT INTO productos (Nombre_Producto, Precio, Categoria, ID_Supermercado) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, precio, categoria, 16))

# Confirmar cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Inserción completada exitosamente.")
