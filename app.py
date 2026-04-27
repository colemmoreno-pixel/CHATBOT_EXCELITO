import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="Asistente de Excel", page_icon="📊")
st.title("📊 Mi Asistente de Excel para Alumnos")
st.info("👋 ¡Hola! Soy tu tutor de Excel. Escribe tu duda abajo y te ayudaré con la fórmula.")

# 2. Configuración de la API
try:
    # Usamos el nombre del secret tal como lo pusiste
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Intentamos con el modelo más compatible actualmente
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

# 3. Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat
if prompt := st.chat_input("¿Cómo hago una suma en Excel?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción simplificada para asegurar respuesta
            contexto = "Eres un profesor de Excel. Explica fórmulas de forma clara."
            response = model.generate_content(f"{contexto}\nPregunta: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Lo siento, hubo un pequeño error al conectar con el cerebro del bot.")
            st.info("Revisa si tu API Key en Google AI Studio dice 'Active'.")
            st.write(f"Detalle técnico: {e}")
