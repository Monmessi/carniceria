

from flask import Flask, request, render_template, render_template_string, send_from_directory
import folium
import pandas as pd
from geopy.distance import geodesic
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
from folium.plugins import MarkerCluster

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Conexión a la base de datos
def conectar_db():
    try:
        conexion = connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para obtener las carnicerías con coordenadas y precios promedio por categoría
def obtener_carnicerias():
    conexion = conectar_db()
    if not conexion:
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error
    
    query = """
        SELECT s.ID_Sucursal, s.Sucursal, s.Latitud, s.Longitud, sp.Nombre_Supermercado,
               AVG(CASE WHEN p.Categoria = 'Vaca' THEN p.Precio END) AS Promedio_Vaca,
               AVG(CASE WHEN p.Categoria = 'Cerdo' THEN p.Precio END) AS Promedio_Cerdo,
               AVG(CASE WHEN p.Categoria = 'Pollo' THEN p.Precio END) AS Promedio_Pollo
        FROM Sucursales s
        JOIN Productos p ON s.ID_Supermercado = p.ID_Supermercado
        JOIN Supermercados sp ON s.ID_Supermercado = sp.ID_Supermercado
        WHERE s.Latitud IS NOT NULL AND s.Longitud IS NOT NULL
        GROUP BY s.ID_Sucursal;
    """
    carnicerias = pd.read_sql(query, conexion)
    conexion.close()
    return carnicerias

# Función para obtener productos de una sucursal específica
def obtener_productos(id_sucursal):
    conexion = conectar_db()
    if not conexion:
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error
    
    query = """
        SELECT p.Nombre_Producto, p.Categoria, p.Precio, p.Descuento
        FROM Productos p
        JOIN Sucursales s ON p.ID_Supermercado = s.ID_Supermercado
        WHERE s.ID_Sucursal = %s;
    """
    productos = pd.read_sql(query, conexion, params=(id_sucursal,))
    conexion.close()
    return productos

# Función para buscar productos por nombre y mostrar los más baratos
def buscar_productos(nombre_producto):
    conexion = conectar_db()
    if not conexion:
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error
    
    query = """
        SELECT p.Nombre_Producto, p.Categoria, p.Precio, s.Sucursal, sp.Nombre_Supermercado
        FROM Productos p
        JOIN Sucursales s ON p.ID_Supermercado = s.ID_Supermercado
        JOIN Supermercados sp ON s.ID_Supermercado = sp.ID_Supermercado
        WHERE p.Nombre_Producto LIKE %s
        ORDER BY p.Precio ASC;
    """
    productos = pd.read_sql(query, conexion, params=(f"%{nombre_producto}%",))
    conexion.close()
    return productos

# Ruta principal para mostrar el mapa y el buscador
@app.route('/', methods=['GET', 'POST'])
def index():
    carnicerias = obtener_carnicerias()
    
    # Crear un mapa inicial centrado en Córdoba, Argentina
    mapa = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, width='100%', height='100%')
    
    # Crear un objeto de agrupación de marcadores
    marker_cluster = MarkerCluster().add_to(mapa)

    # Agregar marcadores para las carnicerías cercanas
    for _, row in carnicerias.iterrows():
        # Verificar que las coordenadas no sean NULL
        if not pd.isna(row['Latitud']) and not pd.isna(row['Longitud']):
            # Formatear los promedios de precios
            promedio_vaca = f"${row['Promedio_Vaca']:.2f}" if pd.notna(row['Promedio_Vaca']) else "No Disponible"
            promedio_cerdo = f"${row['Promedio_Cerdo']:.2f}" if pd.notna(row['Promedio_Cerdo']) else "No Disponible"
            promedio_pollo = f"${row['Promedio_Pollo']:.2f}" if pd.notna(row['Promedio_Pollo']) else "No Disponible"
            
            # Contenido del popup con promedios formateados
            popup_content = f"""
            <b>{row['Nombre_Supermercado']}</b><br>
            {row['Sucursal']}<br>
            Promedio Vaca: {promedio_vaca}<br>
            Promedio Cerdo: {promedio_cerdo}<br>
            Promedio Pollo: {promedio_pollo}<br>
            <a href='/productos/{row['ID_Sucursal']}' target='_blank'>Ver Productos</a>
            """
            folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=popup_content,
                icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
            ).add_to(marker_cluster)  # Agregar al cluster en lugar del mapa directamente

    # Guardar el mapa en un archivo HTML en la carpeta templates
    mapa.save(os.path.join(app.root_path, 'templates', 'mapa.html'))  # Aquí colocamos esta línea

    # Formulario de búsqueda de productos
    if request.method == 'POST':
        producto_buscado = request.form.get('producto')
        resultados = buscar_productos(producto_buscado)
        return render_template_string(f"""
        <html>
            <head>
                <title>Mapa de Carnicerías</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container">
                    <h2>Resultados de la búsqueda: {producto_buscado}</h2>
                    {resultados.to_html(classes='table table-striped', index=False)}
                    <a href="/">Volver al mapa</a>
                </div>
            </body>
        </html>
        """)

    # Renderizar la página principal con el mapa y la barra de búsqueda
    return render_template_string("""
    <html>
        <head>
            <title>Mapa de Carnicerías</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                #map-container {
                    display: flex;
                    justify-content: center; /* Centrar horizontalmente */
                    margin-top: 20px; /* Espacio desde arriba */
                }
                #map {
                    width: 80%;
                    height: 600px; /* Ajusta la altura del mapa */
                    border: 2px solid #ddd;
                }
                #search-container {
                    text-align: center; /* Centrar el formulario de búsqueda */
                    margin-top: 30px; /* Espacio arriba del formulario */
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div id="search-container">
                    <form method="POST" class="form-inline mt-3">
                        <input type="text" name="producto" class="form-control" placeholder="Buscar producto...">
                        <button type="submit" class="btn btn-primary ml-2">Buscar</button>
                    </form>
                </div>
                <div id="map-container">
                    <iframe id="map" src="/mapa" style="border:none;"></iframe> <!-- Cambiar ruta a /mapa -->
                </div>
            </div>
        </body>
    </html>
    """)

# Ruta para servir el archivo mapa.html
@app.route('/mapa')
def servir_mapa():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'mapa.html')

# Ruta para mostrar los productos de una sucursal específica
@app.route('/productos/<int:id_sucursal>', methods=['GET'])
def mostrar_productos(id_sucursal):
    productos = obtener_productos(id_sucursal)
    if productos.empty:
        return "<h3>No se encontraron productos para esta sucursal.</h3>", 404

    # Renderizar los productos en una tabla HTML
    productos_html = productos.to_html(classes='table table-striped', index=False)
    return render_template_string(f"""
    <html>
        <head>
            <title>Productos de la Sucursal {id_sucursal}</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h2>Productos de la Sucursal {id_sucursal}</h2>
                {productos_html}
            </div>
        </body>
    </html>
    """)

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
