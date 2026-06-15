import streamlit as st
import openai
import unicodedata

# Configuración de la interfaz de la página web
st.set_page_config(page_title="Chatbot Nutrición Renal", page_icon="😀", layout="centered")

# Llave API integrada
openai.api_key = "AQ.Ab8RN6KkzCycaAsqrsj2ZplsccBfTkkArejOMR5CU8adacWIWQ"

# Base de datos completa de alimentos (Verdes, Amarillos y Rojos)
alimentos_db = {
    # SE PUEDE CONSUMIR (Verde)
    "pechuga de pollo": "se puede consumir", 
    "pechuga de pavo": "se puede consumir",
    "clara de huevo": "se puede consumir", 
    "filete tilapia": "se puede consumir",
    "filete de tilapia": "se puede consumir",
    "filete de bacalao": "se puede consumir", 
    "filete de rosajo": "se puede consumir",
    "chayote": "se puede consumir", 
    "chayote cocido": "se puede consumir",
    "calabacin": "se puede consumir", 
    "calabacita": "se puede consumir",
    "coliflor": "se puede consumir", 
    "coliflor cocida": "se puede consumir",
    "ejotes": "se puede consumir", 
    "judias verdes": "se puede consumir",
    "pepino": "se puede consumir", 
    "pepino sin cascara ni semillas": "se puede consumir",
    "lechuga italiana": "se puede consumir", 
    "cebolla blanca": "se puede consumir",
    "pimiento morron": "se puede consumir", 
    "pimiento morron rojo crudo": "se puede consumir",
    "ajo": "se puede consumir", 
    "manzana": "se puede consumir", 
    "manzana sin cascara": "se puede consumir",
    "pera": "se puede consumir", 
    "pera sin cascara": "se puede consumir",
    "fresas": "se puede consumir", 
    "arandanos": "se puede consumir",
    "pina": "se puede consumir", 
    "pinas": "se puede consumir", 
    "uvas": "se puede consumir",
    "gelatina": "se puede consumir", 
    "arroz blanco": "se puede consumir",

    # CON MODERACIÓN (Amarillo)
    "huevo entero": "con moderación", 
    "huevo entero cocido": "con moderación",
    "carne de res magra": "con moderación", 
    "lomo de cerdo magra": "con moderación",
    "lomo de cerdo magro": "con moderación", 
    "queso cottage": "con moderación",
    "queso cottage bajo en sodio": "con moderación", 
    "camarones": "con moderación",
    "zanahoria": "con moderación", 
    "zanahoria cocida": "con moderación",
    "zanahoria cocida, escurrida": "con moderación", 
    "jitomate": "con moderación",
    "papas": "con moderación", 
    "melon": "con moderación", 
    "refrescos": "con moderación",
    "sandia": "con moderación",
    "refresco": "con moderación",
    "refresco claro": "con moderación",
    "refrescos claros": "con moderación",
    "aceite": "con moderación",
    "aceite de oliva": "con moderación",
    

    # NO SE PUEDEN CONSUMIR - ROJOS (Peligrosos / Evitar por completo)
    "platano": "no se pueden consumir", 
    "aguacates": "no se pueden consumir",
    "naranja": "no se pueden consumir", 
    "camote": "no se pueden consumir",
    "espinaca": "no se pueden consumir", 
    "kiwi": "no se pueden consumir",
    "frijoles": "no se pueden consumir", 
    "lentejas": "no se pueden consumir",
    "quesos": "no se pueden consumir", 
    "productos integrales": "no se pueden consumir",
    "lacteos": "no se pueden consumir", 
    "frutos secos": "no se pueden consumir",
    "cerveza": "no se pueden consumir", 
    "chocolates": "no se pueden consumir",
    "embutidos": "no se pueden consumir", 
    "enlatados": "no se pueden consumir",
    "botana salada": "no se pueden consumir", 
    "salsa embotellada": "no se pueden consumir",
    "encurtidos": "no se pueden consumir", 
    "carne ahumada": "no se pueden consumir",
    "pescado ahumado": "no se pueden consumir", 
    "carambola": "no se pueden consumir",
    "toronja": "no se pueden consumir", 
    "caldos": "no se pueden consumir",
    "atun en lata": "no se pueden consumir", 
    "sardinas enlatadas": "no se pueden consumir",
    "sopas instantanas": "no se pueden consumir", 
    "sopas instantaneas": "no se pueden consumir", 
    "sopas en lata": "no se pueden consumir",
    "verduras enlatadas": "no se pueden consumir", 
    "frijoles enlatados": "no se pueden consumir",
    "chiles en lata": "no se pueden consumir", 
    "salsas enlatadas": "no se pueden consumir",
    "leche evaporada": "no se pueden consumir", 
    "leche condensada": "no se pueden consumir",
    "carnes enlatadas": "no se pueden consumir", 
    "pepinillos": "no se pueden consumir",
    "chiles en vinagre": "no se pueden consumir", 
    "zanahorias en escabeche": "no se pueden consumir",
    "cebollas encurtidas": "no se pueden consumir", 
    "col encurtida": "no se pueden consumir",
    "nopales en conserva": "no se pueden consumir", 
    "aceitunas en salmuera": "no se pueden consumir",
    "verduras en vinagre comerciales": "no se pueden consumir", 
    "maruchan": "no se pueden consumir",
    "cubos de caldo": "no se pueden consumir", 
    "salsas comerciales": "no se pueden consumir",
    "soya": "no se pueden consumir", 
    "salsa inglesa": "no se pueden consumir",
    "catsup": "no se pueden consumir", 
    "quesos procesados": "no se pueden consumir",
    "queso amarillo": "no se pueden consumir", 
    "queso tipo americano": "no se pueden consumir",
    "refrescos oscuros": "no se pueden consumir", 
    "bebidas energeticas": "no se pueden consumir",
    "chocolate en exceso": "no se pueden consumir", 
    "comida congelada procesada": "no se pueden consumir",
    "hamburguesas": "no se pueden consumir", 
    "pizza": "no se pueden consumir",
    "hot dogs": "no se pueden consumir", 
    "papas fritas": "no se pueden consumir",
    "pollo frito": "no se pueden consumir", 
    "nuggets": "no se pueden consumir",
    "tacos fritos": "no se pueden consumir", 
    "burritos": "no se pueden consumir",
    "sincronizadas con jamon": "no se pueden consumir", 
    "tortas con embutidos": "no se pueden consumir",
    "papas fritas de bolsa": "no se pueden consumir", 
    "cheetos": "no se pueden consumir",
    "doritos": "no se pueden consumir", 
    "takis": "no se pueden consumir",
    "totopos con sal": "no se pueden consumir", 
    "nachos con queso": "no se pueden consumir",
    "palomitas con mantequilla y sal": "no se pueden consumir", 
    "galletas saladas": "no se pueden consumir",
    "pretzels": "no se pueden consumir", 
    "semillas saladas": "no se pueden consumir",
    "botanas enchiladas industriales": "no se pueden consumir", 
    "papas a la francesa": "no se pueden consumir",
    "alitas": "no se pueden consumir"
    
}

