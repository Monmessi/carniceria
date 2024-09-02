from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

'''''este codigo recopila todos los datos de las urls los limpia, les elimi los duplicados y los guarda en un csv
para posteriormente limpiar todos los duplicados '''

# Configuración del WebDriver para Firefox
firefox_options = Options()
service = Service('/opt/homebrew/bin/geckodriver')  # Ajusta la ruta según donde tengas geckodriver instalado
driver = webdriver.Firefox(service=service, options=firefox_options)

# URLs para acceder directamente
urls = [
   "https://www.disco.com.ar/carnes?initialMap=c&initialQuery=carnes&map=category-1,category-2,category-2,category-2,category-2,category-2,category-2,category-2&query=/carnes/carne-de-cerdo/carne-vacuna/cordero-lechon-chivito-y-conejo/embutidos/listos-para-cocinar/menudencias/pollos&searchState",
    "https://www.disco.com.ar/carnes?initialMap=c&initialQuery=carnes&map=category-1,category-2,category-2,category-2,category-2,category-2,category-2,category-2&page=2&query=/carnes/carne-de-cerdo/carne-vacuna/cordero-lechon-chivito-y-conejo/embutidos/listos-para-cocinar/menudencias/pollos&searchState",
    "https://www.disco.com.ar/carnes?initialMap=c&initialQuery=carnes&map=category-1,category-2,category-2,category-2,category-2,category-2,category-2,category-2&page=3&query=/carnes/carne-de-cerdo/carne-vacuna/cordero-lechon-chivito-y-conejo/embutidos/listos-para-cocinar/menudencias/pollos&searchState",
    "https://www.disco.com.ar/carnes?initialMap=c&initialQuery=carnes&map=category-1,category-2,category-2,category-2,category-2,category-2,category-2,category-2&page=4&query=/carnes/carne-de-cerdo/carne-vacuna/cordero-lechon-chivito-y-conejo/embutidos/listos-para-cocinar/menudencias/pollos&searchState",
    "https://www.disco.com.ar/carnes?initialMap=c&initialQuery=carnes&map=category-1,category-2,category-2,category-2,category-2,category-2,category-2,category-2&page=5&query=/carnes/carne-de-cerdo/carne-vacuna/cordero-lechon-chivito-y-conejo/embutidos/listos-para-cocinar/menudencias/pollos&searchState",
    "https://www.disco.com.ar/carnes?initialMap=c&initialQuery=carnes&map=category-1,category-2,category-2,category-2,category-2,category-2,category-2,category-2&page=6&query=/carnes/carne-de-cerdo/carne-vacuna/cordero-lechon-chivito-y-conejo/embutidos/listos-para-cocinar/menudencias/pollos&searchState"

]

productos = []

# Función para desplazarse hacia abajo y cargar todos los productos
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_products_loaded = True
    attempts = 0  # Contador para asegurar un número de intentos razonable

    while new_products_loaded and attempts < 10:  # Limitar el número de intentos para evitar bucles infinitos
        driver.execute_script("window.scrollBy(0, 500);")  # Desplazarse en pequeños incrementos
        time.sleep(2)  # Espera adaptativa para permitir la carga de productos

        # Verificar si se han cargado nuevos productos
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempts += 1  # Incrementa el contador si no hay nuevos productos
        else:
            last_height = new_height
            attempts = 0  # Reinicia el contador si se cargan nuevos productos

        # Esperar explícitamente hasta que se carguen los productos nuevos visibles
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')))
        except:
            print("Esperando más productos...")

# Función para cerrar el popup si existe
def cerrar_popup():
    try:
        popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnNoIdWpnPush')))
        if popup:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnNoIdWpnPush'))).click()
            print("Popup cerrado.")
    except:
        print("No se encontró el popup o ya fue cerrado anteriormente.")

# Función para capturar datos de la página
def extraer_datos():
    try:
        # Esperar dinámicamente hasta que los nombres de los productos sean visibles
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')))
        nombres = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')
        precios = driver.find_elements(By.XPATH, '//div[contains(@id, "priceContainer")]')

        for nombre, precio in zip(nombres, precios):
            productos.append({
                'Producto': nombre.text.strip(),
                'Precio': precio.text.strip()
            })
    except Exception as e:
        print(f"Error al extraer datos: {e}")

# Iterar sobre todas las URLs
for url in urls:
    driver.get(url)
    time.sleep(5)  # Esperar un poco para que la página cargue antes de intentar cerrar el popup
    cerrar_popup()  # Intentar cerrar popup si aparece
    scroll_to_bottom()  # Asegurarse de que todos los productos se carguen
    extraer_datos()

# Crear DataFrame con los datos
df = pd.DataFrame(productos)

# Limpiar los datos de la columna 'Precio'
df['Precio'] = df['Precio'].str.replace('[\$,]', '', regex=True)

# Guardar los datos en un archivo CSV
df.to_csv('cac.csv', index=False)

driver.quit()
print("Datos guardados en productos.csv")

# Crear DataFrame con los datos
df = pd.DataFrame(productos)

# Limpiar los datos de la columna 'Precio'
df['Precio'] = df['Precio'].str.replace('[\$,]', '', regex=True)

# Eliminar filas duplicadas
df = df.drop_duplicates(subset=['Producto', 'Precio'])

# Guardar los datos en un archivo CSV
df.to_csv('cac.csv', index=False)

driver.quit()
print("Datos guardados en productos.csv")
