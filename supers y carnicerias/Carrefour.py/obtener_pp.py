from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Configuración del navegador (usa Firefox con Geckodriver)
service = Service('/opt/homebrew/bin/geckodriver')  # Cambia a la ruta donde está geckodriver
driver = webdriver.Firefox(service=service)

# URL inicial
url = 'https://www.carrefour.com.ar/Carnes-y-Pescados?page=1'
driver.get(url)

# Esperar a que la página se cargue completamente
time.sleep(6)

# Intentar cerrar el pop-up repetidamente hasta que ya no esté presente
for intento in range(1):  # Cambiado a 1 intento según tu ajuste
    try:
        # Esperar a que el pop-up aparezca completamente
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'onetrust-close-btn-container'))
        )
        
        # Usar JavaScript para hacer clic en el botón de cierre
        pop_up_close_button = driver.find_element(By.CLASS_NAME, 'onetrust-close-btn-handler')
        driver.execute_script("arguments[0].click();", pop_up_close_button)
        print("Pop-up cerrado exitosamente con JavaScript.")
        time.sleep(2)  # Espera para asegurarse de que el pop-up esté completamente cerrado
        
        # Verificar si el pop-up sigue presente
        if not driver.find_elements(By.CLASS_NAME, 'onetrust-close-btn-handler'):
            break  # Salir del bucle si el pop-up se ha cerrado
    except Exception as e:
        print(f"Intento {intento + 1}: No se encontró o no se pudo cerrar el pop-up: {e}")
        time.sleep(2)  # Espera y reintenta

# Preparar archivo CSV para guardar los datos
with open('Carrefour.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Nombre_Producto', 'Precio']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop para navegar a través de las páginas
    pagina = 1
    while True:
        try:
            # Esperar hasta que los productos estén cargados
            WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'vtex-flex-layout-0-x-flexColChild--wrapPrice'))
            )

            # Extraer nombres de los productos
            productos = driver.find_elements(By.CSS_SELECTOR, ".vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body")

            # Usar selectores específicos para capturar solo los precios reales
            precios_selector_1 = driver.find_elements(By.CSS_SELECTOR, ".valtech-carrefourar-product-price-0-x-sellingPriceValue")
            precios_selector_2 = driver.find_elements(By.CSS_SELECTOR, ".vtex-flex-layout-0-x-flexColChild.vtex-flex-layout-0-x-flexColChild--wrapPrice.pb0 .valtech-carrefourar-product-price-0-x-sellingPriceValue")

            # Combinar los precios de ambos selectores en una lista única
            precios = precios_selector_1 + precios_selector_2

            # Filtrar precios válidos que contienen el símbolo "$" y excluir aquellos con "%"
            precios_filtrados = [precio for precio in precios if "$" in precio.text and "%" not in precio.text]

            if not productos or not precios_filtrados:  # Verificar si no se encontraron productos/precios
                print("No se encontraron productos o precios en la página actual.")
                break

            # Asegurarse de que la longitud de los productos y precios coincida
            min_length = min(len(productos), len(precios_filtrados))
            productos = productos[:min_length]
            precios_filtrados = precios_filtrados[:min_length]

            for producto, precio in zip(productos, precios_filtrados):
                nombre = producto.text.strip()
                precio_valor = precio.text.strip()
                writer.writerow({'Nombre_Producto': nombre, 'Precio': precio_valor})

            # Esperar antes de desplazarse hacia abajo
            time.sleep(5)

            # Desplazar solo un poco hacia abajo para asegurarse de que se carguen más productos sin saltarse los botones
            driver.execute_script("window.scrollBy(0, 1500);")  # Desplazar solo 1500 píxeles

            # Esperar a que se cargue más contenido
            time.sleep(3)

            # Encontrar el botón de siguiente página y hacer clic si está visible
            boton_siguiente = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f"button.vtex-button[value='{pagina + 1}']"))
            )
            boton_siguiente.click()

            # Esperar a que la nueva página se cargue completamente
            time.sleep(6)
            
            # Incrementar el contador de páginas
            pagina += 1

        except Exception as e:
            print(f"Error: {e}")
            break

# Cerrar el navegador
driver.quit()

print("Scraping completado y guardado en Carrefour.csv.")
