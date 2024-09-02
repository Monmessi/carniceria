from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os


'''''este codigo no dunciona, es un intento de categorizar los productos de cordiez'''

# Configuración del WebDriver para Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")
service = Service('/opt/homebrew/bin/geckodriver')

driver = webdriver.Firefox(service=service, options=firefox_options)

# Directorio para guardar las capturas de pantalla
screenshot_dir = "capturas"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def guardar_captura(paso):
    screenshot_path = os.path.join(screenshot_dir, f"captura_{paso}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Captura guardada: {screenshot_path}")

# Abre la página de la categoría "Carnes"
driver.get('https://www.cordiez.com.ar/carnes')
guardar_captura("inicio")

# Espera 30 segundos para que el popup aparezca
time.sleep(30)

# Intentar cerrar el popup
try:
    popup_close_button = driver.find_element(By.CSS_SELECTOR, "div.cn_content_close-800d0b5f-8980-4509-a495-6e79f7840739 svg")
    popup_close_button.click()
    print("Popup cerrado exitosamente.")
    guardar_captura("popup_cerrado")
except Exception as e:
    print("No se encontró el popup o no se pudo cerrar:", e)
    guardar_captura("popup_no_encontrado")

try:
    # Espera explícita para que las categorías estén presentes
    wait = WebDriverWait(driver, 30)
    category_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.text-filters a')))

    # Guardar captura después de intentar encontrar las categorías
    guardar_captura("despues_captura_categorias")

    # Verificar que se encontraron enlaces de categoría
    print(f"Se encontraron {len(category_links)} categorías.")

    all_products = []

    for idx, link in enumerate(category_links):
        category_name = link.text.strip()
        category_url = link.get_attribute('href')

        print(f"Visitando la categoría: {category_name} - {category_url}")

        # Visitar la categoría
        driver.get(category_url)
        guardar_captura(f"visitando_categoria_{idx}")

        # Espera explícita para que los productos estén presentes
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product')))

        # Simular el desplazamiento hacia abajo para cargar todos los productos
        last_height = driver.execute_script("return document.body.scrollHeight")
        SCROLL_PAUSE_TIME = 5

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                for _ in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height > last_height:
                        last_height = new_height
                        break
                else:
                    break
            else:
                last_height = new_height

        guardar_captura(f"productos_cargados_{idx}")

        # Captura todos los contenedores de productos después del desplazamiento
        product_containers = driver.find_elements(By.CLASS_NAME, 'product')

        # Verificar que se encontraron productos
        print(f"Se encontraron {len(product_containers)} productos en la categoría: {category_name}")

        for container in product_containers:
            name = container.find_element(By.TAG_NAME, 'h5').text
            price_elements = container.find_elements(By.CLASS_NAME, 'offer-price')
            if price_elements:
                price = price_elements[0].text
            else:
                price = "N/A"

            all_products.append({
                'Producto': name,
                'Precio': price,
                'Categoría': category_name
            })

    # Crear un DataFrame con todos los productos
    df = pd.DataFrame(all_products)

    # Guardar captura antes de limpiar los precios
    guardar_captura("antes_limpiar_precios")

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
    if 'Precio' in df.columns:
        df[['Precio', 'Descuento']] = df['Precio'].apply(lambda x: pd.Series(limpiar_precio(x)))
    else:
        print("La columna 'Precio' no se encontró en el DataFrame.")

    # Guardar el nuevo DataFrame en un archivo CSV
    df.to_csv('productos_cordiez_categorias_limpio.csv', index=False)

    # Mostrar el DataFrame para verificar
    print(df)

finally:
    # Guardar captura en caso de error
    guardar_captura("error_ocurrido")

    # Cierra el WebDriver
    driver.quit()
