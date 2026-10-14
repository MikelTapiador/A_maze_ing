*This project has been created as part of the 42 curriculum by mtapiado, arabago-.*

# A-Maze-ing — This is the way

## Description

**A-Maze-ing** es un proyecto desarrollado como parte del currículo de 42 cuyo objetivo es generar, resolver y representar laberintos en una terminal.

El programa permite definir las dimensiones de un laberinto, establecer las coordenadas de entrada y salida, generar su estructura mediante diferentes algoritmos y encontrar un camino que conecte ambos puntos.

El proyecto combina algoritmos, estructuras de datos, validación de configuraciones y representación visual mediante caracteres Unicode y colores ANSI en la terminal.

La aplicación está organizada en componentes independientes para separar la gestión de la configuración, la generación del laberinto, la búsqueda de una solución y su representación visual. Esta separación facilita el mantenimiento, las pruebas y la incorporación de nuevas funcionalidades.

Entre sus principales características se encuentran:

- Generación de laberintos con dimensiones configurables.
- Definición de las posiciones de entrada y salida.
- Generación reproducible mediante una semilla aleatoria.
- Posibilidad de generar laberintos perfectos.
- Selección entre dos algoritmos de generación: DFS y Prim.
- Resolución del laberinto mediante el algoritmo BFS.
- Representación del laberinto en la terminal mediante caracteres y colores.
- Visualización opcional del camino de la solución.
- Opciones de visualización y animación.
- Exportación del laberinto a un archivo de salida.
- Menú interactivo para gestionar las opciones disponibles y reiniciar la generación.

## Instructions

### Requirements

Para ejecutar el proyecto se necesita:

- Python 3.10 o una versión compatible con las dependencias del proyecto.
- Las dependencias definidas en los archivos de configuración del repositorio.
- Un terminal compatible con secuencias ANSI y caracteres Unicode para visualizar correctamente los colores, las paredes y los símbolos utilizados.

Se recomienda utilizar un entorno virtual para mantener aisladas las dependencias del proyecto.

### Installation

Clona el repositorio y accede al directorio del proyecto:

```bash
git clone <repository-url>
cd A_maze_ing
```

Instala las dependencias mediante Poetry:

```bash
python3 -m poetry install
```

Este comando instala las dependencias definidas en la configuración del proyecto.

### Execution

Ejecuta el programa desde el directorio raíz del proyecto:

```bash
python3 -m poetry run python main.py
```

Si las dependencias ya están instaladas y el entorno correspondiente está activado, también puedes ejecutar el programa directamente:

```bash
python3 main.py
```

Al iniciarse, el programa carga y valida los parámetros de configuración, genera el laberinto, calcula una solución y muestra el resultado en la terminal.

Una vez finalizada la representación, el usuario puede utilizar el menú interactivo para seleccionar las opciones disponibles, como reiniciar la generación o modificar la visualización.

Antes de ejecutar el programa, comprueba que el archivo de configuración se encuentra en la ubicación esperada y contiene valores válidos.

### Configuration File

El comportamiento del programa se controla mediante un archivo de configuración que define las dimensiones del laberinto, la entrada, la salida, el archivo de resultados y las opciones de generación.

El archivo utiliza el formato `KEY=VALUE`, con un parámetro por línea.

#### Configuration Example

```ini
WIDTH=5
HEIGHT=5
ENTRY=0,0
EXIT=4,5
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=100
ALGORITHM=DFS
```

#### Configuration Parameters

| Parameter | Description |
|---|---|
| `WIDTH` | Anchura del laberinto, expresada en número de celdas. |
| `HEIGHT` | Altura del laberinto, expresada en número de celdas. |
| `ENTRY` | Coordenadas de la entrada, en formato `x,y`. |
| `EXIT` | Coordenadas de la salida, en formato `x,y`. |
| `OUTPUT_FILE` | Nombre o ruta del archivo donde se guarda el laberinto. |
| `PERFECT` | Indica si se debe generar un laberinto perfecto. |
| `SEED` | Semilla utilizada para controlar la generación aleatoria. |
| `ALGORITHM` | Algoritmo de generación seleccionado: `DFS` o `PRIM`. Por defecto, se utiliza `DFS`. |

#### Configuration Rules

- Las dimensiones deben respetar los límites establecidos por el programa.
- La entrada y la salida deben tener el formato de coordenadas esperado.
- Las posiciones de entrada y salida deben cumplir las reglas de ubicación definidas por el proyecto.
- `PERFECT` debe utilizar uno de los valores booleanos admitidos por el validador.
- `SEED` permite reproducir una generación cuando se utiliza la misma configuración y el mismo algoritmo.
- `ALGORITHM` debe ser `DFS` o `PRIM`. Si no se especifica otro valor, se utiliza `DFS`.

