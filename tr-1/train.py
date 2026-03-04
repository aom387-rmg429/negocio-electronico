import sys
import argparse
import pandas as pd
import torch
import warnings
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# Silence some warnings
warnings.filterwarnings("ignore")

MODEL_NAME = "distilbert-base-multilingual-cased"
OUTPUT_DIR = "./modelo_entrenado"

def train_model(data_file):
    print(f"[*] Cargando datos desde {data_file}...")
    texts = []
    labels = []
    
    # Leer el archivo de dataset
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '#' in line:
                    text, label = line.rsplit('#', 1)
                    text = text.strip()
                    label = label.strip().lower()
                    if label in ['bueno', 'malo']:
                        texts.append(text)
                        labels.append(1 if label == 'bueno' else 0)
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo {data_file}")
        sys.exit(1)
    
    if len(texts) < 10:
        print("[!] Error: No hay suficientes datos válidos en el archivo. El formato debe ser 'texto # bueno/malo'")
        sys.exit(1)
        
    df = pd.DataFrame({"text": texts, "label": labels})
    dataset = Dataset.from_pandas(df)
    
    print("[*] Cargando tokenizador y modelo pre-entrenado...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    
    print("[*] Tokenizando el dataset...")
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    # Dividimos en entrenamiento y validación (20% para test)
    split_dataset = tokenized_datasets.train_test_split(test_size=0.2, seed=42)
    train_dataset = split_dataset["train"]
    eval_dataset = split_dataset["test"]
    
    training_args = TrainingArguments(
        output_dir="./resultados",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_strategy="epoch",
        load_best_model_at_end=True,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    
    print("[*] Iniciando entrenamiento. Esto puede tomar unos minutos...")
    trainer.train()
    
    print(f"[*] Guardando modelo entrenado en {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("[+] Entrenamiento completado satisfactoriamente.")

def predict_cli():
    try:
        tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(OUTPUT_DIR)
        model.eval()
    except Exception as e:
        print(f"[!] Error al cargar el modelo desde '{OUTPUT_DIR}'. ¿Lo has entrenado primero?")
        sys.exit(1)
        
    print("\n[+] Modelo cargado. Escribe una frase para analizar su opinión.")
    print("    (Escribe 'salir' o pulsa Ctrl+C para abandonar)")
    
    label_map = {0: 'MALO', 1: 'BUENO'}
    
    while True:
        try:
            phrase = input("\n> Frase: ")
            if phrase.lower() in ['salir', 'quit', 'exit']:
                break
                
            if not phrase.strip():
                continue
                
            inputs = tokenizer(phrase, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = model(**inputs)
                
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_class].item()
            
            print(f"  --> Resultado: {label_map[predicted_class]} (Confianza: {confidence:.2f})")
            
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema de Análisis de Opinión con HuggingFace")
    parser.add_argument("--train", type=str, metavar="FILE", help="Ruta al archivo de entrenamiento (ej. dataset.txt)")
    parser.add_argument("--predict", action="store_true", help="Modo interactivo por consola para evaluar frases")
    
    args = parser.parse_args()
    
    if args.train:
        train_model(args.train)
    elif args.predict:
        predict_cli()
    else:
        print("[!] Debes indicar una acción: entrenar o predecir.")
        parser.print_help()
