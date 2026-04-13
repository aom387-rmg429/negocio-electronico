"""
TR-3: Clasificador de opiniones de productos con Transformers
Entrena un modelo para clasificar frases en:
  - manual_instrucciones
  - enviar_tecnico
"""

import os
import sys
import re
import argparse
import numpy as np
from pathlib import Path

# Suprimir warnings innecesarios
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    pipeline,
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
MODELO_BASE = "dccuchile/bert-base-spanish-wwm-cased"  # BERT en español
DIRECTORIO_MODELO = Path("modelo_entrenado")
ETIQUETAS = ["manual_instrucciones", "enviar_tecnico"]
ETIQUETA2ID = {e: i for i, e in enumerate(ETIQUETAS)}
ID2ETIQUETA = {i: e for i, e in enumerate(ETIQUETAS)}
SEPARADORES = r"[#;|\t]"  # separadores soportados


# ---------------------------------------------------------------------------
# 1. Lectura del archivo de datos
# ---------------------------------------------------------------------------
def cargar_datos(ruta_archivo: str):
    """Lee el archivo y devuelve listas de frases y etiquetas."""
    frases, etiquetas = [], []
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    with open(ruta, encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            linea = linea.strip()
            # Ignorar vacías y comentarios
            if not linea or linea.startswith("#"):
                continue
            partes = re.split(SEPARADORES, linea, maxsplit=1)
            if len(partes) != 2:
                print(f"  [!] Línea {num_linea} ignorada (formato incorrecto): {linea}")
                continue
            frase, etiqueta = partes[0].strip(), partes[1].strip()
            if etiqueta not in ETIQUETA2ID:
                print(f"  [!] Línea {num_linea} ignorada (etiqueta desconocida '{etiqueta}'): {linea}")
                continue
            frases.append(frase)
            etiquetas.append(ETIQUETA2ID[etiqueta])

    print(f"  Cargadas {len(frases)} muestras desde '{ruta_archivo}'")
    return frases, etiquetas


# ---------------------------------------------------------------------------
# 2. Dataset de PyTorch
# ---------------------------------------------------------------------------
class OpinionesDataset(Dataset):
    def __init__(self, frases, etiquetas, tokenizer, max_len=128):
        self.encodings = tokenizer(
            frases,
            truncation=True,
            padding=True,
            max_length=max_len,
            return_tensors="pt",
        )
        self.labels = torch.tensor(etiquetas, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item


# ---------------------------------------------------------------------------
# 3. Métricas
# ---------------------------------------------------------------------------
def calcular_metricas(eval_pred):
    logits, labels = eval_pred
    predicciones = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, predicciones)}