Las coordenadas siguen el formato `x,y`, donde `x` representa la posición horizontal e `y` la posición vertical.

La configuración se valida antes de iniciar la generación. Si se detectan valores incorrectos, dimensiones no permitidas o coordenadas inválidas, el programa informa del error para que el usuario pueda corregirlo.

## Maze Generation Algorithm

### Selected Algorithms

El proyecto implementa dos algoritmos de generación de laberintos: **Depth-First Search (DFS)** y **Prim's algorithm**.

El algoritmo utilizado por defecto es DFS. También es posible seleccionar Prim mediante el parámetro `ALGORITHM` del archivo de configuración.

#### Depth-First Search (DFS)

DFS genera el laberinto explorando caminos en profundidad.

El algoritmo comienza en una celda inicial y marca las celdas visitadas. En cada paso, selecciona una celda vecina que todavía no ha sido visitada y elimina la pared que las separa. A continuación, continúa explorando desde la nueva celda.

Cuando no quedan vecinos sin visitar, retrocede hasta encontrar una celda desde la que pueda continuar la exploración. Este proceso se repite hasta recorrer todas las celdas del laberinto.

Este método permite generar laberintos conectados y, cuando se utiliza el procedimiento habitual de retroceso y se elimina una única pared para incorporar cada nueva celda, laberintos perfectos.

#### Prim's Algorithm

El algoritmo de Prim genera el laberinto haciendo crecer progresivamente una región conectada.

Comienza en una celda inicial y mantiene una lista de paredes que separan las celdas visitadas de las que todavía no se han incorporado al laberinto.

En cada paso selecciona una de las paredes de esa lista. Si la pared conecta una celda visitada con otra que todavía no ha sido visitada, elimina la pared e incorpora la nueva celda a la región conectada. Las paredes de esta nueva celda se añaden a la lista de candidatas.

El proceso continúa hasta incorporar todas las celdas al laberinto.

En esta variante, la incorporación de cada nueva celda mediante la eliminación de una única pared permite generar un laberinto perfecto.

### Reasons for Choosing These Algorithms

Se han implementado dos algoritmos para disponer de diferentes estrategias de generación y poder comparar los resultados.

**DFS se utiliza por defecto** porque ofrece una lógica de exploración sencilla de comprender y mantener. Su recorrido en profundidad y su mecanismo de retroceso permiten generar laberintos con caminos largos y sinuosos.

**Prim se ofrece como alternativa** porque construye el laberinto progresivamente a partir de una frontera de paredes. Su estrategia de crecimiento es diferente de la de DFS y permite obtener otras distribuciones de caminos.

La elección de ambos algoritmos aporta flexibilidad al programa y permite estudiar cómo influye la estrategia de generación en la estructura del laberinto.

Los principales criterios considerados son:

- **Correctness:** los algoritmos deben generar una estructura que respete las reglas del proyecto.
- **Connectivity:** las celdas deben estar conectadas y debe existir un camino válido entre la entrada y la salida.
- **Performance:** la generación debe ser eficiente para las dimensiones admitidas.
- **Reproducibility:** el uso de una semilla permite repetir una generación y facilita las pruebas.
- **Maintainability:** la implementación debe ser comprensible y permitir futuras ampliaciones.

### Maze Solver

Una vez generado el laberinto, el programa busca un camino entre la entrada y la salida mediante **Breadth-First Search (BFS)**.

BFS es un algoritmo de búsqueda en anchura que explora las celdas alcanzables por niveles. Para gestionar la exploración, utiliza una cola de posiciones pendientes y mantiene un registro de las celdas visitadas y de sus predecesoras.

Cuando encuentra la salida, reconstruye el camino hasta la entrada utilizando la información almacenada durante la búsqueda.

Como todos los movimientos entre celdas tienen el mismo coste, BFS encuentra un camino con el menor número de movimientos.

Si no existe un camino válido entre la entrada y la salida, el solucionador informa de que no se ha encontrado una solución.

## Reusable Code

El proyecto se ha organizado en componentes independientes para facilitar la reutilización de la lógica y evitar que cada módulo dependa de los detalles internos de los demás.

### Configuration Management and Validation

El módulo de configuración se encarga de cargar los parámetros del archivo y comprobar que sus valores sean válidos antes de comenzar la generación.

