import streamlit as st
import openai

# Configuración de la interfaz de la página
st.set_page_config(page_title="Chatbot de Nutrición Renal", page_icon="🍎")

# Llave API integrada usando los Secrets seguros de Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Base de datos completa de alimentos (Original + Ajustes + Apuntes Nuevos)
alimentos_db = {
    # SE PUEDE CONSUMIR (Verde)
    "pechuga de pollo": "se puede conocer",
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
    "gelatina": "se puede conocer",
    "manzana": "se puede consumir",
    "arroz": "se puede consumir",
    
    # CON MODERACIÓN (Amarillo)
    "queso cottage": "con moderación",
    "queso cottage bajo en sodio": "con moderación",
    "productos integrales": "con moderación",
    "lacteos": "con moderación",
    "leche": "con moderación (máximo 1/2 taza al día)",
    "sandia": "con moderación",
    "refrescos": "con moderación (solo claros)",
    "refresco": "con moderación (solo claros)",
    "refresco claro": "con moderación",
    "refrescos claros": "con moderación",
    "aceite": "con moderación",
    "aceite de oliva": "con moderación",
    "aceite vegetal": "con moderación",
    
    # NO SE PUEDEN CONSUMIR (Rojo)
    "quesos": "no se pueden consumir",
    "queso": "no se pueden consumir",
    "queso amarillo": "no se pueden consumir",
    "queso tipo americano": "no se pueden consumir",
    "quesos procesados": "no se pueden consumir",
    "frutos secos": "no se pueden consumir",
    "cerveza": "no se pueden consumir",
    "chocolates": "no se pueden consumir",
    "embutidos": "no se pueden consumir",
    "sopas instantaneas": "no se pueden consumir",
    "alimentos enlatados": "no se pueden consumir",
    "botana salada": "no se pueden consumir",
    "salsa embotellada": "no se pueden consumir",
    "comida rapida": "no se pueden consumir",
    "encurtidos": "no se pueden consumir",
    "carne ahumada": "no se pueden consumir",
    "pescado ahumado": "no se pueden consumir",
    "carambola": "no se pueden consumir",
    "toronja": "no se pueden consumir",
    "caldos": "no se pueden consumir",
    "perros calientes": "no se pueden consumir",
    "chili enlatado": "no se pueden consumir",
    "carnes procesadas": "no se pueden consumir",
    "refrescos oscuros": "no se pueden consumir",
    "refresco oscuro": "no se pueden consumir",
    "refresco negro": "no se pueden consumir",
}

# Respuestas temáticas conceptuales basadas en apuntes oficiales (NIDDK / menutritionpr)
respuestas_tematicas = {
    "liquidos": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acumularse en el organismo. El exceso de líquidos puede causar aumento de peso entre sesiones, cambios en la presión arterial, problemas cardíacos graves e incluso acumulación en los pulmones dificultando la respiración. Se debe limitar estrictamente el sodio, potasio y fósforo para ayudar a controlarlo.",
    "agua": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acumularse en el organismo. El exceso de líquidos puede causar aumento de peso entre sesiones, cambios en la presión arterial, problemas cardíacos graves e incluso acumulación en los pulmones dificultando la respiración. Se debe limitar estrictamente el sodio, potasio y fósforo para ayudar a controlarlo.",
    "proteina": "El paciente debe asegurar el consumo de suficientes proteínas de alta calidad (como carne, aves, pescado y huevos), ya que producen menos toxinas. Sin embargo, se debe cuidar la cantidad exacta para no elevar el fósforo en el organismo. Se deben evitar por completo las carnes procesadas como perros calientes o embutidos por su alto contenido de sodio.",
    "proteinas": "El paciente debe asegurar el consumo de suficientes proteínas de alta calidad (como carne, aves, pescado y huevos), ya que producen menos toxinas. Sin embargo, se debe cuidar la cantidad exacta para no elevar el fósforo en el organismo. Se deben evitar por completo las carnes procesadas como perros calientes o embutidos por su alto contenido de sodio.",
    "calorias": "Muchos pacientes en hemodiálisis pierden el apetito y no obtienen suficientes calorías. Una forma saludable de agregar calorías y grasa a la dieta (si se necesita aumentar o mantener el peso) es usar aceites vegetales como el de oliva, canola o cártamo. La mantequilla y margarinas aportan calorías pero contienen grasas saturadas que obstruyen arterias, por lo que deben usarse con menos frecuencia.",
    "dulces": "Los caramelos duros, el azúcar, la miel, la mermelada y la jalea proporcionan calorías y energía rápida sin grasas y sin añadir minerales dañinos al cuerpo. Sin embargo, si el paciente padece diabetes, debe tener mucho cuidado y consultar las porciones.",
    "vitaminas": "La hemodiálisis elimina algunas vitaminas esenciales del organismo. El médico especialista puede recetar un suplemento diseñado específicamente para la insuficiencia renal. ADVERTENCIA: Nunca se deben tomar suplementos nutricionales que se compren sin receta médica, ya que pueden contener minerales perjudiciales.",
}

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
    # Guardar y mostrar la pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
        
    # Pasar la consulta a minúsculas para facilitar la búsqueda
    query_lower = user_query.lower()
    
    # 1. PASO: Verificar si coincide con algún tema conceptual de los apuntes
    respuesta_encontrada = None
    for tema, texto in respuestas_tematicas.items():
        if tema in query_lower:
            respuesta_encontrada = f"🤖 **Información sobre {tema.capitalize()}:** {texto}\n\n*Recuerda que este chatbot fue creado con fines educativos.*"
            break
            
    # 2. PASO: Si no fue un tema, verificar si coincide con la base de datos de alimentos
    if not respuesta_encontrada:
        for alimento, semaforo in alimentos_db.items():
            if alimento in query_lower:
                if "puede" in semaforo:
                    respuesta_encontrada = f"🟢 **{alimento.capitalize()}**: Se puede consumir libremente en la dieta para diálisis."
                elif "moderación" in semaforo:
                    respuesta_encontrada = f"🟡 **{alimento.capitalize()}**: Se debe consumir con moderación e idealmente bajo las especificaciones de tu nutriólogo."
                else:
                    respuesta_encontrada = f"🔴 **{alimento.capitalize()}**: No se puede consumir. Es un alimento peligroso para pacientes en diálisis."
                break

    # 3. PASO: Si no es alimento ni tema de apuntes, usar la Inteligencia Artificial de OpenAI
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
        except Exception as e:
            respuesta_encontrada = "Lo siento, no tengo esa información detallada en este momento. Recuerda que este chatbot fue creado con fines educativos."

    # Guardar y mostrar la respuesta del Chatbot
    st.session_state.messages.append({"role": "assistant", "content": respuesta_encontrada})
    with st.chat_message("assistant"):
        st.write(respuesta_encontrada)
            
