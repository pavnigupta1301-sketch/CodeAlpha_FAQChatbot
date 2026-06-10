"""
app.py
------
CodeAlpha AI FAQ Chatbot — Main Streamlit Application

This module implements a full FAQ chatbot that:
  1. Loads FAQ data from faq_data.py
  2. Preprocesses questions using NLTK (lowercase, punctuation removal,
     tokenisation, stopword removal)
  3. Vectorises questions with scikit-learn's TF-IDF Vectorizer
  4. Finds the most similar FAQ using Cosine Similarity
  5. Renders an interactive Streamlit chat UI with history, score display,
     and clear-chat functionality

Author : CodeAlpha Intern
Version: 1.0.0
"""

# ─── Standard Library ─────────────────────────────────────────────────────────
import re
import string
import time

# ─── Third-Party ──────────────────────────────────────────────────────────────
import nltk
import pandas as pd
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── Local ────────────────────────────────────────────────────────────────────
from faq_data import FAQ_DATA

# ──────────────────────────────────────────────────────────────────────────────
# 1.  NLTK RESOURCE DOWNLOAD
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def download_nltk_resources() -> None:
    """Download required NLTK data files (runs once, then cached)."""
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    nltk.download("stopwords", quiet=True)


download_nltk_resources()

# ──────────────────────────────────────────────────────────────────────────────
# 2.  NLP PREPROCESSING
# ──────────────────────────────────────────────────────────────────────────────

def preprocess(text: str) -> str:
    """
    Clean and normalise a text string using NLP preprocessing steps:
      a) Convert to lowercase
      b) Remove punctuation
      c) Tokenise into words
      d) Remove English stop-words

    Parameters
    ----------
    text : str
        Raw input text (a question or FAQ question).

    Returns
    -------
    str
        Space-joined list of clean, meaningful tokens.
    """
    # a) Lowercase
    text = text.lower()

    # b) Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # c) Tokenise
    tokens = word_tokenize(text)

    # d) Remove stop-words
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    return " ".join(tokens)


# ──────────────────────────────────────────────────────────────────────────────
# 3.  VECTOR MODEL (CACHED — BUILT ONCE PER SESSION)
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def build_model():
    """
    Preprocess all FAQ questions and fit a TF-IDF Vectorizer on them.

    Returns
    -------
    tuple
        (tfidf_matrix, vectorizer, faq_df)
        - tfidf_matrix : scipy sparse matrix of shape (n_faqs, n_features)
        - vectorizer   : fitted TfidfVectorizer instance
        - faq_df       : Pandas DataFrame with columns ['question', 'answer',
                          'processed_question']
    """
    faq_df = pd.DataFrame(FAQ_DATA)
    faq_df["processed_question"] = faq_df["question"].apply(preprocess)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(faq_df["processed_question"])

    return tfidf_matrix, vectorizer, faq_df


# ──────────────────────────────────────────────────────────────────────────────
# 4.  ANSWER RETRIEVAL
# ──────────────────────────────────────────────────────────────────────────────

SIMILARITY_THRESHOLD = 0.15   # Minimum cosine similarity to return an answer


def get_answer(user_question: str, tfidf_matrix, vectorizer, faq_df: pd.DataFrame):
    """
    Find the FAQ entry most similar to the user's question.

    Steps
    -----
    1. Preprocess the user question.
    2. Transform it using the fitted TF-IDF vectorizer.
    3. Compute cosine similarity against all FAQ vectors.
    4. Return the best match if score ≥ SIMILARITY_THRESHOLD, else a fallback.

    Parameters
    ----------
    user_question : str
        Raw question string typed by the user.
    tfidf_matrix  : scipy sparse matrix
        Pre-computed TF-IDF matrix for all FAQ questions.
    vectorizer    : TfidfVectorizer
        The fitted vectorizer.
    faq_df        : pd.DataFrame
        DataFrame containing FAQ questions and answers.

    Returns
    -------
    tuple[str, float, str]
        (answer_text, similarity_score, matched_question)
    """
    if not user_question.strip():
        return "Please type a question first!", 0.0, ""

    processed_q = preprocess(user_question)

    # Guard: if preprocessing removes all tokens (e.g. pure punctuation)
    if not processed_q.strip():
        return "I couldn't understand that. Please rephrase your question.", 0.0, ""

    user_vector = vectorizer.transform([processed_q])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    best_idx = similarities.argmax()
    best_score = float(similarities[best_idx])

    if best_score < SIMILARITY_THRESHOLD:
        return (
            "Sorry, I couldn't find a matching answer. "
            "Please try rephrasing or ask another question!",
            best_score,
            "",
        )

    answer = faq_df.iloc[best_idx]["answer"]
    matched_question = faq_df.iloc[best_idx]["question"]
    return answer, best_score, matched_question


