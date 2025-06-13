import streamlit as st
import os
import openai

# Set key thru streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

st.set_page_config(page_title="Adamo 2.0 – Virtual Sommelier", layout="centered")

# CSS styling for DaVinci branding
st.markdown(
    """
    <style>
    body {
        background: repeating-linear-gradient(
            90deg,
            #FFF8E1,
            #FFF8E1 10px,
            #FFE082 10px,
            #FFE082 20px
        );
    }
    .stApp {
        font-family: Georgia, serif;
    }
    .header {
        background-color: #800000;
        color: #FFD700;
        padding: 1rem;
        text-align: center;
        font-size: 2rem;
        border-radius: 5px;
    }
    .user-msg {
        text-align: right;
        color: #555;
        padding: 0.5rem;
    }
    .assistant-msg {
        text-align: left;
        color: #800000;
        padding: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="header">Adamo 2.0 – Virtual Sommelier</div>', unsafe_allow_html=True)

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Tone selector
tone = st.selectbox("Choose Adamo's tone:", ["refined", "warm", "playful", "minimalist"])

# User input
user_input = st.text_input("Ask Adamo about wine pairings, full meals, or drink suggestions:")

# Display chat history
for entry in st.session_state.history:
    role = entry["role"]
    msg = entry["message"]
    css_class = "user-msg" if role == "user" else "assistant-msg"
    st.markdown(f'<div class="{css_class}"><strong>{role.title()}:</strong> {msg}</div>', unsafe_allow_html=True)

# Handle user input
if user_input:
    st.session_state.history.append({"role": "user", "message": user_input})

    # full prompt with tone and background
    system_prompt = f"You are Adamo 2.0, a virtual sommelier for a fine Italian restaurant. Speak in a {tone} tone. Suggest wine pairings for meals, or alternatives like cocktails, beers, or digestifs. Always be helpful and match DaVinci's elegant atmosphere."

    messages = [{"role": "system", "content": system_prompt}]
    for h in st.session_state.history:
        messages.append({"role": h["role"], "content": h["message"]})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        reply = f"Error contacting the sommelier brain: {str(e)}"

    st.session_state.history.append({"role": "assistant", "message": reply})
    st.experimental_rerun()


