import datetime
import sqlite3
import streamlit as st

# ==========================================
# 🌸 MOMO FASHION - BLUSH PINK & FLORAL EDITION
# ==========================================
st.set_page_config(page_title="Momo Fashion", layout="wide", page_icon="🌸")

# Persistent SQLite database setup for users, notes, and direct messages (Permanent 10+ year storage)
conn = sqlite3.connect("momo_secure_workspace.db", check_same_thread=False)
c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS users 
             (username TEXT PRIMARY KEY, password TEXT)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS notes 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, content TEXT, timestamp TEXT, status TEXT)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS messages 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, receiver TEXT, content TEXT, timestamp TEXT)"""
)
conn.commit()

# Enhanced Blush Pink Aesthetic matching the Momo Fashion brand logo
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    .stApp {
        background-color: #F7EBE8;
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
        border-bottom: 1px solid #E8C8C4;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .editorial-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 400;
        color: #2D1820;
        line-height: 1.1;
        margin: 0;
    }

    .editorial-title span {
        font-style: italic;
        color: #C25E73;
    }

    .stButton>button {
        background: #C25E73;
        color: #FFFFFF;
        border-radius: 4px;
        height: 46px;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.8rem;
        width: 100%;
        border: 1px solid #C25E73;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #A8495E;
        color: #FFFFFF;
        border: 1px solid #A8495E;
        transform: translateY(-2px);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 4px;
        border: 1px solid #E8C8C4;
        background-color: #FFFDFD;
        padding: 12px;
        color: #3D2C31;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #C25E73;
        box-shadow: 0 0 0 1px #C25E73;
    }

    .editorial-card {
        background: #FFFDFD;
        padding: 24px;
        border: 1px solid #E8C8C4;
        border-radius: 6px;
        margin-bottom: 18px;
        transition: all 0.3s ease;
    }
    .editorial-card:hover {
        border-color: #C25E73;
        box-shadow: 0 8px 25px rgba(194, 94, 115, 0.08);
    }

    .card-meta {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #9E737B;
        margin-bottom: 6px;
    }

    .card-content {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #3D2C31;
        line-height: 1.4;
    }
    
    .completed-banner {
        background-color: #F3D9DF;
        border-left: 4px solid #C25E73;
        padding: 10px 15px;
        font-size: 0.85rem;
        color: #4A1B24;
        border-radius: 0 4px 4px 0;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
        animation: fadeInApp 0.4s ease;
    }
    
    .msg-bubble-sent {
        background-color: #C25E73;
        color: #FFFFFF;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 12px 12px 2px 12px;
        max-width: 75%;
        margin-left: auto;
    }
    .msg-bubble-recv {
        background-color: #FFFDFD;
        color: #3D2C31;
        border: 1px solid #E8C8C4;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 12px 12px 12px 2px;
        max-width: 75%;
        margin-right: auto;
    }

    .brand-subtitle {
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #9E737B;
        margin-top: 5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SECURE LOGIN / REGISTRATION SYSTEM ---
if "user_name" not in st.session_state:
    st.markdown(
        "<div style='max-width: 450px; margin: 80px auto; background: #FFFDFD; padding: 40px; border: 1px solid #E8C8C4; border-radius: 8px;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='font-family: Playfair Display; color: #2D1820; text-align: center; margin-bottom: 0;'>Momo Fashion</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-size: 0.75rem; letter-spacing: 2px; color: #9E737B; text-transform: uppercase; margin-bottom: 25px;'>Clothing Brand Portal</p>",
        unsafe_allow_html=True,
    )

    auth_tab1, auth_tab2 = st.tabs(["🔐 Sign In", "📝 Register"])

    with auth_tab1:
        with st.form("login_form"):
            login_user = st.text_input("Name", placeholder="Your worker name")
            login_pass = st.text_input(
                "Password", type="password", placeholder="Your password"
            )
            login_btn = st.form_submit_button("Access Portal")

            if login_btn:
                clean_user = login_user.strip()
                c.execute(
                    "SELECT password FROM users WHERE username = ?",
                    (clean_user,),
                )
                row = c.fetchone()
                if row and row[0] == login_pass:
                    st.session_state["user_name"] = clean_user
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error("Invalid name or password.")

    with auth_tab2:
        with st.form("register_form"):
            reg_user = st.text_input(
                "Choose Name", placeholder="e.g. Ayan or Sarah"
            )
            reg_pass = st.text_input(
                "Choose Password",
                type="password",
                placeholder="Create a password",
            )
            reg_btn = st.form_submit_button("Register & Enter")

            if reg_btn:
                clean_user = reg_user.strip()
                if not clean_user or not reg_pass:
                    st.warning("Please fill in both fields.")
                else:
                    try:
                        c.execute(
                            "INSERT INTO users (username, password) VALUES (?, ?)",
                            (clean_user, reg_pass),
                        )
                        conn.commit()
                        st.session_state["user_name"] = clean_user
                        st.success("Account created successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error(
                            "This name is already registered. Please sign in instead."
                        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Check if current user was kicked/deleted by admin (Ayan)
c.execute(
    "SELECT username FROM users WHERE username = ?",
    (st.session_state["user_name"],),
)
if not c.fetchone():
    st.error("Your account has been removed by administrator Ayan.")
    del st.session_state["user_name"]
    if st.button("Return to Login"):
        st.rerun()
    st.stop()

is_admin = st.session_state["user_name"].lower() == "ayan"

# --- MAIN APP INTERFACE ---
st.markdown(
    f"""
    <div class="hero-container">
        <div>
            <h1 class="editorial-title">MOMO <span>FASHION</span></h1>
            <div class="brand-subtitle">Clothing Brand &bull; Permanent Secure Portal</div>
        </div>
        <div style="text-align: right; color: #9E737B; font-size: 0.85rem; letter-spacing: 1px;">
            LOGGED IN AS: <strong style="color: #C25E73;">{st.session_state['user_name'].upper()}</strong> {"⭐ [ADMIN]" if is_admin else ""}
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar controls & Signed Users List with Admin Kick Capability
with st.sidebar:
    st.markdown(
        "<h3 style='font-family: Playfair Display; color: #2D1820;'>Workspace Menu</h3>",
        unsafe_allow_html=True,
    )
    if st.button("Log Out"):
        del st.session_state["user_name"]
        st.rerun()
    st.markdown("<hr style='border-color: #E8C8C4;'>", unsafe_allow_html=True)

    st.markdown(
        "<h4 style='font-family: Playfair Display; color: #2D1820; font-size: 1.1rem;'>Signed Team Members</h4>",
        unsafe_allow_html=True,
    )
    c.execute("SELECT username FROM users ORDER BY username ASC")
    all_registered_users = c.fetchall()

    if not all_registered_users:
        st.write("No signed members yet.")
    else:
        for u_row in all_registered_users:
            uname = u_row[0]
            if uname == st.session_state["user_name"]:
                st.markdown(
                    f"<div style='padding: 6px 10px; background: #F3D9DF; color: #2D1820; border-radius: 4px; margin-bottom: 5px; font-size: 0.9em;'>🌸 <b>{uname}</b> (You)</div>",
                    unsafe_allow_html=True,
                )
            else:
                col_u1, col_u2 = st.columns([3, 2])
                with col_u1:
                    st.markdown(
                        f"<div style='padding: 6px 0px; color: #3D2C31; font-size: 0.9em;'>• {uname}</div>",
                        unsafe_allow_html=True,
                    )
                with col_u2:
                    if is_admin:
                        if st.button("Kick", key=f"kick_{uname}"):
                            c.execute(
                                "DELETE FROM users WHERE username = ?",
                                (uname,),
                            )
                            conn.commit()
                            st.success(f"Kicked {uname}")
                            st.rerun()

    st.markdown("<hr style='border-color: #E8C8C4;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.8rem; color: #9E737B; line-height: 1.6;'>All data is permanently stored and will never expire. Admin Ayan holds full management control.</p>",
        unsafe_allow_html=True,
    )

