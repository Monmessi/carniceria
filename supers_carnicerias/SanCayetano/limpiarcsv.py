import pandas as pd
import re

# Cargar el archivo CSV
df = pd.read_csv('SanCayetano.csv')

# Función para limpiar los precios
def limpiar_precio(precio):
    # Eliminar cualquier texto como "Desde" y el signo de dólar
    precio_limpio = re.sub(r'[^\d,.-]', '', precio)  # Eliminar cualquier texto que no sea número, coma, punto o guión

    # Eliminar puntos que son separadores de miles
    precio_limpio = precio_limpio.replace('$', '').replace('.', '')
    
    # Reemplazar comas por puntos para convertir decimales correctamente
    precio_limpio = precio_limpio.replace(',', '.')

    try:
        # Convertir a float y luego a un string formateado para mantener ceros finales
        precio_float = float(precio_limpio)
        return '{:.2f}'.format(precio_float)  # Convertir a string manteniendo dos decimales
    except ValueError:
        return None  # Manejar casos donde la conversión a float falla

# Aplicar la función de limpieza a la columna de precios
df['Precio'] = df['Precio'].apply(limpiar_precio)

# Eliminar filas con precios no convertibles (None)
df = df.dropna(subset=['Precio'])

# Guardar el DataFrame limpio en un nuevo archivo CSV
df.to_csv('SanCayetano_limpio.csv', index=False)

print("Columna de precios limpiada y guardada en 'SanCayetano_limpio.csv'.")
