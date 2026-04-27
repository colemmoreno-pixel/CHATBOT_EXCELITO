import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")

# 2. Conexión con la API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la clave API en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Usamos el nombre de modelo más estándar
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Aquí intentamos la respuesta
            response = model.generate_content(f"Eres un experto en Excel. Responde a: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Si vuelve a fallar, este mensaje nos dirá exactamente por qué
            st.error("Lo siento, sigo teniendo problemas para conectar.")
            st.write(f"Aviso técnico: {e}")
