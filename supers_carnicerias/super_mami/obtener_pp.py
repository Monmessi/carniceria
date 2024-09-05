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
url_base = 'https://www.dinoonline.com.ar/super/categoria/supermami-fresco-carnes/_/N-h5mno0?Nf=product.endDate%7CGTEQ+1.7252352E12%7C%7Cproduct.startDate%7CLTEQ+1.7252352E12&No={}&Nr=AND%28product.disponible%3ADisponible%2Cproduct.language%3Aespa%C3%B1ol%2Cproduct.priceListPair%3AsalePrices_listPrices%2COR%28product.siteId%3AsuperSite%29%29&Nrpp=36'

# Contador de páginas
pagina = 1

# Navegar a la primera página
driver.get(url_base.format(0))

# Esperar a que la página se cargue completamente
time.sleep(6)

# Preparar archivo CSV para guardar los datos
with open('Supermami.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Nombre_Producto', 'Precio']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Definir el desplazamiento en píxeles
    desplazamiento_pixeles = 3250  # Ajusta el número de píxeles según sea necesario

    # Loop para navegar a través de las páginas
    while True:
        try:
            # Esperar hasta que los productos estén cargados
            WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'description.limitRow.tooltipHere'))
            )

            # Extraer nombres de los productos
            productos = driver.find_elements(By.CSS_SELECTOR, ".description.limitRow.tooltipHere")

            # Extraer precios de los productos
            precios = driver.find_elements(By.CSS_SELECTOR, ".precio-unidad span")

            # Filtrar precios válidos que contienen el símbolo "$"
            precios_filtrados = [precio for precio in precios if "$" in precio.text]

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
            driver.execute_script(f"window.scrollBy(0, {desplazamiento_pixeles});")  # Desplazar el número de píxeles definido

            # Esperar a que se cargue más contenido
            time.sleep(3)

            # Incrementar el contador de páginas
            pagina += 1

            # Navegar a la siguiente página usando el número de página en la URL
            driver.get(url_base.format((pagina - 1) * 36))  # Cada página tiene 36 elementos, ajusta si es necesario

            # Esperar a que la nueva página se cargue completamente
            time.sleep(6)
            
        except Exception as e:
            print(f"Error: {e}")
            break

# Cerrar el navegador
driver.quit()

print("Scraping completado y guardado en Supermami.csv.")
