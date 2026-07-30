import streamlit as st
import os
from groq import Groq

# 1. Configuración visual
st.set_page_config(page_title="Agente IA - Alegra", page_icon="⚡")
st.title("⚡ Asistente Virtual Alegra")
st.caption("Agente conversacional ultra rápido creado con Llama 3 y Groq.")

# 2. Conexión segura con la API
API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    st.error("Falta configurar la clave GROQ_API_KEY en los Secrets.")
    st.stop()

client = Groq(api_key=API_KEY)

# 3. Memoria y personalidad del agente
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente virtual amable y experto en facturación, contabilidad y soporte para usuarios de Alegra. Responde de forma concisa, clara y estructurada."}
    ]

# 4. Mostrar el historial en pantalla (ocultando la instrucción del sistema)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. Lógica de interacción
if prompt := st.chat_input("Hazme una pregunta sobre el servicio..."):
    # Guardar lo que dice el usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            try:
                completion = client.chat.completions.create(
                    model="llama3-8b-8192", # Modelo gratuito y súper rápido
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                respuesta = completion.choices[0].message.content
                st.markdown(respuesta)
                # Guardar la respuesta en la memoria
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
            except Exception as e:
                st.error(f"Error al conectar con la IA: {e}")
