# Walkthrough: Trabajo 1 - Análisis de Opinión

Este documento resume las tareas completadas para entregar el Trabajo 1, en el que se ha desarrollado un analizador de sentimientos empleando la librería `transformers` y se ha envuelto con `Flask` para proveer una interfaz web de uso. Todo el código desarrollado se ha ubicado en la ruta solicitada: `tr-1`.

## 📦 Componentes Creados

### Configuración del Entorno
- Se ha generado un archivo [requirements.txt](file:///Users/antonio/Desktop/negocio-electronico/tr-1/requirements.txt) que incluye todas las dependencias necesarias: `transformers`, `torch`, `flask`, `pandas`, `datasets`, etc.
- Se ha creado y activado un entorno virtual de Python para instalar las dependencias aisladas del sistema, evitando conflictos globales.

### Datos y Entrenamiento
- **Dataset**: Se diseñó un dataset inicial de prueba en [dataset.txt](file:///Users/antonio/Desktop/negocio-electronico/tr-1/dataset.txt). Contiene diversas frases divididas en reseñas positivas y negativas con el separador `#` y las etiquetas `bueno` / `malo`.
- **Script de Entrenamiento**: El código base reside en [train.py](file:///Users/antonio/Desktop/negocio-electronico/tr-1/train.py). Este script cumple dos roles:
  1. **Entrenar el modelo**: Al ejecutar `python train.py --train dataset.txt`, el script carga el modelo `distilbert-base-multilingual-cased` de HuggingFace, tokeniza las frases, y evalúa el proceso iterativamente usando la API `Trainer` de HuggingFace. El resultado se guarda en el subdirectorio `modelo_entrenado`.
  2. **Interactivo CLI**: Usando el switch `python train.py --predict`, el CLI permite escribir frases como entrada de teclado usando el modelo previamente guardado sin tener que arrancar un servidor.

### Interfaz Web con Flask
- **Aplicación Web**: Implementada en [app.py](file:///Users/antonio/Desktop/negocio-electronico/tr-1/app.py). Levanta un servidor Flask que importa el modelo pre-entrenado y atiende las peticiones por POST y GET y responde integrando los resultados a la interfaz.
- **Frontend HTML**: Diseñado en [templates/index.html](file:///Users/antonio/Desktop/negocio-electronico/tr-1/templates/index.html). Presenta una interfaz de usuario atractiva y moderna, usando CSS embebido, para incluir en el cuado de texto la reseña que el sistema debe procesar. Muestra el nivel de confianza de la predicción y coloreado la categoría.

## 🧪 Verificación

El entrenamiento del modelo local se ha completado existosamente guardando los pesos correspondientes. 
Posteriormente, levantamos temporalmente el servidor usando el script de Flask para validar que el endpoint `/` responde sin errores, mostrando el HTML de `Evaluador de Opiniones IA`.

## 🚀 Próximos Pasos (Para Demo)

Cuando vayas al despacho de tu profesor para la demo, simplemente tienes que realizar estos pasos en una ventana de tu terminal en el mismo directorio `tr-1`:

```bash
# Entrar al entorno virtual
source venv/bin/activate

# Opcional (Para mostrar el CLI de prueba por teclado sin web)
python train.py --predict

# Para ejecutar la aplicación entera (Web)
python app.py
```
Abre en tu navegador la URL: `http://127.0.0.1:5000` y haz la demostración.


TR-1

Trabajo 1: Sistema de análisis de opinión
*  Planificación de la implementación
*  Configuración del entorno (requirements.txt)
*  Creación de un dataset de prueba (dataset.txt)
*  Desarrollo del script de entrenamiento y CLI (train.py)
    *  Carga y procesamiento del archivo de texto
    *  Entrenamiento del modelo usando Transformers
    *  Guardado del modelo
    *  Interfaz de línea de comandos para inferencia
*  Desarrollo de la aplicación web con Flask (app.py)
    *  Servidor Flask y carga del modelo
    *  Interfaz web (HTML/CSS)
    *  Integración para realizar predicciones


TR-1

Trabajo 1: Sistema de análisis de opinión
*  Planificación de la implementación
*  Configuración del entorno (requirements.txt)
*  Creación de un dataset de prueba (dataset.txt)
*  Desarrollo del script de entrenamiento y CLI (train.py)
    *  Carga y procesamiento del archivo de texto
    *  Entrenamiento del modelo usando Transformers
    *  Guardado del modelo
    *  Interfaz de línea de comandos para inferencia
*  Desarrollo de la aplicación web con Flask (app.py)
    *  Servidor Flask y carga del modelo
    *  Interfaz web (HTML/CSS)
    *  Integración para realizar predicciones


Entrenar.

cd /Users/antonio/Desktop/negocio-electronico/tr-1
source venv/bin/activate
python train.py --train dataset.txt

Run App.cd /Users/antonio/Desktop/negocio-electronico/tr-1
source venv/bin/activate
python app.py