def normalizar_texto(texto):
    """Limpia el texto quitando acentos y mayúsculas para evitar errores."""
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def analizar_entrada(usuario_input):
    entrada_limpia = normalizar_texto(usuario_input)
    
    # 1. Saludo básico
    if entrada_limpia in ["hola", "buen dia", "buenos dias"]:
        return "Hola, buen día, en qué te gustaría que te ayudará en el día de hoy ? 😀"

    # 2. Respuestas exactas del cuaderno sobre recetas o menús
    if "ayudame a preparar" in entrada_limpia or "alimento para el dia de hoy" in entrada_limpia:
        return (
            "Chat: ¡Con gusto! Aquí te dejo algunas recetas para que puedas preparar el día de hoy:\n\n"
            "* **Huevos revueltos (solo usar claras):** Puedes cocinarlas en un sartén con un toque mínimo de aceite, "
            "agregando vegetales permitidos picados como pimiento morrón, calabacín o un poco de cebolla blanca y ajo para dar gran sabor.\n"
            "* **Filete de tilapia o bacalao al vapor:** Cocinado con finas rodajas de chayote y pepino (sin cáscara ni semillas), "
            "sazonado con ajo y cebolla.\n\n"
            "¿Te pareció bien las recetas que te recomendé? O gustas que te diga más recetas con ingredientes en específico."
        )
        
    if "mas economica y saludable" in entrada_limpia:
        return (
            "Chatbot: Claro, con gusto, aquí tienes más recetas:\n\n"
            "* **Arroz blanco con verduras bajas en potasio:** Recuerda que es altamente recomendable remojar las verduras "
            "(como el chayote o ejotes picados) y cambiar el agua antes de cocinar para reducir su potasio. Es una opción muy económica, llenadora y segura.\n"
            "* **Ensalada fresca de lechuga y pepino:** Utiliza lechuga italiana fresca y rodajas de pepino (sin cáscara ni semillas). "
            "Puedes sazonar con un toque de ajo picado finamente para dar sabor.\n\n"
            "¿Puedo ayudarte a verificar si puedes consumir algún otro (alimento) para tu dieta?"
        )

    # 3. Solicitud genérica de combinación de ingredientes que el usuario tenga a la mano
    if "que puedo preparar" in entrada_limpia or "que puedo cocinar" in entrada_limpia or "tengo" in entrada_limpia:
        encontrados = [alimento for alimento in alimentos_db if alimento in entrada_limpia]
        
        if encontrados:
            seguros = [f"**{alt}** ({alimentos_db[alt]})" for alt in encontrados if alimentos_db[alt] in ["se puede consumir", "con moderación"]]
            prohibidos = [f"**{alt}**" for alt in encontrados if alimentos_db[alt] == "no se pueden consumir"]
            
            respuesta = "Disculpa, este alimento no lo tengo, sin embargo te puedo dar la información de los otros alimentos:\n\n"
            if seguros:
                respuesta += "🟢 **Permitidos/Moderados encontrados:**\n" + "\n".join([f"* {s}" for s in seguros]) + "\n\n"
            if prohibidos:
                respuesta += "🔴 **No se pueden consumir:**\n" + "\n".join([f"* {p} (Es muy peligroso y puede hacerle daño a la persona)" for p in prohibidos]) + "\n\n"
            
            # Llamar a la API para crear una receta segura basada en lo permitido
            alimentos_aptos = [alt for alt in encontrados if alimentos_db[alt] in ["se puede consumir", "con moderación"]]
            if alimentos_aptos:
                try:
                    prompt = f"Actúa como un nutriólogo experto en diálisis. El usuario quiere cocinar y tiene estos alimentos aptos: {', '.join(alimentos_aptos)}. Crea una sugerencia de platillo breve, económica y saludable, recordando el cuidado del potasio y sodio."
                    res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=200)
                    respuesta += "🍲 **Sugerencia de Platillo:** " + res.choices[0].message['content'].strip()
                except:
                    respuesta += "🍲 **Sugerencia:** Combina tus ingredientes verdes al vapor o a la plancha sin agregar sales artificiales."
            return respuesta
            
        return "Chatbot: Lo siento no tengo esa información, me puedes decir que alimentos tienes a la mano, recuerda que este chatbot fue creado por fines educativos."

    # 4. Análisis de alimentos específicos (Individuales o múltiples separados por comas o 'y')
    palabras = entrada_limpia.replace(" y ", ",").split(",")
    respuestas_individuales = []
    
    for palabra in palabras:
        palabra = palabra.strip()
        if not palabra: continue
        
        coincidencia = None
        for k in alimentos_db:
            if k in palabra or palabra in k:
                coincidencia = k
                break
                
        if coincidencia:
            estado = alimentos_db[coincidencia]
            if estado == "se puede consumir":
                respuestas_individuales.append(f"El alimento '**{coincidencia}**' **sí, es muy recomendable y saludable**.")
            elif estado == "con moderación":
                respuestas_individuales.append(f"El alimento '**{coincidencia}**' se debe consumir **con moderación**.")
            else:
                respuestas_individuales.append(f"El alimento '**{coincidencia}**' **NO, es muy peligroso y puede hacerle daño a la persona**.")
                
    if respuestas_individuales:
        return "Chatbot:\n" + "\n".join(respuestas_individuales)

    # 5. Respuesta por defecto si no coincide con nada
    return "Chatbot: Lo siento no tengo esa información, me puedes decir que alimentos tienes a la mano, recuerda que este chatbot fue creado por fines educativos."

# --- DISEÑO DE LA INTERFAZ WEB (STREAMLIT) ---
st.title("🥗 Asistente de Nutrición Renal")
st.caption("Aplicación independiente creada con fines educativos para el control dietético en pacientes de diálisis.")

# Inicializar la memoria del chat en la página web
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hola, buen día, en qué te gustaría que te ayudará en el día de hoy ? 😀"}]

# Mostrar los mensajes acumulados en la pantalla
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Capturar lo que escribe el usuario en la barra inferior de la página
if user_query := st.chat_input("Escribe el nombre de un alimento o consulta aquí..."):
    # Guardar y mostrar lo que escribió el usuario
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
        
    # Obtener la respuesta calculada por el chatbot
    bot_res = analizar_entrada(user_query)
    
    # Guardar y mostrar la respuesta del bot en la web
    st.session_state.messages.append({"role": "assistant", "content": bot_res})
    with st.chat_message("assistant"):
        st.write(bot_res)
