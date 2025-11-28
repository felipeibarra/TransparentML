# Complemento Tarea 2 — Módulo 2: Fundamentos del Machine Learning

## 1. Aprendizaje adversario

### 1.1 Estrategias de ataque
- **Envenenamiento de datos (data poisoning):** se manipulan ejemplos antes de entrenar el modelo para introducir sesgos o errores.
- **Evasión (adversarial evasion):** se generan perturbaciones luego de desplegar el modelo para confundir sus predicciones.
- **Night Shade (o shock attack):** inyección de píxeles o características mínimas que producen decisiones equivocadas sin alterar perceptiblemente la entrada.

### 1.2 Tipos de acceso
- **Caja blanca:** el atacante conoce la arquitectura y parámetros del modelo. Puede aplicar métodos como FGSM (Fast Gradient Sign Method) para calcular pérdida, gradiente, signo y añadir perturbación.
- **Caja negra:** el atacante opera “a ciegas” y solo consulta salidas. Es un escenario más realista pero requiere más tiempo y dedicación.

### 1.3 Extracción de modelos
- **Robo del algoritmo o información sensible** por medio de consultas masivas que permiten reconstruir el comportamiento del sistema.
- **Defensa:** limitar acceso o agregar ruido a respuestas para dificultar la extracción.

## 2. Estrategias de defensa

- **Fortaleza digital:** combinar modelos (conjuntos) para estabilizar decisiones ante ejemplos adversarios.
- **Entrenamiento adversario:** reentrenar el modelo con ejemplos adversarios etiquetados (“fuego con fuego”) para que aprenda a reconocer los trucos.
- **Enmascaramiento de gradiente:** alterar gradientes para dar una falsa sensación de seguridad sin eliminar la vulnerabilidad real.

## 3. Repaso de temas vistos en clase

### 3.1 Aprendizaje profundo y no supervisado
- Redes neuronales (Perceptron, ReLU, sigmoide, tangente hiperbólica).
- Descenso por gradiente y cálculo de gradientes de pérdida.
- Aprendizaje no supervisado: K-Means, Clustering, DBSCAN.
- Análisis de componentes principales (PCA) para reducción de dimensionalidad.

### 3.2 PCA y análisis estadístico
- Matriz de covarianza: varianza, covarianza y otras medidas de dispersión y correlación.
- Vulnerabilidades del PCA: depende de relaciones lineales, es sensible a outliers y requiere escalado coherente de variables.
- Cálculo de autovalores/autovectores con librerías como NumPy y scikit-learn para interpretar la varianza explicada.

## 4. Trabajo práctico y recomendaciones

- **Práctica sugerida:** aplicar PCA sobre un dataset ya disponible para reforzar comprensión de sus caracteríticas, explorar cómo cargar conjuntos adicionales y comparar resultados.
- **Segunda opción:** clonar otro dataset (Dataset 2) y experimentar con scikit-learn para ejercitar extracción de componentes principales y clustering.
- **Mejora de nota:** documentar análisis, explicar pasos y resaltar qué se aprendió, además de mostrar una comparación de resultados.

## 5. Notas finales

- Reforzar el entendimiento de PCA y los conceptos adversarios ayuda a interpretar resultados y a diseñar defensas.
- Documentar cada experimento y justificar su utilidad para la tarea puede incrementar la calificación.
