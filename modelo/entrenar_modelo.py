# --------------------------------------------
# ENTRENAMIENTO DEL MODELO DE PREDICCIÓN DE DIABETES
# --------------------------------------------
# Este script:
# 1. Carga el dataset Pima Indians Diabetes.
# 2. Limpia los datos (reemplaza ceros imposibles).
# 3. Entrena un modelo de Regresión Logística.
# 4. Evalúa su rendimiento.
# 5. Guarda el modelo y el escalador para uso posterior.
# --------------------------------------------

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
from pathlib import Path

#Definir rutas
BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "dataset" / "diabetes.csv"
MODEL_PATH = BASE / "modelo" / "modelo_diabetes.sav"
SCALER_PATH = BASE / "modelo" / "scaler_diabetes.sav"

#Cargar dataset
print("Cargando conjunto de datos...")
df = pd.read_csv(DATA_PATH)
print(f"Conjunto de datos cargado correctamente: {df.shape[0]} registros y {df.shape[1]} columnas.\n")

#Limpieza de datos por datos faltantes
columnas_invalidas = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
df[columnas_invalidas] = df[columnas_invalidas].replace(0, np.nan)

# Reemplazamos los valores faltantes con la mediana de cada columna
for c in columnas_invalidas:
    df[c] = df[c].fillna(df[c].median())

#Separar variables
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

#Dividir en entrenamiento y prueba
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Escalamiento
escalador = StandardScaler()
X_entrenamiento_esc = escalador.fit_transform(X_entrenamiento)
X_prueba_esc = escalador.transform(X_prueba)

#Entrenar modelo
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_entrenamiento_esc, y_entrenamiento)

#Evaluar modelo
y_pred = modelo.predict(X_prueba_esc)
exactitud = accuracy_score(y_prueba, y_pred)
matriz = confusion_matrix(y_prueba, y_pred)
reporte = classification_report(y_prueba, y_pred, output_dict=True)

print("RESULTADOS DEL MODELO")
print(f"Exactitud general del modelo: {exactitud:.2f}")
print("\nMatriz de confusión:")
print(matriz)
print("\n REPORTE DE CLASIFICACIÓN")
print(f"Clase 0 (Sin diabetes) → Precisión: {reporte['0']['precision']:.2f}, Sensibilidad: {reporte['0']['recall']:.2f}, F1: {reporte['0']['f1-score']:.2f}")
print(f"Clase 1 (Con diabetes) → Precisión: {reporte['1']['precision']:.2f}, Sensibilidad: {reporte['1']['recall']:.2f}, F1: {reporte['1']['f1-score']:.2f}")
print(f"\nExactitud total del modelo: {reporte['accuracy']:.2f}")

#Guardar modelo y escalador
joblib.dump(modelo, MODEL_PATH)
joblib.dump(escalador, SCALER_PATH)

print(f"\n Modelo guardado en: {MODEL_PATH}")
print(f" Escalador guardado en: {SCALER_PATH}")
print("\n Entrenamiento completado exitosamente.")
