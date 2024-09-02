from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Configuración del driver
service = Service('/opt/homebrew/bin/geckodriver')  # Cambia '/path/to/geckodriver' por la ruta correcta de tu geckodriver
driver = webdriver.Firefox(service=service)

# Lista de URLs y categorías
links = [
    ('https://pedix.app/carnes-cordoba/categoria/SPyuxWndR6AF16pQyo3t', 'Vaca'),
    ('https://pedix.app/carnes-cordoba/categoria/yLgzIRMJJACi6ShIJDz4', 'Cerdo'),
    ('https://pedix.app/carnes-cordoba/categoria/2Ye9V1Db36EIjPsyxRXA', 'Pollo'),
    ('https://pedix.app/carnes-cordoba/categoria/vzUlQxhSZeQ7XrbAP2u8', 'Vaca'),
    ('https://pedix.app/carnes-cordoba/categoria/NC4eUfwamTbFmoPdWDVF', 'Cerdo')
]

# Lista para almacenar los datos
productos = []

# Iterar sobre los enlaces y categorías
for link, categoria in links:
    driver.get(link)
    time.sleep(4)  # Espera 4 segundos para que la página cargue

    # Desplazarse hacia abajo para cargar más productos
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)  # Espera para cargar más productos
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extraer nombres y precios de los productos
    try:
        nombres = driver.find_elements(By.CSS_SELECTOR, "h2.product-name")
        precios = driver.find_elements(By.CSS_SELECTOR, "span.current-price")

        # Asegurarse de que la longitud de nombres y precios coincida
        for nombre, precio in zip(nombres, precios):
            productos.append({
                'Nombre': nombre.text.strip(),
                'Precio': precio.text.strip(),
                'Categoría': categoria
            })

    except Exception as e:
        print(f"Error al extraer datos de {link}: {e}")

# Guardar los datos en un archivo CSV
with open('productos_carnes.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Nombre', 'Precio', 'Categoría'])
    writer.writeheader()
    writer.writerows(productos)

# Cerrar el navegador
driver.quit()

print("Datos guardados en 'productos_carnes.csv'.")
