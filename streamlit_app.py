import streamlit as st
import requests

st.set_page_config(page_title="💬 Web Bot")

with st.sidebar:
    st.title('💬 Web Bot')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('Login erfolgreich!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
        hf_token = st.secrets['HF_TOKEN']
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

# Function for generating LLM response
def generate_response(prompt_input, hf_token):
    headers = {"Authorization": f"Bearer {hf_token}"}
    API_URL = "https://lucom7fjkrjfxwyk.us-east-1.aws.endpoints.huggingface.cloud" 
    response = requests.post(API_URL, headers=headers, json=prompt_input)
    return response.json()[0]['generated_text'].replace(prompt_input['inputs'], '')

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt_input = {"inputs": f"Du bist ein hilfreicher Assistent. USER: {prompt} ASSISTANT:",
              "param_grid": {"max_tokens": 500, "temperature": 0.6},
              "options": {"wait_for_model": True}}
            response = generate_response(prompt_input, hf_token) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
