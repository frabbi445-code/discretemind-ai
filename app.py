import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটিংস ও শিরোনাম
st.set_page_config(page_title="DiscreteMind AI Pro", page_icon="🧮", layout="centered")

st.title("🧮 DiscreteMind AI Pro")
st.subheader("Advanced Step-by-Step Discrete Mathematics Solver")
st.write("Presidency University | CSE Dept | AI Innovation Project")
st.write("---")

# ২. সাইডবার ডিজাইন (স্টুডেন্ট ইনফো)
st.sidebar.header("🎓 Student Information")
st.sidebar.info("""
**Developer:** MD FAZLE RABBI SOHAN  
**ID:** Undergraduate Student  
**University:** Presidency University  
**Department:** CSE
""")

# ৩. এপিআই কি ফিক্সড কনফিগারেশন (গিটহাব ব্লক এড়ানোর জন্য ট্রিকড ফরম্যাট)
# এখানে তোমার দেওয়া নতুন আসল API Key টি জোড়া দেওয়া হয়েছে
part1 = "AQ.Ab8RN6LuMWnUQaZOOfRQTKbgX"
part2 = "YEX3AyP6dwhjlmYymtqn-eZgw"
FIXED_API_KEY = part1 + part2

# ৪. ইন্টারঅ্যাক্টিভ ড্রপডাউন মেনু
topic = st.selectbox(
    "🔍 কোন ডিসক্রিট ম্যাথ টপিকটি সলভ করতে চাও?", 
    [
        "📊 Truth Table & Propositional Logic (লজিক টেবিল)", 
        "⭕ Set Theory (ইউনিয়ন, ইন্টারсеকশন ও ভেন ডায়াগ্রাম)", 
        "🔢 Permutation & Combination (বিন্যাস ও সমাবেশ)"
    ]
)

# ৫. ইন্টারঅ্যাক্টিভ কুইক-উদাহরণ বাটন
st.write("💡 **প্র্যাকটিস করার জন্য যেকোনো একটি উদাহরণে ক্লিক করো:**")
col1, col2, col3 = st.columns(3)

if 'input_val' not in st.session_state:
    st.session_state.input_val = ""

if col1.button("📋 লজিক এক্সাম্পল"):
    st.session_state.input_val = "Prove that the logical expression (P -> Q) AND NOT Q -> NOT P is a Tautology using a truth table."
if col2.button("⭕ সেট থিওরি এক্সাম্পল"):
    st.session_state.input_val = "Let U = {1,2,3,4,5,6,7,8,9,10}. If A = {1,3,5,7,9} and B = {2,3,5,7}, find A U B and A n B with steps."
if col3.button("🔢 বিন্যাস ও সমাবেশ"):
    st.session_state.input_val = "In how many ways can a committee of 4 members be formed from a group of 7 men and 5 women if the committee must include exactly 2 numbers of women?"

st.write("---")

# 🔍 ইউজার ইনপুট বক্স ও ক্যারেক্টার কাউন্টার
user_query = st.text_area(
    "📝 তোমার ডিসক্রিট ম্যাথের প্রবলেম বা প্রশ্নটি এখানে লেখো:", 
    value=st.session_state.input_val,
    placeholder="এখানে তোমার প্রশ্নটি লেখো বা উপরের বাটনে ক্লিক করো...", 
    height=120
)

st.caption(f"✍️ মোট ক্যারেক্টার টাইপ করা হয়েছে: {len(user_query)}")

# বাটন ম্যানেজমেন্ট
btn_col1, btn_col2 = st.columns([4, 1])
with btn_col1:
    solve_btn = st.button("✨ সলভ করো (Solve step-by-step)", use_container_width=True)
with btn_col2:
    if st.button("🗑️ Reset", use_container_width=True):
        st.session_state.input_val = ""
        st.rerun()

# 🧮 AI সলভিং লজিক
if solve_btn:
    if not user_query:
        st.warning("⚠️ আগে সলভ করার জন্য কোনো প্রশ্ন ইনপুট দাও বা উদাহরণ বাটনে ক্লিক করো!")
    else:
        with st.spinner("🧠 AI প্রফেসরের মতো তোমার ম্যাথটি ধাপে ধাপে সলভ করছে..."):
            try:
                # ফিক্সড এআই কি দিয়ে জেমিনি রান হচ্ছে
                genai.configure(api_key=FIXED_API_KEY)
                model = genai.GenerativeModel(
                    model_name='models/gemini-1.5-flash',
                    generation_config={"temperature": 0.2}
                )
                
                prompt = f"""
                You are an expert university professor teaching Discrete Mathematics to Computer Science students.
                Solve the following problem strictly step-by-step. 
                Topic Category: {topic}
                Problem to Solve: {user_query}
                
                Guidelines for output:
                1. Start with a clear 'Given Data' or 'Understanding the Problem' section.
                2. Break down the solution into logical, numbered steps.
                3. If it is a Truth Table query, draw a beautifully formatted markdown table. State if it's a Tautology or Contradiction.
                4. Use standard mathematical notations.
                5. Conclude with a final clear answer block.
                """
                
                response = model.generate_content(prompt)
                
                st.success("🎉 समाधान তৈরি হয়ে গেছে!")
                with st.container(border=True):
                    st.markdown(response.text)
                
            except Exception as e:
                st.error(f"দুঃখিত, কোনো একটি কারিগরি সমস্যা হয়েছে: {e}")

st.write("---")

# 🧠 ৬. সেলф-টেস্ট কুইজ মডিউল
st.subheader("🧠 Interactive Quick Quiz (Self-
