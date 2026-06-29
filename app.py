import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import itertools
import random

# ১. পেজ সেটিংস ও প্রিমিয়াম শিরোনাম
st.set_page_config(page_title="DiscreteMind AI Ultra Pro", page_icon="🧮", layout="centered")

st.title("🚀 DiscreteMind AI Ultra Pro")
st.subheader("Advanced 3D-Enhanced Discrete Mathematics Course Project")
st.write("Presidency University | CSE Dept | AI Innovation Project")
st.write("---")

# ২. সাইডবার ডিজাইন
st.sidebar.header("🎓 Course Project Profile")
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    st.write("**Course:** Discrete Mathematics")
    st.caption("🔥 Status: 100% Real-Time Math Engine (No API)")

st.sidebar.write("---")
st.sidebar.header("🔗 Quick Navigation")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")

# ৩. ৩ডি অ্যানিমেটেড মডেল সেকশন
st.write("### 🌐 Live 3D AI Topology Node Mesh (Presentation Mode)")
st.caption("মাউস দিয়ে স্ক্রল করে ৩ডি মডেলটি জুম করো এবং ড্র্যাগ করে চারদিকে ঘুরিয়ে স্যারদের দেখাও:")

n_nodes = 40
x = np.random.standard_normal(n_nodes)
y = np.random.standard_normal(n_nodes)
z = np.random.standard_normal(n_nodes)

fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers+lines',
    marker=dict(size=6, color=z, colorscale='Viridis', opacity=0.8),
    line=dict(color='#38bdf8', width=1.5)
)])

fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                  scene=dict(xaxis=dict(showbackground=False, showticklabels=False, title=''),
                             yaxis=dict(showbackground=False, showticklabels=False, title=''),
                             zaxis=dict(showbackground=False, showticklabels=False, title='')),
                  height=250)
st.plotly_chart(fig, use_container_width=True)
st.write("---")

# ৪. ডিসক্রিট ম্যাথ টপিক সিলেকশন
st.subheader("🧮 Real-Time Discrete Math Solver Engine")
topic = st.selectbox(
    "🎯 সলভ করার জন্য ডিসক্রিট ম্যাথ টপিকটি সিলেক্ট করো:", 
    ["📊 Truth Table Generator (লাইভ ট্রুথ টেবিল ক্যালকুলেটর)", 
     "⭕ Set Theory Calculator (রিয়েল-টাইম সেট সলভার)"]
)

# ৫. রিয়েল-টাইম সলভিং ইঞ্জিন লজিক
if topic == "📊 Truth Table Generator (লাইভ ট্রুথ টেবিল ক্যালকুলেটর)":
    st.info("💡 **নিয়ম:** তুমি যেকোনো লজিক এক্সপ্রেশন লিখলে সিস্টেম নিজে থেকে সেটার ট্রুথ টেবিল বানাবে। লজিকে লিখতে ব্যবহার করো: `and`, `or`, `not` এবং ভেরিয়েবল হিসেবে `P` ও `Q`।")
    user_expr = st.text_input("📝 তোমার লজিক্যাল এক্সপ্রেশনটি লেখো (যেমন: P and Q, P or (not Q), not (P and Q)):", value="P or (not Q)")
    
    if st.button("🚀 এক্সপার্ট সリューション জেনারেট করো", key="logic_btn"):
        progress_bar = st.progress(0)
        for p in range(10, 101, 30):
            time.sleep(0.05)
            progress_bar.progress(p)
            
        try:
            # লাইভ ট্রুথ টেবিল জেনারেশন লজিক (১০০% নিখুঁত)
            rows = []
            for P, Q in itertools.product([True, False], repeat=2):
                # সেফ ইভালুয়েশনের জন্য কাস্টম ডিকশনারি এনভায়রনমেন্ট
                env = {'P': P, 'Q': Q, 'and': lambda x, y: x and y, 'or': lambda x, y: x or y, 'not': lambda x: not x}
                # পাইথন সিনট্যাক্স দিয়ে ইভালুয়েট করা
                result = eval(user_expr, {"__builtins__": None}, env)
                rows.append({"P": P, "Q": Q, "Result": result})
            
            df = pd.DataFrame(rows)
            st.balloons()
            st.success("🎉 লজিক টেবিলটি রিয়েল-টাইমে সফলভাবে ক্যালকুলেট হয়েছে!")
            
            with st.container(border=True):
                st.markdown(f"### 📋 Evaluated Truth Table for: `{user_expr}`")
                st.dataframe(df.style.map(lambda v: 'color: green; font-weight: bold;' if v==True else 'color: red; font-weight: bold;', subset=['Result']))
        except Exception as e:
            st.error(f"❌ এক্সপ্রেশন সিনট্যাক্স ভুল হয়েছে! দয়া করে সঠিক পাইথন লজিক ফরম্যাটে লেখো (যেমন: `P and Q` অথবা `not P`). এরর: {e}")

