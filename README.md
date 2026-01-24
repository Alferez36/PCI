# Manual del desarrollador

Instrucciones para desplegar el proyecto de manera local. 

## Estructura del proyecto
Para un correcto funcionamiento de la aplicación, el directorio del proyecto debe mantener la siguiente estructura: 

/
├── app.py   
├── model_A_forest.joblib
├── preprocessor_A.joblib
├── model_C_forest.joblib
├── preprocessor_C.joblib
└── requirements.txt

Incluye los preprocesadores de ambos modelos, los propios modelos entrenados, el código fuente para la aplicación (app.py) y las dependencias del sistema (requirements.txt). 

## Requisitos
- Python 3.9 o superior. 
- Gestor de paquetes pip.
- scikit-learn==1.6.1. 
El entrenamiento de los modelos se hizo sobre la versión scikit-learn 1.6.1. Se ha declarado para que no haya problemas en el deployment, ya que algunos sistemas utilizan versiones más actualizadas. 

## Instalación
1. Clonar el repositorio en local. 
2. Instalar dependencias:
`pip install -r requirements.txt`

## Ejecución local 
Se lanza la aplicación en el navegador en una URL local con el siguiente comando: 
`python -m streamlit run app.py`

# Manual de usuario 

Instrucciones de uso del prototipo. 

Este prototipo permite evaluar la presencia de diabetes en un paciente a través de modelo de aprendizaje automático supervisado. 

## 1. Selección del modelo 
En la barra lateral izquierda, puede seleccionar el modelo: 

- Modelo A (Diagnóstico): Diseñado para uso clínico como una herramienta de ayuda para los médicos para diagnosticar la diabetes. 
- Modelo B (Índice de riesgo): Evalúa el índice de riesgo basado en el estilo de vida y los antecendentes del paciente.  

## 2. Introducción de datos
La interfaz está organizada en varias pestañas en la que se debe de ingresar la información de cada paciente. 
1. Perfil: Datos demográficos y situación socioeconómica. 
2. Biomarcadores (Solo Modelo A): Glucosa e insulina. 
3. Vitales y lípidos: Valores cardiovasculares y perfil lipídico.  
4. Antecendetes y Estilo de vida: Posibles antecedentes y registro de actividad física, sueño, dieta y otros hábitos. 

## 3. Obtención del resultado
Tras haber completado todos los campos haga clic en el botón "EJECUTAR DIAGNÓSTICO". La aplicación le mostrará la métrica de probabilidad (0-100%) de padecer la enfermedad junto a un mensaje visual (Rojo para Positivo, Verde para negativo). 

[!WARNING] Aviso importante: Esta herramienta es un prototipo con fines informativos y no sustituye el juicio de un profesional de la salud. Siempre consulte a un médico.
