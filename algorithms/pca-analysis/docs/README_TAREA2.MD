# Tarea 2 · Fundamentos de Machine Learning

## Contexto y propósito
Esta tarea continúa con el ejercicio desarrollado en [Tarea 1](../TAREA_1/README.MD). Se enfoca en aplicar los conceptos vistos en el Módulo 2 del curso (Fundamentos de Machine Learning) y en presentar un flujo completo de preparación, entrenamiento, evaluación y limpieza de artefactos asociados al modelo. Además, se debe tomar como referencia principal el PDF específico de Tarea 2 (Reducción de la dimensionalidad) que se encuentra en el mismo directorio.

## Objetivos principales
- Replicar la canalización básica de datos, modelo y métricas planteada en Tarea 1, pero con datos limpios y contenedores controlados.
- Revisar los conceptos clave vistos en clase: redes neuronales, aprendizaje no supervisado, regresión lineal y técnicas de defensa contra aprendizaje adversario.
- Documentar el proceso para que quede listo para futuras iteraciones (incluye limpieza, reentrenamiento y reforzamiento).

## Referencias obligatorias
1. **Tarea 2 – Reducción de la dimensionalidad** (`TAREA_2/Tarea 2 - Reducción de la dimensionalidad.pdf`): guía principal de la entrega actual.
2. **Módulo 2 – Fundamentos de Machine Learning** (PDF en el raíz del módulo): contiene teorías y ejemplos de los métodos vinculados.
3. **Entrega anterior**: `/master-ai-cs/MODULO2-MACHINE-LEARNING/TAREA_1/README.MD` para comparar estructura y código reutilizable.

## Pasos recomendados
1. **Revisar y limpiar los datos**
   - Asegúrate de que los datasets estén libres de valores nulos o inconsistentes antes de entrenar.
   - Documenta qué columnas se transformaron o eliminaron y por qué.
2. **Revisar contenedores o entornos**
   - Verifica que los contenedores (Docker, notebooks, scripts) no guarden archivos temporales innecesarios.
   - Si usas contenedores, limpia volúmenes y redes que no se usen con `docker system prune` (solo si ya estás cómodo con el entorno).
3. **Construir el pipeline de entrenamiento**
   - Reutiliza los componentes funcionales de Tarea 1: preprocesamiento, métricas y modelos seleccionados.
   - Añade un paso de validación adicional (k-fold o hold-out) si aún no está presente.
4. **Explorar defensas contra aprendizaje adversario**
   - Describe al menos una estrategia de defensa (p. ej., reentrenamiento adversario, enmascaramiento de gradiente o ensambles).
   - Explica brevemente cómo se puede detectar un intento de envenenamiento o evadir un modelo.
5. **Documentar resultados**
   - Resume métricas de desempeño (precisión, recall, error) en un archivo o en la misma README.
   - Describe qué técnicas fueron útiles para limitar perturbaciones (FGSM, gradients, etc.).

## Contenidos teóricos clave
- **Aprendizaje adversario**: envenenamiento de datos previo a entrenar y ataques de evasión una vez desplegado el modelo. Ejemplos rápidos: insertar píxeles confusos (nightshade), extracción de modelos y robo de algoritmos.
- **Tipos de ataques**:
  - Caja blanca: el atacante conoce toda la arquitectura y peso del modelo; se usa el método FGSM.
  - Caja negra: el atacante no tiene acceso directo; requiere más tiempo para deducir el comportamiento.
- **Defensas**:
  - Frente a FGSM usar entrenamiento con ejemplos adversarios para reforzar el modelo.
  - Monitorear gradientes y enmascaramiento para evitar falsas sensaciones de seguridad.
- **Temas vistos en clase**: redes neuronales, aprendizaje no supervisado, regresión lineal, activaciones (`ReLU`, perceptrón, sigmoide, tangente hiperbólica) y métodos de descenso de gradiente. Incluye implementación de `k-means`, `DBSCAN`, y PCA para análisis exploratorio.
- **Estadística**: analiza la matriz de covarianza (varianza y covarianza) y las medidas de dispersión y correlación para entender la distribución de tus características.

## Recomendaciones finales
- Mantén el repositorio ordenado: elimina artefactos temporales y documenta cómo regenerarlos si es necesario.
- Si surgen dudas con teoría, regresa al PDF del módulo y compáralo con el ejercicio anterior.
- Antes de entregar, confirma que los comandos para entrenar y evaluar estén documentados y se pueden ejecutar nuevamente.
