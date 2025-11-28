# docs/ - Documentación del Proyecto

## 📋 Descripción

Esta carpeta contiene toda la documentación complementaria del proyecto PCA, incluyendo contexto de la tarea, análisis de resultados, referencias y material académico.

## 📚 Contenido

```
docs/
├── README.md                        # Este archivo (índice)
├── README_TAREA2.MD                 # Contexto y especificaciones de la tarea
├── README_COMPLEMENTO_TAREA2.MD     # Información complementaria
└── RESULTADOS.md                    # Análisis detallado de resultados
```

## 📄 Archivos de Documentación

### 1. `README_TAREA2.MD`
**Contexto y Especificaciones de la Tarea**

```
┌──────────────────────────────────────────┐
│      README_TAREA2.MD                    │
├──────────────────────────────────────────┤
│                                          │
│  • Descripción de la tarea académica    │
│  • Objetivos de aprendizaje             │
│  • Requisitos del proyecto               │
│  • Criterios de evaluación               │
│  • Referencias del Máster                │
│                                          │
└──────────────────────────────────────────┘
```

**Contenido**:
- Enunciado oficial de la Tarea 2
- Objetivos específicos del ejercicio
- Metodología requerida (PCA manual)
- Entregables esperados
- Contexto del Módulo 2: Fundamentos de ML

**Audiencia**: Estudiantes, profesores, evaluadores

---

### 2. `README_COMPLEMENTO_TAREA2.MD`
**Información Complementaria y Extensiones**

```
┌──────────────────────────────────────────┐
│   README_COMPLEMENTO_TAREA2.MD           │
├──────────────────────────────────────────┤
│                                          │
│  • Conceptos teóricos adicionales        │
│  • Matemática detrás de PCA              │
│  • Alternativas y variantes              │
│  • Aplicaciones prácticas                │
│  • Material de estudio extra             │
│                                          │
└──────────────────────────────────────────┘
```

**Contenido**:
- Fundamentos matemáticos de PCA
- Álgebra lineal: autovalores y autovectores
- Comparación: PCA vs otros métodos de reducción
- Kernel PCA y variantes
- Casos de uso en ciberseguridad
- Lecturas recomendadas

**Audiencia**: Estudiantes avanzados, investigadores

---

### 3. `RESULTADOS.md`
**Análisis Detallado de Resultados del Proyecto**

```
┌──────────────────────────────────────────┐
│         RESULTADOS.md                    │
├──────────────────────────────────────────┤
│                                          │
│  • Métricas del análisis PCA             │
│  • Interpretación de componentes         │
│  • Análisis de varianza explicada        │
│  • Validación de implementación          │
│  • Conclusiones y hallazgos              │
│  • Visualizaciones comentadas            │
│                                          │
└──────────────────────────────────────────┘
```

**Contenido**:
- Resultados cuantitativos (varianza, autovalores)
- Interpretación cualitativa (separación de clases)
- Comparación manual vs sklearn
- Análisis de cada componente principal
- Loadings y contribución de features
- Conclusiones del análisis
- Recomendaciones

**Audiencia**: Todas (principal documento de resultados)

---

## 🗂️ Estructura de la Documentación

```
┌────────────────────────────────────────────────────┐
│           Jerarquía Documental                     │
└────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Contexto   │ │ Complemento  │ │  Resultados  │
│              │ │              │ │              │
│ Tarea 2      │ │ Teoría       │ │ Análisis     │
│ Requisitos   │ │ Matemática   │ │ Métricas     │
│ Objetivos    │ │ Variantes    │ │ Conclusiones │
└──────────────┘ └──────────────┘ └──────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ▼
                README.md principal
                (raíz del proyecto)
```

## 📖 Guía de Lectura

### Para Nuevos Usuarios
1. **README.md** (raíz) - Inicio rápido
2. **docs/README_TAREA2.MD** - Entender el contexto
3. **src/README.md** - Arquitectura del código
4. **docs/RESULTADOS.md** - Ver resultados

### Para Implementadores
1. **src/README.md** - Módulos disponibles
2. **scripts/README.md** - Cómo ejecutar
3. **notebooks/README.md** - Análisis interactivo
4. **docs/README_COMPLEMENTO_TAREA2.MD** - Teoría

### Para Evaluadores
1. **docs/README_TAREA2.MD** - Requisitos
2. **docs/RESULTADOS.md** - Cumplimiento de objetivos
3. **results/README.md** - Visualizaciones
4. **README.md** (raíz) - Resumen ejecutivo

## 🎯 Objetivos de la Documentación

### 1. Claridad
- Explicar qué hace el proyecto
- Documentar decisiones de diseño
- Facilitar comprensión del código

### 2. Reproducibilidad
- Permitir replicar resultados
- Documentar pasos del análisis
- Especificar dependencias

### 3. Aprendizaje
- Enseñar conceptos de PCA
- Mostrar implementación práctica
- Proporcionar referencias

### 4. Evaluación
- Demostrar cumplimiento de objetivos
- Presentar resultados claramente
- Validar metodología

## 📝 Convenciones de Documentación

### Formato
- **Markdown** (.md) para compatibilidad
- **Títulos jerárquicos** (H1, H2, H3...)
- **Bloques de código** con sintaxis highlighting
- **Diagramas ASCII** para visualización textual
- **Emojis** para mejorar legibilidad

