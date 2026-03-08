---
title: TR1 - Análisis de Opinión
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Aplicación de Análisis de Opinión con Transformers y Flask

Este proyecto utiliza Fine-tuning de DistilBERT para clasificar opiniones como "buenas" o "malas". 
Desarrollado como parte del **Trabajo 1** para la asignatura de Negocio Electrónico.

## Ejecución Local

### Si es la primera vez que se ejecuta en la máquina

1. Crear el entorno virtual mediante `python -m venv venv`

### Una vez se tiene el entorno virtual

1. Activar el entorno virtual con `venv\Scripts\activate` en Windows o `source venv/bin/activate` en macOS\Linux.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Entrenar: `python train.py --train dataset.txt`
4. Ejecutar web: `python app.py`
