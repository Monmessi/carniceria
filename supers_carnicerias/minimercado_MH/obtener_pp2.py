import csv
import re
import pymysql

# Conexión a la base de datos MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='44273842',
    database='carnes'
)


'''''em este codigo se cargan los datos de un mensaje de wp que previamente fue convertido en csv
ademas se fija que si los datos de las primeras deo tablas ya existen se pase a la de los productos a cargarla'''

def limpiar_precio(precio):
    precio_limpio = precio.replace(" ", "").replace(",", ".")
    try:
        return float(precio_limpio)
    except ValueError:
        return None

try:
    with connection.cursor() as cursor:
        # Verificar si el supermercado ya existe
        cursor.execute("SELECT ID_Supermercado FROM Supermercados WHERE Nombre_Supermercado='MH minimercado'")
        result = cursor.fetchone()
        
        if result:
            id_supermercado = result[0]
        else:
            cursor.execute("INSERT INTO Supermercados (Nombre_Supermercado) VALUES ('MH minimercado')")
            connection.commit()
            id_supermercado = cursor.lastrowid
        
        # Verificar si la sucursal ya existe
        cursor.execute("""
            SELECT ID_Sucursal FROM Sucursales 
            WHERE ID_Supermercado=%s AND Direccion='Av. Recta Martinolli 8024' AND Sucursal='Argüello'
        """, (id_supermercado,))
        result = cursor.fetchone()
        
        if result:
            id_sucursal = result[0]
        else:
            cursor.execute("""
                INSERT INTO Sucursales (ID_Supermercado, Direccion, Departamento, Provincia, Sucursal) 
                VALUES (%s, 'Av. Recta Martinolli 8024', 'Córdoba Capital', 'Córdoba', 'Argüello')
            """, (id_supermercado,))
            connection.commit()
            id_sucursal = cursor.lastrowid
        
        # Leer el archivo CSV generado y agregar los productos a la base de datos
        with open("productos.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                precio_limpio = limpiar_precio(row['Precio'])
                if precio_limpio is not None:
                    cursor.execute(
                        "INSERT INTO Productos (Nombre_Producto, Categoria, ID_Supermercado, Fecha_Carga, Precio) VALUES (%s, %s, %s, CURDATE(), %s)",
                        (row['Producto'], row['Categoría'], id_supermercado, precio_limpio)
                    )
            connection.commit()

        print("Datos insertados correctamente en la base de datos.")

finally:
    connection.close()
