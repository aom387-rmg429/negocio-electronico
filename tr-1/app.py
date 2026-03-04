from flask import Flask, render_template, request
import torch
import warnings
from transformers import AutoTokenizer, AutoModelForSequenceClassification

warnings.filterwarnings("ignore")

app = Flask(__name__)

MODEL_DIR = "./modelo_entrenado"

print("[*] Iniciando aplicación web Flask y cargando modelo...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    print("[+] Modelo cargado correctamente.")
except Exception as e:
    print(f"[!] Advertencia: No se pudo cargar el modelo desde {MODEL_DIR}.")
    print("    Asegúrate de ejecutar el script de entrenamiento primero (python train.py --train dataset.txt).")
    tokenizer = None
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence = None
    phrase = ""
    
    if request.method == "POST":
        phrase = request.form.get("phrase", "")
        if phrase and model and tokenizer:
            inputs = tokenizer(phrase, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = model(**inputs)
            
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(predictions, dim=-1).item()
            
            label_map = {0: 'malo', 1: 'bueno'}
            result = label_map[predicted_class]
            confidence = round(predictions[0][predicted_class].item() * 100, 2)
            
    return render_template(
        "index.html", 
        result=result, 
        confidence=confidence, 
        phrase=phrase, 
        model_loaded=(model is not None)
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860)
