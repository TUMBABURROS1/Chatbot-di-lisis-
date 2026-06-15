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
    # SE PUEDE CONSUMIR (Verde)
    "pechuga de pollo": "se puede consumir",
    "pechuga de pavo": "se puede consumir",
    "clara de huevo": "se puede consumir",
    "claras de huevo": "se puede consumir",
    "ejotes": "se puede consumir",
    "pimiento morron": "se puede consumir",
    "cebolla blanca": "se puede consumir",
    "ajo": "se puede consumir",
    "zanahoria cocida": "se puede consumir",
    "pera": "se puede consumir",
    "fresas": "se puede consumir",
    "arandanos": "se puede consumir",
    "uva": "se puede consumir",
    "uvas": "se puede consumir",
    "gelatina": "se puede consumir",
    "manzana": "se puede consumir",
    "arroz": "se puede consumir",
    
    # CON MODERACIÓN (Amarillo)
    "queso cottage": "con moderacion",
    "queso cottage bajo en sodio": "con moderacion",
    "productos integrales": "con moderacion",
    "lacteos": "con moderacion",
    "leche": "con moderacion (maximo 1/2 taza al dia)",
    "sandia": "con moderacion",
    "refrescos": "con moderacion (solo claros)",
    "refresco": "con moderacion (solo claros)",
    "refresco claro": "con moderacion",
    "refrescos claros": "con moderacion",
    "aceite": "con moderacion",
    "aceite de oliva": "con moderacion",
    "aceite vegetal": "con moderacion",
    
    # NO SE PUEDEN CONSUMIR (Rojo)
    "quesos": "no se puede consumir",
    "queso": "no se puede consumir",
    "queso amarillo": "no se puede consumir",
    "queso tipo americano": "no se puede consumir",
    "quesos procesados": "no se puede consumir",
    "frutos secos": "no se puede consumir",
    "cerveza": "no se puede consumir",
    "chocolates": "no se puede consumir",
    "embutidos": "no se puede consumir",
    "sopas instantaneas": "no se puede consumir",
    "alimentos enlatados": "no se puede consumir",
    "botana salada": "no se puede consumir",
    "salsa embotellada": "no se puede consumir",
    "comida rapida": "no se puede consumir",
    "encurtidos": "no se puede consumir",
    "carne ahumada": "no se puede consumir",
    "pescado ahumado": "no se puede consumir",
    "carambola": "no se puede consumir",
    "toronja": "no se puede consumir",
    "caldos": "no se puede consumir",
    "perros calientes": "no se puede consumir",
    "chili enlatado": "no se puede consumir",
    "carnes procesadas": "no se puede consumir",
    "refrescos oscuros": "no se puede consumir",
    "refresco oscuro": "no se puede consumir",
    "refresco negro": "no se puede consumir",
}

# Respuestas temáticas conceptuales basadas en tus apuntes
respuestas_tematicas = {
    "liquidos": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acumularse en el organismo. El exceso de líquidos puede causar aumento de peso entre sesiones, cambios en la presión arterial, problemas cardíacos graves e incluso acumulación en los pulmones dificultando la respiración. Se debe limitar estrictamente el sodio, potasio y fósforo para ayudar a controlarlo.",
    "agua": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acumularse en el organismo. El exceso de líquidos puede causar aumento de peso entre sesiones, cambios en la presión arterial, problemas cardíacos graves e incluso acumulación en los pulmones dificultando la respiración. Se debe limitar estrictamente el sodio, potasio y fósforo para ayudar a controlarlo.",
    "proteina": "El paciente debe asegurar el consumo de suficientes proteínas de alta calidad (como carne, aves, pescado y huevos), ya que producen menos toxinas. Sin embargo, se debe cuidar la cantidad exacta para no elevar el fósforo en el organismo. Se deben evitar por completo las carnes procesadas como perros calientes o embutidos por su alto contenido de sodio.",
    "proteinas": "El paciente debe asegurar el consumo de suficientes proteínas de alta calidad (como carne, aves, pescado y huevos), ya que producen menos toxinas. Sin embargo, se debe cuidar la cantidad exacta para no elevar el fósforo en el organismo. Se deben evitar por completo las carnes procesadas como perros calientes o embutidos por su alto contenido de sodio.",
    "calorias": "Muchos pacientes en hemodiálisis pierden el apetito y no obtienen suficientes calorías. Una forma saludable de agregar calorías y grasa a la dieta (si se necesita aumentar o mantener el peso) es usar aceites vegetales como el de oliva, canola o cártamo. La mantequilla y margarinas aportan calorías pero contienen grasas saturadas que obstruyen arterias, por lo que deben usarse con menos frecuencia.",
    "dulces": "Los caramelos duros, el azúcar, la miel, la mermelada y la jalea proporcionan calorías y energía rápida sin grasas y sin añadir minerales dañinos al cuerpo. Sin embargo, si el paciente padece diabetes, debe tener mucho cuidado y consultar las porciones.",
    "vitaminas": "La hemodiálisis elimina algunas vitaminas esenciales del organismo. El médico especialista puede recetar un suplemento diseñado específicamente para la insuficiencia renal. ADVERTENCIA: Nunca se deben tomar suplementos nutricionales que se compren sin receta médica, ya que pueden contener minerales perjudiciales.",
}

