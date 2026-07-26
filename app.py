import datetime
import sqlite3
import streamlit as st

# ==========================================
# 🌸 MOMO FASHION - ANIMATED EDITORIAL UI
# ==========================================
st.set_page_config(
    page_title="Momo Fashion", layout="wide", page_icon="👗"
)

# Editorial High-End Serif & Minimalist Styling with Smooth CSS Page Transitions
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    .stApp {
        background-color: #FFF8FA;
        color: #3D2C31;
        font-family: 'Plus Jakarta Sans', sans-serif;
        animation: fadeInApp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    @keyframes fadeInApp {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Editorial Hero Section */
    .hero-container {
        padding: 40px 0px 20px 0px;
        border-bottom: 1px solid #E8D5DC;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        animation: slideDown 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .editorial-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 400;
        color: #4A1525;
        line-height: 1.1;
        margin: 0;
    }

    .editorial-title span {
        font-style: italic;
        color: #B83B5E;
    }

    /* Minimalist Outline / Solid Buttons with Smooth Hover Animation */
    .stButton>button {
        background: #4A1525;
        color: #FFFFFF;
        border-radius: 0px;
        height: 48px;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.85rem;
        width: 100%;
        border: 1px solid #4A1525;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        background: transparent;
        color: #4A1525;
        border: 1px solid #4A1525;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 21, 37, 0.08);
    }

    /* Clean Input Fields with Glow Transition */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 0px;
        border: 1px solid #E8D5DC;
        background-color: #FFFFFF;
        padding: 12px;
        color: #3D2C31;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #B83B5E;
        box-shadow: 0 0 0 2px rgba(184, 59, 94, 0.1);
    }

    /* Editorial Note Cards with Slide-Up Entrance Animation */
    .editorial-card {
        background: #FFFFFF;
        padding: 28px;
        border: 1px solid #E8D5DC;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: cardEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    @keyframes cardEntrance {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .editorial-card:hover {
        border-color: #B83B5E;
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(184, 59, 94, 0.08);
    }

    .card-meta {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8C6D76;
        margin-bottom: 8px;
    }

    .card-content {
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        color: #3D2C31;
        line-height: 1.5;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- DATABASE SETUP ---
conn = sqlite3.connect("momo_editorial_notes.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS notes 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, content TEXT, timestamp TEXT)"""
)
conn.commit()

# --- HEADER LAYOUT ---
st.markdown(
    """
    <div class="hero-container">
        <div>
            <h1 class="editorial-title">MOMO <span>FASHION.</span></h1>
        </div>
        <div style="text-align: right; color: #8C6D76; font-size: 0.9rem; letter-spacing: 1px;">
            SHARED WORKSPACE • ANIMATED EDITION
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        "<h3 style='font-family: Playfair Display; color: #4A1525;'>Session</h3>",
        unsafe_allow_html=True,
    )
    worker_name = st.text_input(
        "Worker Name", value="Staff", placeholder="Your name"
    )
    st.markdown("<hr style='border-color: #E8D5DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.8rem; color: #8C6D76; line-height: 1.6;'>Entries recorded here synchronize instantly across all team devices with smooth animations.</p>",
        unsafe_allow_html=True,
    )

# --- TABS WITH SMOOTH TRANSITIONS ---
tab1, tab2 = st.tabs(["✦ NEW ENTRY", "✦ TEAM FEED"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "<h3 style='font-family: Playfair Display; font-weight: 400; color: #4A1525;'>Log New Order / Note</h3>",
            unsafe_allow_html=True,
        )
        with st.form("editorial_form", clear_on_submit=True):
            note_content = st.text_area(
                "Details",
                height=150,
                placeholder="e.g. Ahmed Khan — Black Suit Medium — Confirmed",
            )
            submit_btn = st.form_submit_button("Publish Entry")

            if submit_btn:
                if note_content.strip():
                    current_time = datetime.datetime.now().strftime(
                        "%B %d, %Y — %I:%M %p"
                    )
                    c.execute(
                        "INSERT INTO notes (author, content, timestamp) VALUES (?, ?, ?)",
                        (worker_name, note_content, current_time),
                    )
                    conn.commit()
                    st.success("Entry published to team stream.")
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
        "<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True
    )

    c.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = c.fetchall()

    if not notes:
        st.info("No records found in the live stream.")
    else:
        for note in notes:
            st.markdown(
                f"""
                <div class="editorial-card">
                    <div class="card-meta">BY {note[1].upper()} &nbsp;&bull;&nbsp; {note[3]}</div>
                    <div class="card-content">{note[2]}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