Esta lógica puede reutilizarse en otras aplicaciones que necesiten leer y validar parámetros externos. Para ello, sería necesario adaptar el formato del archivo y las reglas específicas de validación.

### Maze Generator

El generador es responsable de construir la estructura del laberinto y gestionar las paredes de cada celda.

La representación interna permite determinar qué paredes existen y qué conexiones están abiertas entre celdas vecinas.

La implementación de diferentes algoritmos permite seleccionar una estrategia de generación sin cambiar el resto de los componentes que trabajan con la estructura del laberinto.

Este componente puede reutilizarse en otros proyectos que trabajen con laberintos o cuadrículas conectadas, adaptando las dimensiones, la configuración y las reglas de movimiento cuando sea necesario.

### Maze Solver

El solucionador utiliza BFS para encontrar un camino entre dos posiciones del laberinto.

La lógica de búsqueda puede reutilizarse en otros problemas de navegación sobre cuadrículas en los que los movimientos estén definidos mediante posiciones vecinas y reglas de accesibilidad.

Para ello, basta con proporcionar una representación de las posiciones y una forma de determinar qué movimientos están permitidos.

### Maze Renderer

El renderizador transforma la estructura interna del laberinto en una representación visual para la terminal.

Se encarga de dibujar las paredes, las esquinas, los colores y los elementos que permiten identificar la entrada, la salida y el camino de la solución.

Mantener esta responsabilidad separada de la generación permite representar el mismo laberinto de diferentes maneras sin modificar el algoritmo que lo ha creado.

También facilita incorporar nuevos estilos visuales y opciones de presentación.

### Future Extensions

La arquitectura permite ampliar el proyecto mediante nuevos algoritmos de generación, otros métodos de resolución o diferentes formas de representación.

Al mantener los componentes separados, estas ampliaciones pueden realizarse sin necesidad de reescribir toda la aplicación.

## Team and Project Management

### Team Members and Roles

| Team Member | Responsibilities |
|---|---|
| `mtapiado` | Generación y resolución del laberinto  |
| `arabago-` | Parsing fichero de configuración y renderizado del laberinto |

El reparto de responsabilidades debe reflejar el trabajo realizado por cada integrante durante el proyecto.

Además del desarrollo individual, deben documentarse las tareas compartidas, la integración de los módulos, las revisiones de código y las decisiones técnicas tomadas conjuntamente.

### Planning and Evolution

La planificación inicial se organizó en varias etapas:

1. Analizar los requisitos del proyecto y definir el formato de configuración.
2. Implementar la carga y validación de los parámetros.
3. Desarrollar los algoritmos de generación del laberinto.
4. Implementar el solucionador para encontrar un camino entre la entrada y la salida.
5. Desarrollar el renderizador para representar el laberinto en la terminal.
6. Integrar los componentes y comprobar su funcionamiento conjunto.
7. Incorporar las opciones adicionales de visualización y el menú interactivo.
8. Realizar pruebas finales, corregir errores y preparar la documentación.

Durante el desarrollo, la planificación evolucionó para adaptarse a los problemas encontrados y a las nuevas necesidades identificadas.

Una de las áreas que requirió especial atención fue la representación visual del laberinto. Fue necesario coordinar las coordenadas de las celdas, la posición de las paredes y las uniones entre ellas para conseguir una representación coherente.

También se tuvieron que considerar las particularidades de los caracteres Unicode y las secuencias ANSI para mostrar correctamente los símbolos, los colores y los elementos de la solución.

La planificación definitiva debe reflejar cómo se distribuyeron las tareas, qué actividades llevaron más tiempo del previsto y qué cambios se realizaron respecto al plan inicial.

### What Worked Well

- La separación entre configuración, generación, resolución y representación facilitó el mantenimiento del código.
- La validación de los parámetros permitió detectar configuraciones incorrectas antes de iniciar la generación.
- El uso de semillas facilitó la reproducción de resultados y la depuración de errores.
- La implementación de DFS y Prim permitió disponer de dos estrategias de generación.
- La implementación modular permitió trabajar sobre componentes concretos sin modificar toda la aplicación.
- Las pruebas y la depuración progresiva ayudaron a detectar problemas de integración y representación.

### What Could Be Improved

- Dedicar más tiempo al diseño inicial de las interfaces entre módulos.
- Planificar con mayor precisión las tareas de integración y depuración.
- Ampliar las pruebas automatizadas para cubrir configuraciones límite y entradas incorrectas.
- Documentar las decisiones técnicas durante el desarrollo.
- Establecer criterios de aceptación claros para las funcionalidades adicionales.
- Reservar tiempo suficiente para revisar la documentación y comprobar todos los requisitos de evaluación.

