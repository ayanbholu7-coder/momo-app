import datetime
import sqlite3
import streamlit as st

# ==========================================
# 🎨 MOMO FASHION - SHARED TEAM NOTES UI
# ==========================================
st.set_page_config(
    page_title="Momo Fashion", layout="centered", page_icon="👗"
)

# Custom Minimalist Pink & White CSS with smooth fade animations
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF5F7;
        color: #4A4A4A;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        color: #D81B60;
        text-align: center;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #D81B60;
        color: white;
        border-radius: 12px;
        height: 48px;
        font-weight: 600;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #AD1457;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(216, 27, 96, 0.2);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #F8BBD0;
        background-color: #FFFFFF;
    }
    .note-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(216, 27, 96, 0.05);
        margin-bottom: 15px;
        border-left: 5px solid #D81B60;
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- DATABASE SETUP FOR SHARED TEAM ACCESS ---
conn = sqlite3.connect("momo_shared_notes.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS notes 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, content TEXT, timestamp TEXT)"""
)
conn.commit()

st.title("👗 Momo Fashion Team Notes")
st.markdown(
    "<p style='text-align: center; color: #888;'>Collaborative workspace for all workers</p>",
    unsafe_allow_html=True,
)

# Sidebar for worker identification
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=300&auto=format&fit=crop&q=60",
        use_container_width=True,
    )
    st.subheader("Worker Profile")
    worker_name = st.text_input(
        "Your Name / Tag", value="Worker", placeholder="Enter your name"
    )
    st.info(
        "💡 Everything you post here is saved to the shared cloud database so other workers can see it instantly upon refreshing."
    )

# --- MAIN INTERFACE ---
tab1, tab2 = st.tabs(["✍️ New Note / Order", "📋 Shared Team Feed"])

with tab1:
    st.subheader("Add a New Note")
    with st.form("note_form", clear_on_submit=True):
        note_content = st.text_area(
            "Write customer order detail, update, or note:",
            height=140,
            placeholder="e.g. Ahmed Khan requested a black suit medium size...",
        )
        submit_btn = st.form_submit_button("Post to Team Feed ✨")

        if submit_btn:
            if note_content.strip():
                current_time = datetime.datetime.now().strftime(
                    "%b %d, %Y - %I:%M %p"
                )
                c.execute(
                    "INSERT INTO notes (author, content, timestamp) VALUES (?, ?, ?)",
                    (worker_name, note_content, current_time),
                )
                conn.commit()
                st.success("Note posted successfully for everyone to see!")
                st.rerun()
            else:
                st.warning("Please write something before posting.")

with tab2:
    st.subheader("Live Shared Feed")

    if st.button("🔄 Refresh Feed"):
        st.rerun()

    c.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = c.fetchall()

    if not notes:
        st.info("No team notes yet. Be the first to add one!")
    else:
        for note in notes:
            # Render a clean, animated minimal card for each note
            st.markdown(
                f"""
                <div class="note-card">
                    <strong style="color: #D81B60; font-size: 1.1em;">👤 {note[1]}</strong>
                    <span style="float: right; color: #aaa; font-size: 0.85em;">{note[3]}</span>
                    <p style="margin-top: 10px; white-space: pre-wrap; font-size: 1em;">{note[2]}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )
