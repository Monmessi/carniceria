import mysql.connector

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host='localhost',  # Cambia esto si tu base de datos no está en el localhost
    user='root',  # Reemplaza con tu nombre de usuario de MySQL
    password='44273842',  # Reemplaza con tu contraseña de MySQL
    database='carnes'  # Nombre de la base de datos
)

cursor = conexion.cursor()

# Lista de datos de sucursales
sucursales = [
    ("Av. Recta Martinolli 8469", "Córdoba Capital", "Córdoba", "Carolinos", 6),
    ("Av. Recta Martinolli 7120", "Córdoba Capital", "Córdoba", "Arguello", 6),
    ("Av. Rafael Núñez 3657", "Córdoba Capital", "Córdoba", "Cerro de las rosas", 6),
    ("Jose Antonio de Goyechea 2851", "Córdoba Capital", "Córdoba", "Altos villa cabrera", 6),
    ("Av. Vélez Sarsfield 1845", "Córdoba Capital", "Córdoba", "Colina de Velez Sarfield", 6),
    ("Av. Colón 683", "Córdoba Capital", "Córdoba", "Alberdi", 6),
    ("José Manuel Estrada 66", "Córdoba Capital", "Córdoba", "Nueva Cordoba", 6),
    ("Ituzaingó 701", "Córdoba Capital", "Córdoba", "Nueva Cordoba", 6),
    ("Jerónimo Luis de Cabrera 493", "Córdoba Capital", "Córdoba", "Alta cordoba", 6)
]

# Insertar cada sucursal en la tabla
for sucursal in sucursales:
    cursor.execute("""
        INSERT INTO Sucursales (Direccion, Departamento, Provincia, Sucursal, ID_Supermercado)
        VALUES (%s, %s, %s, %s, %s)
    """, sucursal)

# Confirmar los cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Sucursales agregadas a la base de datos 'carnes'.")