### Tools Used

Las herramientas utilizadas durante el desarrollo incluyen:

- **Python:** lenguaje de programación principal.
- **Git:** control de versiones y seguimiento de cambios.
- **GitHub:** alojamiento del repositorio, gestión de ramas y pull requests.
- **Visual Studio Code:** edición y depuración del código.
- **Poetry:** gestión de dependencias y ejecución del proyecto.
- **Pydantic:** validación de parámetros de configuración, si se utiliza en la implementación definitiva.
- **Terminal con soporte ANSI:** representación de colores, símbolos y control de la visualización.

## Resources

### Documentation and References

Las siguientes referencias permiten profundizar en los conceptos y las tecnologías empleados en el proyecto.

- [Python Documentation](https://docs.python.org/3/): documentación oficial del lenguaje Python y sus módulos.
- [Python Random Module](https://docs.python.org/3/library/random.html): generación de valores aleatorios y uso de semillas.
- [Python Collections Module](https://docs.python.org/3/library/collections.html): estructuras de datos como `deque`, útil para implementar BFS.
- [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search): fundamentos del algoritmo de búsqueda en anchura.
- [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search): fundamentos de la búsqueda en profundidad.
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm): descripción de diferentes algoritmos para generar laberintos.
- [Prim's Algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm): explicación del algoritmo de Prim y de su estrategia de crecimiento.
- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code): secuencias de control y colores utilizados en terminales.
- [Unicode](https://home.unicode.org/): referencia sobre caracteres y representación de símbolos.
- [Pydantic Documentation](https://docs.pydantic.dev/): documentación de validación de datos, si se utiliza en el proyecto.
- [Poetry Documentation](https://python-poetry.org/docs/): documentación sobre instalación y gestión de dependencias.

### Use of Artificial Intelligence

Se utilizaron herramientas de inteligencia artificial como apoyo durante el desarrollo y el aprendizaje.

Su uso se centró en las siguientes tareas:

- Comprender conceptos de Python, algoritmos y estructuras de datos.
- Analizar alternativas de implementación y organización del código.
- Investigar errores y comprender sus causas.
- Resolver dudas sobre la representación del laberinto, las coordenadas y las secuencias ANSI.
- Revisar la legibilidad del código, los nombres de funciones y los mensajes de error.
- Mejorar la documentación y estructurar este archivo README.
- Contrastar posibles soluciones y comprender las ventajas e inconvenientes de diferentes enfoques.

Las sugerencias generadas por la inteligencia artificial se revisaron y adaptaron a las necesidades del proyecto. Las decisiones finales de diseño, las pruebas y la integración corresponden al trabajo realizado por el equipo.

Se deben indicar las herramientas de IA utilizadas, las tareas concretas en las que se emplearon y qué partes del código o de la documentación se desarrollaron o modificaron con su ayuda.

## Advanced Features

### Multiple Generation Algorithms

El programa permite seleccionar entre dos algoritmos de generación mediante el parámetro `ALGORITHM` del archivo de configuración.

- **DFS:** algoritmo utilizado por defecto. Explora caminos en profundidad y retrocede cuando no puede continuar.
- **Prim:** alternativa que construye progresivamente una región conectada a partir de las paredes que separan las celdas visitadas de las no visitadas.

Para seleccionar DFS:

```ini
ALGORITHM=DFS
```

Para seleccionar Prim:

```ini
ALGORITHM=PRIM
```

Esta funcionalidad permite comparar diferentes estrategias de generación sin modificar el resto de la configuración del laberinto.

### Display Options

El proyecto incluye opciones que permiten personalizar la visualización del laberinto.

- **Coloured rendering:** utiliza colores para distinguir los elementos visuales de la representación.
- **Solution path:** permite mostrar u ocultar el camino calculado entre la entrada y la salida.
- **Animation:** permite representar el proceso de forma progresiva.

Estas opciones permiten adaptar la presentación a las preferencias del usuario sin modificar la estructura lógica del laberinto.

### Reproducibility

El parámetro `SEED` permite controlar la generación aleatoria.

Al utilizar la misma semilla, configuración, algoritmo y versión de la implementación, es posible reproducir el mismo laberinto, siempre que el algoritmo utilice la fuente de aleatoriedad de manera determinista.

Esta funcionalidad resulta útil para depurar errores, comparar resultados y realizar pruebas repetibles.