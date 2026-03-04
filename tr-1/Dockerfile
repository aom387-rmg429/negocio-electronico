# Usar la imagen base de Python oficial
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .
COPY app.py .
COPY train.py .
COPY dataset.txt .
COPY templates/ ./templates/

# Instalar dependencias
# Se añade --no-cache-dir para reducir el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Entrenar el modelo durante la construcción de la imagen
# Esto asegura que el modelo esté listo cuando arranque el contenedor
RUN python train.py --train dataset.txt

# Exponer el puerto que usa Hugging Face Spaces
EXPOSE 7860

# Ejecutar la aplicación
# Usamos 0.0.0.0 para que sea accesible externamente y el puerto 7860
CMD ["python", "app.py"]
