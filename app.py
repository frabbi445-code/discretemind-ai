import streamlit as st
import google.generativeai as genai
import time
import pandas as pd
import random
import math

# ১. পেজ সেটিংস ও প্রিমিয়াম থিম
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
            status_text.markdown(f"⚙️ **এআই ওমনি-পার্সার ম্যাথমেტიკ্যাল লজিক প্রসেস করছে... {percent_complete}%**")
            
        with st.spinner("✨ সমাধান একাডেমিক স্ট্যান্ডার্ডে ফরম্যাট করা হচ্ছে..."):
            try:
                if GEMINI_API_KEY:
                    genai.configure(api_key=GEMINI_API_KEY)
                    
                    # ইউনিভার্সাল বেস মডেল সেটআপ যা ৪MD এরর দেবে না
                    model = genai.GenerativeModel(model_name='gemini-pro')
                    prompt = f"You are an expert university professor in Discrete Mathematics. Provide a rigorous, step-by-step, textbook-style solution for: {user_query}. Use LaTeX formatting."
                    response = model.generate_content(prompt)
                    output_text = response.text
                else:
                    cleaned_q = user_query.lower()
                    if "isomorphic" in cleaned_q:
                        output_text = "\n### 📝 Given Data & Analysis\n* Graph 1 and Graph 2 have 4 vertices each.\n* All vertices have a degree of 2.\n\n### 🎯 Adjacency Matrices & Structural Invariants\nBoth graphs represent a cyclic graph of order 4 ($C_4$). Since a bijection exists preserving adjacency, the graphs are **Isomorphic**."
                    else:
                        output_text = "\n⚠️ **System Note:** Please add your `GEMINI_API_KEY` in Streamlit Secrets to solve custom questions live."
            except Exception as e:
                output_text = f"❌ API Method Access Error: {e}. অনুগ্রহ করে নিশ্চিত করুন যে আপনার API key-টি সচল এবং সঠিক পারমিশনযুক্ত।"
            
            status_text.empty()
            progress_bar.empty()
            st.balloons()
            st.success("🎉 সমাধান সফলভাবে জেনারেট হয়েছে!")
            with st.container(border=True):
                st.markdown(output_text)

st.write("---")

# 🧠 ৫. অ্যাডভান্সড ডাইনামিক মক টেস্ট সিমুলেটর
st.subheader("📝 Discrete Mathematics Mid/Final Mock Test")
st.caption("💡 এটি একটি প্রফেশনাল এক্সাম এনভায়রনমেন্ট। প্রশ্ন সিলেক্ট করে একদম শেষে 'সাবমিট মক টেস্ট' বাটনে চাপ দাও।")

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
        "question": "২. ডিসক্রিট ম্যাথে একটি কানেক্টেড গ্রাফে যদি কোনো সাইকেল (Cycle) না থাকে, তবে তাকে কী বলা হয়?",
        "options": ["Tree (বৃক্ষ)", "Complete Graph", "Bipartite Graph"],
        "correct": "Tree (বৃক্ষ)"
    },
    {
        "id": 3,
        "topic": "Set Theory & Relations",
        "question": f"৩. একটি সেটে উপাদান সংখ্যা {subset_n} হলে, সেটটির রিফ্লেক্সিভ রিলেশন (Reflexive Relations) এর সংখ্যা কতটি হবে?",
        "options": [f"2^{subset_n * (subset_n - 1)}টি", f"2^{subset_n**2}টি", f"{2**subset_n}টি"],
        "correct": f"2^{subset_n * (subset_n - 1)}টি"
    },
    {
        "topic": "Set Theory & Relations",
        "id": 4,
        "question": "৪. যদি কোনো ফাংশন একই সাথে One-to-One এবং Onto হয়, তবে তাকে কী ধরণের ফাংশন বলা হয়?",
        "options": ["Bijective Function", "Surjective Function", "Injective Function"],
        "correct": "Bijective Function"
    },
    {
        "topic": "Propositional Logic",
        "id": 5,
        "question": "৫. প্রপোজিশনাল লজিকের নিয়ম অনুযায়ী, একটি কন্ডিশনাল উক্তি P → Q কখন একমাত্র মিথ্যা (False) হয়?",
        "options": ["যখন P সত্য এবং Q মিথ্যা", "যখন দুটি উক্তিই মিথ্যা হয়", "যখন P মিথ্যা এবং Q সত্য"],
        "correct": "যখন P সত্য এবং Q মিথ্যা"
    }
]

