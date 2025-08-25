import streamlit as st
from openai import OpenAI

HF_TOKEN = "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"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("🤖 Web Chatbot with Math Support")

user_input = st.text_input("Type your message and press Enter:")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=st.session_state["messages"]
    )
    reply = completion.choices[0].message.content

    # Replace ((...)) with $...$ for inline LaTeX
    import re
    reply = re.sub(r"\(\((.*?)\)\)", r"$\1$", reply)
    
    # Replace [[...]] with $$...$$ for display LaTeX if needed
    reply = re.sub(r"\[\[(.*?)\]\]", r"$$\1$$", reply)

    st.session_state["messages"].append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
