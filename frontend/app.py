import os
import streamlit as st
import requests

st.set_page_config(page_title="Assistente ONS - TIAGO", page_icon="⚡", layout="wide")

st.title("⚡ Assistente de Dados Abertos ONS (TIAGO + SLM Local)")
st.markdown("Plataforma corporativa interna de consulta inteligente ao setor elétrico brasileiro.")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001/chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: Quais datasets estão disponíveis ou qual a carga no Nordeste?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("O SLM está analisando e consultando os dados do ONS..."):
            try:
                response = requests.post(BACKEND_URL, json={"pregunta": prompt}, timeout=60)
                if response.status_code == 200:
                    resposta_texto = response.json().get("resposta")
                else:
                    resposta_texto = f"Erro no servidor backend (Status {response.status_code})."
            except Exception as e:
                resposta_texto = f"Erro de conexão com o backend: {e}"
            
            st.markdown(resposta_texto)
            
    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})