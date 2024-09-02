from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

'''''en este codigo se extrae todos los productos de la pagina de cordiez, separando los precios con descuento
de los precios originales, se guardan con nombre y categoria en un archivo csv para luego limpiarlo y que se pueda cargar 
facilmente en la base de datos'''


# Configuración del WebDriver para Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")
service = Service('/opt/homebrew/bin/geckodriver')

driver = webdriver.Firefox(service=service, options=firefox_options)

# Abre la página de la categoría "Carnes"
driver.get('https://www.cordiez.com.ar/carnes')

try:
    # Espera hasta que los elementos de productos estén presentes
    driver.implicitly_wait(120)

    # Simular el desplazamiento hacia abajo para cargar todos los productos
    last_height = driver.execute_script("return document.body.scrollHeight")
    SCROLL_PAUSE_TIME = 5

    while True:
        # Desplaza hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Espera a que se carguen los nuevos productos
        time.sleep(SCROLL_PAUSE_TIME)

        # Calcula la nueva altura y compara con la anterior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Reintentar desplazarse si no hay cambio en la altura
            for _ in range(3):  # Reintentar tres veces
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height > last_height:
                    last_height = new_height
                    break
            else:
                break  # Si después de tres intentos la altura no cambia, rompe el bucle
        else:
            last_height = new_height

    # Captura todos los contenedores de productos después del desplazamiento
    product_containers = driver.find_elements(By.CLASS_NAME, 'product')

    product_names = []
    product_prices = []

    for container in product_containers:
        # Captura el nombre del producto
        name = container.find_element(By.TAG_NAME, 'h5').text
        product_names.append(name)

        # Captura el primer precio disponible
        price_elements = container.find_elements(By.CLASS_NAME, 'offer-price')
        if price_elements:
            price = price_elements[0].text
            product_prices.append(price)
        else:
            product_prices.append("N/A")

    # Crear un DataFrame con los nombres y precios
    df = pd.DataFrame({
        'Producto': product_names,
        'Precio': product_prices,
    })

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Función para limpiar los precios y separar el descuento del precio original
    def limpiar_precio(precio):
        # Eliminar los signos de dinero y espacios
        precios_limpios = precio.replace("$", "").replace(",", "").split()
        
        # Si hay dos precios, el primero es el descuento y el segundo el precio original
        if len(precios_limpios) == 2:
            return float(precios_limpios[1]), float(precios_limpios[0])
        # Si solo hay un precio, es el precio original y no hay descuento
        elif len(precios_limpios) == 1:
            return float(precios_limpios[0]), None
        else:
            return None, None

    # Aplicar la función de limpieza a cada fila del DataFrame
    df[['Precio', 'Descuento']] = df['Precio'].apply(lambda x: pd.Series(limpiar_precio(x)))

    # Guardar el nuevo DataFrame en un archivo CSV
    df.to_csv('productos_cordiez_limpio.csv', index=False)

    # Mostrar el DataFrame para verificar
    print(df)

finally:
    # Cierra el WebDriver
    driver.quit()