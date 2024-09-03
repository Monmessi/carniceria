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
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES (%s)", ("Los Amigos",))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Avenida Presidente Perón 5416", "Villa Allende", "Córdoba", "Sucursal 1"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {
    # Vaca
    "Nalga - Cuadril": (8600, "Vaca"),
    "Jamón Cuadrado": (8300, "Vaca"),
    "Cabeza de Lomo": (8300, "Vaca"),
    "Punta de Vacío": (8600, "Vaca"),
    "Jamón Redondo": (8800, "Vaca"),
    "Brazuelos S/H": (7600, "Vaca"),
    "Entrecot Común": (7100, "Vaca"),
    "Palomita": (7000, "Vaca"),
    "Chingolo": (6000, "Vaca"),
    "Lomo": (8200, "Vaca"),
    "Entraña Fina": (8900, "Vaca"),
    "Entrecot Especial": (8800, "Vaca"),
    "Tapa de Nalga": (7600, "Vaca"),
    "Costilla Ternera": (8600, "Vaca"),
    "Vacío Ternera": (8800, "Vaca"),
    "Matambre Ternera": (8400, "Vaca"),
    "Falda Ternera": (5900, "Vaca"),
    "Tapa de Asado": (7600, "Vaca"),
    "Costeletas Grandes": (4800, "Vaca"),
    "Costeletas Chicas o Medianas": (1000, "Vaca"),
    "Brazuelos C/H": (4800, "Vaca"),
    "Picada Especial": (5000, "Vaca"),  # Especificando por kilo (precio indicado)
    "Picada Común": (6200, "Vaca"),
    "Mar del Plata Especial": (9000, "Vaca"),
    "Mar del Plata Común": (6300, "Vaca"),
    "Caracú": (5000, "Vaca"),  # Precio aproximado
    "Costilla Asado Ternera": (8600, "Vaca"),
    "Vacío Asado Ternera": (8800, "Vaca"),
    "Matambre Asado Ternera": (8400, "Vaca"),
    "Falda Asado Ternera": (5900, "Vaca"),
    "Costilla Asado Novillo": (5999, "Vaca"),
    "Vacío Asado Novillo": (7700, "Vaca"),
    "Matambre Asado Novillo": (6700, "Vaca"),
    "Falda Asado Novillo": (4500, "Vaca"),

    # Achuras
    "Chinchulín": (2500, "Achuras"),
    "Mondongo": (4200, "Achuras"),
    "Corazón": (3000, "Achuras"),
    "Entraña": (5600, "Achuras"),
    "Mollejas": (10000, "Achuras"),
    "Nervios": (7300, "Achuras"),
    "Lengua": (5200, "Achuras"),
    "Hígado": (2000, "Achuras"),
    "Riñón": (2400, "Achuras"),
    "Tripa": (2500, "Achuras"),
    "Rabo": (5200, "Achuras"),
    "Seso": (750, "Achuras"),  # Precio por unidad
    "Cuajo": (1700, "Achuras"),

    # Pollo
    "Supremas Pata-Muslo": (3900, "Pollo"),
    "Supremas Rellenas": (5500, "Pollo"),
    "Pollo Relleno": (5500, "Pollo"),
    "Muslo Relleno": (5500, "Pollo"),
    "BastonCitos": (5500, "Pollo"),
    "Supremas": (4500, "Pollo"),
    "Milanesas": (1200, "Pollo"),
    "Filet de Pollo": (4800, "Pollo"),
    "Pollo Soy Chu": (2900, "Pollo"),
    "Ricosaurios": (6000, "Pollo"),
    "Medallón de Pollo": (4800, "Pollo"),
    "Patitas Rebozadas": (6000, "Pollo"),
    "Patas": (2300, "Pollo"),
    "Carcaza": (600, "Pollo"),
    "Alitas": (2000, "Pollo"),

    # Lechón
    "Lechón": (6750, "Lechón"),

    # Cordero
    "Cordero": (6500, "Cordero"),

    # Cerdo
    "Pulpa de Cerdo": (5600, "Cerdo"),
    "Mar del Plata de Cerdo": (5200, "Cerdo"),
    "Churrasquito de Cerdo": (4000, "Cerdo"),
    "Matambrito de Cerdo": (7400, "Cerdo"),
    "Bondiola": (7500, "Cerdo"),
    "Pechito de Cerdo": (5000, "Cerdo"),
    "Carré de Cerdo": (4600, "Cerdo"),
    "Solomillo": (6000, "Cerdo"),
    "Chorizos Especiales (Paladini)": (8300, "Cerdo"),
    "Chorizos Comunes (Paladini)": (7500, "Cerdo"),
    "Salchicha Fresca (Paladini)": (9000, "Cerdo"),
    "Morcilla Parrillera (Paladini)": (5900, "Cerdo"),
    "Morcilla Rosca (Paladini)": (5600, "Cerdo"),
    "Chorizo Especial (Baltazar)": (8300, "Cerdo"),
    "Chorizos Comunes (Baltazar)": (4700, "Cerdo"),
    "Chorizo Rellenos (Baltazar)": (8300, "Cerdo"),
    "Salchicha Fresca (Baltazar)": (8400, "Cerdo"),
    "Morcilla (Baltazar)": (5000, "Cerdo"),
    "Morcilla (Moriconi)": (5000, "Cerdo"),
    "Chorizos Especiales (Moriconi)": (8300, "Cerdo"),
    "Chorizo Prasino (El Cherú)": (4800, "Cerdo"),
    "Chorizo Fiorentina (El Cherú)": (3800, "Cerdo"),

    # Pescado
    "Filet de Merluza": (6000, "Pescado"),
    "Medallón de Merluza": (4800, "Pescado"),
    "Merluza Rebozada": (8000, "Pescado"),
}

# Inserción de productos
for nombre, (precio, categoria) in precios_carnes.items():
    cursor.execute("""
        INSERT INTO productos (Nombre_Producto, Precio, Categoria, ID_Supermercado) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, precio, categoria, id_sucursal))

# Confirmar cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Inserción completada exitosamente.")
