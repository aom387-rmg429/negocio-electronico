# TR-3: Clasificador de opiniones de productos

Clasifica frases de opinión en dos categorías de acción de mantenimiento:
- `manual_instrucciones` — el usuario puede resolver el problema consultando el manual
- `enviar_tecnico` — el producto necesita revisión por un técnico

## Instalación

```bash
pip install -r requirements.txt
```

## Archivo de datos

Cada línea del archivo de entrenamiento sigue el formato:

```
<frase>#<etiqueta>
```

Separadores soportados: `#`, `;`, `|`, tabulador.
Las líneas que empiecen con `#` se tratan como comentarios.

**Ejemplo:**
```
No sé cómo configurar la pantalla inicial#manual_instrucciones
El motor hace un sonido raro y huele a quemado#enviar_tecnico
```

## Uso

### 1. Entrenar y luego usar el modo interactivo

```bash
python clasificador_opiniones.py --entrenar
```

### 2. Entrenar con un archivo personalizado y más épocas

```bash
python clasificador_opiniones.py --entrenar --archivo mis_datos.txt --epocas 10
```

### 3. Solo modo interactivo (modelo ya entrenado)

```bash
python clasificador_opiniones.py
```

## Notas

- El modelo base utilizado es `dccuchile/bert-base-spanish-wwm-cased` (BERT en español).
- El modelo entrenado se guarda en `modelo_entrenado/`.
- Se necesita conexión a Internet la primera vez para descargar el modelo base.


## Extras

- Crear enntorno virtual `python3 -m venv venv`

- Usar entorno virtual `source venv/bin/activate`