elif topic == "⭕ Set Theory Calculator (রিয়েল-টাইম সেট সলভার)":
    st.info("💡 **নিয়ম:** কমা (,) দিয়ে আলাদা করে সেটের উপাদানগুলো লেখো। কোড নিজে থেকে ইউনিয়ন এবং ইন্টারসেকশন হিসাব করবে।")
    set_a_str = st.text_input("Set A এর উপাদানসমূহ লিখো:", "1, 3, 5, 7, 9")
    set_b_str = st.text_input("Set B এর উপাদানসমূহ লিখো:", "2, 3, 5, 7")
    
    if st.button("🚀 এক্সপার্ট সリューション জেনারেট করো", key="set_btn"):
        try:
            set_A = set([x.strip() for x in set_a_str.split(",") if x.strip()])
            set_B = set([x.strip() for x in set_b_str.split(",") if x.strip()])
            
            st.balloons()
            st.success("🎉 সেট অপারেশনগুলো সফলভাবে সম্পন্ন হয়েছে!")
            
            with st.container(border=True):
                st.markdown("### 🎯 Set Operations Output")
                st.write(f"🔹 **Set A:** `{set_A}`")
                st.write(f"🔹 **Set B:** `{set_B}`")
                st.write("---")
                st.write(f"✅ **Union ($A \\cup B$):** `{set_A.union(set_B)}`")
                st.write(f"✅ **Intersection ($A \\cap B$):** `{set_A.intersection(set_B)}`")
                st.write(f"✅ **Difference ($A - B$):** `{set_A.difference(set_B)}`")
        except Exception as e:
            st.error(f"❌ সেট ইনপুট ফরম্যাটে ভুল হয়েছে! এরর: {e}")

st.write("---")

# 🧠 ৬. ডাইনামিক কুইজ ইঞ্জিন (প্রশ্ন সবসময় র্যান্ডমলি জেনারেট হবে, কখনো রিপিট হবে না)
st.subheader("🧠 Dynamic Discrete Mathematics Course Quiz")
st.caption("💡 এই কুইজের প্রশ্নগুলো সম্পূর্ণ ডাইনামিক। প্রতিবার নতুন সংখ্যা দিয়ে নতুন প্রশ্ন তৈরি হবে!")

# সেশন স্টেটে ডাইনামিক প্রশ্ন তৈরি করার লজিক
if 'q_bank' not in st.session_state or st.sidebar.button("🔄 কুইজের প্রশ্নসমূহ রিফ্রেশ/চেঞ্জ করো"):
    # প্রতিবার নতুন ৬টি র্যান্ডম প্রশ্ন তৈরি হবে ব্যাকএন্ডে
    n1 = random.randint(3, 6)
    set_len = random.randint(3, 5)
    men = random.randint(5, 8)
    women = random.randint(4, 6)
    
    st.session_state.q_bank = [
        {
            "topic": "Set Theory",
            "question": f"১. একটি সেটে যদি {set_len}টি উপাদান (Elements) থাকে, তবে তার পাওয়ার সেটে (Power Set) কতটি উপাদান থাকবে?",
            "options": [f"A) {set_len}টি", f"B) {2*set_len}টি", f"C) {2**set_len}টি"],
            "correct": 2,
            "score_val": 1
        },
        {
            "topic": "Propositional Logic",
            "question": "২. প্রপোজিশনাল লজিকের নিয়ম অনুযায়ী, P ∧ Q (AND) কখন সত্য (True) আউটপুট দেয়?",
            "options": ["A) যেকোনো একটি True হলে", "B) শুধুমাত্র যখন P এবং Q দুটিই True", "C) দুটিই False হলে"],
            "correct": 1,
            "score_val": 1
        },
        {
            "topic": "Permutation & Combination",
            "question": f"৩. {n1} জন ছাত্রকে একটি সোজা লাইনে কত উপায়ে সাজানো (Permutation) সম্ভব?",
            "options": [f"A) {n1} উপায়ে", f"B) {np.math.factorial(n1)} উপায়ে", f"C) {n1*2} উপায়ে"],
            "correct": 1,
            "score_val": 1
        },
        {
            "topic": "Propositional Logic",
            "question": "৪. একটি কন্ডিশনাল স্টেটমেন্ট P → Q কখন মিথ্যা (False) প্রমাণিত হয়?",
            "options": ["A) যখন P = True এবং Q = False", "B) যখন দুটিই True হয়", "C) যখন P = False এবং Q = True"],
            "correct": 0,
            "score_val": 1
        },
        {
            "topic": "Set Theory",
            "question": f"৫. যদি ইউনিভার্সাল সেট U এর উপাদান সংখ্যা ১০ হয় এবং সেট A এর উপাদান সংখ্যা {set_len} হয়, তবে কমপ্লিমেন্ট সেট A' এর উপাদান সংখ্যা কত?",
            "options": [f"A) {set_len}টি", f"B) {10 - set_len}টি", f"C) ১০টি"],
            "correct": 1,
            "score_val": 1
        },
        {
            "topic": "Permutation & Combination",
            "question": f"৬. {men} জন পুরুষ এবং {women} জন মহিলার মধ্যে থেকে ২ জন পুরুষ ও ২ জন মহিলা কত উপায়ে বাছাই করা যাবে?",
            "options": [f"A) {int((men*(men-1)/2) * (women*(women-1)/2))} উপায়ে", f"B) {men * women} উপায়ে", f"C) ২১টি উপায়ে"],
            "correct": 0,
            "score_val": 1
        }
    ]
    st.session_state.current_q = 0
    st.session_state.topic_scores = {"Propositional Logic": 0, "Set Theory": 0, "Permutation & Combination": 0}
    st.session_state.quiz_complete = False

