import datetime
import sqlite3
import streamlit as st

# ==========================================
# 🌸 MOMO FASHION - PERSISTENT REAL-TIME WORKSPACE
# ==========================================
st.set_page_config(page_title="Momo Fashion", layout="wide", page_icon="👗")

# Persistent SQLite database setup that survives reloads & restarts
conn = sqlite3.connect("momo_persistent_notes.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS notes 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, content TEXT, timestamp TEXT, status TEXT)"""
)
conn.commit()

# Editorial High-End Styling with Smooth Animations
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    .stApp {
        background-color: #FFF8FA;
        color: #3D2C31;
        font-family: 'Plus Jakarta Sans', sans-serif;
        animation: fadeInApp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    @keyframes fadeInApp {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero-container {
        padding: 30px 0px 20px 0px;
        border-bottom: 1px solid #E8D5DC;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .editorial-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 400;
        color: #4A1525;
        line-height: 1.1;
        margin: 0;
    }

    .editorial-title span {
        font-style: italic;
        color: #B83B5E;
    }

    .stButton>button {
        background: #4A1525;
        color: #FFFFFF;
        border-radius: 0px;
        height: 46px;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.8rem;
        width: 100%;
        border: 1px solid #4A1525;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: transparent;
        color: #4A1525;
        border: 1px solid #4A1525;
        transform: translateY(-2px);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 0px;
        border: 1px solid #E8D5DC;
        background-color: #FFFFFF;
        padding: 12px;
        color: #3D2C31;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #B83B5E;
        box-shadow: none;
    }

    .editorial-card {
        background: #FFFFFF;
        padding: 24px;
        border: 1px solid #E8D5DC;
        margin-bottom: 18px;
        transition: all 0.3s ease;
    }
    .editorial-card:hover {
        border-color: #B83B5E;
        box-shadow: 0 8px 25px rgba(184, 59, 94, 0.05);
    }

    .card-meta {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8C6D76;
        margin-bottom: 6px;
    }

    .card-content {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #3D2C31;
        line-height: 1.4;
    }
    
    .completed-banner {
        background-color: #FCE8EE;
        border-left: 4px solid #B83B5E;
        padding: 10px 15px;
        font-size: 0.85rem;
        color: #4A1525;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
        animation: fadeInApp 0.4s ease;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- REQUIRE NAME MODAL / SCREEN ON FIRST LOAD ---
if "user_name" not in st.session_state:
    st.markdown(
        "<div style='max-width: 450px; margin: 100px auto; text-align: center;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='font-family: Playfair Display; color: #4A1525;'>Momo Fashion.</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #8C6D76; font-size: 0.9rem; margin-bottom: 25px;'>Please enter your name to enter the workspace</p>",
        unsafe_allow_html=True,
    )

    with st.form("name_entry_form"):
        entered_name = st.text_input(
            "Your Name", placeholder="e.g. Ali or Sarah"
        )
        enter_btn = st.form_submit_button("Enter Workspace")
        if enter_btn:
            if entered_name.strip():
                st.session_state["user_name"] = entered_name.strip()
                st.rerun()
            else:
                st.warning("Please enter your name to proceed.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN APP INTERFACE ---
st.markdown(
    f"""
    <div class="hero-container">
        <div>
            <h1 class="editorial-title">MOMO <span>FASHION.</span></h1>
        </div>
        <div style="text-align: right; color: #8C6D76; font-size: 0.85rem; letter-spacing: 1px;">
            LOGGED IN AS: <strong style="color: #4A1525;">{st.session_state['user_name'].upper()}</strong>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar controls
with st.sidebar:
    st.markdown(
        "<h3 style='font-family: Playfair Display; color: #4A1525;'>Workspace</h3>",
        unsafe_allow_html=True,
    )
    if st.button("Change Name"):
        del st.session_state["user_name"]
        st.rerun()
    st.markdown("<hr style='border-color: #E8D5DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.8rem; color: #8C6D76; line-height: 1.6;'>All entries and check-offs are permanently saved and synchronized across devices.</p>",
        unsafe_allow_html=True,
    )

# Check for recently completed notification triggers stored in DB or session
c.execute(
    "SELECT content FROM notes WHERE status LIKE 'Completed by%' ORDER BY id DESC LIMIT 1"
)
recent_completion = c.fetchone()

tab1, tab2 = st.tabs(["✦ NEW ENTRY", "✦ LIVE TEAM FEED"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "<h3 style='font-family: Playfair Display; font-weight: 400; color: #4A1525;'>Create New Entry</h3>",
            unsafe_allow_html=True,
        )
        with st.form("editorial_form", clear_on_submit=True):
            note_content = st.text_area(
                "Details",
                height=140,
                placeholder="e.g. Ahmed Khan — Black Suit Medium — Pending",
            )
            submit_btn = st.form_submit_button("Publish Entry")

            if submit_btn:
                if note_content.strip():
                    current_time = datetime.datetime.now().strftime(
                        "%B %d, %Y — %I:%M %p"
                    )
                    c.execute(
                        "INSERT INTO notes (author, content, timestamp, status) VALUES (?, ?, ?, ?)",
                        (
                            st.session_state["user_name"],
                            note_content,
                            current_time,
                            "Active",
                        ),
                    )
                    conn.commit()
                    st.success("Entry saved permanently to team feed.")
                    st.rerun()
                else:
                    st.warning("Please provide details before publishing.")

with tab2:
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.markdown(
            "<h3 style='font-family: Playfair Display; font-weight: 400; color: #4A1525;'>Live Team Stream</h3>",
            unsafe_allow_html=True,
        )
    with col_b:
        if st.button("Sync Feed"):
            st.rerun()

    st.markdown(
        "<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True
    )

    c.execute("SELECT id, author, content, timestamp, status FROM notes ORDER BY id DESC")
    notes = c.fetchall()

    if not notes:
        st.info("No records found in the live stream.")
    else:
        for note in notes:
            note_id, author, content, timestamp, status = note

            # If marked completed, show completion notification banner above or inside card
            if status != "Active":
                st.markdown(
                    f"""<div class="completed-banner">✓ {status}</div>""",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class="editorial-card">
                    <div class="card-meta">BY {author.upper()} &nbsp;&bull;&nbsp; {timestamp}</div>
                    <div class="card-content">{content}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Checkbox / Button to mark as completed if it's still active
            if status == "Active":
                col_c, col_d = st.columns([1, 4])
                with col_c:
                    if st.button("Mark Completed", key=f"complete_{note_id}"):
                        completion_msg = f"'{content[:30]}...' is completed by {st.session_state['user_name']}"
                        c.execute(
                            "UPDATE notes SET status = ? WHERE id = ?",
                            (completion_msg, note_id),
                        )
                        conn.commit()
                        st.rerun()
                st.markdown(
                    "<div style='margin-bottom: 10px;'></div>",
                    unsafe_allow_html=True,
                )
