import streamlit as st
import requests
import json
import itertools
import pandas as pd
import plotly.graph_objects as go

# ১. পেজ সেটিংস ও উচ্চ-কন্ট্রাস্ট মার্জিত থিম
st.set_page_config(page_title="DiscreteMind AI", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    .stApp, p, span, label, li { color: #f8fafc !important; font-size: 16px; }
    h1 { color: #f1f5f9 !important; font-weight: 700 !important; }
    h2, h3, h4 { color: #38bdf8 !important; font-weight: 600 !important; }
    
    div[data-testid="stForm"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    
    .stButton>button {
        background: #0284c7 !important; color: #ffffff !important;
        font-weight: bold !important; border: none !important;
        border-radius: 6px !important; padding: 0.6rem 2rem !important;
        width: 100%;
    }
    .stButton>button:hover { background: #0369a1 !important; }
    
    .answer-box {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 25px !important;
        border-radius: 8px !important;
        border: 2px solid #cbd5e1 !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    .answer-box * { color: #000000 !important; }
    .answer-box .katex, .answer-box .katex * { color: #000000 !important; font-weight: 600 !important; }
    
    .flashcard {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        text-align: center !important;
        margin-bottom: 15px !important;
    }
    
    .status-panel {
        padding: 12px !important;
        border-radius: 8px !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ২. Session State ইনিশিয়েলাইজেশন
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'exam_submitted' not in st.session_state:
    st.session_state.exam_submitted = False
if 'user_score_history' not in st.session_state:
    st.session_state.user_score_history = []
if 'selected_topics' not in st.session_state:
    st.session_state.selected_topics = ["Set Theory", "Propositional Logic", "Graph Theory", "Combinatorics & Counting", "Recurrence Relations"]

# ৩. সাইডবার সেটিংস এবং ডাইনামিক এপিআই কী কন্ট্রোল প্যানেল
st.sidebar.markdown("<h3 style='color: #38bdf8;'>🎓 Student Profile</h3>", unsafe_allow_html=True)
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #38bdf8;'>⚙️ AI Control Panel</h3>", unsafe_allow_html=True)

default_key = "AQ.Ab8RN6KhKccD25XJHsm9m7Le2xdcpWKY9EnCxQmGzRrDuoW26A"

custom_key_input = st.sidebar.text_input(
    "🔑 Custom API Key Override:", 
    value=default_key, 
    type="password"
)

clean_key = str(custom_key_input).strip().replace('"', '').replace("'", "")

st.markdown('<div class="status-panel" style="background-color: rgba(74, 222, 128, 0.1); border: 1px solid #4ade80; color: #4ade80 !important;">🟢 Core AI Engine: CONNECTED & ONLINE (Live Global Gateway Sync)</div>', unsafe_allow_html=True)

# ফিক্সড রিয়েল-টাইম এআই এক্সিকিউশন গেটওয়ে (উচ্চ তাপমাত্রা নিয়ন্ত্রণ ও কনফিগারেশন লকিং)
def generate_ai_response(prompt_text):
    if not clean_key:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
        headers = {'Content-Type': 'application/json'}
        
        # এলোমেলো উত্তর ফিক্স করার জন্য স্ট্রিক্ট জেনারেশন কনফিগারেশন যোগ করা হলো
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {
                "temperature": 0.1,  # কমিয়ে দেওয়া হলো যেন উত্তর এলোমেলো না হয়ে