tab1, tab2, tab3 = st.tabs(
    ["✦ NEW ENTRY", "✦ LIVE TEAM FEED", "✦ DIRECT MESSAGES"]
)

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "<h3 style='font-family: Playfair Display; font-weight: 400; color: #2D1820;'>Create New Entry</h3>",
            unsafe_allow_html=True,
        )
        with st.form("editorial_form", clear_on_submit=True):
            note_content = st.text_area(
                "Details",
                height=140,
                placeholder="e.g. Floral Summer Dress Collection — Medium — Pending",
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
                    st.success(
                        "Entry safely committed to permanent database storage."
                    )
                    st.rerun()
                else:
                    st.warning("Please provide details before publishing.")

with tab2:
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.markdown(
            "<h3 style='font-family: Playfair Display; font-weight: 400; color: #2D1820;'>Live Team Stream</h3>",
            unsafe_allow_html=True,
        )
    with col_b:
        if st.button("Sync Feed"):
            st.rerun()

    st.markdown(
        "<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True
    )

    c.execute(
        "SELECT id, author, content, timestamp, status FROM notes ORDER BY id DESC"
    )
    notes = c.fetchall()

    if not notes:
        st.info("No records found in the live stream.")
    else:
        for note in notes:
            note_id, author, content, timestamp, status = note

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

            col_c, col_d = st.columns([1, 4])
            with col_c:
                if status == "Active":
                    if st.button("Mark Completed", key=f"complete_{note_id}"):
                        completion_msg = f"'{content[:30]}...' is completed by {st.session_state['user_name']}"
                        c.execute(
                            "UPDATE notes SET status = ? WHERE id = ?",
                            (completion_msg, note_id),
                        )
                        conn.commit()
                        st.rerun()
            if is_admin:
                with col_d:
                    if st.button(
                        "🗑️ Delete Entry (Admin)", key=f"del_note_{note_id}"
                    ):
                        c.execute(
                            "DELETE FROM notes WHERE id = ?", (note_id,)
                        )
                        conn.commit()
                        st.rerun()

            st.markdown(
                "<div style='margin-bottom: 10px;'></div>",
                unsafe_allow_html=True,
            )

with tab3:
    st.markdown(
        "<h3 style='font-family: Playfair Display; font-weight: 400; color: #2D1820;'>Direct Messages</h3>",
        unsafe_allow_html=True,
    )

    c.execute(
        "SELECT username FROM users WHERE username != ? ORDER BY username ASC",
        (st.session_state["user_name"],),
    )
    other_users = [row[0] for row in c.fetchall()]

    if not other_users:
        st.info(
            "No other registered team members yet. Register another user to start messaging!"
        )
    else:
        selected_recipient = st.selectbox(
            "Select Team Member to Message", other_users
        )

        st.markdown("<hr style='border-color: #E8C8C4;'>", unsafe_allow_html=True)

        c.execute(
            """SELECT id, sender, content, timestamp FROM messages 
                     WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?) 
                     ORDER BY id ASC""",
            (
                st.session_state["user_name"],
                selected_recipient,
                selected_recipient,
                st.session_state["user_name"],
            ),
        )
        chat_history = c.fetchall()

        chat_container = st.container(height=350)
        with chat_container:
            if not chat_history:
                st.write(
                    f"No messages with {selected_recipient} yet. Permanent database archiving is active."
                )
            else:
                for msg_id, sender, msg_content, timestamp in chat_history:
                    if sender == st.session_state["user_name"]:
                        st.markdown(
                            f"""
                            <div class="msg-bubble-sent">
                                <div style="font-size: 0.7rem; opacity: 0.8; margin-bottom: 4px;">YOU &bull; {timestamp}</div>
                                {msg_content}
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="msg-bubble-recv">
                                <div style="font-size: 0.7rem; color: #9E737B; margin-bottom: 4px;">{sender.upper()} &bull; {timestamp}</div>
                                {msg_content}
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    if is_admin:
                        if st.button(
                            "🗑️ Delete Message", key=f"del_msg_{msg_id}"
                        ):
                            c.execute(
                                "DELETE FROM messages WHERE id = ?", (msg_id,)
                            )
                            conn.commit()
                            st.rerun()

        with st.form("send_msg_form", clear_on_submit=True):
            msg_text = st.text_input(
                "Type your message...", placeholder="Write a direct message..."
            )
            send_btn = st.form_submit_button("Send Message")

            if send_btn:
                if msg_text.strip():
                    msg_time = datetime.datetime.now().strftime("%I:%M %p")
                    c.execute(
                        "INSERT INTO messages (sender, receiver, content, timestamp) VALUES (?, ?, ?, ?)",
                        (
                            st.session_state["user_name"],
                            selected_recipient,
                            msg_text,
                            msg_time,
                        ),
                    )
                    conn.commit()
                    st.rerun()
                else:
                    st.warning("Cannot send an empty message.")