# ──────────────────────────────────────────────────────────────────────────────
# 5.  PAGE CONFIG & GLOBAL STYLES
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI FAQ Chatbot | CodeAlpha",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inject custom CSS for a premium dark-themed chat UI
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Page background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* ── Header ── */
    .hero-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .hero-header h1 {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero-header p {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-top: 0;
    }

    /* ── Chat bubbles ── */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem 0;
    }

    .chat-bubble {
        max-width: 82%;
        padding: 0.85rem 1.2rem;
        border-radius: 18px;
        line-height: 1.6;
        font-size: 0.95rem;
        animation: fadeSlideIn 0.3s ease;
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* User bubble — right-aligned */
    .user-bubble-wrapper {
        display: flex;
        justify-content: flex-end;
    }
    .user-bubble {
        background: linear-gradient(135deg, #6d28d9, #4f46e5);
        color: #fff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(109,40,217,0.35);
    }

    /* Bot bubble — left-aligned */
    .bot-bubble-wrapper {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 0.6rem;
    }
    .bot-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .bot-bubble {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        color: #e2e8f0;
        border-bottom-left-radius: 4px;
        backdrop-filter: blur(8px);
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 999px;
        margin-top: 6px;
        font-weight: 600;
    }
    .score-high   { background: rgba(52,211,153,0.18); color: #34d399; border: 1px solid #34d399; }
    .score-medium { background: rgba(251,191,36,0.18);  color: #fbbf24; border: 1px solid #fbbf24; }
    .score-low    { background: rgba(248,113,113,0.18); color: #f87171; border: 1px solid #f87171; }

    /* Matched question label */
    .matched-q {
        font-size: 0.75rem;
        color: #7dd3fc;
        margin-top: 4px;
        font-style: italic;
    }

    /* ── Welcome card ── */
    .welcome-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeSlideIn 0.5s ease;
    }
    .welcome-card h3 {
        color: #a78bfa;
        margin-bottom: 0.4rem;
    }
    .welcome-card p {
        color: #94a3b8;
        font-size: 0.9rem;
        margin: 0;
    }

    /* ── Input row ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.25) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.1) !important; }

    /* ── FAQ example chips ── */
    .faq-chip {
        display: inline-block;
        background: rgba(124,58,237,0.15);
        border: 1px solid rgba(124,58,237,0.4);
        color: #c4b5fd;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        margin: 3px;
        cursor: default;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────────────────
# 6.  SESSION STATE INITIALISATION
# ──────────────────────────────────────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list of dicts: {role, content, score, matched_q}

if "first_visit" not in st.session_state:
    st.session_state.first_visit = True


# ──────────────────────────────────────────────────────────────────────────────
# 7.  BUILD / LOAD MODEL
# ──────────────────────────────────────────────────────────────────────────────

with st.spinner("🔧 Loading NLP model…"):
    tfidf_matrix, vectorizer, faq_df = build_model()


# ──────────────────────────────────────────────────────────────────────────────
# 8.  SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🤖 AI FAQ Chatbot")
    st.markdown("*Powered by TF-IDF & Cosine Similarity*")
    st.markdown("---")

    st.markdown("### 📊 Model Info")
    st.info(
        f"**FAQ Entries:** {len(faq_df)}\n\n"
        f"**NLP Pipeline:** Lowercase → Punctuation Removal → Tokenisation → Stopword Removal\n\n"
        f"**Vectoriser:** TF-IDF\n\n"
        f"**Similarity:** Cosine Similarity\n\n"
        f"**Threshold:** {SIMILARITY_THRESHOLD}"
    )

    st.markdown("---")

    # ── Clear chat button ──
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.first_visit = True
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    examples = [
        "What is Python?",
        "How does machine learning work?",
        "What is TF-IDF?",
        "How do I start data science?",
        "What is an API?",
    ]
    for ex in examples:
        st.markdown(f"`{ex}`")

    st.markdown("---")
    st.caption("© 2025 CodeAlpha Internship Project")


# ──────────────────────────────────────────────────────────────────────────────
# 9.  MAIN PAGE — HEADER
# ──────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="hero-header">
        <h1>🤖 AI FAQ Chatbot</h1>
        <p>Ask questions and get instant answers</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Quick example chips
st.markdown(
    "<div style='text-align:center; margin-bottom:1rem;'>"
    + " ".join(
        f"<span class='faq-chip'>{q[:40]}</span>"
        for q in [faq["question"] for faq in FAQ_DATA[:6]]
    )
    + "</div>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# 10.  CHAT HISTORY DISPLAY
# ──────────────────────────────────────────────────────────────────────────────

chat_placeholder = st.container()

with chat_placeholder:
    # Welcome message on first visit / after clear
    if st.session_state.first_visit:
        st.markdown(
            """
            <div class="welcome-card">
                <h3>👋 Welcome! I'm your AI FAQ Assistant.</h3>
                <p>I can answer questions about Python, Machine Learning, NLP, Data Science,
                   APIs, Git, and more.<br>Type your question below to get started!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render chat bubbles
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="user-bubble-wrapper">
                        <div class="chat-bubble user-bubble">👤 {msg['content']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Determine score badge class
            score = msg.get("score", 0.0)
            if score >= 0.5:
                badge_cls, label = "score-high", "High Confidence"
            elif score >= 0.25:
                badge_cls, label = "score-medium", "Medium Confidence"
            else:
                badge_cls, label = "score-low", "Low Confidence"

            score_html = (
                f"<br><span class='score-badge {badge_cls}'>"
                f"🎯 Score: {score:.2%} — {label}</span>"
                if score > 0
                else ""
            )

            matched_html = (
                f"<div class='matched-q'>📌 Matched: \"{msg.get('matched_q', '')[:70]}\"</div>"
                if msg.get("matched_q")
                else ""
            )

            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="bot-bubble-wrapper">
                        <div class="bot-avatar">🤖</div>
                        <div class="chat-bubble bot-bubble">
                            {msg['content']}
                            {score_html}
                            {matched_html}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────────────────────────────────────
# 11.  INPUT FORM
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("---")

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            label="Your Question",
            placeholder="e.g.  What is machine learning?",
            label_visibility="collapsed",
        )
    with col2:
        submitted = st.form_submit_button("Send 🚀", use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# 12.  PROCESS SUBMISSION
# ──────────────────────────────────────────────────────────────────────────────

if submitted and user_input.strip():
    # Mark first visit as done
    st.session_state.first_visit = False

    # Add user message to history
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input.strip()}
    )

    # Show a brief spinner while "thinking"
    with st.spinner("🤔 Thinking…"):
        time.sleep(0.4)   # Simulate slight processing delay for UX
        answer, score, matched_q = get_answer(
            user_input, tfidf_matrix, vectorizer, faq_df
        )

    # Add bot response to history
    st.session_state.chat_history.append(
        {
            "role": "bot",
            "content": answer,
            "score": score,
            "matched_q": matched_q,
        }
    )

    # Re-run to refresh chat display
    st.rerun()

elif submitted and not user_input.strip():
    st.warning("⚠️ Please type a question before sending.", icon="⚠️")


# ──────────────────────────────────────────────────────────────────────────────
# 13.  FOOTER
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#475569; font-size:0.8rem;'>"
    "Built with ❤️ using Python • Streamlit • NLTK • Scikit-learn | CodeAlpha AI Internship"
    "</p>",
    unsafe_allow_html=True,
)
