import streamlit as st
import pandas as pd
import joblib

# Configuración
st.set_page_config(page_title="Asistente de Diagnóstico - Modelo A", layout="wide")

@st.cache_resource
def load_assets():
    model = joblib.load('model_A_diag.joblib')
    preprocessor = joblib.load('preprocessor_A.joblib')
    return model, preprocessor

model, preprocessor = load_assets()

st.title("🧪 Sistema de Soporte al Diagnóstico de Diabetes")
st.info("Este modelo utiliza biomarcadores clínicos (Glucosa, HbA1c) para confirmar la presencia de diabetes.")

with st.form("clinical_form"):
    # Sección 1: Marcadores Críticos (Los que RandomForest marcó como más importantes)
    st.subheader("🩸 Biomarcadores de Glucosa")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        hba1c = st.number_input("HbA1c (%)", 4.0, 15.0, 5.4, help="Hemoglobina Glicosilada")
    with c2:
        glu_fasting = st.number_input("Glucosa Basal (mg/dL)", 50, 400, 95)
    with c3:
        glu_post = st.number_input("Glucosa Postprandial (mg/dL)", 70, 500, 120)
    with c4:
        insulin = st.number_input("Nivel de Insulina (µU/mL)", 2.0, 100.0, 15.0)

    st.divider()

    # Sección 2: Otros datos clínicos y demográficos
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📊 Perfil del Paciente")
        age = st.number_input("Edad", 1, 120, 45)
        gender = st.selectbox("Género", ["Male", "Female", "Other"])
        bmi = st.number_input("IMC", 10.0, 60.0, 26.5)
        risk_score = st.slider("Diabetes Risk Score previo", 0.0, 1.0, 0.4)
        ethnicity = st.selectbox("Etnia", ["Caucasian", "African American", "Asian", "Hispanic", "Other"])
        employment = st.selectbox("Empleo", ["Employed", "Unemployed", "Self-Employed", "Retired"])
        education = st.selectbox("Educación", ['No formal', 'Highschool', 'Graduate', 'Postgraduate'])
        income = st.selectbox("Ingresos", ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High'])
        
    with col_b:
        st.subheader("💓 Signos Vitales y Lípidos")
        sys_bp = st.number_input("Sistólica", 80, 200, 120)
        dia_bp = st.number_input("Diastólica", 50, 120, 80)
        heart_rate = st.number_input("Frecuencia Cardíaca", 40, 150, 72)
        chol = st.number_input("Colesterol Total", 100, 400, 200)
        tri = st.number_input("Triglicéridos", 50, 500, 150)
        hdl = st.number_input("HDL", 20, 100, 50)
        ldl = st.number_input("LDL", 50, 300, 120)

    st.subheader("📋 Antecedentes y Estilo de Vida")
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        fam_hist = st.checkbox("Historia Familiar")
        hyp_hist = st.checkbox("Hipertensión")
    with c6:
        cardio = st.checkbox("Cardiopatía")
        smoking = st.selectbox("Fumador", ['Never', 'Former', 'Current'])
    with c7:
        activity = st.number_input("Actividad (min/sem)", 0, 1000, 150)
        alcohol = st.number_input("Alcohol (u/sem)", 0, 100, 2)
    with c8:
        diet = st.slider("Dieta (0-10)", 0, 10, 6)
        sleep = st.number_input("Sueño (h/día)", 0, 24, 7)
        screen = st.number_input("Pantalla (h/día)", 0, 24, 4)
        whr = st.number_input("WHR (Cintura/Cadera)", 0.5, 1.5, 0.85)

    submit = st.form_submit_button("EJECUTAR DIAGNÓSTICO")

if submit:
    # Construir el diccionario con todas las columnas que espera el preprocesador A
    input_data = pd.DataFrame({
        'age': [age], 'gender': [gender], 'ethnicity': [ethnicity],
        'education_level': [education], 'income_level': [income],
        'employment_status': [employment], 'alcohol_consumption_per_week': [alcohol],
        'physical_activity_minutes_per_week': [activity], 'diet_score': [diet],
        'sleep_hours_per_day': [sleep], 'screen_time_hours_per_day': [screen],
        'smoking_status': [smoking], 'bmi': [bmi], 'waist_to_hip_ratio': [whr],
        'systolic_bp': [sys_bp], 'diastolic_bp': [dia_bp], 'heart_rate': [heart_rate],
        'cholesterol_total': [chol], 'hdl_cholesterol': [hdl], 'ldl_cholesterol': [ldl],
        'triglycerides': [tri], 'glucose_fasting': [glu_fasting], 
        'glucose_postprandial': [glu_post], 'insulin_level': [insulin], 'hba1c': [hba1c],
        'diabetes_risk_score': [risk_score], 'family_history_diabetes': [1 if fam_hist else 0],
        'hypertension_history': [1 if hyp_hist else 0],
        'cardiovascular_history': [1 if cardio else 0]
    })

    # Procesar y predecir
    input_p = preprocessor.transform(input_data)
    prob = model.predict_proba(input_p)[0][1]
    
    # Umbral sugerido en tu análisis (0.3)
    umbral = 0.3
    
    st.divider()
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.metric(label="Probabilidad de Diabetes", value=f"{prob*100:.1f}%")
        
    with col_res2:
        if prob >= umbral:
            st.error("RESULTADO: POSITIVO PARA DIABETES")
            st.write("El modelo detecta patrones claros compatibles con diabetes.")
        else:
            st.success("RESULTADO: NEGATIVO")
            st.write("Los valores se encuentran dentro de los rangos normales para el modelo.")

    st.warning("⚠️ Nota: Esta es una herramienta experimental basada en datos históricos. No sustituye un diagnóstico médico profesional.")