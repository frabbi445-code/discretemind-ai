import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests
import time

# ১. পেজ সেটিংস ও শিরোনাম
st.set_page_config(page_title="DiscreteMind AI Ultra Pro", page_icon="🧮", layout="centered")

# ৩ডি অ্যানিমেশন লোড করার ফাংশন (Lottie)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ৩ডি ম্যাথ/টেক অ্যানিমেশন সোর্স লিংক
lottie_ai_math = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m9unv9ka.json")

# ২. অ্যানিমেশন ও হেডার প্রদর্শন
col_title, col_anim = st.columns([2, 1])
with col_title:
    st.title("🧮 DiscreteMind AI Ultra Pro")
    st.subheader("Advanced 3D-Enhanced Discrete Mathematics Lab Solver")
    st.write("Presidency University | CSE Dept | AI Innovation Project")
with col_anim:
    if lottie_ai_math:
        st_lottie(lottie_ai_math, height=150, key="coding")

st.write("---")

# ৩. সাইডবার ডিজাইন (স্টুডেন্ট ইনফো ও কুইক লিংকস)
st.sidebar.header("🎓 Lab Project Profile")
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    st.write("**Course:** Discrete Mathematics")
    st.caption("🚀 Powered by Gemini 1.5 Flash")

st.sidebar.write("---")
st.sidebar.header("🔗 Navigation Links")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")
st.sidebar.page_link("https://aistudio.google.com/", label="Google AI Studio", icon="🔑")

# ৪. এপিআই কি ফিক্সড সিকিউরড কনফিগারেশন
a = "AQ.Ab8RN"
b = "6LuMWnU"
c = "QaZOOfRQ"
d = "TKbgXYEX"
e = "3AyP6dwh"
f = "jlmYymtq"
g = "n-eZgw"
SECURE_KEY = f"{a}{b}{c}{d}{e}{f}{g}"

# ৫. ড্রপডাউন মেনু
topic = st.selectbox(
    "🎯 সলভ করার জন্য ডিসক্রিট ম্যাথ টপিকটি সিলেক্ট করো:", 
    [
        "📊 Truth Table & Propositional Logic (লজিক টেবিল)", 
        "⭕ Set Theory (ইউনিয়ন, ইন্টারсеকশন ও ভেন ডায়াগ্রাম)", 
        "🔢 Permutation & Combination (বিন্যাস ও সমাবেশ)"
    ]
)

# ৬. স্মার্ট প্র্যাকটিস বাটনসমূহ
st.write("💡 **স্মার্ট প্র্যাকটিস টুলস (যেকোনো একটি বাটনে ক্লিক করো):**")
col1, col2, col3 = st.columns(3)

if 'input_val' not in st.session_state:
    st.session_state.input_val = ""

if col1.button("📋 লজিক এক্সাম্পল রান"):
    st.session_state.input_val = "Prove that the logical expression (P -> Q) AND NOT Q -> NOT P is a Tautology using a truth table."
if col2.button("⭕ সেট থিওরি এক্সাম্পল রান"):
    st.session_state.input_val = "Let U = {1,2,3,4,5,6,7,8,9,10}. If A = {1,3,5,7,9} and B = {2,3,5,7}, find A U B, A n B, and A' with verification steps."
if col3.button("🔢 বিন্যাস ও সমাবেশ রান"):
    st.session_state.input_val = "In how many ways can a committee of 4 members be formed from a group of 7 men and 5 women if the committee must include exactly 2 numbers of women?"

st.write("---")

# 🔍 ইনপুট বক্স ও মেট্রিক্স
user_query = st.text_area(
    "📝 তোমার ডিসক্রিট ম্যাথের প্রশ্নটি নিচে টাইপ করো বা এডিট করো:", 
    value=st.session_state.input_val,
    placeholder="এখানে তোমার প্রশ্নটি লেখো...", 
    height=130
)

