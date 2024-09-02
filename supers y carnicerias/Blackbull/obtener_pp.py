from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuración de Selenium con Firefox (GeckoDriver)
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Ejecuta el navegador en modo headless (sin interfaz)
driver = webdriver.Firefox(options=options)

# Función para hacer scroll hasta el final de la página
def scroll_to_end(driver):
    """Scroll down to the end of the page using Selenium and JavaScript."""
    scroll_pause_time = 2  # Segundos de pausa para que el contenido se cargue
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Hacer scroll hasta el final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Esperar a que se cargue el contenido

        # Calcular la nueva altura de la página después del scroll
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Salir del bucle si no hay más scroll (es decir, no se cargó contenido adicional)
        if new_height == last_height:
            break
        last_height = new_height

# Lista de URLs a scrapear
urls = [
    'https://blackbull.com.ar/productos-actualizados/',
    'https://blackbull.com.ar/productos-actualizados/?product-page=2',
    'https://blackbull.com.ar/productos-actualizados/?product-page=3',
    'https://blackbull.com.ar/productos-actualizados/?product-page=4'
]

# Listas para almacenar nombres de productos y precios
product_names = []
product_prices = []

# Scraping de cada URL
for url in urls:
    driver.get(url)
    time.sleep(2)  # Espera inicial para que se cargue la página

    # Hacer scroll hasta el final de la página
    scroll_to_end(driver)

    # Encontrar elementos de nombre de producto y precio
    products = driver.find_elements(By.CSS_SELECTOR, 'li.ast-article-single')
    
    for product in products:
        try:
            # Extraer el nombre del producto
            name = product.find_element(By.CSS_SELECTOR, 'h2.woocommerce-loop-product__title').text
            # Extraer el precio del producto
            price = product.find_element(By.CSS_SELECTOR, 'span.woocommerce-Price-amount.amount').text
            
            product_names.append(name)
            product_prices.append(price)
        except Exception as e:
            print(f"Error al obtener datos del producto: {e}")

# Cerrar el navegador
driver.quit()

# Guardar los datos en un archivo CSV
data = {'Nombre': product_names, 'Precio': product_prices}
df = pd.DataFrame(data)
df.to_csv('blackbull.csv', index=False)

print("Datos guardados en blackbull.csv")
