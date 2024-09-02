import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('blackbull.csv')

# Función para limpiar precios
def clean_price(price):
    # Eliminar el signo de moneda y puntos, reemplazar coma por punto
    cleaned_price = price.replace('$', '').replace('.', '').replace(',', '.').strip()
    return float(cleaned_price)

# Aplicar la función a la columna de precios
df['Precio'] = df['Precio'].apply(clean_price)

# Verificar los resultados
print(df)

# Guardar el DataFrame limpio en un nuevo archivo CSV (opcional)
df.to_csv('blackbull_clean.csv', index=False)
