import datetime
import sqlite3
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 🌸 MOMO FASHION - MINIMALISTIC & BUBBLY EDITION
# ==========================================
st.set_page_config(page_title="Momo Fashion", layout="wide", page_icon="🌸")

# Auto-refresh chat and live feed every 3 seconds to instantly display new messages without losing selection
st_autorefresh(interval=3000, key="momo_live_sync")

# Persistent SQLite database setup for users, notes, and direct messages (Permanent storage)
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

# Bubbly, Minimalistic, Soft Pink Aesthetic matching the Momo Fashion logo
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Quicksand:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #F4D5CD;
        color: #3E2723;
        font-family: 'Quicksand', sans-serif;
        animation: fadeInApp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    @keyframes fadeInApp {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero-container {
        padding: 25px 0px 20px 0px;
        border-bottom: 2px dashed #E0B5AC;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        animation: slideDown 0.6s ease;
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .editorial-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #2C1815;
        line-height: 1.1;
        margin: 0;
    }

    .editorial-title span {
        font-style: italic;
        color: #C2566F;
    }

    .stButton>button {
        background: #D96B82;
        color: #FFFFFF;
        border-radius: 20px;
        height: 48px;
        font-weight: 600;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
        width: 100%;
        border: none;
        box-shadow: 0 4px 15px rgba(217, 107, 130, 0.25);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .stButton>button:hover {
        background: #C2566F;
        color: #FFFFFF;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(194, 86, 111, 0.35);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 16px;
        border: 2px solid #E0B5AC;
        background-color: #FFF9F7;
        padding: 14px;
        color: #3E2723;
        font-family: 'Quicksand', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #D96B82;
        background-color: #FFFFFF;
        box-shadow: 0 0 0 4px rgba(217, 107, 130, 0.15);
    }

    .editorial-card {
        background: #FFF9F7;
        padding: 24px;
        border: 2px solid #E0B5AC;
        border-radius: 20px;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .editorial-card:hover {
        border-color: #D96B82;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(217, 107, 130, 0.12);
    }

    .card-meta {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8C5C55;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .card-content {
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        color: #2C1815;
        line-height: 1.4;
    }
    
    .completed-banner {
        background-color: #F8D7D2;
        border-left: 5px solid #D96B82;
        padding: 12px 18px;
        font-size: 0.9rem;
        color: #3E2723;
        font-weight: 600;
        border-radius: 0 12px 12px 0;
        margin-bottom: 15px;
        animation: fadeInApp 0.4s ease;
    }
    
    .msg-bubble-sent {
        background-color: #D96B82;
        color: #FFFFFF;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(217, 107, 130, 0.2);
        animation: fadeInApp 0.3s ease;
    }
    .msg-bubble-recv {
        background-color: #FFF9F7;
        color: #3E2723;
        border: 2px solid #E0B5AC;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 18px 18px 18px 4px;
        max-width: 75%;
        margin-right: auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        animation: fadeInApp 0.3s ease;
    }

    .brand-subtitle {
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #8C5C55;
        font-weight: 600;
        margin-top: 4px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SECURE LOGIN / REGISTRATION SYSTEM ---
if "user_name" not in st.session_state:
    st.markdown(
        "<div style='max-width: 420px; margin: 70px auto; background: #FFF9F7; padding: 40px; border: 2px solid #E0B5AC; border-radius: 28px; box-shadow: 0 15px 35px rgba(0,0,0,0.05); animation: fadeInApp 0.5s ease;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='font-family: Playfair Display; color: #2C1815; text-align: center; margin-bottom: 0;'>Momo Fashion</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-size: 0.75rem; letter-spacing: 2px; color: #8C5C55; text-transform: uppercase; margin-bottom: 25px; font-weight: 600;'>Clothing Brand Portal</p>",
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
        <div style="text-align: right; color: #8C5C55; font-size: 0.85rem; letter-spacing: 1px; font-weight: 600;">
            LOGGED IN AS: <strong style="color: #D96B82;">{st.session_state['user_name'].upper()}</strong> {"⭐ [ADMIN]" if is_admin else ""}
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar controls & Signed Users List with Admin Kick Capability
with st.sidebar:
    st.markdown(
        "<h3 style='font-family: Playfair Display; color: #2C1815;'>Workspace Menu</h3>",
        unsafe_allow_html=True,
    )
    if st.button("Log Out"):
        del st.session_state["user_name"]
        st.rerun()
    st.markdown("<hr style='border-color: #E0B5AC;'>", unsafe_allow_html=True)

    st.markdown(
        "<h4 style='font-family: Playfair Display; color: #2C1815; font-size: 1.1rem;'>Signed Team Members</h4>",
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
                    f"<div style='padding: 8px 12px; background: #F8D7D2; color: #2C1815; border-radius: 12px; margin-bottom: 6px; font-size: 0.9em; font-weight: 600;'>🌸 <b>{uname}</b> (You)</div>",
                    unsafe_allow_html=True,
                )
            else:
                col_u1, col_u2 = st.columns([3, 2])
                with col_u1:
                    st.markdown(
                        f"<div style='padding: 6px 0px; color: #3E2723; font-size: 0.9em; font-weight: 500;'>• {uname}</div>",
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

    st.markdown("<hr style='border-color: #E0B5AC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.8rem; color: #8C5C55; line-height: 1.6;'>All data is permanently stored and never expires. Admin Ayan holds full management control.</p>",
        unsafe_allow_html=True,
    )

tab1, tab2, tab3 = st.tabs(
    ["✦ NEW ENTRY", "✦ LIVE TEAM FEED", "✦ DIRECT MESSAGES"]
)

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "<h3 style='font-family: Playfair Display; font-weight: 700; color: #2C1815;'>Create New Entry</h3>",
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
            "<h3 style='font-family: Playfair Display; font-weight: 700; color: #2C1815;'>Live Team Stream</h3>",
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
        "<h3 style='font-family: Playfair Display; font-weight: 700; color: #2C1815;'>Direct Messages</h3>",
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
        # Preserve selected recipient in session state so auto-refreshes don't reset the dropdown
        if (
            "selected_recipient" not in st.session_state
            or st.session_state["selected_recipient"] not in other_users
        ):
            st.session_state["selected_recipient"] = other_users[0]

        selected_recipient = st.selectbox(
            "Select Team Member to Message",
            other_users,
            index=other_users.index(st.session_state["selected_recipient"]),
            key="recipient_selectbox",
        )
        st.session_state["selected_recipient"] = selected_recipient

        st.markdown("<hr style='border-color: #E0B5AC;'>", unsafe_allow_html=True)

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
                                <div style="font-size: 0.7rem; opacity: 0.85; margin-bottom: 4px; font-weight: 600;">YOU &bull; {timestamp}</div>
                                {msg_content}
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="msg-bubble-recv">
                                <div style="font-size: 0.7rem; color: #8C5C55; margin-bottom: 4px; font-weight: 600;">{sender.upper()} &bull; {timestamp}</div>
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

        # Handle message sending via form and automatically trigger a clean rerun
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