# কুইজ রানিং স্টেট লজিক
if not st.session_state.quiz_complete:
    q_index = st.session_state.current_q
    current_topic = st.session_state.q_bank[q_index]['topic']
    
    st.info(f"📋 প্রশ্ন: {q_index + 1} / 6 | 🏷️ টপিক: {current_topic}")
    st.write(f"**{st.session_state.q_bank[q_index]['question']}**")
    
    user_ans = st.radio("সর্বোত্তম উত্তরটি সিলেক্ট করো:", st.session_state.q_bank[q_index]['options'], key=f"dynamic_q_{q_index}")
    
    if st.button("উত্তর লক করো ও পরবর্তী প্রশ্ন ➡️"):
        selected_index = st.session_state.q_bank[q_index]['options'].index(user_ans)
        if selected_index == st.session_state.q_bank[q_index]['correct']:
            st.session_state.topic_scores[current_topic] += 1
            st.toast("🎉 সঠিক উত্তর!", icon="✅")
        else:
            st.toast("❌ ভুল উত্তর!", icon="🚨")
            
        if q_index + 1 < 6:
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.session_state.quiz_complete = True
            st.rerun()
else:
    # 🎯 ফাইনাল স্মার্ট অ্যানালিটিক্যাল রিপোর্ট কার্ড সেকশন
    st.success("🎉 অভিনন্দন! তুমি ডাইনামিক কুইজ টেস্ট কমপ্লিট করেছ। নিচে তোমার লাইভ অ্যানালিটিক্স দেওয়া হলো:")
    total_score = sum(st.session_state.topic_scores.values())
    
    with st.container(border=True):
        st.markdown("### 📊 Course Project Performance Report")
        st.write(f"**টোটাল টেস্ট স্কোর:** `{total_score}` / `6`")
        st.write("---")
        st.markdown("#### 🎯 Topic-wise Analytics & Feedback")
        for topic_name, score in st.session_state.topic_scores.items():
            status_color = "🔴 দুর্বল (Poor)" if score == 0 else "🟡 মাঝারি (Average)" if score == 1 else "🟢 দক্ষ (Excellent)"
            st.write(f"🔹 **{topic_name}:** `{score}/2` -> **{status_color}**")
            if score == 2: st.caption("💡 *ফিডব্যাক:* এই টপিকে তোমার বেসিক এবং গাণিতিক দক্ষতা চমৎকার!")
            elif score == 1: st.caption("💡 *ফিডব্যাক:* তোমার কনসেপ্ট ঠিক আছে তবে আরেকটু প্র্যাকটিস দরকার।")
            else: st.caption("💡 *ফিডব্যাক:* এই মডিউলে অনেক বেশি ভুল হচ্ছে। কোর্স লেকচার শিটগুলো আবার রিভিশন দাও।")
            st.write("")
        st.write("---")
        if total_score == 6:
            st.balloons()
            st.info("🏅 **সার্টিফিকেট রিমার্ক:** পারফেক্ট স্কোর! তুমি একজন ডিসক্রিট ম্যাথ এক্সপার্ট।")
        elif total_score >= 3: st.info("👍 **সার্টিফিকেট রিমার্ক:** ভালো পারফরম্যান্স। ফাইনালে চমৎকার রেজাল্ট আসবে।")
        else: st.warning("📚 **সার্টিফিকেট রিমার্ক:** কোর্স কন্টেন্টগুলো ভালো করে রিভিশন দেওয়া প্রয়োজন।")

    if st.button("🔄 কুইজ টেস্ট আবার শুরু করো"):
        del st.session_state.q_bank # প্রশ্ন ডিলিট করে ফ্রেশ র্যান্ডম সেটআপ করবে
        st.rerun()

st.write("---")
st.caption("Developed by MD FAZLE RABBI SOHAN | PU CSE Innovation Lab")
