import datetime
import sqlite3
import streamlit as st

# ==========================================
# 🎨 MOMO FASHION - ULTRA MINIMALIST UI
# ==========================================
st.set_page_config(
    page_title="Momo Fashion", layout="centered", page_icon="👗"
)

# Ultra-modern frosted glass and pink/white minimalist aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #FFF0F3 0%, #FFFFFF 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #2D3748;
    }
    
    /* Hide default streamlit headers/footers for a cleaner app look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    h1, h2, h3 {
        color: #9C1445;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Sleek Modern Buttons */
    .stButton>button {
        background: #9C1445;
        color: #FFFFFF;
        border-radius: 14px;
        height: 50px;
        font-weight: 600;
        width: 100%;
        border: none;
        box-shadow: 0 4px 14px rgba(156, 20, 69, 0.2);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        background: #7B0E35;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(156, 20, 69, 0.3);
    }
    .stButton>button:active {
        transform: translateY(0px);
    }

    /* Minimalist Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 1.5px solid #F3D2DE;
        background-color: #FFFFFF;
        padding: 12px;
        color: #2D3748;
        transition: all 0.2s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #9C1445;
        box-shadow: 0 0 0 3px rgba(156, 20, 69, 0.1);
    }

    /* Glassmorphism Feed Cards */
    .note-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid rgba(243, 210, 222, 0.6);
        box-shadow: 0 10px 30px rgba(156, 20, 69, 0.04);
        margin-bottom: 18px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: slideUp 0.4s ease-out;
    }
    .note-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 35px rgba(156, 20, 69, 0.08);
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Badge styles */
    .worker-badge {
        background-color: #FCE8EE;
        color: #9C1445;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- DATABASE SETUP ---
conn = sqlite3.connect("momo_shared_notes.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS notes 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, content TEXT, timestamp TEXT)"""
)
conn.commit()

st.title("👗 Momo Fashion")
st.markdown(
    "<p style='text-align: center; color: #718096; margin-top: -10px; margin-bottom: 30px;'>Clean, shared workspace for team orders & updates</p>",
    unsafe_allow_html=True,
)

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("Worker Session")
    worker_name = st.text_input(
        "Your Name", value="Worker", placeholder="Enter your display name"
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size: 0.85em; color: #A0AEC0;'>Everything posted syncs instantly across all connected devices.</p>",
        unsafe_allow_html=True,
    )

# --- TABS ---
tab1, tab2 = st.tabs(["✨ New Update", "📋 Live Team Feed"])

with tab1:
    st.subheader("Post Order / Note")
    with st.form("note_form", clear_on_submit=True):
        note_content = st.text_area(
            "Write details here...",
            height=130,
            placeholder="e.g. Ahmed Khan - Black suit medium size - Verified",
        )
        submit_btn = st.form_submit_button("Publish to Team ✨")

        if submit_btn:
            if note_content.strip():
                current_time = datetime.datetime.now().strftime(
                    "%b %d, %Y • %I:%M %p"
                )
                c.execute(
                    "INSERT INTO notes (author, content, timestamp) VALUES (?, ?, ?)",
                    (worker_name, note_content, current_time),
                )
                conn.commit()
                st.success("Published successfully!")
                st.rerun()
            else:
                st.warning("Please type a message before publishing.")

with tab2:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Feed")
    with col2:
        if st.button("🔄 Sync"):
            st.rerun()

    c.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = c.fetchall()

    if not notes:
        st.info("No notes found. Be the first to add an entry!")
    else:
        for note in notes:
            st.markdown(
                f"""
                <div class="note-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="worker-badge">👤 {note[1]}</span>
                        <span style="color: #A0AEC0; font-size: 0.8em;">{note[3]}</span>
                    </div>
                    <p style="margin-top: 12px; white-space: pre-wrap; font-size: 0.95em; line-height: 1.5;">{note[2]}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )
