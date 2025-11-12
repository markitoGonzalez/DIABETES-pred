from flask import Flask, request, jsonify
import joblib
import numpy as np
from pathlib import Path
from flask_cors import CORS

#Configuración básica
app = Flask(__name__)
CORS(app)

BASE = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE / "modelo" / "modelo_diabetes.sav"
SCALER_PATH = BASE / "modelo" / "scaler_diabetes.sav"

#Cargar modelo y escalador
modelo = joblib.load(MODEL_PATH)
escalador = joblib.load(SCALER_PATH)

print("✅ Modelo y escalador cargados correctamente.")

#Endpoint principal
@app.route('/predict', methods=['POST'])
def predecir_diabetes():
    try:
        data = request.get_json()
        valores = [
            data["Pregnancies"],
            data["Glucose"],
            data["BloodPressure"],
            data["SkinThickness"],
            data["Insulin"],
            data["BMI"],
            data["DiabetesPedigreeFunction"],
            data["Age"]
        ]

        # Convertir a array NumPy y escalar
        datos_np = np.array([valores])
        datos_escalados = escalador.transform(datos_np)

        # Predicción
        resultado = modelo.predict(datos_escalados)[0]
        probabilidad = modelo.predict_proba(datos_escalados)[0][1]

        # Interpretación del resultado
        mensaje = "Riesgo de diabetes detectado" if resultado == 1 else "Sin riesgo aparente"

        return jsonify({
            "resultado": int(resultado),
            "probabilidad": round(float(probabilidad), 2),
            "mensaje": mensaje
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#Ruta de prueba
@app.route('/')
def inicio():
    return jsonify({"mensaje": "API de predicción de diabetes funcionando correctamente"})

#Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
