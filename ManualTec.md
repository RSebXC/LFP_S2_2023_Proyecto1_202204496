# Manual Técnico

## 1. Introducción
Este manual técnico tiene como objetivo proporcionar una descripción detallada de la estructura y funcionamiento del código de la aplicación de analizador de operaciones. El programa está escrito en Python y utiliza las bibliotecas Tkinter y Graphviz para crear una interfaz gráfica y generar gráficos de operaciones matemáticas a partir de archivos JSON.

## 2. Estructura del Código
La aplicación está diseñada en torno a la clase principal llamada GUI. A continuación, se detallan las principales secciones del código:

### 2.1. Configuración de la Interfaz de Usuario
La función `setup_navbar` se encarga de configurar la barra de navegación y los botones en la interfaz de usuario. Esta sección establece el estilo visual de la aplicación y define acciones para eventos de botones.

### 2.2. Gestión de Archivos
Las funciones `load_file`, `save_file`, y `save_file_as` permiten al usuario cargar archivos JSON desde el sistema de archivos, guardar el archivo actual o guardar el contenido con un nuevo nombre.

### 2.3. Análisis de Operaciones
- `analyze_and_show_results`: Realiza el análisis de las operaciones contenidas en el archivo JSON cargado. Los resultados se almacenan y se pueden mostrar al usuario.
- `analyze_operation`: Analiza una operación matemática específica y devuelve su resultado.

### 2.4. Operaciones Matemáticas
Cada operación matemática (suma, resta, multiplicación, división, potencia, raíz, inverso, seno, coseno, tangente y módulo) tiene su propia función de análisis. Estas funciones validan y realizan las operaciones correspondientes.

### 2.5. Generación de Gráficos
La función `generate_graphs` utiliza la biblioteca Graphviz para crear gráficos visuales de las operaciones analizadas. Se aplican configuraciones de apariencia personalizada a los nodos de los gráficos.

### 2.6. Ejecución de la Aplicación
En la sección `if __name__ == "__main__":`, se crea una instancia de la clase GUI y se inicia la aplicación.

## 3. Uso de Configuraciones
Dentro de los archivos JSON que se cargan, es posible especificar configuraciones para la apariencia de los nodos en los gráficos de las operaciones. Los atributos que se pueden configurar son:
- "color-fondo-nodo": Color de fondo del nodo.
- "color-fuente-nodo": Color del texto del nodo.
- "forma-nodo": Forma del nodo.

Las configuraciones se aplican a cada operación individualmente, permitiendo una personalización flexible de la apariencia de los gráficos.
