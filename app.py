import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটিংস ও শিরোনাম
st.set_page_config(page_title="DiscreteMind AI", page_icon="🧮", layout="centered")

st.title("🧮 DiscreteMind AI")
st.subheader("Step-by-Step Discrete Mathematics Logic Solver")
st.write("Presidency University | CSE Dept | AI Innovation Project")
st.write("---")

# ২. সাইডবার ডিজাইন (স্টুডেন্ট ইনফো এবং সেফ এপিআই ইনপুট)
st.sidebar.header("🎓 Student Information")
st.sidebar.info("""
**Developer:** MD FAZLE RABBI SOHAN  
**ID:** Undergraduate Student  
**University:** Presidency University  
**Department:** CSE
""")

st.sidebar.write("---")
st.sidebar.header("🔑 Authentication")

# ইউজার সরাসরি এখান থেকে নতুন API Key বসাতে পারবে, কোডে এক্সপোজ হবে না
user_api_key = st.sidebar.text_input(
    "তোমার Gemini API Key টি এখানে বসাও:", 
    type="password", 
    placeholder="AI Studio থেকে পাওয়া Key টি পেস্ট করো..."
)
st.sidebar.caption("💡 [Google AI Studio](https://aistudio.google.com/) থেকে ফ্রিতে নতুন Key তৈরি করে এখানে বসাও।")

# ৩. ইন্টারঅ্যাক্টিভ ড্রপডাউন মেনু
topic = st.selectbox(
    "🔍 কোন ডিসক্রিট ম্যাথ টপিকটি সলভ করতে চাও?", 
    [
        "📊 Truth Table & Propositional Logic (লজিক টেবিল)", 
        "⭕ Set Theory (ইউনিয়ন, ইন্টারসেকশন ও ভেন ডায়াগ্রাম)", 
        "🔢 Permutation & Combination (বিন্যাস ও সমাবেশ)"
    ]
)

# ৪. ইন্টারঅ্যাক্টিভ কুইক-উদাহরণ বাটন (ক্লিক করলেই বক্সে প্রশ্ন চলে যাবে)
st.write("💡 **প্র্যাকটিস করার জন্য যেকোনো একটি উদাহরণে ক্লিক করো:**")
col1, col2, col3 = st.columns(3)

example_text = ""
if col1.button("📋 লজিক এক্সাম্পল"):
    example_text = "Prove that the logical expression (P -> Q) AND NOT Q -> NOT P is a Tautology using a truth table."
if col2.button("⭕ সেট থিওরি এক্সাম্পল"):
    example_text = "If A = {1, 2, 3, 4} and B = {3, 4, 5, 6}, find A U B, A n B, and A - B with step-by-step verification."
if col3.button("🔢 বিন্যাস ও সমাবেশ"):
    example_text = "In how many ways can a committee of 4 members be formed from a group of 7 men and 5 women if the committee must include exactly 2 numbers of women?"

st.write("---")

# ৫. ইউজার ইনপুট বক্স (বাটন ক্লিকের ভ্যালুসহ)
user_query = st.text_area(
    "📝 তোমার ডিসক্রিট ম্যাথের প্রবলেম বা প্রশ্নটি এখানে লেখো:", 
    value=example_text,
    placeholder="এখানে তোমার প্রশ্নটি লেখো বা উপরের বাটনে ক্লিক করো...", 
    height=120
)

# ৬. AI সলভিং লজিক
if st.button("✨ সলভ করো (Solve step-by-step)"):
    if not user_api_key:
        st.error("❌ অ্যাপটি চালানোর জন্য বামপাশের সাইডবারে তোমার Gemini API Key টি বসাতে হবে!")
    elif not user_query:
        st.warning("⚠️ আগে সলভ করার জন্য কোনো প্রশ্ন ইনপুট দাও বা উদাহরণ বাটনে ক্লিক করো!")
    else:
        with st.spinner("🧠 AI প্রফেসরের মতো তোমার ম্যাথটি ধাপে ধাপে সলভ করছে..."):
            try:
                # ইউজারের দেওয়া এপিআই কি কনফিগার করা হচ্ছে
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are an expert university professor teaching Discrete Mathematics to Computer Science students.
                Solve the following problem strictly step-by-step. 
                Topic Category: {topic}
                Problem to Solve: {user_query}
                
                Guidelines for output:
                1. Start with a clear 'Given Data' or 'Understanding the Problem' section.
                2. Break down the solution into logical, numbered steps (e.g., Step 1, Step 2).
                3. If it is a Truth Table query, draw a beautifully formatted text/markdown table containing columns for variables and sub-expressions. State if it's a Tautology or Contradiction.
                4. Use standard mathematical notations.
                5. Conclude with a final clear answer block.
                Keep the tone academic, helpful, and professional.
                """
                
                response = model.generate_content(prompt)
                
                st.success("🎉 সমাধান তৈরি হয়ে গেছে!")
                # স্ট্যান্ডার্ড বর্ডার কন্টেইনারে রেজাল্ট শো করা
                with st.container(border=True):
                    st.markdown(response.text)
                
            except Exception as e:
                st.error(f"দুঃখিত, কোনো একটি কারিগরি সমস্যা হয়েছে: {e}\n\nসম্ভবত তোমার এপিআই কি-টি সঠিক নয় বা ব্লক হয়েছে। দয়া করে নতুন একটি কি বসিয়ে চেষ্টা করো।")

st.write("---")
st.caption("Developed by MD FAZLE RABBI SOHAN | PU CSE")