### Estructura de documentos
```markdown
# Título Principal

## 📋 Descripción
Breve descripción del contenido

## 🎯 Objetivos
Lista de objetivos

## 📊 Contenido
Desarrollo detallado

## 🔗 Referencias
Enlaces y recursos externos
```

## 🔗 Relaciones con Otros Directorios

```
┌──────────────────────────────────────────┐
│              docs/                       │
│                                          │
│  Documenta:                              │
│  ├── src/          (código fuente)       │
│  ├── scripts/      (ejecución)           │
│  ├── notebooks/    (análisis)            │
│  ├── results/      (visualizaciones)     │
│  └── data/         (dataset)             │
│                                          │
│  Referenciado por:                       │
│  └── README.md (raíz)                    │
└──────────────────────────────────────────┘
```

## 📚 Referencias Académicas

### Máster en IA Aplicada a la Ciberseguridad
- **Módulo**: Fundamentos de Machine Learning
- **Tarea**: Tarea 2 - Reducción de Dimensionalidad
- **Fecha**: Noviembre 2025
- **Autor**: Felipe Ibarra

### Material de Estudio
- PDF de la tarea: `../Tarea 2 - Reducción de la dimensionalidad.pdf`
- Notebooks de clase
- Presentaciones del módulo

### Libros y Papers Recomendados
1. **"Pattern Recognition and Machine Learning"** - Christopher Bishop
   - Capítulo 12: PCA y dimensionality reduction

2. **"The Elements of Statistical Learning"** - Hastie, Tibshirani, Friedman
   - Capítulo 14.5: Principal Components

3. **"Python Machine Learning"** - Sebastian Raschka
   - Capítulo 5: Compressing Data via Dimensionality Reduction

4. **Paper Original PCA**:
   Pearson, K. (1901). "On Lines and Planes of Closest Fit to Systems of Points in Space"

5. **Fisher's Iris Paper**:
   Fisher, R.A. (1936). "The use of multiple measurements in taxonomic problems"

## 🌐 Recursos Online

### Tutoriales
- [Scikit-learn PCA Guide](https://scikit-learn.org/stable/modules/decomposition.html#pca)
- [StatQuest: PCA Explained](https://www.youtube.com/watch?v=FgakZw6K1QQ)
- [Towards Data Science: PCA](https://towardsdatascience.com/a-one-stop-shop-for-principal-component-analysis-5582fb7e0a9c)

### Herramientas
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

## 💡 Contribuir a la Documentación

### Agregar nueva documentación
1. Crear archivo `.md` en `docs/`
2. Seguir convenciones de formato
3. Actualizar este README con enlace
4. Referenciar desde README principal si es relevante

### Actualizar documentación existente
1. Editar archivo correspondiente
2. Mantener consistencia de estilo
3. Actualizar fecha de modificación
4. Verificar enlaces y referencias

## 📊 Diagrama de Flujo Documental

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         Usuario lee README.md (raíz)                │
│                     │                               │
│         ┌───────────┼───────────┐                   │
│         │           │           │                   │
│         ▼           ▼           ▼                   │
│    ¿Contexto?  ¿Teoría?   ¿Resultados?             │
│         │           │           │                   │
│         ▼           ▼           ▼                   │
│   TAREA2.MD  COMPLEMENTO RESULTADOS.md              │
│                                                     │
│         └───────────┼───────────┘                   │
│                     │                               │
│                     ▼                               │
│         Navegar a carpetas técnicas:                │
│         src/, scripts/, notebooks/                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔍 Búsqueda en Documentación

### Temas clave por documento

| Documento | Palabras clave |
|-----------|----------------|
| README_TAREA2.MD | tarea, objetivos, requisitos, evaluación |
| COMPLEMENTO | teoría, matemática, autovalores, variantes |
| RESULTADOS | métricas, varianza, separación, conclusiones |

### Usando grep para buscar
```bash
# Buscar término en toda la documentación
grep -r "autovalores" docs/

# Buscar en archivo específico
grep "varianza explicada" docs/RESULTADOS.md
```

## 📦 Exportar Documentación

### A PDF
```bash
# Usando pandoc
pandoc docs/RESULTADOS.md -o RESULTADOS.pdf

# Con tabla de contenidos
pandoc docs/RESULTADOS.md -o RESULTADOS.pdf --toc
```

### A HTML
```bash
# Usando pandoc
pandoc docs/RESULTADOS.md -o RESULTADOS.html -s

# Con estilo CSS
pandoc docs/RESULTADOS.md -o RESULTADOS.html -c style.css
```

## ✅ Checklist de Documentación

Para considerar el proyecto completamente documentado:

- [x] README principal en raíz
- [x] README en cada carpeta (src/, scripts/, notebooks/, etc.)
- [x] Documentación de contexto académico
- [x] Análisis de resultados detallado
- [x] Diagramas explicativos
- [x] Referencias y recursos
- [x] Ejemplos de código
- [x] Instrucciones de uso
- [x] Guía de instalación
- [ ] Docstrings en todos los módulos (ya existe, verificar completitud)
- [ ] Tests documentados (por agregar)

## 🎓 Notas Finales

Esta documentación está diseñada para:
- Facilitar la evaluación académica
- Permitir reproducibilidad del análisis
- Servir como referencia educativa
- Demostrar comprensión profunda de PCA

**Actualización**: La documentación se mantiene sincronizada con el código. Cualquier cambio significativo en la implementación debe reflejarse aquí.
