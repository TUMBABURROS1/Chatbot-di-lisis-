import streamlit as st
import openai

# Configuración de la interfaz de la página
st.set_page_config(page_title="Chatbot de Nutrición Renal", page_icon="🍎")

# Intentar usar la llave de los secrets (si no es válida, el código no se caerá)
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    openai.api_key = "no_key"

# Base de datos completa de alimentos
alimentos_db = {
    # NO SE PUEDEN CONSUMIR (Rojo) - Prioridad alta en la búsqueda
    "refrescos oscuros": "🔴 **Refrescos oscuros**: No se pueden consumir. Son peligrosos por su alto contenido de fósforo aditivo.",
    "refresco oscuro": "🔴 **Refresco oscuro**: No se puede consumir. Es peligroso por su alto contenido de fósforo aditivo.",
    "refresco negro": "🔴 **Refresco negro**: No se puede consumir. Es peligroso por su alto contenido de fósforo aditivo.",
    "queso amarillo": "🔴 **Queso amarillo**: No se puede consumir. Es un queso procesado muy alto en sodio y fósforo.",
    "queso tipo americano": "🔴 **Queso tipo americano**: No se puede consumir. Es procesado y dañino para los riñones.",
    "quesos procesados": "🔴 **Quesos procesados**: No se pueden consumir por su alta cantidad de aditivos de sodio y fósforo.",
    "frutos secos": "🔴 **Frutos secos**: No se pueden consumir por su altísimo contenido de potasio y fósforo.",
    "cerveza": "🔴 **Cerveza**: No se puede consumir. Altera el equilibrio de líquidos y aporta fósforo innecesario.",
    "chocolates": "🔴 **Chocolates**: No se pueden consumir por sus niveles elevados de potasio y fósforo.",
    "embutidos": "🔴 **Embutidos**: No se pueden consumir. Tienen demasiado sodio y conservadores perjudiciales.",
    "sopas instantaneas": "🔴 **Sopas instantáneas**: No se pueden consumir. Su contenido de sodio es crítico.",
    "alimentos enlatados": "🔴 **Alimentos enlatados**: No se pueden consumir debido al exceso de sodio usado para conservarlos.",
    "botana salada": "🔴 **Botana salada**: No se puede consumir. Aumenta gravemente la sed y la presión arterial.",
    "salsa embotellada": "🔴 **Salsa embotellada**: No se puede consumir por la cantidad oculta de sodio.",
    "comida rapida": "🔴 **Comida rápida**: No se puede consumir. Es alta en sodio, fósforo y grasas saturadas.",
    "encurtidos": "🔴 **Encurtidos**: No se pueden consumir. Están sumergidos en altas cantidades de sal.",
    "carne ahumada": "🔴 **Carne ahumada**: No se puede consumir por su excesiva carga de sodio.",
    "pescado ahumado": "🔴 **Pescado ahumado**: No se puede consumir por su excesiva carga de sodio.",
    "carambola": "🔴 **Carambola**: ¡Prohibido! Contiene una neurotoxina que los riñones en diálisis no pueden filtrar.",
    "toronja": "🔴 **Toronja**: No se puede consumir. Interfiere de forma peligrosa con múltiples medicamentos.",
    "caldos": "🔴 **Caldos**: No se pueden consumir. Concentran demasiado potasio y sodio de los ingredientes.",
    "perros calientes": "🔴 **Perros calientes**: No se pueden consumir. Es carne procesada con exceso de fósforo y sal.",
    "chili enlatado": "🔴 **Chili enlatado**: No se puede consumir por su alto nivel de sodio en conserva.",
    "carnes procesadas": "🔴 **Carnes procesadas**: No se pueden consumir. Dañan el control de toxinas en hemodiálisis.",
    "quesos": "🔴 **Quesos**: En general, la mayoría de los quesos (especialmente maduros o procesados) no se pueden consumir.",
    "queso": "🔴 **Queso**: En general, la mayoría de los quesos no se pueden consumir por su aporte de fósforo.",

    # CON MODERACIÓN (Amarillo)
    "refresco claro": "🟡 **Refresco claro**: Se debe consumir con moderación e idealmente bajo las especificaciones de tu nutriólogo.",
    "refrescos claros": "🟡 **Refrescos claros**: Se deben consumir con moderación e idealmente bajo las especificaciones de tu nutriólogo.",
    "refrescos": "🟡 **Refrescos**: Ojo, solo los refrescos claros se permiten con moderación; los oscuros están prohibidos.",
    "refresco": "🟡 **Refresco**: Ojo, solo el refresco claro se permite con moderación; los oscuros están prohibidos.",
    "queso cottage bajo en sodio": "🟡 **Queso cottage bajo en sodio**: Consumir con moderación bajo la vigilancia de tu nutriólogo.",
    "queso cottage": "🟡 **Queso cottage**: Consumir con moderación por su contenido moderado de fósforo.",
    "productos integrales": "🟡 **Productos integrales**: Consumir con moderación (aportan más fósforo que los refinados).",
    "lacteos": "🟡 **Lácteos**: Consumir con estricta moderación por su aporte de calcio y fósforo.",
    "leche": "🟡 **Leche**: Con moderación (máximo 1/2 taza al día para cuidar los niveles de minerales).",
    "sandia": "🟡 **Sandía**: Con moderación debido a su alto contenido de agua.",
    "aceite de oliva": "🟡 **Aceite de oliva**: Con moderación. Es una grasa saludable excelente para aportar calorías.",
    "aceite vegetal": "🟡 **Aceite vegetal**: Con moderación. Ayuda a dar energía limpia si se cuidan las porciones.",
    "aceite": "🟡 **Aceite**: Con moderación. Prefiere aceites vegetales como oliva o canola sobre grasas animales.",
    
    # SE PUEDE CONSUMIR (Verde)
    "pechuga de pollo": "🟢 **Pechuga de pollo**: Se puede consumir libremente (proteína de alta calidad con pocas toxinas).",
    "pechuga de pavo": "🟢 **Pechuga de pavo**: Se puede consumir libremente (excelente fuente de proteína limpia).",
    "clara de huevo": "🟢 **Clara de huevo**: Se puede consumir libremente. Es la proteína más limpia disponible.",
    "claras de huevo": "🟢 **Claras de huevo**: Se pueden consumir libremente. Ideal para pacientes en diálisis.",
    "ejotes": "🟢 **Ejotes**: Se pueden consumir libremente (verdura baja en potasio).",
    "pimiento morron": "🟢 **Pimiento morrón**: Se puede consumir libremente en tus platillos.",
    "cebolla blanca": "🟢 **Cebolla blanca**: Se puede consumir libremente para dar sabor sin sal.",
    "ajo": "🟢 **Ajo**: Se puede consumir libremente. Excelente sazonador natural.",
    "zanahoria cocida": "🟢 **Zanahoria cocida**: Se puede consumir libremente en las porciones recomendadas.",
    "pera": "🟢 **Pera**: Se puede consumir libremente (fruta con bajo aporte de potasio).",
    "fresas": "🟢 **Fresas**: Se pueden consumir libremente (bajas en potasio y ricas en antioxidantes).",
    "arandanos": "🟢 **Arándanos**: Se pueden consumir libremente. Apoyan además la salud urinaria.",
    "uva": "🟢 **Uva**: Se puede consumir libremente como opción de fruta segura.",
    "uvas": "🟢 **Uvas**: Se pueden consumir libremente en la dieta diaria.",
    "gelatina": "🟢 **Gelatina**: Se puede consumir libremente (pero controla el líquido total del día).",
    "manzana": "🟢 **Manzana**: Se puede consumir libremente. Una de las mejores frutas renales.",
    "arroz": "🟢 **Arroz**: Se puede consumir libremente (aporta energía y es bajo en minerales).",
}

# Respuestas temáticas conceptuales basadas en tus apuntes técnicos
respuestas_tematicas = {
    "liquidos": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acum
    
