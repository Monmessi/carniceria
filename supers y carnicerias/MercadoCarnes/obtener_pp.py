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
cursor.execute("INSERT INTO supermercados (Nombre_Supermercado, Contacto, Pagina_web, Negocio) VALUES (%s, %s, %s, %s)", ("Mercado De Carnes", "03513199590" , "No", "Carniceria"))
conexion.commit()

# Obtener el ID del supermercado recién insertado
id_supermercado = cursor.lastrowid

# Inserción de la sucursal "Avenida Presidente Perón 5416, Villa Allende, Córdoba"
cursor.execute("""
    INSERT INTO sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
    VALUES (%s, %s, %s, %s, %s)
""", (id_supermercado, "Av. Recta Martinolli 8296", "Córdoba Capital", "Córdoba", "Argüello"))  # Asegúrate de que 'Sucursal' tenga un valor claro y significativo
conexion.commit()

# Obtener el ID de la sucursal recién insertada
id_sucursal = cursor.lastrowid

# Diccionario de precios y categorías
precios_carnes = {
    # Vaca
    "Milanesa Carne (1kg)": (8000, "Vaca"),
    "Peceto": (9500, "Vaca"),
    "Jamón Cuadrado": (8950, "Vaca"),
    "Lomo (Bola)": (7800, "Vaca"),
    "Carne Molida Especial (1kg)": (7500, "Vaca"),
    "Molida Común (1kg)": (4950, "Vaca"),
    "Osobuco (1kg)": (4900, "Vaca"),
    "Puchero (1kg)": (2800, "Vaca"),
    "Bife de Chorizo": (10150, "Vaca"),
    "Tapa de Nalga": (9000, "Vaca"),
    "Lomo": (11300, "Vaca"),
    "Colita Cuadril": (10300, "Vaca"),
    "Cuadril": (9600, "Vaca"),
    "Costilla (1kg)": (9400, "Vaca"),
    "Vacio": (9950, "Vaca"),
    "Tapa de Asado": (9600, "Vaca"),
    "Bocado Fino (1kg)": (5250, "Vaca"),
    "Falda (1kg)": (5950, "Vaca"),
    "Falda Especial": (7700, "Vaca"),
    "Bocado Ancho (1kg)": (6600, "Vaca"),
    "Costeleta Ancha (1kg)": (6500, "Vaca"),
    "Arañita": (10500, "Vaca"),
    "Entrecot": (9300, "Vaca"),
    "Matambre Vaca (1kg)": (9750, "Vaca"),

    # Pollo
    "Milanesa Pollo (1kg)": (6950, "Pollo"),
    "Alitas (1kg)": (1950, "Pollo"),
    "Alitas (2kg)": (3600, "Pollo"),
    "Pata Muslo (1kg)": (2850, "Pollo"),
    "Pata Muslo (3kg)": (7950, "Pollo"),
    "Menudos (1kg)": (1050, "Pollo"),
    "Menudos (3kg)": (2400, "Pollo"),
    "Pechuga con Hueso (1kg)": (4900, "Pollo"),
    "Pechuga Deshuesada (1kg)": (7300, "Pollo"),
    "Pollo Entero": (2750, "Pollo"),

    # Cerdo
    "Paleta": (8000, "Cerdo"),
    "Costeleta (1kg)": (7200, "Cerdo"),
    "Morcilla": (5500, "Cerdo"),
    "Chorizo Criollo (1kg)": (4850, "Cerdo"),
    "Chorizo Colorado": (9000, "Cerdo"),
    "Bocado de Cerdo (1kg)": (3900, "Cerdo"),

    # Achura
    "Mondongo": (3500, "Achura"),
    "Riñon": (3300, "Achura"),
    "Higado (1kg)": (2600, "Achura"),
    "Chinchulin": (3000, "Achura"),
    "Molleja": (9990, "Achura"),
}


# Inserción de productos
for nombre, (precio, categoria) in precios_carnes.items():
    cursor.execute("""
        INSERT INTO productos (Nombre_Producto, Precio, Categoria, ID_Supermercado) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, precio, categoria, 14))

# Confirmar cambios
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Inserción completada exitosamente.")