if not st.session_state.test_submitted:
    with st.form("mock_test_form"):
        st.info("⏱️ **পরীক্ষার নিয়মাবলী:** নিচে ৫টি প্রশ্ন দেওয়া আছে। প্রতিটি প্রশ্নের জন্য ১ মার্কস। নেগেটিভ মার্কিং নেই।")
        
        for q in questions_list:
            st.markdown(f"#### **{q['question']}**")
            st.caption(f"🏷️ ক্যাটাগরি: {q['topic']} | মার্কস: ১.০০")
            
            st.session_state.answers[q['id']] = st.radio(
                "সঠিক উত্তরটি সিলেক্ট করো:", 
                q['options'], 
                key=f"mock_ans_{q['id']}_{st.session_state.mock_seed}"
            )
            st.write("---")
            
        submit_test = st.form_submit_button("📤 সাবমিট মক টেস্ট (Submit Exam)")
        
        if submit_test:
            st.session_state.test_submitted = True
            st.rerun()

else:
    st.success("🎉 তোমার উত্তরপত্র সফলভাবে মূল্যায়িত হয়েছে! নিচে লাইভ গ্রেড ও ফিডব্যাক রিপোর্ট দেওয়া হলো:")
    
    score = 0
    detailed_report = []
    
    for q in questions_list:
        user_ans = st.session_state.answers.get(q['id'])
        is_correct = user_ans == q['correct']
        if is_correct:
            score += 1
        detailed_report.append({
            "প্রশ্ন": q['question'],
            "তোমার উত্তর": user_ans,
            "সঠিক উত্তর": q['correct'],
            "স্ট্যাটাস": "✅ সঠিক" if is_correct else "❌ ভুল"
        })
        
    success_rate = (score / 5) * 100
    if score == 5:
        grade = "A+"
        color = "green"
        feedback = "অসাধারণ পারফরম্যান্স! তোমার ডিসক্রিট ম্যাথ প্রিপারেশন ১০০% পারফেক্ট। ল্যাব ফাইনাল এবং থিওরিতে তুমি নির্ঘাত ফুল মার্কস পাচ্ছো। কিপ ইট আপ!"
    elif score >= 4:
        grade = "A"
        color = "blue"
        feedback = "খুব ভালো পারফরম্যান্স! মাইনর কিছু গ্যাপ ছাড়া তোমার বেসিক কনসেপ্ট বেশ পরিষ্কার। ভুল হওয়া প্রশ্নগুলো আরেকবার রিভিশন দিলে ল্যাবে চমৎকার এ-প্লাস নিশ্চিত।"
    elif score >= 2:
        grade = "B"
        color = "orange"
        feedback = "মাঝারি পারফরম্যান্স। গ্রাফ থিওরি এবং লজিকের কিছু জায়গায় তোমার এখনও ঘাটতি রয়েছে। ল্যাব লেকচার শিটগুলো ভালোভাবে রিভিশন দেওয়ার পরামর্শ দেওয়া হলো।"
    else:
        grade = "F (Fail)"
        color = "red"
        feedback = "অসস্তোষজনক স্কোর। ডিসক্রিট ম্যাথমেটিক্সের মূল থিওরিগুলো তোমার আরেকবার স্ক্র্যাচ থেকে পড়া উচিত। উপরের এআই সলভার ইঞ্জিন ব্যবহার করে প্র্যাকটিস করো।"

    with st.container(border=True):
        st.markdown(f"### 📊 Comprehensive Exam Report Card")
        st.write(f"**পরীক্ষার্থী:** MD FAZLE RABBI SOHAN")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric(label="প্রাপ্ত নম্বর (Score)", value=f"{score} / 5")
        with col_s2:
            st.metric(label="সাফল্যের হার (Accuracy)", value=f"{int(success_rate)}%")
        with col_s3:
            st.markdown(f"<h4>ফাইনাল গ্রেড: <span style='color:{color}; font-weight:bold;'>{grade}</span></h4>", unsafe_allow_html=True)
            
        st.write("---")
        st.markdown(f"🗣️ **একাডেমিক ফিডব্যাক ও গাইড:**")
        st.info(feedback)
        
        st.write("---")
        st.markdown("#### 📋 প্রশ্নভিত্তিক উত্তরপত্র পর্যালোচনা (Answer Review)")
        df_report = pd.DataFrame(detailed_report)
        st.dataframe(df_report, use_container_width=True)

    if st.button("🔄 নতুন প্রশ্নপত্রে আবার মক টেস্ট দাও"):
        st.session_state.mock_seed = random.randint(1, 9999)
        st.session_state.test_submitted = False
        st.session_state.answers = {}
        st.rerun()

st.write("---")
st.caption("Developed by MD FAZLE RABBI SOHAN | PU CSE Innovation Lab")
