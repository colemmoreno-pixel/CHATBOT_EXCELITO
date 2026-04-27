import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")

# Aquí conectamos con la llave secreta que pondremos luego
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes antiguos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué te ayudo con Excel?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Instrucción para el bot
    instruccion = f"Eres un profesor experto en Excel. Responde de forma sencilla a: {prompt}"

    with st.chat_message("assistant"):
        response = model.generate_content(instruccion)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
