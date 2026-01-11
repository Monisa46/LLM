import streamlit as st
import pandas as pd


from backend.groq_client import get_llama_response

# =====================================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="LLM-Based AI Chat System",
    page_icon="🤖",
    layout="wide"
)
 
# ================== GLOBAL DARK THEME ==================
st.markdown("""
<style>

/* ---------- ROOT FIX ---------- */
:root {
    --background-color: #050814;
    --secondary-background-color: #050814;
    --text-color: #EAEAEA;
}

/* ---------- APP BACKGROUND ---------- */
html, body, .stApp {
    background-color: #050814 !important;
}

.stApp {
    background: radial-gradient(circle at top, #1a1037, #050814) !important;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background-color: #0b0f2a !important;
    animation: slideIn 0.8s ease-out;
}

/* ---------- ALL TEXT ---------- */
h1, h2, h3, h4, h5, h6,
p, label, span, li, strong, b, em {
    color: #EAEAEA !important;
}

/* ---------- MARKDOWN / AI OUTPUT ---------- */
.stMarkdown, .stText {
    color: #EAEAEA !important;
}

/* ---------- CODE BLOCKS ---------- */
pre {
    background-color: #0b1025 !important;
    color: #EAEAEA !important;
    border-radius: 12px;
    padding: 10px;
}

code {
    color: #FFD700 !important;
    background-color: #0b1025 !important;
}

/* ---------- ALERTS ---------- */
[data-testid="stAlert"] p {
    color: #FFFFFF !important;
}

/* ========== FINAL SELECTBOX FORCE FIX ========== */

/* Dropdown menu container (white box fix) */
div[data-baseweb="menu"] {
    background-color: #0b1025 !important;
    opacity: 1 !important;
}

/* Dropdown listbox */
div[role="listbox"] {
    background-color: #0b1025 !important;
    opacity: 1 !important;
}

/* Each option (THIS fixes faded look) */
div[role="option"] {
    background-color: #0b1025 !important;
    color: #FFFFFF !important;
    opacity: 1 !important;
    font-weight: 500 !important;
}

/* Hover option */
div[role="option"]:hover {
    background-color: #7F00FF !important;
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Selected option */
div[role="option"][aria-selected="true"] {
    background-color: #1a1037 !important;
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Remove disabled look */
div[role="option"][aria-disabled="true"] {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Arrow icon */
div[data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    opacity: 1 !important;
}


/* ---------- INPUTS ---------- */
input, textarea {
    background-color: #0b1025 !important;
    color: #FFFFFF !important;
}

input:focus, textarea:focus {
    border: 2px solid #7F00FF !important;
    box-shadow: 0 0 10px rgba(127,0,255,0.8);
}

/* ---------- BUTTON ---------- */
button {
    transition: all 0.3s ease !important;
}

button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #7F00FF, #E100FF) !important;
}

/* ---------- CARD ---------- */
.card {
    background: #12172b;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

/* ---------- ANIMATIONS ---------- */
@keyframes slideIn {
    from { transform: translateX(-30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.fade-in {
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown(
    "<h1 class='fade-in'>🤖 LLM-Based AI Chat System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p class='fade-in'>Upload enterprise datasets (English / Japanese supported) and ask questions using AI.</p>",
    unsafe_allow_html=True
)

# =====================================================
# DATASET SELECTION
# =====================================================
st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)

dataset_type = st.radio(
    "📂 Select Dataset Type",
    ["Sales", "Manufacturing", "Invoice", "Purchase", "Inventory"]
)

uploaded_file = st.file_uploader(
    f"Upload {dataset_type} CSV File",
    type=["csv"]
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# DATASET HANDLING
# =====================================================
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, on_bad_lines="skip")

        st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
        st.success("✅ Dataset uploaded successfully")
        st.dataframe(df.head(5))
        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # QUESTION INPUT
        # =================================================
        st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)

        user_query = st.text_input(
            "💬 Ask a Question (English or Japanese)",
            placeholder="Example: How many orders are in this dataset?"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # AI RESPONSE
        # =================================================
        if user_query:
            with st.spinner("🤖 AI is thinking..."):


                # TOKEN SAFE: only summary, not full CSV
                context_text = f"""
Columns: {list(df.columns)}
Total rows: {len(df)}
Sample rows:
{df.head(3).to_string(index=False)}
"""

                prompt = f"""
You are an AI assistant.
Answer using ONLY the dataset summary below.

Dataset Type: {dataset_type}

Dataset Info:
{context_text}

Question:
{user_query}

Give a short and clear answer.
"""

                answer = get_llama_response(prompt)

            st.markdown(
                f"""
                <div class="card fade-in">
                <h3>🧠 AI Answer</h3>
                <p>{answer}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("⬆️ Please upload a CSV file to begin.")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("🚀 Hackathon Prototype | Streamlit + Python + LLaMA (Groq)")
