from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import csv
import time

# Configuración del driver de Selenium
driver = webdriver.Firefox()

# URL de la página de donde vas a hacer el scraping
url = 'https://www.cordiez.com.ar/sucursales'
driver.get(url)

# Esperar hasta que el emergente esté presente y cerrarlo si aparece
try:
    # Esperar que el botón de cerrar aparezca y hacer clic en él
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'cn_close'))  # Ajusta el selector según sea necesario
    )
    close_button.click()
    print("Elemento emergente cerrado.")
except Exception as e:
    print("No se encontró ningún elemento emergente o no se pudo cerrar. Continuando de todas formas...")

# Esperar hasta que los selectores de provincia y departamentos estén presentes
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'sucursales-select-provinces'))
)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'sucursales-select-departments'))
)

# Seleccionar la provincia de Córdoba (con el acento correcto)
select_provincia = Select(driver.find_element(By.ID, 'sucursales-select-provinces'))

# Seleccionar la opción 'Córdoba' con acento
try:
    select_provincia.select_by_visible_text('Córdoba')
except NoSuchElementException:
    print("No se encontró la opción 'Córdoba'. Por favor verifica el texto exacto.")
    driver.quit()
    exit()

# Obtener todos los departamentos disponibles en el select
select_departamento = Select(driver.find_element(By.ID, 'sucursales-select-departments'))
departamentos = [option.text for option in select_departamento.options]

# Abrir o crear un archivo CSV para guardar los datos
with open('sucursales_cordoba.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Provincia', 'Departamento', 'Sucursal', 'Dirección'])  # Escribir encabezados

    # Iterar sobre cada departamento
    for departamento in departamentos:
        try:
            select_departamento.select_by_visible_text(departamento)
        except ElementClickInterceptedException:
            # Desplazarse a la vista del elemento antes de hacer clic
            driver.execute_script("arguments[0].scrollIntoView(true);", select_departamento)
            select_departamento.select_by_visible_text(departamento)

        # Agregar una pausa para permitir que las sucursales se carguen
        time.sleep(2)

        # Intentar capturar las sucursales, con captura de pantalla en caso de error
        try:
            sucursales = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'sucursales-list__suc'))
            )
        except Exception as e:
            # Captura de pantalla en caso de error
            driver.save_screenshot(f'screenshot_error_{departamento}.png')
            print(f"Error al cargar sucursales para {departamento}: {e}")
            continue  # Saltar al siguiente departamento si hay un error

        # Extraer información de cada sucursal y guardarla en el CSV
        for sucursal in sucursales:
            titulo = sucursal.find_element(By.CLASS_NAME, 'sucursales-list__suc-title').text.strip()
            direccion = sucursal.find_element(By.CLASS_NAME, 'sucursales-list__suc-address').text.strip()
            writer.writerow(['Córdoba', departamento, titulo, direccion])

print("Datos guardados en 'sucursales_cordoba.csv'")

# Cerrar el navegador
driver.quit()
