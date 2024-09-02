from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import csv

# Configuración del WebDriver para Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")
service = Service('/opt/homebrew/bin/geckodriver')

driver = webdriver.Firefox(service=service, options=firefox_options)

# URL de la página a la que queremos acceder
url = "https://docs.google.com/forms/d/e/1FAIpQLSfGw5DJv9HXdPSGphHqt92Au4OkxLkg_S9cFVNLU1BC_UjWvw/viewform?pli=1"
driver.get(url)

# Esperar un tiempo para que la página cargue completamente
time.sleep(5)

# Intentar hacer scroll hasta el final de la página para cargar todas las imágenes
SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Desplazar hacia abajo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    # Calcular la nueva altura de la página y compararla con la anterior
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Seleccionar todas las imágenes utilizando los selectores proporcionados
image_selectors = [
    'img.HxhGpf[src*="lh4.googleusercontent.com"]',
    'img.HxhGpf[src*="lh5.googleusercontent.com"]',
    'img.HxhGpf[src*="lh6.googleusercontent.com"]'
]

# Lista para almacenar las URLs de las imágenes
image_urls = []

for selector in image_selectors:
    try:
        img_element = driver.find_element(By.CSS_SELECTOR, selector)
        img_url = img_element.get_attribute("src")
        image_urls.append(img_url)
    except Exception as e:
        print(f"Error procesando {selector}: {str(e)}")

# Guardar las URLs de las imágenes en un archivo CSV
with open("imagenes.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["URL de la Imagen"])
    for url in image_urls:
        writer.writerow([url])

# Cerrar el WebDriver
driver.quit()

print("Proceso completado. Las URLs de las imágenes se han guardado en 'imagenes.csv'.")
