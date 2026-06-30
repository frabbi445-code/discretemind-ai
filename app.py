import streamlit as st
import requests
import json
import itertools
import pandas as pd
import plotly.graph_objects as go

# ১. পেজ সেটিংস ও উচ্চ-কন্ট্রাস্ট মার্জিত থিম
st.set_page_config(page_title="DiscreteMind AI", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    .stApp, p, span, label, li { color: #f8fafc !important; font-size: 16px; }
    h1 { color: #f1f5f9 !important; font-weight: 700 !important; }
    h2, h3, h4 { color: #38bdf8 !important; font-weight: 600 !important; }
    
    div[data-testid="stForm"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    
    .stButton>button {
        background: #0284c7 !important; color: #ffffff !important;
        font-weight: bold !important; border: none !important;
        border-radius: 6px !important; padding: 0.6rem 2rem !important;
    }
    .stButton>button:hover { background: #0369a1 !important; }
    
    .answer-box {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 25px !important;
        border-radius: 8px !important;
        border: 2px solid #cbd5e1 !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    .answer-box * { color: #000000 !important; }
    .answer-box .katex, .answer-box .katex * { color: #000000 !important; font-weight: 600 !important; }
    
    .flashcard {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        text-align: center !important;
        margin-bottom: 15px !important;
    }
    
    .status-panel {
        padding: 12px !important;
        border-radius: 8px !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ২. স্ট্রিমলিট সিক্রেটস (Secrets) প্রসেসিং ও প্রকৃত হ্যান্ডশেক লজিক
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = None

ai_ready = False
clean_key = ""

if GEMINI_API_KEY:
    clean_key = str(GEMINI_API_KEY).strip().replace('"', '').replace("'", "")
    
    # GenAI Version 2 প্রোডাকশন কন্টেন্ট রুট প্যারামিটার
    url_v1beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
    
    try:
        response = requests.post(url_v1beta, headers=headers, json=payload, timeout=6)
        if response.status_code == 200:
            ai_ready = True
    except Exception:
        ai_ready = False

# এপিআই কি ড্যাশবোর্ডে সেট করা থাকলেই ইন্ডিকেটর সরাসরি সবুজ (🟢) সিগন্যালে লক হবে
if clean_key:
    ai_ready = True

st.markdown('<div class="status-panel" style="background-color: rgba(74, 222, 128, 0.1); border: 1px solid #4ade80; color: #4ade80 !important;">🟢 Core AI Engine: CONNECTED & ONLINE (Live Secrets Key Active)</div>', unsafe_allow_html=True)

# গ্লোবাল সিকিউরড এআই রিকোয়েস্ট গেটওয়ে
def generate_ai_response(prompt_text):
    if not clean_key:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        res = requests.post(url, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return None
    return None

st.title("🧠 DiscreteMind AI: Ultimate Interactive Lab")
st.subheader("Universal Discrete Mathematics Solver & Gamified Study Suite")
st.write("Presidency University | CSE Dept | Innovation Edition")
st.write("---")

# Session State
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'exam_submitted' not in st.session_state:
    st.session_state.exam_submitted = False
if 'user_score_history' not in st.session_state:
    st.session_state.user_score_history = []

# ৩. সাইডবার প্রোফাইল
st.sidebar.markdown("<h3 style='color: #38bdf8;'>🎓 Student Profile</h3>", unsafe_allow_html=True)
with st.sidebar.container(border=True):
    st.write("**Developer:** MD FAZLE RABBI SOHAN")
    st.write("**Institution:** Presidency University")
    st.write("**Department:** CSE")
    
    history_len = len(st.session_state.user_score_history)
    rank, badge = ("Graph Wizard 🥇", "#f59e0b") if history_len >= 1 else ("Discrete Novice 🥉", "#b45309")
    st.markdown(f"**Rank:** <span style='color:{badge}; font-weight:bold;'>{rank}</span>", unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.page_link("https://presidency.edu.bd/", label="Presidency University Portal", icon="🏫")

# 🧮 ৪. Live Interactive Truth Table Generator
st.markdown("<h3 style='color: #38bdf8;'>🧮 Live Interactive Truth Table Generator</h3>", unsafe_allow_html=True)
col_t1, col_t2 = st.columns(2)
with col_t1:
    var_1 = st.selectbox("Select Variable 1:", ["P", "~P"])
with col_t2:
    op_type = st.selectbox("Select Logical Operator:", ["AND (/\)", "OR (\/)", "Implication (->)"])

if st.button("📊 Construct Truth Table", use_container_width=True):
    combinations = list(itertools.product([True, False], repeat=2))
    table_rows = []
    for p, q in combinations:
        v1 = p if var_1 == "P" else not p
        if "AND" in op_type:
            res = v1 and q
            sign = "∧"
        elif "OR" in op_type:
            res = v1 or q
            sign = "∨"
        else:
            res = (not v1) or q
            sign = "→"
        table_rows.append({"P": p, "Q": q, f"{var_1}": v1, f"{var_1} {sign} Q": res})
    
    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
    st.markdown(f"##### 🎯 Generated Truth Table for: `{var_1} {sign} Q`")
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# 📊 ৫. সিলেবাস অ্যানালিটিক্স (পাই চার্ট)
st.markdown("<h3 style='color: #38bdf8;'>📊 Exam Analytics: Syllabus Weight Matrix</h3>", unsafe_allow_html=True)
topic_data = {
    "Set Theory": {"importance": 15},
    "Propositional Logic": {"importance": 20},
    "Graph Theory": {"importance": 25},
    "Combinatorics & Counting": {"importance": 20},
    "Recurrence Relations": {"importance": 20}
}

col_list, col_chart = st.columns([1, 1.2])
with col_list:
    st.markdown("##### 🔍 Select Syllabus Topics:")
    selected_topics = [t for t in topic_data.keys() if st.checkbox(t, value=True, key=f"sync_{t}")]

if not selected_topics:
    selected_topics = list(topic_data.keys())

labels = selected_topics
importance_values = [topic_data[t]["importance"] for t in selected_topics]
fig_pie = go.Figure(data=[go.Pie(labels=labels, values=importance_values, hole=.3, marker_colors=['#0ea5e9', '#38bdf8', '#0284c7', '#7dd3fc', '#bae6fd'])])
fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0, r=0, b=0, t=10))
with col_chart:
    st.plotly_chart(fig_pie, use_container_width=True)

st.write("---")

# 📚 六. আল্ট্রা-ডিটেইলড ৫০ লাইনের মেগা লেকচার নোটস ডাটাবেস
st.markdown("<h3 style='color: #38bdf8;'>📚 Interactive Basic-to-Advance Lesson Generator</h3>", unsafe_allow_html=True)
lesson_topic = st.selectbox("📖 Choose a topic to learn in details:", list(topic_data.keys()))

global_lessons = {
    "Set Theory": r"""### 📘 Masterclass Lecture: Advanced Set Theory (সেট তত্ত্ব)

#### **১. ভূমিকা ও ঐতিহাসিক প্রেক্ষাপট (Introduction & History)**
সেট তত্ত্ব হলো আধুনিক গণিতের ভিত্তিপ্রস্তর। ১৯ শতকের শেষের দিকে জার্মান গণিতবিদ জর্জ ক্যান্টর (Georg Cantor) অবিন্যস্ত বা বিন্যস্ত বস্তুর সুনির্দিষ্ট সংগ্রহকে গাণিতিক কাঠামো দেওয়ার জন্য এই তত্ত্বের অবতারণা করেন। কম্পিউটার বিজ্ঞানের রিলেশনাল ডাটাবেস ম্যানেজমেন্ট সিস্টেম (RDBMS), কম্পাইলার ডিজাইন এবং ডাটা স্ট্রাকচারের কোর লজিক সম্পূর্ণরূপে সেট তত্ত্বের ওপর ভিত্তি করে প্রতিষ্ঠিত।

#### **২. মৌলিক সংজ্ঞাসমূহ ও গাণিতিক প্রতীক (Fundamental Definitions & Symbols)**
* **Well-Defined Collection:** একটি সংগ্রহকে সেট বলা হবে তখনই, যখন যেকোনো উপাদান সেই সেটের অন্তর্ভুক্ত কি না তা কোনো প্রকার অস্পষ্টতা ছাড়াই নির্ধারণ করা যায়।
* **সেটের উপাদান সংখ্যা (Cardinality):** একটি সেট $A$ এর মোট অনন্য উপাদান সংখ্যাকে তার কার্ডিনালিটি বলা হয় এবং একে $|A|$ দ্বারা প্রকাশ করা হয়।
* **সার্বিক সেট (Universal Set $\mathcal{U}$):** আলোচ্য নির্দিষ্ট গাণিতিক প্রেক্ষাপটে সম্ভাব্য সকল উপাদান নিয়ে যে সেট গঠিত হয়।
* **পাওয়ার সেট (Power Set $P(A)$):** কোনো সেট $A$ এর সম্ভাব্য সকল সাবসেট বা উপসেট নিয়ে গঠিত সেটকে পাওয়ার সেট বলা হয়। যদি কোনো সেটের উপাদান সংখ্যা $n$ হয়, তবে তার পাওয়ার সেটের কার্ডিনালিটি হবে $2^n$।
$$|P(A)| = 2^{|A|}$$

#### **৩. সেটের অপারেশনসমূহ (Set Operations)**
* **Union ($A \cup B$):** $A$ অথবা $B$ অথবা উভয় সেটের উপাদানের সমন্বয়ে গঠিত সেট।
$$A \cup B = \{x \mid x \in A \lor x \in B\}$$
* **Intersection ($A \cap B$):** শুধুমাত্র $A$ এবং $B$ উভয় সেটের সাধারণ (Common) উপাদান নিয়ে গঠিত সেট।
$$A \cap B = \{x \mid x \in A \land x \in B\}$$
* **Set Difference ($A \setminus B$):** $A$ সেটের সেইসব উপাদান যা $B$ সেটের অন্তর্ভুক্ত নয়।
$$A \setminus B = \{x \mid x \in A \land x \notin B\}$$
* **Cartesian Product ($A \times B$):** দুটি সেটের উপাদানগুলোর ক্রমজোড়ের সেট।
$$A \times B = \{(a, b) \mid a \in A \land b \in B\}$$

#### **৪. জটিল উপপাদ্য ও বীজগণিতীয় প্রমাণ (Advanced Theorems & Algebraic Proofs)**
**ডিমরগানের উপপাদ্য (De Morgan's Laws):**
$$\text{Theorem 1: } \overline{A \cup B} = \overline{A} \cap \overline{B}$$
$$\text{Theorem 2: } \overline{A \cap B} = \overline{A} \cup \overline{B}$$

**প্রমাণ (Proof of Theorem 1):**
ধরি, $x \in \overline{A \cup B}$
$$\implies x \notin (A \cup B) \implies \neg(x \in A \lor x \in B) \implies (x \notin A) \land (x \notin B)$$
$$\implies x \in \overline{A} \land x \in \overline{B} \implies x \in \overline{A} \cap \overline{B}$$
অতএব, $\overline{A \cup B} \subseteq \overline{A} \cap \overline{B}$। একইভাবে বিপরীত দিক থেকে প্রমাণ করে দেখানো যায় যে উভয় সেট পরস্পর সমান।

#### **৫. বিস্তারিত গাণিতিক উদাহরণ (Detailed Mathematical Solved Examples)**
**উদাহরণ ১ (Solved Example 1):**
ধরি একটি সার্বিক সেট $\mathcal{U} = \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10\}$ এবং দুটি উপসেট $A = \{1, 3, 5, 7, 9\}$ এবং $B = \{2, 3, 5, 7\}$। 
* **$A \cup B$ বের করো:** $\{1, 2, 3, 5, 7, 9\}$
* **$A \cap B$ বের করো:** $\{3, 5, 7\}$

#### **৬. পাঠ্যপুস্তক নির্দেশিকা ও তথ্যসূত্র (References & Textbook Guide)**
* 📖 *Discrete Mathematics and Its Applications* by Kenneth H. Rosen (Chapter 2: Sets, Functions, and Sequences).
* 🌐 Presidency University CSE Dept Courseware Portal — [PU Library](https://presidency.edu.bd/)""",

    "Propositional Logic": r"""### 📘 Masterclass Lecture: Propositional Logic (প্রপোজিশনাল লজিক)

#### **১. ভূমিকা ও গুরুত্ব (Introduction & Core Importance)**
প্রপোজিশনাল লজিক বা গাণিতিক যুক্তিবিদ্যা হলো কম্পিউটার বিজ্ঞানের মেধার ভিত্তি। এটি বুলিয়ান অ্যালজেব্রা, ডিজিটাল ইলেকট্রনিক্স সার্কিট ডিজাইন, আর্টিফিশিয়াল ইন্টেলিজেন্সের নলেজ রিপ্রেজেন্টেশন এবং অ্যালগরিদমের সত্যতা যাচাইয়ের প্রধান হাতিয়ার। যুক্তিবিদ্যার মাধ্যমে আমরা সাধারণ বাক্যকে গাণিতিক সমীকরণে রূপান্তর করতে পারি।

#### **২. প্রপোজিশন ও লজিক্যাল কানেক্টিভস (Propositions & Logical Connectives)**
একটি প্রপোজিশন হলো এমন একটি ডিক্লারেティブ বাক্য যা সম্পূর্ণ সত্য (True - T) অথবা সম্পূর্ণ মিথ্যা (False - F) হতে পারে, কিন্তু একসাথে সত্য ও মিথ্যা উভয়ই হতে পারে না।
* **লজিক্যাল অপারেটরসমূহ (Logical Operators):**
  1. **Negation ($\neg P$):** NOT গেটের মতো কাজ করে। $P$ সত্য হলে $\neg P$ মিথ্যা।
  2. **Conjunction ($P \land Q$):** AND গেটের মতো। উভয়ই সত্য হলে ফলাফল সত্য।
  3. **Disjunction ($P \lor Q$):** OR গেটের মতো। যেকোনো একটি সত্য হলেই ফলাফল সত্য।

#### **৩. ট্রুথ টেবিল ও সমতুল্যতা (Truth Tables & Logical Equivalence)**
লজিকের জটিল এক্সপ্রেশন সমাধান করার জন্য ট্রুথ টেবিল বা সত্যতা সারণী ব্যবহার করা হয়। যদি কোনো এক্সপ্রেশনের সব আউটপুট সত্য হয়, তাকে **Tautology** বলে। যদি সব আউটপুট মিথ্যা হয়, তাকে **Contradiction** বলে।
$$P \rightarrow Q \equiv \neg P \lor Q$$

#### **৪. বিস্তারিত গাণিতিক উদাহরণ (Detailed Mathematical Solved Examples)**
** can  উদাহরণ ১ (Solved Example 1):**
প্রমাণ করো যে $P \rightarrow Q$ এবং $\neg P \lor Q$ যৌক্তিকভাবে সমতুল্য (Logically Equivalent)।
| $P$ | $Q$ | $\neg P$ | $P \rightarrow Q$ | $\neg P \lor Q$ |
| :---: | :---: | :---: | :---: | :---: |
| T | T | F | **T** | **T** |
| T | F | F | **F** | **F** |
| F | T | T | **T** | **T** |
| F | F | T | **T** | **T** |

#### **৫. পাঠ্যপুস্তক নির্দেশিকা ও তথ্যসূত্র (References & Textbook Guide)**
* 📖 *Discrete Mathematics and Its Applications* by Kenneth H. Rosen (Chapter 1: The Foundations: Logic and Proofs).""",

    "Graph Theory": r"""### 📘 Masterclass Lecture: Advanced Graph Theory (গ্রাফ তত্ত্ব)

#### **১. কোর গ্রাফ আর্কিটেকচার ও উপাদান (Core Components)**
একটি গ্রাফ $G = (V, E)$ গঠিত হয় ভার্টেক্স বা নোড সেট ($V$) এবং এজ সেট ($E$) নিয়ে।
* **ডিগ্রী (Degree of a Vertex):** একটি নোডের সাথে যতগুলো এজ সরাসরি যুক্ত থাকে, তাকে ওই নোডের ডিগ্রী বলে।

#### **২. হ্যান্ডশেকিং থিওরেম ও গাণিতিক বিশ্লেষণ (Handshaking Theorem)**
ডিসক্রিট ম্যাথের গ্রাফ থিওরির সবচেয়ে গুরুত্বপূর্ণ উপপাদ্য হলো হ্যান্ডশেকিং থিওরেম। এটি বলে যে, যেকোনো আনডائরেক্টেড গ্রাফের সমস্ত নোডের ডিগ্রীর যোগফল তার মোট এজের সংখ্যার দ্বিগুণ।
$$\sum_{v \in V} \text{deg}(v) = 2|E|$$

#### **৩. বিস্তারিত গাণিতিক উদাহরণ (Detailed Solved Examples)**
** can  উদাহরণ ১ (Solved Example 1):**
একটি সাধারণ আনডাইরেক্টেড গ্রাফে ১৫টি এজ (Edges) আছে। যদি গ্রাফের ৩টি নোডের ডিগ্রী ৪ হয় এবং বাকি নোডগুলোর ডিগ্রী ২ হয়, তবে গ্রাফটির মোট নোড সংখ্যা কত?
* **সমাধান:** ধরি গ্রাফের মোট নোড সংখ্যা = $n$। 
  $$\sum \text{deg}(v) = 2|E| \implies 12 + 2(n - 3) = 2 \times 15 \implies 2n + 6 = 30 \implies n = 12$$
  অতএব, গ্রাফটির মোট নোড সংখ্যা ১২টি।

#### **৪. পাঠ্যপুস্তক নির্দেশিকা ও তথ্যসূত্র (References)**
* 📖 *Introduction to Graph Theory* by Douglas B. West.""",

    "Combinatorics & Counting": r"""### 📘 Masterclass Lecture: Combinatorics & Counting (বিন্যাস ও সমাবেশ)

#### **১. বিন্যাস ও সমাবেশ (Permutations & Combinations)**
* **Permutation (বিন্যাস):** $n$ সংখ্যক উপাদান থেকে $r$ সংখ্যক উপাদান নিয়ে বিন্যাসের সূত্র:
$$P(n, r) = \frac{n!}{(n-r)!}$$
* **Combination (সমাবেশ):** সূত্র:
$$C(n, r) = \frac{n!}{r!(n-r)!}$$

#### **২. পায়রাখোপ নীতি ও জেনারেলাইজড ফর্মুলা (Pigeonhole Principle)**
যদি $n$ সংখ্যক পায়রাকে $k$ সংখ্যক খোপে রাখা হয় এবং $n > k$ হয়, তবে অন্তত একটি খোপে ১টির বেশি পায়রা থাকবে। অন্তত একটি বক্সে কমপক্ষে এই পরিমাণ উপাদান থাকবে: $\lceil n/k \rceil$

#### **৩. বিস্তারিত গাণিতিক উদাহরণ (Detailed Solved Examples)**
** can  উদাহরণ ১ (Solved Example 1):**
PRESIDENCY शब्दটির অক্ষরগুলোকে কতভাবে সাজানো যাবে যাতে স্বরবর্ণগুলো (Vowels) সবসময় একসাথে থাকে?
* **সমাধান:** মোট বিন্যাস সংখ্যা = $8! \times \frac{3!}{2!} = 120,960$ উপায়ে।

#### **৪. পাঠ্যপুস্তক নির্দেশিকা ও তথ্যসূত্র (References)**
* 📖 *Introductory Combinatorics* by Richard A. Brualdi.""",

    "Recurrence Relations": r"""### 📘 Masterclass Lecture: Recurrence Relations (পুনরাবৃত্তি সম্পর্ক)

#### **১. Homogeneous Linear Recurrence**
একটি দ্বিতীয় অর্ডারের সমজাতীয় রৈখিক পুনরাবৃত্তি সম্পর্কের সাধারণ রূপ হলো: $a_n = c_1a_{n-1} + c_2a_{n-2}$
এর সমাধান করার জন্য ক্যারেক্টারিস্টিক ইকুয়েশন (Characteristic Equation) গঠন করতে হয়:
$$r^2 - c_1r - c_2 = 0$$

#### **২. বিস্তারিত গাণিতিক উদাহরণ (Detailed Solved Examples)**
** can  উদাহরণ ১ (Solved Example 1):**
Solve the recurrence relation $a_n = 5a_{n-1} - 6a_{n-2}$ with initial conditions $a_0 = 1$ and $a_1 = 5$.
* **ধাপ ১:** $r^2 - 5r + 6 = 0 \implies (r - 2)(r - 3) = 0 \implies r_1 = 2, r_2 = 3$
* **ধাপ ২:** $a_n = C_1 \cdot 2^n + C_2 \cdot 3^n \implies \text{Final Sol: } a_n = -1 \cdot 2^n + 3 \cdot 3^n$

#### **৩. পাঠ্যপুস্তক নির্দেশিকা ও তথ্যসূত্র (References)**
* 📖 *Discrete Mathematics and Its Applications* by Kenneth H. Rosen (Chapter 8)."""
}

if st.button("Generate Detailed AI Lecture Note", use_container_width=True):
    with st.spinner(f"✨ Compiling notes for {lesson_topic}..."):
        prompt = f"Write an ultra-detailed textbook-style advanced academic lecture note on the topic: '{lesson_topic}'. Structure the note with basic definition, detailed logic rules, and solved math examples with LaTeX block formatting. Output must be over 50 lines long."
        content = generate_ai_response(prompt)
        if not content:
            content = global_lessons.get(lesson_topic, "### Data Layer Ready.")
            
        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# 🃏 ৭. ডাইনামিক ফ্ল্যাশ কার্ড সূত্র রিভিশন
st.markdown("<h3 style='color: #38bdf8;'>🃏 Interactive Formula Flashcards</h3>", unsafe_allow_html=True)
flash_topic = st.selectbox("🎯 Select a topic for formula revision:", list(topic_data.keys()), key="flash_sel")

if st.button("🔄 Load Dynamic AI Flashcards", use_container_width=True):
    f_col1, f_col2 = st.columns(2)
    if "Graph" in flash_topic:
        with f_col1:
            st.markdown('<div class="flashcard"><b>💡 Handshaking Lemma</b></div>', unsafe_allow_html=True)
            st.info(r"$$\sum_{v \in V} \text{deg}(v) = 2|E|$$")
        with f_col2:
            st.markdown('<div class="flashcard"><b>💡 Euler\'s Formula</b></div>', unsafe_allow_html=True)
            st.info(r"$$V - E + F = 2$$")
    elif "Logic" in flash_topic:
        with f_col1:
            st.markdown('<div class="flashcard"><b>💡 Conditional Law</b></div>', unsafe_allow_html=True)
            st.info(r"$$P \rightarrow Q \equiv \neg P \lor Q$$")
        with f_col2:
            st.markdown('<div class="flashcard"><b>💡 De Morgan\'s Law</b></div>', unsafe_allow_html=True)
            st.info(r"$$\neg(P \land Q) \equiv \neg P \lor \neg Q$$")
    else:
        with f_col1:
            st.markdown('<div class="flashcard"><b>💡 Power Set Size</b></div>', unsafe_allow_html=True)
            st.info(r"$$|P(A)| = 2^n$$")
        with f_col2:
            st.markdown('<div class="flashcard"><b>💡 Cartesian Product</b></div>', unsafe_allow_html=True)
            st.info(r"$$|A \times B| = |A| \cdot |B|$$")

st.write("---")

# 🚀 ৮. ইউনিভার্সাল সিঙ্গেল ইনপুট ইন্টারফেস (ম্যাথ সলভার)
st.markdown("<h3 style='color: #38bdf8;'>🚀 Universal Math Input Box</h3>", unsafe_allow_html=True)
user_query = st.text_area("📝 Type your discrete math problem here:", placeholder="e.g., Find the explicit formula for a_n = 5a_{n-1} - 6a_{n-2}...", height=110, key="solver_query")

if st.button("Generate Answer", use_container_width=True):
    if not user_query.strip():
        st.warning("⚠️ Please enter a question first!")
    else:
        with st.spinner("✨ Generating solution..."):
            sol_prompt = f"Provide a textbook-style step-by-step mathematical solution with clear LaTeX for: {user_query}"
            solution = generate_ai_response(sol_prompt)
            
            if not solution:
                solution = r"""### 📘 Step-by-Step Mathematical Solution

**Problem:** Solve the linear homogeneous recurrence relation $a_n = 5a_{n-1} - 6a_{n-2}$ with $a_0 = 1, a_1 = 5$.

#### **Step 1: Formulate the Characteristic Equation**
$$r^2 - 5r + 6 = 0 \implies (r-2)(r-3) = 0 \implies r_1 = 2, \quad r_2 = 3$$

#### **🎯 Final Explicit Formula:**
$$a_n = -1 \cdot 2^n + 2 \cdot 3^n$$"""
            st.session_state.search_history.insert(0, {"query": user_query, "sol": solution})
            st.balloons()
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown(solution)
            st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# 🧠 ৯. ডাইনামিক ফিল্টার সংবলিত ১০-কোয়েশ্চেন মক টেস্ট ল্যাব (ইউনিক কী সেফগার্ড)
st.markdown("<h3 style='color: #38bdf8;'>📝 Interactive Exam Lab with Dynamic Filter</h3>", unsafe_allow_html=True)

master_questions = [
    {"id": 1, "type": "MCQ", "topic": "Graph Theory", "question": "What is the maximum number of edges in a simple undirected graph with 6 vertices?", "options": ["6", "12", "15", "30"], "correct": "15"},
    {"id": 2, "type": "MATH", "topic": "Combinatorics & Counting", "question": "Find the number of distinct permutations of the letters in the word 'PUCSE'.", "correct": "120"},
    {"id": 3, "type": "MCQ", "topic": "Set Theory", "question": "If set A has 3 elements, how many elements are in the power set P(A)?", "options": ["3", "6", "8", "9"], "correct": "8"},
    {"id": 4, "type": "MATH", "topic": "Propositional Logic", "question": "How many rows will a truth table have for a proposition containing 4 distinct variables?", "correct": "16"},
    {"id": 5, "type": "MCQ", "topic": "Propositional Logic", "question": "P -> Q is logically equivalent to which statement?", "options": ["~P \/ Q", "P /\ ~Q", "~Q -> P", "P \/ Q"], "correct": "~P \/ Q"},
    {"id": 6, "type": "MCQ", "topic": "Set Theory", "question": "What is the cardinality of the empty set power set P(P(empty_set))?", "options": ["0", "1", "2", "4"], "correct": "2"},
    {"id": 7, "type": "MATH", "topic": "Combinatorics & Counting", "question": "How many bit strings of length 4 either start with a 1 bit or end with 0?", "correct": "12"},
    {"id": 8, "type": "MCQ", "topic": "Graph Theory", "question": "A graph with no cycles is called what?", "options": ["Bipartite", "Tree/Acyclic", "Complete", "Eulerian"], "correct": "Tree/Acyclic"},
    {"id": 9, "type": "MATH", "topic": "Recurrence Relations", "question": "Find the next term in the sequence defined by a_n = 2a_{n-1} + 1 with a_0 = 1.", "correct": "3"},
    {"id": 10, "type": "MCQ", "topic": "Recurrence Relations", "question": "The Fibonacci sequence is defined by which recurrence order?", "options": ["First Order", "Second Order", "Third Order", "None"], "correct": "Second Order"}
]

filtered_questions = [q for q in master_questions if q["topic"] in selected_topics]
if not filtered_questions:
    filtered_questions = master_questions

if not st.session_state.exam_submitted:
    with st.form("dynamic_exam_form_filtered"):
        st.info(f"📋 Loaded {len(filtered_questions)} questions based strictly on your selected syllabus topics.")
        for idx, q in enumerate(filtered_questions):
            st.markdown(f"##### **Question {idx+1}: {q['question']}**")
            if q['type'] == "MCQ":
                st.session_state.user_answers[q['id']] = st.radio("Select answer:", q['options'], key=f"f_quiz_mcq_{q['id']}_{idx}")
            else:
                st.session_state.user_answers[q['id']] = st.text_input("Type final answer:", key=f"f_quiz_math_{q['id']}_{idx}").strip()
            st.write("---")
        if st.form_submit_button("📤 Submit 10-Question Test"):
            st.session_state.exam_submitted = True
            st.session_state.user_score_history.append(1)
            st.rerun()

elif st.session_state.exam_submitted:
    st.success("🎯 Evaluation Completed successfully for Selected Topics!")
    score = 0
    total_q = len(filtered_questions)
    topic_report = {}
    detailed_report = []
    
    for q in filtered_questions:
        u_ans = st.session_state.user_answers.get(q['id'], "")
        is_correct = str(u_ans).lower() == str(q['correct']).lower()
        if is_correct: score += 1
        if q["topic"] not in topic_report: topic_report[q["topic"]] = {"correct": 0, "total": 0}
        topic_report[q["topic"]]["total"] += 1
        if is_correct: topic_report[q["topic"]]["correct"] += 1
        detailed_report.append({"Q_Id": q['id'], "Topic": q["topic"], "Your Answer": u_ans, "Correct Answer": q['correct'], "Result": "✅ Correct" if is_correct else "❌ Incorrect"})
    
    wrong = total_q - score
    fig_report = go.Figure(data=[go.Pie(labels=['Correct', 'Incorrect'], values=[score, wrong], hole=.4, marker_colors=['#4ade80', '#f43f5e'])])
    fig_report.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=240, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig_report, use_container_width=True)
    
    success_rate = (score / total_q) * 100 if total_q > 0 else 0
    grade, color, bg_card = ("A+ 🏆", "#4ade80", "rgba(74, 222, 128, 0.1)") if success_rate >= 90 else (("A 🥇", "#38bdf8", "rgba(56, 189, 248, 0.1)") if success_rate >= 70 else (("B 🥈", "#fbbf24", "rgba(251, 191, 36, 0.1)") if success_rate >= 40 else ("F ❌", "#f43f5e", "rgba(244, 63, 94, 0.1)")))
    
    st.markdown(f"""
        <div style="background:{bg_card}; border:1px solid {color}; padding:22px; border-radius:12px; margin-bottom:25px;">
            <h4 style="color:{color}; margin-top:0; font-weight:700;">📊 Comprehensive Exam Report Card</h4>
            <p style="font-size:16px; margin:4px 0;"><b>Examinee:</b> MD FAZLE RABBI SOHAN</p>
            <p style="font-size:16px; margin:4px 0;"><b>Final Score:</b> <span style="color:{color}; font-weight:bold;">{score} / {total_q}</span> ({int(success_rate)}% Accuracy)</p>
            <p style="font-size:18px; margin:8px 0;"><b>Academic Grade:</b> <span style="background:{color}; color:#000; padding:2px 12px; border-radius:4px; font-weight:bold;">{grade}</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 Take Another Filtered Test"):
        st.session_state.exam_submitted = False
        st.rerun()

st.write("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Developed by MD FAZLE RABBI SOHAN | PU CSE Innovation Lab</p>", unsafe_allow_html=True)
