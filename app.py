import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")

# 1. Configurar la API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Por favor, añade la GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# CAMBIO CLAVE: Usamos 'gemini-1.5-flash-latest' que es la versión más compatible
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Lógica de mensajes
if prompt := st.chat_input("Escribe tu duda de Excel aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción para el bot
            response = model.generate_content(f"Eres un profesor experto en Excel. Ayuda al alumno con: {prompt}")
            
            # Mostrar la respuesta
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            st.error("Hubo un error al generar la respuesta.")
            st.write(f"Asegúrate de que tu API Key sea correcta. Error: {e}")
