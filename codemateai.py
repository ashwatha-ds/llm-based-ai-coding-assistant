# -*- coding: utf-8 -*-
import streamlit as st
from groq import Groq
import re


st.set_page_config(
    page_title="codemateAI",
    layout="wide"
)


st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #111111; }
    h1, h2, h3, h4 { color: #0f8a5f; text-align: center; }
    .main-title {
        font-size: 54px; font-weight: bold;
        color: #0f8a5f; text-align: center; margin-top: 80px;
    }
    .sub-title {
        font-size: 24px; text-align: center;
        color: #333333; margin-bottom: 40px;
    }
    .stButton > button {
        background-color: #0f8a5f; color: white;
        border: none; border-radius: 10px;
        padding: 12px 20px; font-weight: bold; width: 100%;
    }
    .stButton > button:hover { background-color: #0b6d4a; color: white; }
    .block-container { padding-top: 2rem; max-width: 900px; margin: auto; }
    .mode-badge {
        display: inline-block; background: #e6f4ef;
        color: #0f8a5f; border-radius: 8px;
        padding: 4px 12px; font-weight: bold; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama3-70b-8192"


LANGUAGE_PERSONAS = {
    "Python": """You are a Python specialist. 
- ALL code you generate MUST be in Python only.
- Follow PEP8 style guidelines.
- Prefer Pythonic approaches (list comprehensions, f-strings, etc).
- Suggest relevant Python libraries where appropriate (e.g. os, sys, collections).
- If the user asks something not suited for Python, explain how Python handles it.""",

    "Java": """You are a Java specialist.
- ALL code you generate MUST be in Java only.
- Always use proper OOP structure (classes, access modifiers, constructors).
- Follow standard Java naming conventions (camelCase, PascalCase for classes).
- Mention relevant Java concepts like interfaces, inheritance, or exception handling where useful.
- If the user asks something not suited for Java, explain the Java equivalent.""",

    "C++": """You are a C++ specialist.
- ALL code you generate MUST be in C++ only.
- Always include necessary headers (e.g. #include <iostream>).
- Be mindful of memory management (pointers, references, RAII).
- Use STL (Standard Template Library) where appropriate.
- Explain memory-related concepts when relevant.""",

    "SQL": """You are a SQL specialist.
- ALL queries you generate MUST be in SQL only.
- Default to standard ANSI SQL but mention dialect differences (MySQL, PostgreSQL, SQLite) when relevant.
- Always write clean, readable queries with proper indentation.
- Suggest query optimization tips where relevant.
- If the user asks for loops or logic, explain the SQL equivalent (e.g. CTEs, CASE statements, window functions).""",

    "Data Analytics": """You are a Data Analytics specialist using Python.
- ALL code MUST use Python with Pandas, Matplotlib, or Seaborn.
- Focus on data cleaning, exploration, aggregation, and visualization.
- Always write code assuming a pandas DataFrame named 'df'.
- Suggest the right chart type for the analysis being asked.
- Explain what the output or visualization will show.""",

    "Data Science": """You are a Data Science specialist using Python.
- ALL code MUST use Python with relevant DS libraries: NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn.
- Focus on ML pipelines, model building, evaluation metrics, and statistical analysis.
- Always explain the reasoning behind algorithm choices.
- Mention overfitting, underfitting, or data preprocessing considerations where relevant.
- Write production-ready, well-commented code."""
}


MODES = {
    "General":        "Answer the user's coding question clearly and concisely. Stay strictly within the selected language/domain.",
    "Generate Code":  "GENERATE clean, correct, well-commented code based on the user's description. Always wrap code in proper markdown code blocks. Stay strictly within the selected language/domain.",
    "Debug Code":     "The user will share buggy code. Identify every bug, explain WHY it is wrong, then provide the fully corrected code. Stay strictly within the selected language/domain.",
    "Explain Code":   "Explain the provided code in simple terms: what it does, how it works block by block, and any important concepts used. Stay strictly within the selected language/domain.",
    "Mock Interview": "Act as a technical interviewer for the selected language/domain. Ask ONE coding interview question. Wait for the user's answer, then evaluate it and give detailed feedback.",
}

MODE_ICONS = {
    "General": "💬",
    "Generate Code": "⚙️",
    "Debug Code": "🐛",
    "Explain Code": "📖",
    "Mock Interview": "🎤"
}

LANGUAGE_OPTIONS = ["Python", "Java", "C++", "SQL", "Data Analytics", "Data Science"]
MODE_OPTIONS     = list(MODES.keys())


for key, default in {
    "page": "home",
    "selected_language": "Python",
    "messages": [],
    "prompt_mode": "General"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def get_ai_response(language: str, mode: str, history: list) -> str:
    system_prompt = f"""You are codemateAI, a professional coding assistant and mentor.

{LANGUAGE_PERSONAS[language]}

Current Mode: {mode}
Mode Instructions: {MODES[mode]}

Important Rules:
- Never switch to another language unless explicitly asked.
- Always format code using markdown code blocks with the correct language tag.
- Be concise but thorough.
- Remember the full conversation history provided.
"""
    messages = [{"role": "system", "content": system_prompt}] + history

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=2048,
        temperature=0.4,
    )
    return response.choices[0].message.content


def home_page():
    st.markdown('<div class="main-title">codemateAI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Multi-Language Coding Assistant & Mentor — Powered by Groq</div>',
        unsafe_allow_html=True
    )
    st.write("")
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        if st.button("🚀 Try Now"):
            st.session_state.page = "language"
            st.rerun()


def language_page():
    st.title("Hi! What should I help you with today?")
    st.write("#### Pick a language or domain:")

    for option in LANGUAGE_OPTIONS:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(option):
                st.session_state.selected_language = option
                st.session_state.messages = []
                st.session_state.prompt_mode = "General"
                st.session_state.page = "assistant"
                st.rerun()

    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()


def assistant_page():
    language = st.session_state.selected_language
    st.title(f"codemateAI — {language} Assistant")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("🔙 Change Language"):
            st.session_state.page = "language"
            st.rerun()
    with col3:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    st.write("---")

    
    st.write("#### 🎯 Select Mode:")
    mode_cols = st.columns(len(MODE_OPTIONS))
    for i, mode in enumerate(MODE_OPTIONS):
        with mode_cols[i]:
            if st.button(f"{MODE_ICONS[mode]} {mode}", key=f"mode_{mode}"):
                st.session_state.prompt_mode = mode
                st.rerun()

    mode = st.session_state.prompt_mode
    st.markdown(
        f'<div class="mode-badge">{MODE_ICONS[mode]} Active Mode: {mode}</div>',
        unsafe_allow_html=True
    )
    st.write("---")

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    placeholder_map = {
        "General":        "Ask any coding question...",
        "Generate Code":  "Describe what you want to build...",
        "Debug Code":     "Paste your buggy code here...",
        "Explain Code":   "Paste the code you want explained...",
        "Mock Interview": "Type 'start' to begin the interview, or answer the question...",
    }

    user_input = st.chat_input(placeholder_map[mode])

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(language, mode, st.session_state.messages)
            st.markdown(response)

            code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)
            download_data = "\n\n".join(code_blocks) if code_blocks else response
            st.download_button(
                label="⬇️ Download Code",
                data=download_data,
                file_name=f"codemate_{language.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )

        st.session_state.messages.append({"role": "assistant", "content": response})



if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "language":
    language_page()
elif st.session_state.page == "assistant":
    assistant_page()
