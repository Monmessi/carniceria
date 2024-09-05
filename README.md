# carniceria

estoy haciendo una base de datos SQL llamada carnes, la cual va a tener todos los datos de las carnicerias de cordoba. varios datos los consegui scrapeando paginas web utilizando selenium desde python. suelo crear un archivo csv una vez scrapeada la pagina, para ver los resultados. si estos estan correctos luego los inserto en la base de datos.  

- *Generate project structure*:
    bash
  tree --prune -I 'venv|__pycache__|*.pyc|*.pyo|*.log|*.db|*.sqlite|*.egg-info|__init__.py|node_modules|build|*.js.map|*.css.map' > project_structure.txt

  .

├── README.md
├── carnes.sql
├── project_structure.txt
├── requirements.txt
└── supers_carnicerias
    ├── Blackbull
    │   ├── categorizar.py
    │   ├── insertar_db.py
    │   ├── obtener_pp.py
    │   └── obtenercsv.py
    ├── CarnesCordoba
    │   ├── Insertar_db.py
    │   ├── limpiarcsv.py
    │   └── obtener_pp.py
    ├── Carrefour.py
    │   ├── importar_pp.py
    │   └── obtener_pp.py
    ├── Cordiez
    │   ├── Cordiez_productos.py
    │   ├── cordiez_iterador.py
    │   ├── csv
    │   │   ├── productos_cordiez_con_descuento_separado.csv
    │   │   └── sucursales_cordoba_cordiez.csv
    │   └── direccion_cordiez.py
    ├── Disco
    │   ├── guardardic.py
    │   ├── guardarpp_bd.py
    │   └── obtener_pp.py
    ├── DoblePechuga
    │   └── Obtener_pp.py
    ├── DonJulio
    │   └── Obtener_pp.py
    ├── ElTori
    │   └── obtener_pp.py
    ├── Farmers_market
    │   └── leer_img.Py
    ├── Hiper
    │   └── obtener_pp.py
    ├── Josefina_carnes
    │   └── opiniones.py
    ├── Los amigos
    │   └── obtener_pp.py
    ├── MercadoCarnes
    │   └── obtener_pp.py
    ├── SanCayetano
    │   ├── limpiarcsv.py
    │   └── obtener_pp.py
    ├── caravana.py
    │   ├── leer_img.py
    │   └── obtener_pp.py
    ├── minimercado_MH
    │   ├── obtener_pp.py
    │   └── obtener_pp2.py
    └── super_mami
        └── obtener_pp.py

20 directories, 39 files

