import pandas as pd

# Leer el archivo CSV limpio con precios ya formateados
df = pd.read_csv('blackbull_clean.csv')

# Lista de nombres de productos que son de la categoría "vaca" según las imágenes proporcionadas
productos_vaca = [
    "Asado de falda", "Bife de Chorizo", "Bife de Vacio", "Colita de Cuadril", "Corazón Cuadril",
    "Costeletón", "Costilla Banderita", "Denver", "Entraña x 2", "Entrecot x 2", "Falda sin hueso",
    "Flat Iron", "Lomito de cuadril", "Lomo", "Lomo Por Mitad", "Matambre"
]

# Lista de nombres de productos que son de la categoría "hamburguesa" según las nuevas imágenes proporcionadas
productos_hamburguesa = [
    "Cheddar", "Combo x 4", "Combo x 6", "Hamburguesa x 4", "Hamburguesa x 6",
    "Panes de Hamburguesa x6", "Panes Hamburguesas x4"
]

# Agregar la columna 'Categoría' inicializada con valores vacíos
df['Categoría'] = ''

# Asignar la categoría 'vaca' a los productos específicos
df.loc[df['Nombre'].isin(productos_vaca), 'Categoría'] = 'vaca'

# Asignar la categoría 'hamburguesa' a los productos específicos
df.loc[df['Nombre'].isin(productos_hamburguesa), 'Categoría'] = 'hamburguesa'

# Asignar la categoría 'cerdo' a los productos no categorizados
df.loc[df['Categoría'] == '', 'Categoría'] = 'cerdo'

# Verificar los resultados
print(df)

# Guardar el DataFrame actualizado en un nuevo archivo CSV (opcional)
df.to_csv('blackbull_with_category_complete.csv', index=False)

print("Datos guardados en blackbull_with_category_complete.csv")
