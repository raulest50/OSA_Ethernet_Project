# Guía de Estilo para OSA Remote Control

## Índice
1. [Introducción](#introducción)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Componentes UI](#componentes-ui)
4. [JavaScript y Cliente](#javascript-y-cliente)
5. [CSS y Estilos](#css-y-estilos)
6. [Patrones Comunes](#patrones-comunes)
7. [Errores Comunes a Evitar](#errores-comunes-a-evitar)

## Introducción

Esta guía de estilo establece las mejores prácticas para el desarrollo y mantenimiento de la aplicación OSA Remote Control. Seguir estas pautas asegurará la consistencia del código, facilitará el mantenimiento y evitará errores comunes.

## Estructura del Proyecto

La aplicación sigue una estructura modular:

```
OSA_Ethernet_Project/
├── app.py                  # Punto de entrada principal
├── assets/                 # Archivos estáticos (JS, CSS, imágenes)
├── callbacks/              # Callbacks de Dash
├── components/             # Componentes UI reutilizables
├── layouts/                # Layouts y templates
├── pages/                  # Páginas de la aplicación
└── utils/                  # Utilidades y funciones auxiliares
```

### Principios Generales

1. **Modularidad**: Cada módulo debe tener una responsabilidad única y bien definida.
2. **Reutilización**: Crear componentes reutilizables para evitar duplicación de código.
3. **Separación de Responsabilidades**: Separar la lógica de la UI, la lógica de negocio y la gestión de datos.

## Componentes UI

### Uso de Componentes Refactorizados

Siempre use los componentes refactorizados en lugar de los componentes base de Dash o dbc:

✅ **Correcto**:
```python
from components.buttons import create_button

create_button("Explorar", id="browse-button", color="secondary", icon="folder2-open")
```

❌ **Incorrecto**:
```python
import dash_bootstrap_components as dbc
from dash import html

dbc.Button([html.I(className="bi bi-folder2-open me-2"), "Explorar"], id="browse-button", color="secondary")
```

### Creación de Componentes

Los componentes deben seguir estas pautas:

1. **Documentación**: Incluir docstrings que describan el propósito, parámetros y valor de retorno.
2. **Parámetros Opcionales**: Usar valores predeterminados para parámetros opcionales.
3. **Consistencia**: Mantener nombres de parámetros consistentes entre componentes similares.

### Componentes Disponibles

Utilice los componentes refactorizados disponibles en los siguientes módulos:

- `components.buttons`: Botones y grupos de botones
- `components.forms`: Campos de formulario, dropdowns, etc.
- `components.cards`: Tarjetas y contenedores
- `components.alerts`: Alertas y mensajes
- `components.graphs`: Gráficos y visualizaciones

## JavaScript y Cliente

### Organización del Código JavaScript

El código JavaScript debe organizarse en archivos específicos en la carpeta `assets/`:

- `client_callbacks.js`: Callbacks del lado del cliente para interacciones UI inmediatas
- `file_selector.js`: Funcionalidad para selección de archivos/carpetas
- Otros archivos JS específicos para funcionalidades concretas

### Callbacks del Lado del Cliente

Los callbacks del lado del cliente deben:

1. Estar organizados en el namespace `window.dash_clientside`
2. Tener documentación JSDoc clara
3. Manejar adecuadamente los casos de error y valores nulos

✅ **Correcto**:
```javascript
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    namespace: {
        /**
         * Descripción de la función
         * @param {type} param - Descripción
         * @returns {type} - Descripción
         */
        functionName: function(param) {
            if (!param) return null;
            // Implementación
            return result;
        }
    }
});
```

### Integración con Dash

Para registrar callbacks del lado del cliente en Dash:

```python
clientside_callback(
    """
    window.dash_clientside.namespace.functionName
    """,
    Output("output-id", "property"),
    Input("input-id", "property"),
    prevent_initial_call=True
)
```

## CSS y Estilos

### Organización de Estilos

Los estilos deben organizarse de la siguiente manera:

1. **Estilos Globales**: En `assets/custom.css`
2. **Estilos Específicos de Componentes**: En secciones claramente comentadas
3. **Estilos Inline**: Evitar en lo posible, usar solo para ajustes menores específicos

### Clases de Bootstrap

Aprovechar las clases de Bootstrap para:

- Espaciado (`m-*`, `p-*`)
- Flexbox (`d-flex`, `justify-content-*`)
- Grid (`row`, `col-*`)
- Utilidades (`text-*`, `bg-*`)

## Patrones Comunes

### Creación de Elementos con Iconos

Para crear elementos con iconos, use listas en lugar de concatenación:

✅ **Correcto**:
```python
content = [html.I(className=f"bi bi-{icon} me-2"), text]
```

❌ **Incorrecto**:
```python
content = html.I(className=f"bi bi-{icon} me-2") + text  # ¡Error! No se puede concatenar elementos HTML con strings
```

### Manejo de Componentes Dinámicos

Para componentes que se crean dinámicamente:

1. Usar `dcc.Store` para almacenar datos intermedios
2. Crear componentes completos en callbacks
3. Devolver componentes enteros en lugar de propiedades individuales cuando sea posible

## Errores Comunes a Evitar

### 1. Concatenación de Elementos HTML

No se pueden concatenar elementos HTML directamente con strings usando el operador `+`. Use listas en su lugar.

❌ **Incorrecto**:
```python
html.I(className="bi bi-folder2-open me-2") + "Explorar"  # TypeError
```

✅ **Correcto**:
```python
[html.I(className="bi bi-folder2-open me-2"), "Explorar"]
```

### 2. Uso Directo de Componentes Base

Evite usar directamente componentes base de Dash o dbc cuando existen componentes refactorizados.

❌ **Incorrecto**:
```python
dbc.Button("Guardar", id="save-button", color="success")
```

✅ **Correcto**:
```python
create_success_button("Guardar", id="save-button")
```

### 3. Mezcla de Estilos de Componentes

No mezcle diferentes estilos para componentes similares. Mantenga la consistencia.

❌ **Incorrecto**:
```python
# En una parte del código
create_button("Acción 1", color="primary")

# En otra parte
dbc.Button("Acción 2", color="primary")
```

### 4. Callbacks Innecesarios del Lado del Servidor

Para interacciones UI simples, use callbacks del lado del cliente en lugar de callbacks del servidor.

✅ **Preferido para UI simple**:
```python
clientside_callback(
    """
    function(value) { return value ? false : true; }
    """,
    Output("element", "disabled"),
    Input("condition", "value")
)
```

### 5. Falta de Manejo de Errores en Callbacks

Siempre incluya manejo de errores en callbacks, especialmente aquellos que interactúan con recursos externos.

✅ **Correcto**:
```python
@callback(...)
def my_callback(input_value):
    try:
        # Lógica principal
        return result
    except Exception as e:
        # Manejo de error
        return f"Error: {str(e)}"
```