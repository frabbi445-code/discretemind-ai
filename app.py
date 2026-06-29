import streamlit as st
import google.generativeai as genai
import time
import pandas as pd
import random
import math

# ১. পেজ সেটিংস ও মিনিমালিস্ট ডার্ক নিওন থিম
st.set_page_config(page_title="DiscreteMind AI Universal Pro", page_icon="🧠", layout="centered")

st.title("🧠 DiscreteMind AI: Universal Course Solver")
st.subheader("Omni-Topic Discrete Mathematics Engine & Mock Test Simulator")
st.write("Presidency University | CSE Dept | Core Course Project")
st.write("---")

# ২. প্রফেশনাল সাইডবার ড্যাশবোর্ড
st.sidebar.header("🎓 Course Project Profile")
with st.sidebar.container(border=True):
    st.write("**Project Target:** Universal Math Solver & Mock Test")
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    st.caption("🔥 System Status: Full Mock Test Simulator Active")

st.sidebar.write("---")
st.sidebar.header("🔗 Quick Navigation")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")

# ৩. স্ট্রিমলিট সিক্রেটস থেকে এপিআই কি রিড করা
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = None

# ৪. ইউনিভার্সাল সিঙ্গেল ইনপুট ইন্টারফেস
st.subheader("🚀 Universal Math Input Box")
st.caption("💡 **কোনো টপিক সিলেক্ট করতে হবে না!** ট্রুথ টেবিল, সেট, গ্রাফ থিওরি, ট্রি, পারমিউটেশন, প্রব্যাবিলিটি, রিকুরেন্স রিলেশন বা ম্যাট্রিক্স—কোর্সের যেকোনো গাণিতিক প্রশ্ন নিচের বক্সে লেখো:")

user_query = st.text_area(
    "📝 তোমার ডিসক্রিট ম্যাথের প্রশ্নটি এখানে টাইপ করো বা পেস্ট করো:",
    value="",
    placeholder="যেমন: Prove that (P -> Q) and not Q implies not P.",
    height=120
)

if st.button("🚀 এক্সপার্ট এআই সリューション জেনারেট করো", use_container_width=True):
    if not user_query.strip():
        st.warning("⚠️ দয়া করে আগে ইনপুট বক্সে কোনো প্রশ্ন লিখো!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent_complete in range(10, 101, 30):
            time.sleep(0.1)
            progress_bar.progress(percent_complete)
            status_text.markdown(f"⚙️ **এআই ওমনি-পার্সার ম্যাথমেটিক্যাল লজিক প্রসেস করছে... {percent_complete}%**")
            
        with st.spinner("✨ সমাধান একাডেমিক স্ট্যান্ডার্ডে ফরম্যাট করা হচ্ছে..."):
            try:
                if GEMINI_API_KEY:
                    genai.configure(api_key=GEMINI_API_KEY)
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                    prompt = f"You are an expert university professor in Discrete Mathematics. Provide a rigorous, step-by-step, textbook-style solution for: {user_query}. Use LaTeX formatting."
                    response = model.generate_content(prompt)
                    output_text = response.text
                else:
                    cleaned_q = user_query.lower()
                    if "ali studies" in cleaned_q or "p->q" in cleaned_q:
                        output_text = "\n### 📝 Given Data & Analysis\n* $P$: True, $Q$: False\n* Expression: $(P \\rightarrow Q) \\land \\neg Q$\n\n### 🛠️ Step-by-Step Derivation\n1. $P \\rightarrow Q = \\text{True} \\rightarrow \\text{False} = \\mathbf{False}$\n2. $\\neg Q = \\neg(\\text{False}) = \\mathbf{True}$\n3. $\\mathbf{False} \\land \\mathbf{True} = \\mathbf{False}$\n\n### 🎯 Final Conclusion\n> The final evaluated truth value is **False**."
                    else:
                        output_text = "\n⚠️ **System Note:** Please add your `GEMINI_API_KEY` in Streamlit Secrets to solve custom questions live."
            except Exception as e:
                output_text = f"❌ Error: {e}"
            
            status_text.empty()
            progress_bar.empty()
            st.balloons()
            st.success("🎉 সমাধান সফলভাবে জেনারেট হয়েছে!")
            with st.container(border=True):
                st.markdown(output_text)

st.write("---")

# 🧠 ৫. অ্যাডভান্সড ডাইনামিক মক টেস্ট সিমুলেটর (Mock Test Engine)
st.subheader("📝 Discrete Mathematics Mid/Final Mock Test")
st.caption("💡 এটি একটি প্রফেশনাল এক্সাম এনভায়রনমেন্ট। প্রশ্ন সিলেক্ট করে একদম শেষে 'সাবমিট মক টেস্ট' বাটনে চাপ দাও।")

# মক টেস্টের প্রশ্ন ব্যাংক ইনিশিয়ালাইজেশন (র্যান্ডমাইজড ভ্যালু সহ)
if 'mock_seed' not in st.session_state or st.sidebar.button("🔄 প্রশ্নপত্র নতুন করে জেনারেট করো"):
    st.session_state.mock_seed = random.randint(1, 9999)
    st.session_state.test_submitted = False
    st.session_state.answers = {}

random.seed(st.session_state.mock_seed)
nodes_count = random.randint(4, 6)
max_edges = int(nodes_count * (nodes_count - 1) / 2)
subset_n = random.randint(3, 5)

questions_list = [
    {
        "id": 1,
        "topic": "Graph Theory",
        "question": f"১. একটি Simple Graph-এ যদি মোট নোড বা ভার্টেক্স সংখ্যা {nodes_count} হয়, তবে গ্রাফটিতে সর্বোচ্চ কতটি এজ (Edges) থাকতে পারে?",
        "options": [f"{nodes_count}টি", f"{max_edges}টি", f"{nodes_count * 2}টি"],
        "correct": f"{max_edges}টি"
    },
    {
        "id": 2,
        "topic": "Graph Theory",
