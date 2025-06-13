
# 📐 ArUco Analyzer App – TFG UC3M

Aplicación interactiva para el análisis de desplazamientos en ensayos mecánicos, basada en visión por computador con marcadores **ArUco**. Este proyecto ha sido desarrollado como parte del **Trabajo de Fin de Grado en Ingeniería Mecánica** en la Universidad Carlos III de Madrid.

---

## 🧩 Descripción general

Este TFG presenta una herramienta que permite **medir y analizar desplazamientos** en pruebas de tracción mediante el seguimiento automático de marcadores ArUco en vídeos. El sistema combina visión por computador, interfaces gráficas y procesamiento de imágenes para aportar una alternativa práctica y económica a métodos tradicionales de medición.

A lo largo del desarrollo se abordó también la posibilidad de **utilizar esta herramienta como apoyo en el análisis y selección de materiales**, lo que refuerza su aplicabilidad en entornos académicos, de investigación y profesionales.

---

## 🛠️ Manual de instalación y uso

### ▶️ Requisitos previos

Asegúrate de tener instalado Python 3.8 o superior. Para instalar las dependencias necesarias, ejecuta:

```bash
pip install opencv-contrib-python pillow matplotlib
```

### 📥 Instalación

1. Clona el repositorio o descarga el archivo `aruco_gui.py`.
2. Guarda el archivo en un directorio de trabajo local.

### 💻 Ejecución

Desde la terminal o tu entorno de desarrollo (PyCharm, VSCode, etc.):

```bash
python aruco_gui.py
```

La interfaz gráfica se abrirá automáticamente.

---

### 📋 Uso paso a paso

1. **Seleccionar vídeo:**  
   Pulsa “Seleccionar Video” y carga el archivo de ensayo que deseas analizar.

2. **Calibrar escala:**  
   Haz clic en dos puntos del vídeo con distancia conocida (por ejemplo, una regla), e introduce la distancia real en mm.

3. **Elegir diccionario ArUco:**  
   Selecciona el tipo de diccionario adecuado según el marcador utilizado (por defecto se puede usar `DICT_4X4_50`).

4. **Iniciar análisis:**  
   Haz clic en “Iniciar Análisis”. La herramienta detectará los marcadores frame a frame, calculará coordenadas, rotaciones y desplazamientos, y exportará los resultados en un `.csv`.

5. **Visualizar resultados:**  
   Se mostrará automáticamente una gráfica del desplazamiento relativo entre los marcadores ID 0 e ID 1, con anotaciones detalladas.

6. **Finalización:**  
   Al finalizar el análisis, se notificará con un mensaje de confirmación y se indicará la ubicación del archivo CSV generado.

---

## 🚀 Funcionalidades principales

- ✅ Detección y seguimiento de marcadores ArUco en vídeo.
- 📏 Calibración de escala px/mm mediante selección manual de puntos conocidos.
- 🎞️ Análisis continuo con registro de:
  - Coordenadas (X, Y)
  - Rotación del marcador
  - Desplazamiento vertical relativo entre IDs 0 y 1
- 📊 Generación de gráfico con anotaciones del desplazamiento neto.
- 📂 Exportación automática a CSV con todos los datos y resumen final.
- 🧪 Interfaz gráfica amigable con selección de diccionario ArUco.

---

## 🧰 Tecnologías y librerías usadas

- **Python 3**
- `OpenCV` (detección ArUco y procesamiento de vídeo)
- `Tkinter` (interfaz gráfica)
- `NumPy` (cálculos matemáticos)
- `matplotlib` (visualización de resultados)
- `PIL` (visualización de frames en GUI)

---

## 📁 Estructura de archivos

```
.
├── aruco_gui.py           # Código principal de la aplicación
├── README.md              # Este archivo
├── output/
│   ├── aruco_tracking_*.csv  # Archivos de salida generados por la app
```

---

## 📑 Contenido adicional del TFG

- 📘 Introducción teórica sobre visión por computador y marcadores ArUco.
- 🔬 Comparativa entre datos de máquina de tracción y detección visual.
- 🧾 Presupuesto estimado para implementación real.
- 📚 Revisión del marco normativo aplicable.
- 📄 Guía de buenas prácticas para reproducibilidad del experimento.

---

## 🧪 Ejemplo de uso

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Aruco_Markers.jpg/320px-Aruco_Markers.jpg" width="320" alt="Ejemplo ArUco">

> Tras procesar el vídeo, se genera un gráfico como este con el desplazamiento vertical entre dos marcadores seleccionados, útil para analizar la deformación en ensayos mecánicos.

---

## 📜 Licencia

Este proyecto ha sido desarrollado exclusivamente con fines académicos. El código está disponible bajo los términos de la licencia MIT para su uso, modificación y distribución libre.

---

## 👨‍🎓 Autor

**Hugo Irureta**  
Estudiante de Grado en Ingeniería Mecánica  
Universidad Carlos III de Madrid (UC3M)  
Curso 2024–2025

---

## 📬 Contacto

Para consultas o colaboración, puedes contactar al autor a través del correo institucional UC3M o mediante GitHub.
