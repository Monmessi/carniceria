import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Configuración del WebDriver
driver = webdriver.Firefox()  # Asegúrate de que el controlador de Firefox (geckodriver) esté en tu PATH

# Función para esperar y hacer clic en un elemento
def esperar_y_hacer_click(xpath, mensaje_error):
    try:
        elemento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elemento.click()
    except TimeoutException:
        print(mensaje_error)
    except ElementClickInterceptedException:
        print(mensaje_error)

# Función para obtener productos de una categoría
def obtener_productos(url):
    driver.get(url)
    
    # Manejar el popup de "Minorista"
    esperar_y_hacer_click("//p[contains(text(), 'Minorista')]/ancestor::button", "No se encontró el popup de 'Minorista', continuando sin hacer clic.")
    
    # Manejar el popup de "Lo voy a retirar en una tienda"
    esperar_y_hacer_click("//p[contains(text(), 'Lo voy a retirar en una tienda')]/ancestor::button", "No se encontró el popup de 'Lo voy a retirar en una tienda', continuando sin hacer clic.")
    
    # Manejar la selección de provincia
    esperar_y_hacer_click("//span[contains(text(), 'Seleccione una Provincia')]/ancestor::div[@role='button']", "No se encontró el selector de provincia, continuando sin seleccionar.")
    esperar_y_hacer_click("//span[contains(text(), 'Córdoba')]/ancestor::div[@role='button']", "No se pudo seleccionar la provincia de Córdoba.")

    # Manejar la selección de tienda
    esperar_y_hacer_click("//span[contains(text(), 'Seleccione una Tienda')]/ancestor::div[@role='button']", "No se encontró el selector de tienda, continuando sin seleccionar.")
    esperar_y_hacer_click("//span[contains(text(), 'CÓRDOBA – Hipermercado Lugones')]/ancestor::div[@role='button']", "No se pudo seleccionar la tienda.")

    # Esperar y hacer clic en los productos
    productos = []
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--normal--normal vtex-search-result-3-x-galleryItem--gallery']")))
            nombres = driver.find_elements(By.XPATH, "//div[@class='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-productBrand--default tc']")
            precios = driver.find_elements(By.XPATH, "//span[@class='vtex-product-price-1-x-currencyContainer']")
            if not nombres or not precios:
                break
            for nombre, precio in zip(nombres, precios):
                productos.append({"Nombre": nombre.text, "Precio": precio.text})
            break
        except TimeoutException:
            print("No se encontraron productos en la página.")
            break
    
    return productos

# Lista de URLs a procesar
urls = [
    "https://www.hiperlibertad.com.ar/carnes/carne-vacuna",
    "https://www.hiperlibertad.com.ar/carnes/carne-de-cerdo",
    "https://www.hiperlibertad.com.ar/carnes/carne-de-pollo",
    "https://www.hiperlibertad.com.ar/carnes/embutidos",
    "https://www.hiperlibertad.com.ar/carnes/pescados",
    "https://www.hiperlibertad.com.ar/carnes/mariscos"
]

# Recolectar productos de todas las categorías
todos_los_productos = []
for url in urls:
    productos = obtener_productos(url)
    todos_los_productos.extend(productos)

# Guardar los productos en un archivo CSV
if todos_los_productos:
    df = pd.DataFrame(todos_los_productos)
    df.to_csv("productos_hiperlibertad_completo.csv", index=False)
    print("Los productos fueron guardados exitosamente en 'productos_hiperlibertad_completo.csv'.")
else:
    print("No se guardaron productos porque el DataFrame está vacío.")

# Cerrar el navegador
driver.quit()
