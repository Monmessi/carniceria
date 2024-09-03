import csv

# Nombre del archivo CSV original y del archivo CSV resultante
archivo_entrada = 'Supermami.csv'
archivo_salida = 'Supermami_limpio.csv'

# Función para limpiar el precio y convertirlo a entero
def limpiar_precio(precio):
    # Eliminar los signos de dólar, puntos, comas, comillas simples y espacios
    precio_limpio = precio.replace('$', '').replace('.', '').replace(',', '').replace("'", '').strip()
    # Convertir el precio a entero
    return int(precio_limpio)

# Función para categorizar el producto
def categorizar_producto(nombre_producto):
    # Si contiene la palabra "POLLO", categoría es "Pollo"; de lo contrario, es "Vaca"
    if 'POLLO' in nombre_producto.upper():
        return 'Pollo'
    else:
        return 'Vaca'

# Leer el archivo CSV, limpiar los precios y categorizar productos
with open(archivo_entrada, 'r', newline='', encoding='utf-8') as csvfile_entrada, open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile_salida:
    reader = csv.DictReader(csvfile_entrada)
    fieldnames = ['Nombre_Producto', 'Precio_Limpio', 'Categoria']
    writer = csv.DictWriter(csvfile_salida, fieldnames=fieldnames)
    
    # Escribir la cabecera en el archivo de salida
    writer.writeheader()

    for row in reader:
        nombre_producto = row['Nombre_Producto']
        precio = row['Precio']
        
        # Limpiar el precio y convertirlo a entero
        try:
            precio_limpio = limpiar_precio(precio)
        except ValueError as e:
            print(f"Error al limpiar el precio '{precio}': {e}")
            continue  # Saltar este registro en caso de error
        
        # Categorizar el producto
        categoria = categorizar_producto(nombre_producto)
        
        # Escribir los datos limpios y categorizados en el nuevo archivo CSV
        writer.writerow({
            'Nombre_Producto': nombre_producto,
            'Precio_Limpio': precio_limpio,
            'Categoria': categoria
        })

print(f"Los datos han sido limpiados, convertidos a enteros y categorizados. El archivo resultante se guardó como {archivo_salida}.")
