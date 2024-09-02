import csv

def limpiar_precios_csv(archivo_entrada, archivo_salida=None):
    """
    Limpia los precios en un archivo CSV eliminando el signo '$' y '.' y convierte los precios a enteros.
    
    :param archivo_entrada: Nombre del archivo CSV de entrada.
    :param archivo_salida: Nombre del archivo CSV de salida (opcional). Si no se proporciona, se sobrescribe el archivo de entrada.
    """
    if archivo_salida is None:
        archivo_salida = archivo_entrada  # Sobrescribir el archivo de entrada si no se proporciona un archivo de salida

    # Leer el archivo CSV
    with open(archivo_entrada, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        filas = list(reader)

    # Limpiar los precios en cada fila
    for fila in filas:
        precio_limpio = fila['Precio'].replace('$', '').replace('.', '').replace(',', '')
        fila['Precio'] = int(precio_limpio)  # Convertir a entero

    # Guardar los datos limpios en el archivo de salida
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filas)

    print(f"Archivo CSV limpiado. Datos guardados en '{archivo_salida}'.")

# Ejemplo de uso
limpiar_precios_csv('cas.csv')
