import streamlit as st

st.set_page_config(page_title="💬 Web Bot")

with st.sidebar:
    st.title('💬 Web Bot')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('Login erfolgreich!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('E-mail:', type='password')
        hf_pass = st.text_input('Passwort:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Bitte einloggen!', icon='⚠️')
        else:
            st.success('Jetzt chatten!', icon='👉')
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Wie kann ich helfen?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
