import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")

# 1. Configuración de API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la configuración de la API KEY.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Selección automática de modelo (Para evitar el error 404)
@st.cache_resource
def load_model():
    # Intentamos primero con los más modernos, si fallan, usamos el básico
    for m in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(m)
            # Prueba rápida
            model.generate_content("test")
            return model
        except:
            continue
    return genai.GenerativeModel('gemini-pro')

model = load_model()

# 3. Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat
if prompt := st.chat_input("¿En qué te ayudo con Excel?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Eres un experto en Excel. Ayuda al alumno: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Lo siento, hay un problema con la llave de Google.")
            st.write(f"Error: {e}")
