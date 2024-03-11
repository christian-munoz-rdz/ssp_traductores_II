# Qué es un analizador léxico

Un **_analizador léxico_** es un programa que recibe como entrada el codigo fuente (secuencia de caracteres) de otro programa, produciendo como salida una secuencia de **_tokens_** (componentes léxicos) o símbolos. Estos tokens sirven para una etapa posterior de la compilación, el **_análisis sintáctico_**.

Los tokens son definidos por un conjunto de reglas o expresiones regulares, que especifican el patrón de caracteres que los representan. 

![analizador lexico](https://blogdetito.com/wp-content/uploads/2016/12/Dibujo3.png)

En el análisis se suele utilizar una **_máquina de estados finitos_** para reconocer los tokens. Esta máquina contiene un conjunto de estados que definen las secuencias de caracteres que representan a los tokens. Un ejemplo de máquina de estados finitos es el siguiente:

![maquina de estados](https://3.bp.blogspot.com/-Effz439Mtnk/VyAlnyMM1bI/AAAAAAAABhU/mRgYhtZwk58poKbJNyqOCrMxswY4piUkACLcB/s1600/Python_FSM.png)

## Qué es un Token

Un **_token_** es una secuencia de caracteres con un signifcado asignado e identificado. Se conforma de un nombre de token y un valor de token. Por ejemplo:

| Nombre simbólico | Ejemplos de valores de token |
|------------------|------------------------------|
| identificador    | x, color, ARRIBA             |
| palabra clave    | si, mientras, retorno        |
| separador        | }, (, ;                      |
| operador         | +, <, =                      |
| literal          | verdadero, 6,02e23, "música" |
| comentario       | /* Recupera datos de usuario */, // debe ser negativo |

La tabla de arriba representa los tokens que se pueden encontrar en el lenguaje de programación C.

Referencias:



- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). [Compilers: Principles, techniques, and tools (2a ed.)](https://books.google.com.ar/books?id=yG6qJBAnE9UC&printsec=frontcover#v=onepage&q&f=false). Pearson.

