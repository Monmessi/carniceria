from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Configura el servicio de geckodriver
service = Service('/opt/homebrew/bin/geckodriver')

# Configura el navegador
driver = webdriver.Firefox(service=service)

# URL de Google Maps para la carnicería
url = "https://www.google.com/search?q=la+josefina+carniceria&client=firefox-b-d&sca_esv=9515d3d099d8bbdb&sxsrf=ADLYWIIypOr6pbaFOnDjdvYS7Up6aSVrcw%3A1725025656415&ei=eM3RZpqKGfTB5OUP04-ngQM&gs_ssp=eJwFwTsOgCAMANC4mrg6szhTPmrhCN6CEqqoQYMLx_e9fpC7VOoihYzHC52foDlrtGOHtCgHZGcPjRABItOqjWHGuI13EOfzJc4liBhqyTHVHH5LOxdE&oq=la+josefina+carn&gs_lp=Egxnd3Mtd2l6LXNlcnAiEGxhIGpvc2VmaW5hIGNhcm4qAggAMg4QLhiABBjHARiOBRivATIGEAAYFhgeMgYQABgWGB4yCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMh0QLhiABBjHARiOBRivARiXBRjcBBjeBBjgBNgBA0jBFFCYAliSCXABeAGQAQCYAXagAZQEqgEDMS40uAEDyAEA-AEBmAIGoALFBMICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFwgIOEAAYsAMY5AIY1gTYAQHCAhMQLhiABBiwAxhDGMgDGIoF2AECwgIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBAsICGRAuGIAEGLADGNEDGEMYxwEYyAMYigXYAQLCAgsQLhiABBjHARivAcICChAAGIAEGEMYigXCAhEQLhiABBjHARiYBRiOBRivAcICBRAAGIAEwgIKEAAYgAQYFBiHAsICBRAuGIAEmAMAiAYBkAYTugYGCAEQARgJugYGCAIQARgIugYGCAMQARgUkgcDMi40oAfnSA&sclient=gws-wiz-serp#lrd=0x94329f98b6190b45:0xb8800cfb7233ff8c,1,,,,"

# Abre el navegador en la URL
driver.get(url)

# Espera para que cargue el contenido inicial
time.sleep(5)

# Encuentra el contenedor de opiniones para hacer scroll
reviews_container = driver.find_element(By.CSS_SELECTOR, "div.review-dialog-list")

# Realiza scroll dentro del contenedor de opiniones
for _ in range(10):  # Realiza 10 scrolls
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", reviews_container)
    time.sleep(4)  # Espera 4 segundos después de cada scroll

# Encuentra todos los elementos que contienen la calificación dentro del contenedor de opiniones
ratings_elements = reviews_container.find_elements(By.CSS_SELECTOR, "span[aria-label^='Calificación: ']")

# Calcula el número total de estrellas
total_stars = 0
for rating in ratings_elements:
    rating_text = rating.get_attribute("aria-label")
    stars = float(rating_text.split()[1])  # Extrae la calificación numérica
    total_stars += stars

# Encuentra el número total de opiniones
total_reviews = len(ratings_elements)

# Calcula el promedio de estrellas
if total_reviews > 0:
    average_rating = total_stars / total_reviews
    print(f"Promedio de estrellas: {average_rating} basado en {total_reviews} opiniones.")
else:
    print("No se encontraron opiniones.")

# Guarda los resultados en un archivo CSV
with open('opiniones_carniceria.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Carniceria', 'Promedio de Estrellas', 'Número de Opiniones'])
    writer.writerow(['La Josefina Carnicería', average_rating, total_reviews])

print("Los resultados han sido guardados en 'opiniones_carniceria.csv'.")

# Cierra el navegador
driver.quit()
