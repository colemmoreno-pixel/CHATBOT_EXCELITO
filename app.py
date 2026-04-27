import streamlit as st
import google.generativeai as genai

# 1. Configuración visual
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")
st.markdown("---")
st.info("👋 ¡Hola! Soy tu tutor de Excel. Pregúntame lo que necesites.")

# 2. Conexión segura con la API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Falta la configuración de la API KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Usamos 'gemini-pro' que es el nombre más estable para la API
model = genai.GenerativeModel('gemini-pro')

# 3. Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica del Chat
if prompt := st.chat_input("Escribe tu duda de Excel aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    contexto_maestro = (
        "Eres un profesor experto en Excel. Responde de forma clara y amable. "
        "Usa bloques de código para las fórmulas."
    )

    with st.chat_message("assistant"):
        with st.spinner("Buscando en mi manual de Excel..."):
            try:
                # Intentamos generar la respuesta
                response = model.generate_content(f"{contexto_maestro}\n\nAlumno: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Hubo un problema con la conexión: {e}")
                st.warning("Asegúrate de que tu API Key sea válida y esté bien pegada en Secrets.")
