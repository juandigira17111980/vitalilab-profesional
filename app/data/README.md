# Referencia numérica de crecimiento

`who_bmi_2007.csv` contiene exclusivamente los parámetros numéricos L, M y S de la referencia OMS 2007, por sexo de referencia y mes cumplido, de **61 a 228 meses**. No son datos de usuarios.

Fuentes oficiales, obtenidas el 14 de octubre de 2026 (Colombia):

- [OMS, BMI-for-age 5–19 years](https://www.who.int/toolkits/growth-reference-data-for-5to19-years/indicators/bmi-for-age).
- [Parámetros de niños, tabla expandida](https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-%285-19-years%29/bmi-boys-z-who-2007-exp.xlsx). SHA256 del XLSX: `0a60849673f34a06b8e2fe4defe5d00348de687b6c9fce0278f1525fff89eb6d`.
- [Parámetros de niñas, tabla expandida](https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-%285-19-years%29/bmi-girls-z-who-2007-exp.xlsx). SHA256 del XLSX: `66f5c6284b44579ad6135fc639f22c09e36fe5a695b04390377113f6a00deb72`.
- [Método de cálculo OMS](https://www.who.int/docs/default-source/child-growth/growth-reference-5-19-years/computation.pdf).

Extracción: columnas Month/L/M/S de la primera hoja, 168 filas por referencia; sin redondeos adicionales relevantes a la precisión publicada. Se guardaron como `sex,month,L,M,S`, con valores `male|female`. El CSV tiene 336 filas numéricas. Ninguna celda de texto externa se ejecuta.

La aplicación carga el recurso local en memoria y no transmite medidas a OMS/CDC. Usa LMS y la distribución normal solo para z entre -3 y 3. Fuera de ese intervalo, sin edad/sexo o fuera de los meses cubiertos, no entrega percentil ni aplica umbrales adultos. No implementa extrapolación de extremos ni diagnóstico. La prueba reproduce el ejemplo publicado del niño de nueve años con IMC 19 (z aproximadamente 1,47).

Referencia científica no equivale a validación clínica de VitaliLab ni aval de OMS. No se reproducen marcas o gráficos oficiales. El piloto es académico; antes de comercialización se deben revisar condiciones de reutilización, referencia apropiada para la población y validación profesional.
