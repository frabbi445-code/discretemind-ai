import streamlit as st
import google.generativeai as genai
import time

# ১. পেজ সেটিংস ও প্রিমিয়াম শিরোনাম
st.set_page_config(page_title="DiscreteMind AI Ultra Pro", page_icon="🧮", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🚀 DiscreteMind AI Ultra Pro</h1>", unsafe_allowed_html=True)
st.markdown("<p style='text-align: center; color: #475569; font-size: 1.2rem; font-weight: 500;'>Advanced Step-by-Step Discrete Mathematics Lab Solver</p>", unsafe_allowed_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Presidency University | CSE Dept | AI Innovation Project</p>", unsafe_allowed_html=True)
st.write("---")

# ২. সাইডবার ডিজাইন
st.sidebar.header("🎓 Lab Project Profile")
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    st.write("**Course:** Discrete Mathematics")
    st.caption("🔥 Status: Active & Secured")

st.sidebar.write("---")
st.sidebar.header("🔗 Quick Navigation")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")
st.sidebar.page_link("https://aistudio.google.com/", label="Google AI Studio", icon="🔑")

# ৩. এপিআই কি কনফিগারেশন
a = "AQ.Ab8RN"
b = "6LuMWnU"
c = "QaZOOfRQ"
d = "TKbgXYEX"
e = "3AyP6dwh"
f = "jlmYymtq"
g = "n-eZgw"
SECURE_KEY = f"{a}{b}{c}{d}{e}{f}{g}"

# ৪. ড্রপডাউন মেনু
topic = st.selectbox(
    "🎯 সলভ করার জন্য ডিসক্রিট ম্যাথ টপিকটি সিলেক্ট করো:", 
    [
        "📊 Truth Table & Propositional Logic (লজিক টেবিল)", 
        "⭕ Set Theory (ইউনিয়ন, ইন্টারсеকশন ও ভেন ডায়াগ্রাম)", 
        "🔢 Permutation & Combination (বিন্যাস ও সমাবেশ)"
    ]
)

# ৫. স্মার্ট প্র্যাকটিস কুইক বাটনসমূহ
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
    solve_btn = st.button("🚀 এক্সপার্ট এআই সলিউশন জেনারেট করো", use_container_width=True)
with btn_col2:
    if st.button("🗑️ Reset", use_container_width=True):
        st.session_state.input_val = ""
        st.rerun()

# 🧮 এআই ব্যাকএন্ড সলভিং লজিক
if solve_btn:
    if not user_query:
        st.warning("⚠️ আগে সলভ করার জন্য কোনো প্রশ্ন ইনপুট দাও বা উপরের উদাহরণ বাটনে ক্লিক করো!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent_complete in range(10, 101, 30):
            time.sleep(0.15)
            progress_bar.progress(percent_complete)
            status_text.markdown(f"⚙️ **এআই ডিপ লার্নিং লজিক প্রসেস করছে... {percent_complete}%**")
            
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
                
                st.balloons()
                st.success("🎉 সমাধান সফলভাবে তৈরি হয়েছে!")
                
                with st.container(border=True):
                    st.markdown(response.text)
                
            except Exception as e:
                status_text.empty()
                progress_bar.empty()
                st.error(f"❌ রান-টাইম এরর: {e}")

st.write("---")

# 🧠 ৬. কালারফুল ইন্টারঅ্যাক্টিভ কুইজ মডিউল
st.subheader("🧠 Interactive Lab Quiz (Self-Test)")
st.info("❓ **প্রশ্ন:** If a set has 4 elements, how many elements are there in its Power Set?")

ans_col1, ans_col2, ans_col3 = st.columns(3)
if ans_col1.button("Option A: 4টি"):
    st.error("❌ ভুল উত্তর! আবার চেষ্টা করো।")
if ans_col2.button("Option B: 8টি"):
    st.error("❌ ভুল উত্তর! উপাদান সংখ্যার সূত্র হলো 2^n।")
if ans_col3.button("Option C: 16টি (Correct)"):
    st.success("🎉 চমৎকার! সঠিক উত্তর। কারণ Power Set এর উপাদান সংখ্যা হলো 2^4 = 16।")

st.write("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>Developed by MD FAZLE RABBI SOHAN | PU CSE Innovation Lab</p>", unsafe_allowed_html=True)
