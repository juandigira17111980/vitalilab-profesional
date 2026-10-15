# Referencia numérica de crecimiento

`who_bmi_2007.csv` contiene exclusivamente los parámetros numéricos L, M y S de la referencia OMS 2007, por sexo de referencia y mes cumplido, de **61 a 228 meses**. No son datos de usuarios.

## Explicación desde cero para la sustentación

La carpeta `data` significa «datos», pero aquí no es la base de datos de VitaliLab. Es una carpeta de **consulta** que acompaña al código, como una tabla de fórmulas en un libro. El archivo CSV permite leer una tabla sin necesitar Excel ni conexión con un servicio externo.

Un CSV es texto organizado en filas y columnas, separadas por comas. La primera línea nombra las columnas:

```text
sex,month,L,M,S
```

| Columna | Significado en este archivo | Ejemplo |
|---|---|---|
| `sex` | Referencia de crecimiento consultada; `male` y `female` identifican las dos tablas. No identifica a una persona ni representa su identidad de género. | `female` |
| `month` | Edad en meses cumplidos, no el mes del calendario. | `144` equivale a 12 años |
| `L` | Parámetro que ajusta la asimetría de la distribución para calcular un valor estandarizado. Puede ser negativo; no es un IMC ni un error. | `-1.4006` |
| `M` | Mediana de IMC de esa referencia a esa edad. | `17.9966` |
| `S` | Parámetro que representa su dispersión relativa; no son segundos. | `0.13129` |

La fila que aparece en la captura del proyecto es:

```text
female,144,-1.4006,17.9966,0.13129
```

Se lee así: «Para la referencia femenina y 144 meses cumplidos, estos son los tres parámetros de consulta». **No significa que haya una estudiante de 12 años registrada con esas medidas.** Tampoco hay pesos, alturas, nombres, correos o contraseñas en este archivo. Los números de la izquierda en el editor son números de línea; no son identificadores de estudiantes.

## Para qué se utiliza y para qué no

Primero se calcula el IMC con las medidas del usuario: `peso_kg / altura_m²`. La tabla no es necesaria para esa división. Su función aparece **después**, cuando procede contextualizar el resultado mediante edad y sexo de referencia, en lugar de aplicar automáticamente rangos de adultos a menores.

El recorrido implementado es:

1. `app/services/measurements.py` obtiene la edad en meses cumplidos en la fecha de la medición, no en la fecha actual al consultar un registro antiguo.
2. `growth_reference()` lee el CSV mediante `csv.DictReader` y crea una consulta en memoria por la pareja `(sex, month)`. `lru_cache` evita releer el archivo en cada petición del mismo proceso. Un nuevo proceso vuelve a cargar su copia; no es una caché compartida entre servidores.
3. `growth_snapshot()` busca los parámetros L, M y S de la edad y referencia indicadas.
4. Calcula un valor estandarizado, llamado z, y obtiene un percentil únicamente dentro de los límites implementados.
5. El resultado calculado se conserva, cuando existe, junto a la medición en `health_measurements`, dentro de PostgreSQL. El CSV no se modifica al registrar usuarios o medidas.

El archivo tiene **336 filas de datos**, además de la cabecera: 168 edades mensuales para cada una de las dos referencias. La cobertura implementada es de 61 a 228 meses; por debajo o por encima no se inventa una fila. Si faltan edad o referencia, o si z queda fuera del intervalo central de -3 a 3, no se devuelve un percentil. Estos límites no impiden explicar el IMC numérico; evitan atribuirle una interpretación que el código no respalda.

Un percentil describe una posición frente a esa referencia; **no es una calificación, un porcentaje de salud ni un objetivo que deba alcanzarse**. La tabla no elige ejercicios ni prescribe rutinas. VitaliLab organiza las rutinas por objetivo y preferencia de movimiento; no por una etiqueta corporal.

## Diferencia frente a PostgreSQL

| Recurso | Contenido | Cuándo cambia |
|---|---|---|
| `app/data/who_bmi_2007.csv` | Parámetros de referencia, iguales para todos | Solo mediante un cambio técnico revisado y versionado |
| PostgreSQL: `health_measurements` | Mediciones e indicadores históricos de cada usuario | Cuando el usuario registra información con los permisos y confirmaciones requeridos |
| PostgreSQL: `users`, `user_profiles` | Cuentas y perfiles | Al crear o actualizar una cuenta |

No se debe reemplazar el CSV por medidas personales ni editar sus números para cambiar el resultado de un usuario. El historial real necesita permisos y copias de seguridad de PostgreSQL. La tabla de referencia necesita procedencia, control de versiones y pruebas.

## Guion breve para explicar la captura

«Esta carpeta contiene una tabla de referencia de crecimiento de la OMS. No almacena datos de estudiantes. Cada fila corresponde a una edad en meses y una de las dos referencias; L, M y S son parámetros estadísticos. El programa calcula primero el IMC con peso y altura y, si tiene el contexto necesario, consulta esta tabla para obtener una referencia de crecimiento. Las mediciones personales se guardan por separado en PostgreSQL. El resultado es descriptivo, no un diagnóstico ni una orden de ejercicio».

## Ejercicio de aprendizaje sin datos personales

Busca `female,144` y comprueba que 144 meses equivalen a 12 años. Abre `growth_reference()` y localiza cómo utiliza los nombres de las columnas. Después busca `HealthMeasurement` y distingue el archivo de consulta de la tabla donde se guardan las mediciones. Finalmente ejecuta `python -m pytest tests/test_measurements_movement.py --no-cov`: la prueba reproduce un ejemplo publicado y comprueba los límites de la referencia.

## Procedencia y límites de uso

Fuentes oficiales, obtenidas el 14 de octubre de 2026 (Colombia):

- [OMS, BMI-for-age 5–19 years](https://www.who.int/toolkits/growth-reference-data-for-5to19-years/indicators/bmi-for-age).
- [Parámetros de niños, tabla expandida](https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-%285-19-years%29/bmi-boys-z-who-2007-exp.xlsx). SHA256 del XLSX: `0a60849673f34a06b8e2fe4defe5d00348de687b6c9fce0278f1525fff89eb6d`.
- [Parámetros de niñas, tabla expandida](https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-%285-19-years%29/bmi-girls-z-who-2007-exp.xlsx). SHA256 del XLSX: `66f5c6284b44579ad6135fc639f22c09e36fe5a695b04390377113f6a00deb72`.
- [Método de cálculo OMS](https://www.who.int/docs/default-source/child-growth/growth-reference-5-19-years/computation.pdf).

Extracción: columnas Month/L/M/S de la primera hoja, 168 filas por referencia; sin redondeos adicionales relevantes a la precisión publicada. Se guardaron como `sex,month,L,M,S`, con valores `male|female`. El CSV tiene 336 filas numéricas. Ninguna celda de texto externa se ejecuta.

La aplicación carga el recurso local en memoria y no transmite medidas a OMS/CDC. Usa LMS y la distribución normal solo para z entre -3 y 3. Fuera de ese intervalo, sin edad/sexo o fuera de los meses cubiertos, no entrega percentil ni aplica umbrales adultos. No implementa extrapolación de extremos ni diagnóstico. La prueba reproduce el ejemplo publicado del niño de nueve años con IMC 19 (z aproximadamente 1,47).

Referencia científica no equivale a validación clínica de VitaliLab ni aval de OMS. No se reproducen marcas o gráficos oficiales. El piloto es académico; antes de comercialización se deben revisar condiciones de reutilización, referencia apropiada para la población y validación profesional.
