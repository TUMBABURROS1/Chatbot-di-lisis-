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
    "papas fritas": "🔴 **Papas fritas**: No se pueden consumir. Además de la enorme cantidad de potasio de la papa, contienen exceso de sodio y grasas por la fritura.",
    "papas": "🔴 **Papas**: No se pueden consumir de forma libre por su altísimo contenido de potasio (a menos que pasen por un proceso estricto de doble cocción y remojo).",
    "papa": "🔴 **Papa**: No se puede consumir libremente debido a sus elevados niveles de potasio, peligrosos para el corazón en diálisis.",
    

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
    "liquidos": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acumularse en el organismo. El exceso de líquidos puede causar aumento de peso entre sesiones, cambios en la presión arterial, problemas cardíacos graves e incluso acumulación en los pulmones dificultando la respiración. Se debe limitar estrictamente el sodio, potasio y fósforo para ayudar a controlarlo.",
    "agua": "Durante la hemodiálisis, las toxinas y excesos de líquidos pueden acumularse en el organismo. El exceso de líquidos puede causar aumento de peso entre sesiones, cambios en la presión arterial, problemas cardíacos graves e incluso acumulación en los pulmones dificultando la respiración. Se debe limitar estrictamente el sodio, potasio y fósforo para ayudar a controlarlo.",
    "proteina": "El paciente debe asegurar el consumo de suficientes proteínas de alta calidad (como carne, aves, pescado y huevos), ya que reciben menos toxinas. Sin embargo, se debe cuidar la cantidad exacta para no elevar el fósforo en el organismo. Se deben evitar por completo las carnes procesadas como perros calientes o embutidos por su alto contenido de sodio.",
    "proteinas": "El paciente debe asegurar el consumo de suficientes proteínas de alta calidad (como carne, aves, pescado y huevos), ya que reciben menos toxinas. Sin embargo, se debe cuidar la cantidad exacta para no elevar el fósforo en el organismo. Se deben evitar por completo las carnes procesadas como perros calientes o embutidos por su alto contenido de sodio.",
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
        
    # Procesar texto: minúsculas, sin espacios extras y sin acentos
    query_lower = user_query.lower().strip()
    quitar_acentos = str.maketrans("áéíóúü", "aeiouu")
    query_lower = query_lower.translate(quitar_acentos)
    
    respuesta_encontrada = None
    
    # 1. PASO: Si dice "Hola", repetir exactamente el saludo inicial
    if query_lower in saludos_db:
        respuesta_encontrada = "Hola, buen día, ¿en qué te gustaría que te ayudara en el día de hoy? 😀"

    # 2. PASO: LÓGICA DE TU LIBRETA (Económica / Saludable / Recetas)
    if not respuesta_encontrada:
        if "preparar un alimento" in query_lower or ("receta" in query_lower and "economica" not in query_lower):
            respuesta_encontrada = "¡Con gusto! Aquí te dejo algunas recetas para que puedas preparar el día de hoy:\n\n• **Huevos revueltos** (usar solo las claras)\n\nTe pareció bien las recetas que te recomendé, ¿o gustas que te diga más recetas con ingredientes específicos?"
            
        elif "economica" in query_lower and "saludable" in query_lower:
            respuesta_encontrada = "Claro, con gusto, aquí tienes más recetas:\n\n• **Arroz blanco** (Es recomendable remojar las verduras y cambiarles el agua antes de cocinar para reducir su potasio)"

    # 3. PASO: Verificar si coincide con algún tema conceptual de los apuntes
    if not respuesta_encontrada:
        for tema, texto in respuestas_tematicas.items():
            if tema in query_lower:
                respuesta_encontrada = f"🤖 **Información sobre {tema.capitalize()}:** {texto}\n\n*Recuerda que este chatbot fue creado con fines educativos.*"
                break
            
    # 4. PASO: Lógica Multi-alimento para combinar cosas
    if not respuesta_encontrada:
        alimentos_detectados = []
        ya_agregados = set()
        
        for alimento, texto_respuesta in alimentos_db.items():
            if alimento in query_lower:
                es_subcadena = False
                for ya_agregado in ya_agregados:
                    if alimento in ya_agregado:
                        es_subcadena = True
                        break
                
                if not es_subcadena and alimento not in ya_agregados:
                    alimentos_detectados.append(texto_respuesta)
                    ya_agregados.add(alimento)
        
        if alimentos_detectados:
            respuesta_encontrada = "📋 **Resultados de tu consulta:**\n\n" + "\n".join([f"- {res}" for res in alimentos_detectados])

    # 5. PASO: LÓGICA DE TU LIBRETA (Mensaje genérico "Puedo consumir...?")
    if not respuesta_encontrada and "puedo consumir" in query_lower:
        respuesta_encontrada = "Depende del alimento en específico:\n\n🟢 **Sí**: es muy recomendable y saludable.\n\n🔴 **No**: es muy peligroso y puede hacerle daño a la persona."

    # 6. PASO: RESPUESTA DE RESPALDO (Sustituida por el mensaje de fines educativos)
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
            # Tu mensaje corto original de las capturas
            respuesta_encontrada = "Lo siento, no tengo esa información detallada en este momento. Recuerda que este chatbot fue creado con fines educativos."

    # Guardar y mostrar la respuesta del Chatbot
    st.session_state.messages.append({"role": "assistant", "content": respuesta_encontrada})
    with st.chat_message("assistant"):
        st.write(respuesta_encontrada)
                
