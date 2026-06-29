import streamlit as st
import time
import pandas as pd
import itertools
import random
import math
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# ১. পেজ সেটিংস ও প্রিমিয়াম থিম
st.set_page_config(page_title="DiscreteMind AI Smart Engine", page_icon="🧮", layout="centered")

st.title("🧮 DiscreteMind AI Pro: Auto-Detect Engine")
st.subheader("Single-Input Dynamic Mathematics Course Project")
st.write("Presidency University | CSE Dept | Discrete Mathematics Project")
st.write("---")

# ২. সাইডবার প্রোফাইল কার্ড
st.sidebar.header("🎓 Course Project Profile")
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    st.write("**Course:** Discrete Mathematics")
    st.caption("🔥 Engine: 100% Smart Auto-Detection Active")

st.sidebar.write("---")
st.sidebar.header("🔗 Quick Navigation")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")

# ৩. সিঙ্গেল ইনপুট ইন্টারফেস (কোনো টপিক সিলেকশন লাগবে না)
st.subheader("🚀 Smart Input Box")
st.caption("💡 **নিয়ম:** কোনো টপিক সিলেক্ট করা লাগবে না! নিচে লজিক এক্সপ্রেশন লিখলে ট্রুথ টেবিল আসবে, আর সেটের ম্যাথ (যেমন: `A={1,2}; B={2,3}`) লিখলে ভেন ডায়াগ্রাম আসবে।")

user_input = st.text_area("📝 তোমার ডিসক্রিট ম্যাথের প্রশ্নটি এখানে লিখো বা পেস্ট করো:", value="", placeholder="উদাহরণ ১: (P -> Q) and not P\nউদাহরণ ২: A={1, 2, 3, 5, 7}; B={3, 5, 7, 9}")

