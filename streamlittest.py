import streamlit as st
from streamlit_chat import message
import os
import litellm
from dotenv import load_dotenv

def anfrage(prompt):
    load_dotenv()
    os.environ["GEMINI_API_KEY"] = st.secrets["api_key"]
    
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    
    response = litellm.completion(
        model="gemini/gemini-1.5-flash",
        messages=messages,
    )
    
    content = response.get('choices', [{}])[0].get('message', {}).get('content')
    return content

# Initialisierung des Chatverlaufs in session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Begrüßungsnachricht nur einmal hinzufügen
if not st.session_state.chat_history:
    st.session_state.chat_history.append({"role": "bot", "text": "Ich bin eine KI"})
    st.session_state.chat_history.append({"role": "bot", "text": "Frage mich gerne etwas :)"})

# Chatverlauf anzeigen
for chat in st.session_state.chat_history:
    message(chat["text"], is_user=(chat["role"] == "user"))

# Nutzerinput
prompt = st.chat_input("Say something")

if prompt:
    # Nutzerfrage speichern und anzeigen
    st.session_state.chat_history.append({"role": "user", "text": prompt})
    message(prompt, is_user=True)
    
    # KI-Antwort abrufen, speichern und anzeigen
    response = anfrage(prompt)
    st.session_state.chat_history.append({"role": "bot", "text": response})
    message(response)



