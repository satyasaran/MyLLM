import streamlit as st
from openai import OpenAI
import re
import uuid
import time
from datetime import datetime

# Custom CSS for ChatGPT-style beautiful styling
st.markdown("""
<style>
/* Main container styling */
.main-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

/* Header styling */
.header {
    text-align: center;
    background: linear-gradient(135deg, #87CEEB 0%, #B0E0E6 100%);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px 0 rgba(135, 206, 235, 0.5);
    border: 1px solid rgba(135, 206, 235, 0.3);
}

.header h1 {
    color: #2C3E50;
    font-size: 3rem;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.header p {
    color: #34495E;
    font-size: 1.2rem;
    margin: 10px 0 0 0;
}

/* Chat container styling */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: transparent;
}

.chat-container::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
}

/* Message styling - ChatGPT style */
.message-container {
    margin: 15px 0;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.user-message-container {
    justify-content: flex-end;
    margin-left: 20%;
}

.bot-message-container {
    justify-content: flex-start;
    margin-right: 20%;
}

.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
    flex-shrink: 0;
}

.user-avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    order: 2;
}

.bot-avatar {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
}

.message-content {
    max-width: 70%;
    word-wrap: break-word;
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.bot-message {
    background: rgba(255, 255, 255, 0.95);
    color: #2C3E50;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.timestamp {
    font-size: 0.75rem;
    opacity: 0.7;
    margin-top: 4px;
    text-align: right;
}

.bot-message .timestamp {
    text-align: left;
}

.copy-button {
    background: rgba(0, 0, 0, 0.1);
    border: none;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 11px;
    color: #666;
    cursor: pointer;
    margin-top: 8px;
    transition: background 0.2s;
}

.copy-button:hover {
    background: rgba(0, 0, 0, 0.2);
}

/* Input area styling */
.input-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

/* Sidebar styling */
.sidebar-content {
    background: linear-gradient(135deg, #87CEEB 0%, #B0E0E6 100%);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px 0 rgba(135, 206, 235, 0.3);
    border: 1px solid rgba(135, 206, 235, 0.2);
}

.sidebar-content h3, .sidebar-content h4 {
    color: #2C3E50 !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.sidebar-content ul {
    color: #34495E !important;
}

.sidebar-content li {
    color: #34495E !important;
    margin-bottom: 3px;
}

.sidebar-content p {
    color: #2C3E50 !important;
}

/* Status indicators */
.status-online {
    display: inline-block;
    width: 10px;
    height: 10px;
    background: #4CAF50;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

.stats-card {
    background: linear-gradient(135deg, #87CEEB 0%, #B0E0E6 100%);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    margin-bottom: 10px;
    border: 1px solid rgba(135, 206, 235, 0.2);
    box-shadow: 0 4px 15px 0 rgba(135, 206, 235, 0.3);
}

.stats-number {
    font-size: 2rem;
    font-weight: bold;
    color: #2C3E50;
}

.stats-label {
    font-size: 0.9rem;
    color: #34495E;
    font-weight: 600;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Configuration ---
HF_TOKEN = st.secrets["HF_TOKEN"]  # <-- safe, no key in GitHub
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "message_count" not in st.session_state:
    st.session_state["message_count"] = 0
if "session_start" not in st.session_state:
    st.session_state["session_start"] = datetime.now()

# --- Page Configuration ---
st.set_page_config(
    page_title="Welcome to Satyasaran's AI Chatbot!",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🤖 Chat Statistics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{len(st.session_state['messages'])}</div>
            <div class="stats-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        session_duration = datetime.now() - st.session_state["session_start"]
        minutes = int(session_duration.total_seconds() // 60)
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{minutes}</div>
            <div class="stats-label">Minutes</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🎯 Features</h4>
        <ul>
            <li>✨ ChatGPT-style UI</li>
            <li>🧮 LaTeX Math Support</li>
            <li>📋 Copy Messages</li>
            <li>🕐 Timestamps</li>
            <li>📊 Live Statistics</li>
            <li>🎨 Smooth Design</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>ℹ️ Status</h4>
        <p>
            <span class="status-online"></span>
            AI Model Online
        </p>
        <p>Model: GPT-OSS-120B</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["message_count"] = 0
        st.rerun()

# --- Main Content ---
# Header
st.markdown("""
<div class="header">
    <h1>🤖 Welcome to Satyasaran's AI Chatbot!</h1>
    <p>Powered by OpenAI GPT-OSS-120B model</p>
    <p>App Created by Satyasaran Changdar, Assistant Professor, University of Copenhagen, Denmark</p>
    <p>If it doesn’t work, don’t hesitate to contact me. I will create another free access token for you!🙂</p>
    <p>Enjoy, have a great day! 🙂</p>

</div>
""", unsafe_allow_html=True)

# Chat container
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display messages
    for i, msg in enumerate(st.session_state["messages"]):
        timestamp = datetime.now().strftime("%H:%M")
        
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="message-container user-message-container">
                <div class="message-content">
                    <div class="user-message">
                        {msg['content']}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                <div class="message-avatar user-avatar">U</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Process the bot message content
            processed_content = msg['content']
            # LaTeX conversion for math expressions
            processed_content = re.sub(r"\(\((.+?)\)\)", r"$\1$", processed_content)
            processed_content = re.sub(r"\[\[(.+?)\]\]", r"$$\1$$", processed_content)
            
            st.markdown(f"""
            <div class="message-container bot-message-container">
                <div class="message-avatar bot-avatar">🤖</div>
                <div class="message-content">
                    <div class="bot-message">
                        {processed_content}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create input form
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "💬 Type your message here...",
            placeholder="Ask me anything!",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.form_submit_button("🚀 Send", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Handle input
if send_button and user_input.strip():
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
    st.session_state["message_count"] += 1
    
    # Show typing indicator
    with st.spinner("🤖 AI is thinking..."):
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b:cerebras",
                messages=st.session_state["messages"],
                temperature=0.7,
                max_tokens=1000
            )
            reply = completion.choices[0].message.content
            
            # Add bot response
            st.session_state["messages"].append({"role": "assistant", "content": reply})
            
        except Exception as e:
            error_msg = f"⚠️ Sorry, I encountered an error: {str(e)}"
            st.session_state["messages"].append({"role": "assistant", "content": error_msg})
    
    # Rerun to update the interface
    st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">
        ✨ Enhanced AI Chatbot • Made with Streamlit & Hugging Face •
        <span style="color: #4CAF50;">●</span> Online & Ready
    </p>
</div>
""", unsafe_allow_html=True)
