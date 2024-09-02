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
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado) VALUES (%s)", ("El Tori",))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Rodríguez del busto 3915", "Córdoba Capital", "Córdoba", "Cerro Chico"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {
    "Costilla": (8500, "Vaca"),
    "Ventana": (7800, "Vaca"),
    "Costillar Entero": (7900, "Vaca"),
    "Plancha Entera": (7300, "Vaca"),
    "Matambre": (8850, "Vaca"),
    "Vacio": (8900, "Vaca"),
    "Tapa de Asado": (7500, "Vaca"),
    "Entraña": (8500, "Vaca"),
    "Falda": (6400, "Vaca"),
    "Falda Deshuesada": (7500, "Vaca"),
    "Lomo": (9500, "Vaca"),
    "Costeleta Angosta": (7700, "Vaca"),
    "Costeleta Ancha": (8500, "Vaca"),
    "Costeleta Redonda": (7200, "Vaca"),
    "Bife de Chorizo": (8800, "Vaca"),
    "Entrecot": (8500, "Vaca"),
    "Aguja": (5500, "Vaca"),
    "Marucha": (7200, "Vaca"),
    "Bocado Ancho": (6800, "Vaca"),
    "Bocado Fino": (5400, "Vaca"),
    "Bocado Surtido": (4500, "Vaca"),
    "Osobuco": (5000, "Vaca"),
    "Paleta Pulpa": (7900, "Vaca"),
    "Churrasquito": (7000, "Vaca"),
    "Nalga": (9000, "Vaca"),
    "Tapa de Nalga": (8900, "Vaca"),
    "Cuadril": (9000, "Vaca"),
    "Tapita de Cuadril": (8900, "Vaca"),
    "Colita de Cuadril": (8900, "Vaca"),
    "Bola de Lomo": (8700, "Vaca"),
    "Jamón Cuadrado": (8800, "Vaca"),
    "Peceto": (8800, "Vaca"),
    "Tortuguita": (7850, "Vaca"),
    "Molida Especial": (7850, "Vaca"),
    "Molida Intermedia": (5300, "Vaca"),
    "Milanesa Ternera": (7500, "Vaca"),
    "Asado Surtido": (7500, "Vaca"),
    "Media Res": (5000, "Vaca"),
    "Pierna": (5300, "Vaca"),
    "Carne Vacuno": (6100, "Vaca"),
    "Paleta Entera": (4900, "Vaca")
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