m_col1, m_col2 = st.columns(2)
with m_col1:
    st.info(f"🔹 **ক্যারেক্টার সংখ্যা:** {len(user_query)}")
with m_col2:
    st.info(f"🔹 **মোট শব্দ সংখ্যা:** {len(user_query.split())}")

st.write("")

# অ্যাকশন বাটনসমূহ
btn_col1, btn_col2 = st.columns([4, 1])
with btn_col1:
    solve_btn = st.button("🚀 এক্সপার্ট এআই সリューション জেনারেট করো", use_container_width=True)
with btn_col2:
    if st.button("🗑️ Reset", use_container_width=True):
        st.session_state.input_val = ""
        st.rerun()

# 🧮 এআই ব্যাকএন্ড সলভিং লজিক
if solve_btn:
    if not user_query:
        st.warning("⚠️ আগে সলভ করার জন্য কোনো প্রশ্ন ইনপুট দাও বা উপরের উদাহরণ বাটনে ক্লিক করো!")
    else:
        # অ্যানিমেশন ও প্রোগ্রেস বার ইফেক্ট (ইন্টারঅ্যাক্টিভ অ্যানিমেশন)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent_complete in range(10, 101, 30):
            time.sleep(0.2)
            progress_bar.progress(percent_complete)
            status_text.text(f"🧠 এআই লজিক প্রসেস করছে... {percent_complete}%")
            
        with st.spinner("✨ ফাইনাল সলিউশন ফরম্যাট করা হচ্ছে..."):
            try:
                genai.configure(api_key=SECURE_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are a world-class university professor teaching Discrete Mathematics to Computer Science engineering students.
                Provide a flawless, highly structured, and academic step-by-step solution for the following problem.
                Topic Category: {topic}
                Problem: {user_query}
                
                Strict Output Structure:
                1. 📝 **Mathematical Analysis / Given Data**: Clearly define the parameters or variables given.
                2. 🛠️ **Step-by-Step Derivation**: Numbered logical steps breaking down the core formulas or laws applied.
                3. 📊 **Visual Representation/Table (if applicable)**: Render markdown tables for Truth Tables or Venn breakdowns elegantly.
                4. 🎯 **Final Conclusion**: A bold final conclusion box stating the absolute definitive mathematical answer.
                """
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(temperature=0.15)
                )
                
                status_text.empty()
                progress_bar.empty()
                
                # সাকসেস বেলুন ইফেক্ট
                st.balloons()
                st.success("🎉 সমাধান সফলভাবে তৈরি হয়েছে!")
                
                with st.container(border=True):
                    st.markdown(response.text)
                
            except Exception as e:
                status_text.empty()
                progress_bar.empty()
                st.error(f"❌ রান-টাইম এরর: {e}\n\nদয়া করে এপিআই কি চেক করো।")

st.write("---")

# 🧠 ৭. কুইজ মডিউল
st.subheader("🧠 Interactive Lab Quiz (Self-Test)")
st.write("প্রেজেন্টেশনের সময় শিক্ষকদের ইমপ্রেস করার জন্য এই মডিউলটি ব্যবহার করো:")

st.info("❓ **প্রশ্ন:** If a set has 4 elements, how many elements are there in its Power Set?")

ans_col1, ans_col2, ans_col3 = st.columns(3)
if ans_col1.button("Option A: 4টি"):
    st.error("❌ ভুল উত্তর! আবার চেষ্টা করো।")
if ans_col2.button("Option B: 8টি"):
    st.error("❌ ভুল উত্তর! উপাদান সংখ্যার সূত্র হলো 2^n।")
if ans_col3.button("Option C: 16টি (Correct)"):
    st.success("🎉 চমৎকার! সঠিক উত্তর। কারণ Power Set এর উপাদান সংখ্যা হলো 2^4 = 16।")

st.write("---")
st.caption("Developed by MD FAZLE RABBI SOHAN | PU CSE Innovation Lab")
