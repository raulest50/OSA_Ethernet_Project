# OSA Remote Control

## Descripción
Este proyecto permite conectarse con un Analizador de Espectro Óptico (OSA) de Yokogawa mediante TCP/IP sobre Ethernet. La aplicación proporciona una interfaz gráfica web construida con Dash para visualizar y analizar datos de espectroscopía por reflexión difusa.

## Características
- Interfaz de usuario intuitiva con panel de navegación lateral colapsable
- Múltiples páginas para diferentes funcionalidades
- Conexión TCP/IP con OSA Yokogawa AQ6370D
- Adquisición de datos espectrales
- Procesamiento de datos para análisis de reflectancia
- Visualización interactiva mediante interfaz web Dash
- Soporte para archivos de referencia (.dpt) y mediciones (.csv)
- Componentes reutilizables para una mejor organización del código

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar el mantenimiento y la escalabilidad:

```
OSA_Ethernet_Project/
├── app.py                  # Punto de entrada principal de la aplicación
├── assets/                 # Archivos estáticos (CSS, imágenes, etc.)
│   ├── custom.css          # Estilos personalizados
│   └── logo_final.svg      # Logo del grupo de investigación
├── callbacks/              # Callbacks de Dash
│   ├── __init__.py         # Inicializador del paquete
│   └── update_graphs.py    # Callbacks para actualizar gráficos y UI
├── components/             # Componentes reutilizables
│   ├── __init__.py         # Inicializador del paquete
│   ├── alerts.py           # Componentes de alertas
│   ├── buttons.py          # Componentes de botones
│   ├── cards.py            # Componentes de tarjetas
│   ├── forms.py            # Componentes de formularios
│   └── graphs.py           # Componentes de gráficos
├── layouts/                # Layouts de la aplicación
│   ├── __init__.py         # Inicializador del paquete
│   ├── index_template.py   # Plantilla HTML para la aplicación
│   └── main_layout.py      # Layout principal de la aplicación
├── pages/                  # Páginas de la aplicación
│   ├── __init__.py         # Inicializador del paquete
│   ├── adquisicion_datos.py        # Página de adquisición de datos
│   ├── home.py                     # Página de inicio
│   └── preprocesamiento_visualizacion.py  # Página de preprocesamiento
├── utils/                  # Utilidades
│   ├── __init__.py         # Inicializador del paquete
│   ├── data_processing.py  # Funciones de procesamiento de datos
│   └── osa_connection.py   # Funciones de conexión con el OSA
├── OsaMain.py              # Script para conexión directa con el OSA
├── OSA_Data/               # Directorio para almacenar datos adquiridos
└── ref_data/               # Directorio con archivos de referencia
```

## Componentes Reutilizables

El proyecto utiliza componentes reutilizables para mantener el código limpio y facilitar el mantenimiento:

- **Alertas**: Componentes para mostrar mensajes informativos, de éxito, advertencia o error
- **Botones**: Componentes para crear botones con diferentes estilos y funcionalidades
- **Tarjetas**: Componentes para crear tarjetas con diferentes estilos y contenido
- **Formularios**: Componentes para crear campos de entrada, desplegables y otros elementos de formulario
- **Gráficos**: Componentes para crear y mostrar gráficos

## Requisitos
- Python 3.12 o superior
- Dependencias gestionadas por Poetry (ver sección de instalación)

## Instalación

### 1. Clonar el repositorio
```
git clone <url-del-repositorio>
cd OSA_Ethernet_Project
```

### 2. Instalar dependencias con Poetry
Asegúrate de tener [Poetry](https://python-poetry.org/docs/#installation) instalado, luego ejecuta:
```
poetry install --no-root
```

Alternativamente, puedes instalar las dependencias con pip:
```
pip install -r requirements.txt
```

### 3. Activar el entorno virtual (si usas Poetry)
```
poetry shell
```

## Uso

### Iniciar la aplicación web
```
python app.py
```
La aplicación estará disponible en http://localhost:8050

### Adquisición de datos del OSA
Para adquirir datos directamente del OSA Yokogawa:
```
python OsaMain.py
```

## Configuración
Para cambiar la dirección IP y puerto del OSA, modifica las siguientes líneas en `OsaMain.py`:
```python
device_address = "168.176.118.22"
device_port = 10001
```

## Contacto
Esteban - raulest50@gmail.com