if st.button("🚀 এক্সপার্ট সリューション জেনারেট করো", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ দয়া করে আগে ইনপুট বক্সে কিছু লিখো!")
    else:
        cleaned_input = user_input.lower().strip()
        
        # 📊 কেস ১: লজিক ডিটেকশন (যদি ইনপুটে লজিক্যাল ক্যারেক্টার থাকে)
        if "->" in cleaned_input or "<->" in cleaned_input or "and" in cleaned_input or "or" in cleaned_input or "not" in cleaned_input or "p" in cleaned_input or "q" in cleaned_input and "={" not in cleaned_input:
            try:
                # কাস্টম লজিক পার্সার
                parsed_expr = user_input.replace("<->", " == ").replace("->", " <= ")
                
                rows = []
                for P, Q in itertools.product([True, False], repeat=2):
                    env = {'P': P, 'Q': Q, 'and': lambda x, y: x and y, 'or': lambda x, y: x or y, 'not': lambda x: not x}
                    result = eval(parsed_expr, {"__builtins__": None}, env)
                    rows.append({"P": P, "Q": Q, "Result": bool(result)})
                
                df = pd.DataFrame(rows)
                st.balloons()
                st.success("🎯 লজিক এক্সপ্রেশন সনাক্ত করা হয়েছে এবং ট্রুথ টেবিল জেনারেট হয়েছে!")
                
                with st.container(border=True):
                    st.markdown(f"### 📋 Evaluated Truth Table for: `{user_input}`")
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ লজিক এক্সপ্রেশনের সিনট্যাক্স ভুল হয়েছে! এরর: {e}")
                
        # ⭕ কেস ২: সেট থিওরি ও ভেন ডায়াগ্রাম ডিটেকশন (যদি ইনপুটে সেট ডিক্লেয়ারেশন থাকে)
        elif "a=" in cleaned_input or "b=" in cleaned_input or "{" in cleaned_input or "," in cleaned_input:
            try:
                # ইনপুট থেকে সেট A এবং B এর উপাদান আলাদা করার জন্য সেফ পার্সিং
                # ফরম্যাট যেমনই হোক না কেন, সংখ্যা বা উপাদানগুলো খুঁজে বের করবে
                import re
                sets_found = re.findall(r'\{([^}]+)\}', user_input)
                
                if len(sets_found) >= 2:
                    set_A = set([x.strip() for x in sets_found[0].split(",") if x.strip()])
                    set_B = set([x.strip() for x in sets_found[1].split(",") if x.strip()])
                else:
                    # ব্যাকআপ পার্সিং যদি ব্র্যাকেট না থাকে, জাস্ট কমা দিয়ে আলাদা করা লাইন হলে
                    lines = user_input.split("\n")
                    set_A = set([x.strip() for x in lines[0].replace("A=", "").replace("A =", "").split(",") if x.strip()])
                    set_B = set([x.strip() for x in lines[1].replace("B=", "").replace("B =", "").split(",") if x.strip()])
                
                union_set = set_A.union(set_B)
                inter_set = set_A.intersection(set_B)
                diff_A_B = set_A.difference(set_B)
                diff_B_A = set_B.difference(set_A)
                
                st.balloons()
                st.success("🎯 সেট উপাদান সনাক্ত করা হয়েছে এবং ভেন ডায়াগ্রাম ড্র করা হয়েছে!")
                
                # ভেন ডায়াগ্রাম গ্রাফ
                fig, ax = plt.subplots(figsize=(5, 3.5))
                v = venn2(subsets=(len(diff_A_B), len(diff_B_A), len(inter_set)), set_labels=('Set A', 'Set B'), ax=ax)
                
                if v.get_label_by_id('10'): v.get_label_by_id('10').set_text(", ".join(list(diff_A_B)) if diff_A_B else "Ø")
                if v.get_label_by_id('01'): v.get_label_by_id('01').set_text(", ".join(list(diff_B_A)) if diff_B_A else "Ø")
                if v.get_label_by_id('11'): v.get_label_by_id('11').set_text(", ".join(list(inter_set)) if inter_set else "Ø")
                
                plt.title("Live Auto-Generated Venn Diagram", fontsize=10, color="#4f46e5", weight="bold")
                st.pyplot(fig)
                
                with st.container(border=True):
                    st.markdown("### 🎯 Mathematical Output")
                    st.write(f"✅ **Set A:** `{set_A}`")
                    st.write(f"✅ **Set B:** `{set_B}`")
                    st.write(f"✅ **Union ($A \\cup B$):** `{union_set if union_set else 'Ø'}`")
                    st.write(f"✅ **Intersection ($A \\cap B$):** `{inter_set if inter_set else 'Ø'}`")
            except Exception as e:
                st.error(f"❌ সেট ফরম্যাটটি কোড রিড করতে পারছে না। উপাদানগুলো কমা দিয়ে আলাদা করে লেখো। এরর: {e}")
        
        else:
            st.warning("⚠️ সিস্টেম ইনপুটটি সনাক্ত করতে পারছে না। লজিক উক্তি অথবা সেটের উপাদান (কমা দিয়ে) সঠিকভাবে লিখো।")

st.write("---")

# 🧠 ৪. ফুল-ডাইনামিক ইনফিনিট কুইজ ইঞ্জিন (প্রশ্ন প্রতিবার সম্পূর্ণ চেঞ্জ হবে)
st.subheader("🧠 Infinitely Variable Discrete Math Quiz")
st.caption("💡 কুইজ সেকশনটি একদম আলাদা ও ডাইনামিক করা হয়েছে। 'রিফ্রেশ' বাটনে চাপ দিলে প্রতিবার নতুন প্রশ্ন লোড হবে।")

if 'quiz_seed' not in st.session_state or st.sidebar.button("🔄 কুইজের প্রশ্নসমূহ সম্পূর্ণ চেঞ্জ করো"):
    st.session_state.quiz_seed = random.randint(1, 9999)
    st.session_state.current_q = 0
    st.session_state.topic_scores = {"Logic & Sets": 0, "Counting & Probability": 0}
    st.session_state.quiz_complete = False

random.seed(st.session_state.quiz_seed)
set_size = random.randint(3, 5)
perm_elements = random.randint(4, 6)
prob_men = random.randint(5, 7)
prob_women = random.randint(3, 5)

q_bank = [
    {
        "topic": "Logic & Sets",
        "question": f"১. একটি সেটে উপাদান সংখ্যা (n) = {set_size} হলে, সেটটির মোট সাবসেট (Subsets) কতটি হবে?",
        "options": [f"A) {set_size * 2}টি", f"B) {2**set_size}টি", f"C) {set_size**2}টি"],
        "correct": 1
    },
    {
        "topic": "Logic & Sets",
        "question": "২. প্রপোজিশনাল লজিকে কন্ডিশনাল উক্তি P → Q কখন একমাত্র মিথ্যা (False) হয়?",
        "options": ["A) যখন P সত্য এবং Q মিথ্যা", "B) যখন দুটি উক্তিই মিথ্যা হয়", "C) যখন P মিথ্যা এবং Q সত্য"],
        "correct": 0
    },
    {
        "topic": "Counting & Probability",
        "question": f"৩. {perm_elements} জন প্রতিযোগীকে একটি গোল টেবিле কত উপায়ে বিন্যস্ত (Circular Permutation) করা সম্ভব?",
        "options": [f"A) {math.factorial(perm_elements)} উপায়ে", f"B) {math.factorial(perm_elements - 1)} উপায়ে", f"C) {perm_elements * 2} উপায়ে"],
        "correct": 1
    },
    {
        "topic": "Counting & Probability",
        "question": f"৪. {prob_men} জন ছাত্র এবং {prob_women} জন ছাত্রীর মধ্য থেকে ১ জন ছাত্র ও ১ জন ছাত্রী কত উপায়ে নির্বাচন করা যাবে?",
        "options": [f"A) {prob_men + prob_women} উপায়ে", f"B) {prob_men * prob_women} উপায়ে", f"C) {int(prob_men * (prob_men-1)/2)} উপায়ে"],
        "correct": 1
    }
]

if not st.session_state.quiz_complete:
    q_idx = st.session_state.current_q
    cur_topic = q_bank[q_idx]['topic']
    
    st.info(f"📋 প্রশ্ন নম্বর: {q_idx + 1} / 4 | 🏷️ ক্যাটাগরি: {cur_topic}")
    st.write(f"**{q_bank[q_idx]['question']}**")
    
    user_ans = st.radio("সঠিক উত্তরটি বেছে নাও:", q_bank[q_idx]['options'], key=f"inf_q_{q_idx}_{st.session_state.quiz_seed}")
