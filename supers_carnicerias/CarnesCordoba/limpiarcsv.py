import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('productos_carnes.csv')

# Función para limpiar los precios
def limpiar_precio(precio):
    # Eliminar '$' y '.' y convertir a float o int
    return float(precio.replace('$', '').replace('.', '').replace(',', '.'))

# Aplicar la función de limpieza a la columna 'Precio'
df['Precio'] = df['Precio'].apply(limpiar_precio)

# Guardar el DataFrame limpio en un nuevo archivo CSV
df.to_csv('productos_carnes_limpio.csv', index=False)

print("Precios limpios guardados en 'productos_carnes_limpio.csv'.")
