import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটিংস ও আকর্ষণীয় সিএসই থিম ডিজাইন
st.set_page_config(page_title="DiscreteMind AI", page_icon="🧮", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #1e3a8a; text-align: center; font-family: 'Arial'; font-weight: bold; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 10px; font-weight: bold; width: 100%; padding: 12px; }
    .stButton>button:hover { background-color: #1d4ed8; color: white; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allowed_html=True)

st.title("🧮 DiscreteMind AI")
st.subheader("Step-by-Step Discrete Mathematics Logic Solver")
st.write("Presidency University | CSE Dept | AI Innovation Project")

# ⚠️ তোমার দেওয়া নতুন আসল Gemini API Key
GOOGLE_API_KEY = "AQ.Ab8RN6J-EqMxEPjwE8gsTNWKp-YV2wcs53oVk9MuYwTpTbb7WA"

st.write("---")

# ২. ড্রপডাউন মেনু (টপিক সিলেকশন)
topic = st.selectbox(
    "🔍 কোন ডিসক্রিট ম্যাথ টপিকটি সলভ করতে চাও?", 
    [
        "📊 Truth Table & Propositional Logic (লজিক টেবিল)", 
        "⭕ Set Theory (ইউনিয়ন, ইন্টারসেকশন ও ভেন ডায়াগ্রাম)", 
        "🔢 Permutation & Combination (বিন্যাস ও সমাবেশ)"
    ]
)

# ৩. টপিক অনুযায়ী প্লেসহোল্ডার টেক্সট পরিবর্তন
if "Truth Table" in topic:
    placeholder_text = "যেমন: Prove that (P -> Q) AND P -> Q is a Tautology"
elif "Set Theory" in topic:
    placeholder_text = "যেমন: If A = {1, 2, 3} and B = {3, 4, 5}, find A U B and A n B with steps."
else:
    placeholder_text = "যেমন: In how many ways can a committee of 3 members be formed from 5 people?"

# ৪. ইউজার ইনপুট বক্স
user_query = st.text_area("📝 তোমার ডিসক্রিট ম্যাথের প্রবলেম বা প্রশ্নটি এখানে লেখো:", placeholder=placeholder_text, height=120)

# ৫. AI জেনারেশন ও সলভিং লজিক
if st.button("✨ সলভ করো (Solve step-by-step)"):
    if not GOOGLE_API_KEY:
        st.error("API Key নিশ্চিত করো।")
    elif not user_query:
        st.warning("আগে সলভ করার জন্য কোনো প্রশ্ন ইনপুট দাও!")
    else:
        with st.spinner("🧠 AI প্রফেসরের মতো তোমার ম্যাথটি ধাপে ধাপে সলভ করছে..."):
            try:
                genai.configure(api_key=GOOGLE_API_KEY)
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
                st.markdown("<div class='card'>", unsafe_allowed_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allowed_html=True)
                
            except Exception as e:
                st.error(f"দুঃখিত, কোনো একটি কারিগরি সমস্যা হয়েছে: {e}")

st.write("---")
st.caption("Developed by MD FAZLE RABBI SOHAN | PU CSE")
