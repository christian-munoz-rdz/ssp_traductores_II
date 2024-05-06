# Compilador: Fase de Generación de Análisis semántico

## Modulo de análisis semántico

Agrgué un modulo llamado `SemanticAnalyser` para realizar comprobaciones semánticas. Esta clase utiliza otras clases y módulos para gestionar la tabla de símbolos y la memoria durante la compilación.

### Inicialización y Estructuras de Datos
- **Tablas de Símbolos y Manejo de Memoria**: `SemanticAnalyser` interactúa con `SymbolTableManager` y `MemoryManager` para manipular el entorno de símbolos y la asignación de memoria respectivamente.
- **Diccionarios y Pilas**: Utiliza diccionarios para almacenar rutinas semánticas específicas y varias pilas para manejar la verificación de tipos, argumentos de funciones, y otros aspectos relacionados con el alcance y el contexto de uso de las variables y funciones.

### Rutinas Semánticas
- **Rutinas de Alcance**: Incrementa (`inc_scope_routine`) o decrementa (`dec_scope_routine`) el alcance actual en la tabla de símbolos, lo que afecta a la visibilidad de las variables y funciones.
- **Manejo de Tipos y Variables**: Guarda tipos de datos y asigna estos tipos a las variables o funciones según el contexto. Por ejemplo, `save_type_routine` y `assign_type_routine`.
- **Verificación de la Función `main`**: Verifica que exista una función `main` adecuadamente definida y que sea la última función definida en el nivel global (`check_main_routine`).
- **Manejo de Funciones y Argumentos**: Guarda las características de las funciones y verifica la adecuación de los argumentos pasados a estas (`save_fun_routine`, `check_args_routine`).

### Comprobaciones de Error y Gestión de Errores
- **Registro de Errores**: Los errores detectados durante la fase de análisis semántico se almacenan y se pueden escribir en un archivo para su revisión.
- **Verificaciones Finales**: Al final del archivo o del código fuente, verifica si todas las condiciones necesarias para un programa semánticamente correcto se han cumplido, como la presencia y la correcta definición de la función `main`.

### Flujo de Operación
1. **Análisis de Tokens**: Cada token del código fuente es procesado y según su contexto, se invocan las rutinas semánticas correspondientes utilizando un mapa de acciones a rutinas (`semantic_checks`).
2. **Acciones Semánticas**: Las acciones se determinan en base a los símbolos de acción encontrados en el código (p. ej., `#SA_SAVE_TYPE`), y se ejecutan las funciones correspondientes que manipulan las estructuras de datos en la tabla de símbolos y verifican la corrección del uso de variables y funciones.
3. **Finalización y Verificación**: Al final del análisis, se revisa que todas las condiciones necesarias para un programa válido se cumplen y se reportan errores si es necesario.

Este módulo es un ejemplo de cómo se pueden estructurar las comprobaciones semánticas en el proceso de compilación, asegurando que el código no solo es sintácticamente correcto sino también semánticamente válido según las reglas del lenguaje de programación.