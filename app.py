import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configuración de página
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")

# Conexión con la API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la API KEY en Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- SOLUCIÓN MAESTRA AL ERROR 404 ---
# Forzamos el uso del modelo flash-001 que es el más estable hoy
model = genai.GenerativeModel(model_name='gemini-1.5-flash-001')

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat
if prompt := st.chat_input("¿En qué te ayudo con Excel?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Usamos una configuración simple para evitar bloqueos
            response = model.generate_content(
                f"Eres un experto en Excel. Responde de forma breve a: {prompt}",
                generation_config={"temperature": 0.7}
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Error de comunicación con el servidor.")
            st.write(f"Detalle técnico: {e}")
