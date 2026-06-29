import streamlit as st
import time
import pandas as pd
import itertools
import random
import math
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# ১. পেজ সেটিংস ও প্রিমিয়াম থিম
st.set_page_config(page_title="DiscreteMind AI Advanced", page_icon="🧮", layout="centered")

st.title("🧮 DiscreteMind AI Pro: Advanced Math Lab")
st.subheader("Dynamic Logic Parser, Set Venn Diagram & Infinite Quiz Engine")
st.write("Presidency University | CSE Dept | Discrete Mathematics Project")
st.write("---")

# ২. সাইডবার প্রোফাইলカード
st.sidebar.header("🎓 Course Project Profile")
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    st.write("**Course:** Discrete Mathematics")
    st.caption("🔥 Engine: 100% Offline, Venn Graph & Conditional Logic Enabled")

st.sidebar.write("---")
st.sidebar.header("🔗 Quick Navigation")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")

# ৩. টপিক সিলেকশন
st.subheader("🚀 Real-Time Mathematical Engine")
topic = st.selectbox(
    "🎯 সলভ করার জন্য ডিসক্রিট ম্যাথ মডিউলটি সিলেক্ট করো:", 
    ["📊 Advanced Truth Table Generator (ইম্প্লিকেশন ও বাই-কন্ডিশনাল সলভার)", 
     "⭕ Set Theory Solver & Live Venn Diagram (ভেন ডায়াগ্রাম জেনারেটর)"]
)

# ৪. মডিউল ১: অ্যাডভান্সড লজিক সলভার (-> এবং <-> হ্যান্ডলিং)
if topic == "📊 Advanced Truth Table Generator (ইম্প্লিকেশন ও বাই-কন্ডিশনাল সলভার)":
    st.info("💡 **অ্যাডভান্সড লজিক গাইড:** লজিক এক্সপ্রেশনে লেখো: `and`, `or`, `not` এবং ইম্প্লিকেশনের জন্য `->` ও বাই-কন্ডিশনালের জন্য `<->` ব্যবহার করো।")
    
    # ইনপুট বক্স একদম খালি ও ক্লিন রাখা হয়েছে
    user_expr = st.text_input("📝 তোমার লজিক্যাল এক্সপ্রেশনটি এখানে টাইপ করো (যেমন: (P -> Q) and not P):", value="")
    
    if st.button("🚀 এক্সপার্ট সリューション জেনারেট করো", key="logic_btn"):
        if not user_expr:
            st.warning("⚠️ আগে একটি লজিক্যাল এক্সপ্রেশন ইনপুট দাও!")
        else:
            try:
                # কাস্টম পার্সার লজিক
                parsed_expr = user_expr.replace("<->", " == ").replace("->", " <= ")
                
                rows = []
                for P, Q in itertools.product([True, False], repeat=2):
                    env = {'P': P, 'Q': Q, 'and': lambda x, y: x and y, 'or': lambda x, y: x or y, 'not': lambda x: not x}
                    result = eval(parsed_expr, {"__builtins__": None}, env)
                    rows.append({"P": P, "Q": Q, "Result": bool(result)})
                
                df = pd.DataFrame(rows)
                st.balloons()
                st.success("🎉 কন্ডিশনাল লজিক টেবিলটি সফলভাবে ক্যালকুলেট হয়েছে!")
                
                with st.container(border=True):
                    st.markdown(f"### 📋 Evaluated Truth Table for: `{user_expr}`")
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ এক্সপ্রেশন সিনট্যাক্স ভুল হয়েছে! ব্র্যাকেট বা লজিক অপারেটরগুলো ঠিক করুন। এরর: {e}")