# Lista de saludos que activarán el mensaje de inicio
saludos_db = ["hola", "buen dia", "buenas tardes", "buenas noches", "que onda", "saludos"]

# Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola, buen día, ¿en qué te gustaría que te ayudara en el día de hoy? 😀"}
    ]

# Mostrar los mensajes anteriores en la interfaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada de texto del usuario
if user_query := st.chat_input("Escribe el nombre de un alimento o consulta"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
        
    # Procesar texto: minúsculas, quitar espacios y eliminar acentos manualmente
    query_lower = user_query.lower().strip()
    quitar_acentos = str.maketrans("áéíóúü", "aeiouu")
    query_lower = query_lower.translate(quitar_acentos)
    
    respuesta_encontrada = None
    
    # 1. PASO: Si dice "Hola", repetir exactamente el saludo inicial
    if query_lower in saludos_db:
        respuesta_encontrada = "Hola, buen día, ¿en qué te gustaría que te ayudara en el día de hoy? 😀"

    # 2. PASO: Verificar si coincide con algún tema de los apuntes
    if not respuesta_encontrada:
        for tema, texto in respuestas_tematicas.items():
            if tema in query_lower:
                respuesta_encontrada = f"🤖 **Información sobre {tema.capitalize()}:** {texto}\n\n*Recuerda que este chatbot fue creado con fines educativos.*"
                break
            
    # 3. PASO: Verificar si coincide con la base de datos de alimentos
    if not respuesta_encontrada:
        for alimento, semaforo in alimentos_db.items():
            if alimento in query_lower:
                if semaforo == "se puede consumir":
                    respuesta_encontrada = f"🟢 **{alimento.capitalize()}**: Se puede consumir libremente en la dieta para diálisis."
                elif semaforo == "con moderacion":
                    respuesta_encontrada = f"🟡 **{alimento.capitalize()}**: Se debe consumir con moderación e idealmente bajo las especificaciones de tu nutriólogo."
                else:
                    respuesta_encontrada = f"🔴 **{alimento.capitalize()}**: No se puede consumir. Es un alimento peligroso para pacientes en diálisis."
                break

    # 4. PASO: Si no se encuentra nada, intentar OpenAI (Si falla, da un mensaje sugerente)
    if not respuesta_encontrada:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en nutrición renal para pacientes en hemodiálisis. Responde de forma clara, amable y educativa. Si no tienes certeza sobre un alimento, recuerda siempre sugerir consultar al nefrólogo."},
                    {"role": "user", "content": user_query}
                ]
            )
            respuesta_encontrada = response.choices[0].message.content
        except:
            respuesta_encontrada = "Para ese alimento o consulta en específico, te recomiendo consultarlo directamente con tu nefrólogo o nutriólogo renal para evitar riesgos en tu tratamiento. Puedes intentar preguntándome por alimentos de la vida diaria como: *arroz, manzana, embutidos o refresco claro*."

    # Guardar y mostrar la respuesta del Chatbot
    st.session_state.messages.append({"role": "assistant", "content": respuesta_encontrada})
    with st.chat_message("assistant"):
        st.write(respuesta_encontrada)
