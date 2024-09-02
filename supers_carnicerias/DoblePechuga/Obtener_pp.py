import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",  # Cambia esto si tu host es diferente
    user="root",  # Reemplaza con tu nombre de usuario de MySQL
    password="44273842",  # Reemplaza con tu contraseña de MySQL
    database="carnes"
)

cursor = conexion.cursor()

# Inserción del supermercado "Los Amigos"
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES (%s)", ("Doble Pechuga",))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Av. Ambrosio Olmos 805,", "Villa Allende", "Córdoba", "Ciudad Universitaria"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {

    "Pechuga": (6700, "Pollo"),
    "Pata Muslo": (2900, "Pollo"),
    "Pata Muslo Deshuesada": (4800, "Pollo"),
    "Milanesas de Pollo": (5200, "Pollo"),
    "Hamburguesas de Pollo": (4400, "Pollo"),
    "Medallones - Patitas": (4500, "Pollo"),
    "Alitas": (2000, "Pollo"),
    "Arrollados": (5500, "Pollo"),
    "Milanesas de Carne": (6600, "Vaca"),  # Asumiendo que se puede considerar en esta categoría
    "Hamburguesa Vegetariana": (0, "Vegetariana")  # Precio no proporcionado en la imagen, ajusta según sea necesario


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
