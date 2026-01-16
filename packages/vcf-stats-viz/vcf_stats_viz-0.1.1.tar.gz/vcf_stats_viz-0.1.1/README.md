# vcf-stats-viz 🧬📊

**`vcf-stats-viz`** es una herramienta de línea de comandos para el **análisis eficiente de archivos VCF (Variant Call Format)** y la **generación de un dashboard web interactivo local** para explorar variantes genéticas de forma visual y filtrable.

Está diseñada para trabajar con **archivos VCF grandes**, priorizando un **bajo consumo de memoria** mediante procesamiento por *chunks*, y produce resultados reutilizables que pueden explorarse posteriormente desde un navegador.

---

## ✨ Características principales

- 🔹 **Lectura eficiente de VCF**  
  Procesa archivos VCF grandes utilizando *chunking*, evitando cargar todo el archivo en memoria.

- 🔹 **Análisis completo de variantes**  
  Extrae estadísticas, resúmenes y datasets intermedios optimizados para análisis posterior.

- 🔹 **Resultados persistentes**  
  Guarda los resultados y metadatos en disco para reutilizarlos sin reprocesar el VCF.

- 🔹 **Dashboard web local interactivo**  
  Genera una aplicación web local para:
  - Visualizar estadísticas
  - Explorar variantes
  - Filtrar por distintos atributos
  - Navegar entre múltiples análisis previos

- 🔹 **Pipeline completo o modular**  
  Puedes:
  - Ejecutar análisis + dashboard en un solo paso
  - Lanzar solo el dashboard
  - Listar o limpiar análisis anteriores

---

## 📦 Instalación

Instala el paquete desde tu entorno Python (por ejemplo con `pip`):

```bash
pip install vcf-stats-viz
```

El comando de consola instalado será:

```bash
vcf-analyze
```

---

## 🚀 Uso básico

### Análisis completo + dashboard

```bash
vcf-analyze archivo.vcf
```

Esto hará lo siguiente:

1. Lee y procesa el archivo VCF de forma optimizada
2. Guarda los resultados en disco
3. Lanza automáticamente un dashboard web local

Por defecto, el dashboard estará disponible en:

```
http://127.0.0.1:5000
```

---

## ⚙️ Opciones principales

### Limitar número de variantes

```bash
vcf-analyze archivo.vcf 100000
```

Procesa solo las primeras `100000` variantes (útil para pruebas).

---

### Ajustar tamaño de chunk (memoria vs velocidad)

```bash
vcf-analyze archivo.vcf --chunk-size 20000
```

- Valores más pequeños → menor uso de memoria  
- Valores más grandes → mayor velocidad

---

### Especificar directorio de salida

```bash
vcf-analyze archivo.vcf --output-dir mis_resultados
```

Todos los análisis, metadatos y archivos intermedios se guardarán ahí.

---

### Ejecutar análisis sin lanzar el dashboard

```bash
vcf-analyze archivo.vcf --no-dashboard
```

Ideal para servidores o procesamiento batch.

---

## 🌐 Dashboard web

### Lanzar solo el dashboard (sin reprocesar VCF)

```bash
vcf-analyze --dashboard-only --output-dir vcf_analysis_results
```

El dashboard detecta automáticamente los análisis existentes en el directorio.

---

### Cambiar host y puerto

```bash
vcf-analyze archivo.vcf --host 0.0.0.0 --port 8080
```

---

### No abrir el navegador automáticamente

```bash
vcf-analyze archivo.vcf --no-browser
```

---

## 🗂️ Gestión de análisis

### Listar análisis disponibles

```bash
vcf-analyze --list-analyses
```

Muestra:
- ID del análisis
- Nombre
- Número de variantes
- Fecha
- Modo de procesamiento

---

### Limpiar análisis antiguos

```bash
vcf-analyze --clean
```

Elimina análisis antiguos, conservando los más recientes (por defecto los últimos 5).

---

## 🧠 Arquitectura interna (resumen)

- **Procesamiento**
  - Parsing optimizado del VCF
  - Análisis por chunks
  - Generación de estadísticas y resúmenes
  - Persistencia de resultados y metadatos en JSON

- **Visualización**
  - Descubrimiento automático de análisis guardados
  - Dashboard web local
  - Filtros por variante
  - Navegación entre múltiples análisis

---


## 🧪 Casos de uso típicos

- Exploración interactiva de variantes genéticas
- Análisis preliminar de VCFs grandes
- Debugging y validación de pipelines bioinformáticos
- Visualización local sin depender de servicios externos

---

## 📜 Licencia

Licencia MIT.

---

## 📫 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio de GitHub.

---
