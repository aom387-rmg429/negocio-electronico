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
1. Instalar dependencias: `pip install -r requirements.txt`
2. Entrenar: `python train.py --train dataset.txt`
3. Ejecutar web: `python app.py`