# 📂 মডিউল ২: ভেন ডায়াগ্রাম এবং সেট ক্যালকুলেটর
elif topic == "⭕ Set Theory Solver & Live Venn Diagram (ভেন ডায়াগ্রাম জেনারেটর)":
    st.info("💡 **নিয়ম:** কমা (,) দিয়ে উপাদানগুলো আলাদা করে লিখো। কোড রিয়েল-টাইমে সেট অপারেশনের হিসাব করে কাস্টম Venn Diagram ড্র করবে।")
    
    col1, col2 = st.columns(2)
    with col1:
        set_a_str = st.text_input("Set A এর উপাদানসমূহ লিখো (যেমন: 1, 2, 3):", value="")
    with col2:
        set_b_str = st.text_input("Set B এর উপাদানসমূহ লিখো (যেমন: 3, 4, 5):", value="")
        
    if st.button("🚀 ক্যালকুলেট ও ভেন ডায়াগ্রাম ড্র করো", key="set_btn"):
        if not set_a_str or not set_b_str:
            st.warning("⚠️ সেট A এবং সেট B উভয়ের উপাদান ইনপুট দাও!")
        else:
            try:
                set_A = set([x.strip() for x in set_a_str.split(",") if x.strip()])
                set_B = set([x.strip() for x in set_b_str.split(",") if x.strip()])
                
                union_set = set_A.union(set_B)
                inter_set = set_A.intersection(set_B)
                diff_A_B = set_A.difference(set_B)
                diff_B_A = set_B.difference(set_A)
                
                st.balloons()
                st.success("🎉 সেট অপারেশন এবং ভেন ডায়াগ্রাম জেনারেশন সফল হয়েছে!")
                
                # ভেন ডায়াগ্রাম ড্রয়িং লজিক
                fig, ax = plt.subplots(figsize=(5, 3.5))
                v = venn2(subsets=(len(diff_A_B), len(diff_B_A), len(inter_set)), set_labels=('Set A', 'Set B'), ax=ax)
                
                # লাইভ ডেটা লেবেল হ্যান্ডলিং
                if v.get_label_by_id('10'): v.get_label_by_id('10').set_text(", ".join(list(diff_A_B)) if diff_A_B else "Ø")
                if v.get_label_by_id('01'): v.get_label_by_id('01').set_text(", ".join(list(diff_B_A)) if diff_B_A else "Ø")
                if v.get_label_by_id('11'): v.get_label_by_id('11').set_text(", ".join(list(inter_set)) if inter_set else "Ø")
                
                plt.title("Live Generated Venn Diagram", fontsize=10, color="#4f46e5", weight="bold")
                st.pyplot(fig)
                
                with st.container(border=True):
                    st.markdown("### 🎯 Mathematical Output")
                    st.write(f"✅ **Union ($A \\cup B$):** `{union_set if union_set else 'Ø'}`")
                    st.write(f"✅ **Intersection ($A \\cap B$):** `{inter_set if inter_set else 'Ø'}`")
                    st.write(f"✅ **Difference ($A - B$):** `{diff_A_B if diff_A_B else 'Ø'}`")
            except Exception as e:
                st.error(f"❌ সেট ইনপুট প্রসেস করতে সমস্যা হয়েছে। এরর: {e}")

st.write("---")

# 🧠 ৫. ফুল-ডাইনামিক ইনফিনিট কুইজ ইঞ্জিন (প্রশ্ন ও ভ্যালু প্রতিবার স্ক্র্যাচ থেকে চেঞ্জ হবে)
st.subheader("🧠 Infinitely Variable Discrete Math Quiz")
st.caption("💡 এই সেকশনের প্রশ্ন ও গাণিতিক ডেটা সম্পূর্ণ ডাইনামিক। 'রিসেট/চেঞ্জ করো' বাটনে চাপ দিলে সম্পূর্ণ নতুন ডেটা তৈরি হবে।")

if 'quiz_seed' not in st.session_state or st.sidebar.button("🔄 কুইজের প্রশ্নসমূহ সম্পূর্ণ চেঞ্জ করো"):
    st.session_state.quiz_seed = random.randint(1, 9999)
    st.session_state.current_q = 0
    st.session_state.topic_scores = {"Logic & Sets": 0, "Counting & Probability": 0}
    st.session_state.quiz_complete = False

# সিড ব্যবহার করে ডাইনামিক মান তৈরি
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
        "question": f"৩. {perm_elements} জন প্রতিযোগীকে একটি গোল টেবিলে কত উপায়ে বিন্যস্ত (Circular Permutation) করা সম্ভব?",
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
    
    if st.button("উত্তর লক করো এবং এগিয়ে যাও ➡️"):
        sel_idx = q_bank[q_idx]['options'].index(user_ans)
        if sel_idx == q_bank[q_idx]['correct']:
            st.session_state.topic_scores[cur_topic] += 1
            st.toast("🎉 সঠিক উত্তর হয়েছে!", icon="✅")
        else:
            st.toast("❌ ভুল উত্তর!", icon="🚨")
            
        if q_idx + 1 < 4:
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.session_state.quiz_complete = True
            st.rerun()
else:
    st.success("🎉 চমৎকার! তুমি ডাইনামিক কুইজ পরীক্ষাটি সম্পন্ন করেছ।")
    total_score = sum(st.session_state.topic_scores.values())
    
    with st.container(border=True):
        st.markdown("### 📊 Performance Analytics Report")
        st.write(f"**অর্জিত মোট স্কোর:** `{total_score}` / `4`")
        st.write("---")
        for t_name, score in st.session_state.topic_scores.items():
            st.write(f"🔹 **{t_name}:** `{score}/2` সফলভাবে সম্পন্ন হয়েছে।")
        st.write("---")
        if total_score == 4: st.info("🏅 রিমার্ক: অসামান্য পারফরম্যান্স! তোমার ডিসক্রিট ম্যাথ বেসিকস অত্যন্ত শক্তিশালী।")
        else: st.warning("📚 রিমার্ক: ভালো চেষ্টা! ল্যাব ফাইনালের জন্য টপিকগুলো আর একবার রিভিশন দাও।")
        
    if st.button("🔄 নতুন প্রশ্ন সেটে আবার পরীক্ষা দাও"):
        st.session_state.quiz_seed = random.randint(1, 9999)
        st.session_state.current_q = 0
        st.session_state.topic_scores = {"Logic & Sets": 0, "Counting & Probability": 0}
        st.session_state.quiz_complete = False
        st.rerun()

st.write("---")
st.caption("Developed by MD FAZLE RABBI SOHAN | PU CSE Innovation Lab")
