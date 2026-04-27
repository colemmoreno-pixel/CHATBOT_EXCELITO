import streamlit as st
import google.generativeai as genai

# 1. Configuración visual de la página
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")

# Estilo para mejorar el diseño
st.title("📊 Mi Asistente de Excel para Alumnos")
st.markdown("---")
st.info("👋 ¡Hola! Soy tu tutor de Excel. Puedo ayudarte con fórmulas, tablas dinámicas o cualquier duda que tengas. ¡Pregúntame lo que sea!")

# 2. Conexión con la llave de Google (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Error: No se encontró la API Key. Revisa la configuración en 'Advanced Settings' de Streamlit.")

# 3. Historial de chat para que el bot recuerde la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica del Chat
if prompt := st.chat_input("Escribe tu duda de Excel aquí..."):
    # Guardar y mostrar lo que escribe el alumno
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Instrucciones "secretas" para que el bot actúe como profesor
    contexto_maestro = (
        "Actúa como un profesor experto en Microsoft Excel. "
        "Si el alumno te pide una fórmula, muéstrala claramente en un bloque de código. "
        "Explica los argumentos de la función de forma sencilla. "
        "Menciona siempre el nombre de la función en español y su equivalente en inglés. "
        "Al final, anima al alumno a seguir practicando."
    )

    # Generar la respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando la mejor solución..."):
            response = model.generate_content(f"{contexto_maestro}\n\nAlumno: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
