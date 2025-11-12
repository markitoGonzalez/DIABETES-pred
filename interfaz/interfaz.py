import streamlit as st
import requests

# ---------- CONFIGURACIÓN DE LA PÁGINA ----------
st.set_page_config(
    page_title="Predicción de Diabetes 🩺",
    page_icon="🧬",
    layout="centered",
)

# ---------- ESTILOS PERSONALIZADOS ----------
st.markdown("""
    <style>
        body {
            background-color: #ffffff;  /* Fondo blanco */
        }
        .main {
            background-color: #ffffff;
        }
        .title {
            color: #0a5ba8;
            text-align: center;
            font-size: 38px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #555555;
            font-size: 18px;
            margin-bottom: 40px;
        }
        .form-box {
            background-color: #e6f2ff; /* Azul celeste muy suave */
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0px 0px 10px rgba(0, 90, 150, 0.2);
        }
        .result-box {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-top: 25px;
            font-weight: bold;
        }
        .success {
            background-color: #e6ffed;
            border: 2px solid #00a000;
            color: #007000;
        }
        .alert {
            background-color: #ffe6e6;
            border: 2px solid #cc0000;
            color: #a00000;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- ENCABEZADO ----------
st.markdown('<div class="title">🩺 Sistema de Predicción de Diabetes</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ingrese los valores clínicos del paciente para obtener una predicción médica precisa.</div>', unsafe_allow_html=True)

# URL del backend Flask
API_URL = "http://127.0.0.1:5000/predict"

# ---------- FORMULARIO ----------
with st.container():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        embarazos = st.number_input("🤰 Número de embarazos", 0, 20, 1)
        glucosa = st.number_input("🧪 Nivel de glucosa (mg/dL)", 0, 300, 120)
        presion = st.number_input("❤️ Presión arterial (mm Hg)", 0, 200, 70)
        espesor = st.number_input("📏 Espesor del pliegue cutáneo (mm)", 0, 100, 20)
    with col2:
        insulina = st.number_input("💉 Nivel de insulina (μU/ml)", 0, 900, 80)
        bmi = st.number_input("⚖️ Índice de masa corporal (BMI)", 0.0, 70.0, 25.0)
        genetica = st.number_input("🧬 Predisposición genética", 0.0, 2.5, 0.5)
        edad = st.number_input("🎂 Edad del paciente", 1, 120, 35)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- BOTÓN DE PREDICCIÓN ----------
st.markdown("---")
if st.button("🔍 Analizar Riesgo de Diabetes", use_container_width=True):
    datos = {
        "Pregnancies": embarazos,
        "Glucose": glucosa,
        "BloodPressure": presion,
        "SkinThickness": espesor,
        "Insulin": insulina,
        "BMI": bmi,
        "DiabetesPedigreeFunction": genetica,
        "Age": edad
    }

    try:
        respuesta = requests.post(API_URL, json=datos)
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            if resultado["resultado"] == 1:
                st.markdown(
                    f"<div class='result-box alert'>⚠️ {resultado['mensaje']}<br>"
                    f"<b>Probabilidad estimada:</b> {resultado['probabilidad']*100:.0f}%</div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div class='result-box success'>✅ {resultado['mensaje']}<br>"
                    f"<b>Probabilidad estimada:</b> {resultado['probabilidad']*100:.0f}%</div>",
                    unsafe_allow_html=True)
        else:
            st.warning("No se pudo conectar con el servidor Flask.")
    except Exception as e:
        st.error(f"Error de conexión con la API: {e}")

# ---------- PIE DE PÁGINA ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>PREDICCIÓN DE RIESGO DE DIABETES- Marco González - Juaquin Perez - Javier Casanova</p>",
    unsafe_allow_html=True)