# ---------------------------------------------------------------------------
# 4. Entrenamiento
# ---------------------------------------------------------------------------
def entrenar(ruta_archivo: str, epochs: int = 5):
    print("\n=== FASE DE ENTRENAMIENTO ===\n")

    frases, etiquetas = cargar_datos(ruta_archivo)
    if len(frases) < 4:
        raise ValueError("Se necesitan al menos 4 muestras para entrenar.")

    # División train / validación (80/20)
    f_train, f_val, e_train, e_val = train_test_split(
        frases, etiquetas, test_size=0.2, random_state=42, stratify=etiquetas
    )
    print(f"  Train: {len(f_train)} | Validación: {len(f_val)}")

    print(f"\n  Cargando tokenizador '{MODELO_BASE}'...")
    tokenizer = AutoTokenizer.from_pretrained(MODELO_BASE)

    print("  Tokenizando datos...")
    ds_train = OpinionesDataset(f_train, e_train, tokenizer)
    ds_val = OpinionesDataset(f_val, e_val, tokenizer)

    print(f"  Cargando modelo base '{MODELO_BASE}'...")
    modelo = AutoModelForSequenceClassification.from_pretrained(
        MODELO_BASE,
        num_labels=len(ETIQUETAS),
        id2label=ID2ETIQUETA,
        label2id=ETIQUETA2ID,
    )

    args_entrenamiento = TrainingArguments(
        output_dir=str(DIRECTORIO_MODELO / "checkpoints"),
        num_train_epochs=epochs,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=10,
        weight_decay=0.01,
        # logging_dir se configura vía variable de entorno TENSORBOARD_LOGGING_DIR
        logging_steps=5,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to="none",
    )

    trainer = Trainer(
        model=modelo,
        args=args_entrenamiento,
        train_dataset=ds_train,
        eval_dataset=ds_val,
        compute_metrics=calcular_metricas,
    )

    print(f"\n  Entrenando durante {epochs} épocas...\n")
    trainer.train()

    # Evaluación final
    metricas = trainer.evaluate()
    print(f"\n  Resultados finales: accuracy={metricas.get('eval_accuracy', 0):.2%}")

    # Guardar modelo y tokenizador
    DIRECTORIO_MODELO.mkdir(parents=True, exist_ok=True)
    modelo.save_pretrained(DIRECTORIO_MODELO)
    tokenizer.save_pretrained(DIRECTORIO_MODELO)
    print(f"\n  Modelo guardado en '{DIRECTORIO_MODELO}/'")

    # Reporte detallado con todos los datos
    print("\n  === Reporte de clasificación (train completo) ===")
    ds_todo = OpinionesDataset(frases, etiquetas, tokenizer)
    preds = trainer.predict(ds_todo)
    y_pred = np.argmax(preds.predictions, axis=-1)
    print(classification_report(etiquetas, y_pred, target_names=ETIQUETAS))


# ---------------------------------------------------------------------------
# 5. Inferencia interactiva
# ---------------------------------------------------------------------------
def modo_interactivo():
    print("\n=== MODO INTERACTIVO ===\n")

    if not DIRECTORIO_MODELO.exists():
        print(f"  [ERROR] No se encontró el modelo en '{DIRECTORIO_MODELO}/'.")
        print("  Ejecuta primero: python clasificador_opiniones.py --entrenar\n")
        sys.exit(1)

    print(f"  Cargando modelo desde '{DIRECTORIO_MODELO}'...")
    clasificador = pipeline(
        "text-classification",
        model=str(DIRECTORIO_MODELO),
        tokenizer=str(DIRECTORIO_MODELO),
        device=-1,  # CPU; cambia a 0 para GPU
    )
    print("  Modelo listo.\n")
    print("  Escribe una opinión del producto y el sistema indicará la acción recomendada.")
    print("  Escribe 'salir' para terminar.\n")

    while True:
        try:
            frase = input("Opinión: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Hasta luego.")
            break

        if not frase:
            continue
        if frase.lower() in ("salir", "exit", "quit"):
            print("  Hasta luego.")
            break

        resultado = clasificador(frase)[0]
        etiqueta = resultado["label"]
        confianza = resultado["score"]

        # Mensaje amigable según la etiqueta
        if etiqueta == "manual_instrucciones":
            accion = "Consultar el manual de instrucciones"
            icono = "[MANUAL]"
        else:
            accion = "Enviar al servicio técnico"
            icono = "[TÉCNICO]"

        print(f"  {icono} Acción recomendada : {accion}")
        print(f"           Confianza       : {confianza:.1%}\n")


# ---------------------------------------------------------------------------
# 6. Punto de entrada
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Clasificador de opiniones de productos (manual vs técnico)"
    )
    parser.add_argument(
        "--entrenar",
        action="store_true",
        help="Entrenar el modelo con el archivo de datos",
    )
    parser.add_argument(
        "--archivo",
        default="datos_entrenamiento.txt",
        help="Ruta al archivo de entrenamiento (por defecto: datos_entrenamiento.txt)",
    )
    parser.add_argument(
        "--epocas",
        type=int,
        default=5,
        help="Número de épocas de entrenamiento (por defecto: 5)",
    )
    args = parser.parse_args()

    if args.entrenar:
        entrenar(args.archivo, args.epocas)
        print("\n  Entrenamiento completado. Iniciando modo interactivo...\n")

    modo_interactivo()


if __name__ == "__main__":
    main()
