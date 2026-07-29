import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
import json
import os
import datetime
import hashlib

# 1. Page Setup & Animated Full Pink Theme
st.set_page_config(
    page_title="Momo Fashion",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Auto-refresh the entire app every 1 second (1000 milliseconds)
st_autorefresh(interval=1000, limit=None, key="momo_live_refresh")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        :root {
            --primary-pink: #ff1aff;
            --light-pink: #ff66cc;
            --dark-pink: #cc00cc;
            --glass-bg: rgba(255, 255, 255, 0.18);
            --glass-border: rgba(255, 255, 255, 0.5);
        }

        .stApp {
            background: linear-gradient(135deg, #ff1aff 0%, #ff4dd2 50%, #e600e6 100%);
            background-size: 300% 300%;
            animation: gradientShift 10s ease infinite;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes floatBounce {
            0%, 100% { transform: translateY(0px) rotateX(0deg); }
            50% { transform: translateY(-10px) rotateX(3deg); }
        }

        @keyframes pulseGlow {
            0%, 100% { text-shadow: 0 0 10px #ffffff, 0 0 20px #ffffff, 0 0 30px #ff1aff; }
            50% { text-shadow: 0 0 20px #ffffff, 0 0 30px #ffffff, 0 0 50px #ffffff; }
        }

        .momo-header {
            text-align: center;
            font-size: clamp(2.5rem, 8vw, 3.6rem);
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 25px;
            letter-spacing: -1px;
            -webkit-text-stroke: 1.5px #ffffff;
            animation: floatBounce 3s ease-in-out infinite, pulseGlow 2s ease-in-out infinite;
        }

        h1, h2, h3, h4, h5, h6, label, .stMarkdown p, span {
            color: #ffffff;
        }

        h3, h2 {
            text-shadow: 0 0 10px #ffffff, 0 0 20px rgba(255, 255, 255, 0.6);
            animation: floatBounce 4s ease-in-out infinite;
        }

        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 18px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2), inset 0 0 20px rgba(255, 255, 255, 0.2);
            animation: floatBounce 5s ease-in-out infinite;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        .glass-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), 0 0 30px #ffffff;
            border-color: #ffffff;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: #ffffff;
            box-shadow: 0 0 15px #ffffff;
            animation: pulseGlow 2s infinite;
        }

        div.stButton > button {
            background: rgba(255, 255, 255, 0.2);
            color: #ffffff;
            border-radius: 16px;
            font-weight: 700;
            border: 2px solid rgba(255, 255, 255, 0.7);
            width: 100%;
            padding: 14px;
            min-height: 52px;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2), 0 0 15px rgba(255, 255, 255, 0.3);
            text-shadow: 0 0 8px #ffffff;
            animation: floatBounce 3.5s ease-in-out infinite;
        }

        div.stButton > button:hover {
            background: #ffffff;
            color: #ff1aff;
            border-color: #ffffff;
            transform: translateY(-5px) scale(1.03);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 35px #ffffff;
            text-shadow: none;
        }

        div[data-testid="stFormSubmitButton"] > button {
            background: rgba(255, 255, 255, 0.9) !important;
            color: #ff1aff !important;
            border: 2px solid #ffffff !important;
            text-shadow: none !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2), 0 0 20px #ffffff !important;
        }

        div[data-testid="stFormSubmitButton"] > button:hover {
            background: #ff1aff !important;
            color: #ffffff !important;
            border-color: #ffffff !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 35px #ff1aff !important;
        }

        .status-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            animation: pulseGlow 2s infinite;
        }
        .status-pending { background: rgba(255, 255, 255, 0.3); color: #ffffff; border: 1px solid #ffffff; }
        .status-progress { background: rgba(255, 193, 7, 0.4); color: #fff3cd; border: 1px solid #ffeeba; }
        .status-dispatch { background: rgba(0, 123, 255, 0.4); color: #cce5ff; border: 1px solid #b8daff; }
        .status-completed { background: rgba(40, 167, 69, 0.4); color: #d4edda; border: 1px solid #c3e6cb; }

        input, textarea, select {
            font-size: 16px !important;
            font-weight: 700 !important;
            border-radius: 14px !important;
            border: 2px solid rgba(255, 255, 255, 0.6) !important;
            background: rgba(255, 255, 255, 0.9) !important;
            color: #ff1aff !important;
            transition: all 0.3s ease !important;
        }

        input::placeholder, textarea::placeholder {
            color: #ff66cc !important;
            opacity: 0.8;
        }

        input:focus, textarea:focus, select:focus {
            border-color: #ffffff !important;
            box-shadow: 0 0 25px #ffffff, 0 0 0 3px rgba(255, 255, 255, 0.4) !important;
            background: #ffffff !important;
            color: #ff1aff !important;
            transform: scale(1.01);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.2);
            padding: 8px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), inset 0 0 15px rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.5);
            animation: floatBounce 6s ease-in-out infinite;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            border-radius: 14px;
            font-weight: 700;
            color: #ffffff;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            text-shadow: 0 0 8px #ffffff;
        }

        .stTabs [aria-selected="true"] {
            background: #ffffff !important;
            color: #ff1aff !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), inset 0 0 15px rgba(255,255,255,0.9);
            text-shadow: none;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# 2. Multi-User Database & Admin Storage Setup
USERS_DB_FILE = "momo_users_database.json"
ADMIN_CONFIG_FILE = "momo_admin_config.json"
UPLOAD_DIR = "momo_uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users_db():
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users_db(users_data):
    with open(USERS_DB_FILE, "w") as f:
        json.dump(users_data, f)

def load_admin_config():
    default_config = {"is_locked": False, "unlock_code": "1234", "lock_id": "1"}
    if os.path.exists(ADMIN_CONFIG_FILE):
        try:
            with open(ADMIN_CONFIG_FILE, "r") as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config
    return default_config

def save_admin_config(config):
    with open(ADMIN_CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Initialize Session State Variables
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "selected_order_id" not in st.session_state:
    st.session_state.selected_order_id = None

# Global Lock Check (App locks for everyone if enabled by admin)
admin_config = load_admin_config()
if admin_config.get("is_locked", False):
    current_lock_id = admin_config.get("lock_id", "1")
    if st.session_state.get("unlocked_lock_id") != current_lock_id:
        st.markdown('<div class="momo-header">🔒 APP LOCKED 🔒</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>The application is currently locked by the administrator.</h3>
            <p>Please enter the unlock code to continue using Momo Fashion.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("unlock_form"):
            entered_unlock_code = st.text_input("Enter Unlock Code", type="password")
            unlock_submitted = st.form_submit_button("Unlock App")
            if unlock_submitted:
                if entered_unlock_code == admin_config.get("unlock_code", "1234"):
                    st.session_state.unlocked_lock_id = current_lock_id
                    st.success("App unlocked successfully!")
                    st.rerun()
                else:
                    st.error("Incorrect unlock code. Please try again.")
        st.stop()

def trigger_confetti():
    components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 120,
                spread: 80,
                origin: { y: 0.6 },
                colors: ['#ffffff', '#ff1aff', '#ff66cc', '#ff99ff']
            });
        </script>
        """, height=0)

now = datetime.datetime.now()

# 3. Authentication Screen (Login / Sign Up) if not logged in
if st.session_state.logged_in_user is None:
    st.markdown('<div class="momo-header">MOMO FASHION</div>', unsafe_allow_html=True)
    
    auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
    
    users_db = load_users_db()
    
    with auth_tab1:
        with st.form("login_form"):
            login_user = st.text_input("Username").strip().lower()
            login_pass = st.text_input("Password", type="password")
            login_sub = st.form_submit_button("Log In")
            
            if login_sub:
                if not login_user or not login_pass:
                    st.warning("Please fill in all fields.")
                elif login_user in users_db and users_db[login_user]["password"] == hash_password(login_pass):
                    st.session_state.logged_in_user = login_user
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
    with auth_tab2:
        with st.form("signup_form"):
            new_user = st.text_input("Choose Username").strip().lower()
            new_pass = st.text_input("Choose Password", type="password")
            signup_sub = st.form_submit_button("Sign Up")
            
            if signup_sub:
                if not new_user or not new_pass:
                    st.warning("Please fill in all fields.")
                elif new_user in users_db:
                    st.error("Username already exists. Please choose another or log in.")
                else:
                    users_db[new_user] = {
                        "password": hash_password(new_pass),
                        "orders": []
                    }
                    save_users_db(users_db)
                    st.session_state.logged_in_user = new_user
                    st.success("Account created and logged in successfully!")
                    st.rerun()
    st.stop()

# 4. Main App Logic for Logged-In User
current_user = st.session_state.logged_in_user
users_db = load_users_db()

if current_user not in users_db:
    users_db[current_user] = {"password": "", "orders": []}

user_orders = users_db[current_user]["orders"]

def save_current_user_orders(updated_orders):
    users_db[current_user]["orders"] = updated_orders
    save_users_db(users_db)

# Sidebar / Top Account Header & Logout
with st.sidebar:
    st.markdown(f"### 👤 Logged in as: `{current_user}`")
    if st.button("🚪 Log Out"):
        st.session_state.logged_in_user = None
        st.session_state.selected_order_id = None
        st.rerun()

# 5. Routing: Detail Page vs Main Dashboard
if st.session_state.selected_order_id is not None:
    current_order = next((o for o in user_orders if o["id"] == st.session_state.selected_order_id), None)
    
    if current_order:
        if st.button("← Back to Dashboard"):
            st.session_state.selected_order_id = None
            st.rerun()
            
        st.markdown(f'<div class="momo-header">✨ {current_order["name"]} ✨</div>', unsafe_allow_html=True)
        
        total_p = current_order.get("total_price", 0.0)
        advance_p = current_order.get("advance_paid", 0.0)
        remaining_p = total_p - advance_p
        
        status = current_order.get("status", "Pending")
        status_class = {
            "Pending": "status-pending",
            "In Progress": "status-progress",
            "Ready to Dispatch": "status-dispatch",
            "Completed": "status-completed"
        }.get(status, "status-pending")
        
        phone_val = current_order.get("phone", "")
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                <h3 style="margin:0; color: #ffffff; font-size: 1.3rem;">👤 {current_order['name']}</h3>
                <span class="status-badge {status_class}">{status}</span>
            </div>
            <p style="font-size: 1.05rem; margin-bottom: 8px; color: #ffffff;"><b>📞 Phone:</b> {phone_val if phone_val else 'None'}</p>
            <p style="font-size: 1.05rem; margin-bottom: 12px; color: #ffffff;"><b>📅 Due Date:</b> {current_order['date']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #ffffff;'>⚡ Update Status</h3>", unsafe_allow_html=True)
        status_options = ["Pending", "In Progress", "Ready to Dispatch", "Completed"]
        current_status_index = status_options.index(status) if status in status_options else 0
        new_status_val = st.selectbox("Change Order Status", status_options, index=current_status_index, key=f"status_select_{current_order['id']}")
        if new_status_val != status:
            current_order["status"] = new_status_val
            save_current_user_orders(user_orders)
            st.success(f"Status updated to {new_status_val}!")
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #ffffff;'>💰 Financial Breakdown</h3>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            st.metric("Total Bill", f"${total_p:.2f}")
        with f_col2:
            st.metric("Paid Advance", f"${advance_p:.2f}")
        with f_col3:
            st.metric("Balance Due", f"${remaining_p:.2f}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #ffffff;'>📝 Notes & Measurements</h3>", unsafe_allow_html=True)
        st.info(current_order["notes"] if current_order["notes"] else "No special notes recorded.")
        
        img_path = current_order.get("image_path")
        if img_path and os.path.exists(img_path):
            st.markdown("<br><h3 style='color: #ffffff; font-size: 1.1rem;'>📸 Design / Swatch Reference</h3>", unsafe_allow_html=True)
            st.image(img_path, caption="Reference Photo", use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Delete Order Record"):
            if img_path and os.path.exists(img_path):
                try:
                    os.remove(img_path)
                except:
                    pass
            updated_list = [o for o in user_orders if o["id"] != st.session_state.selected_order_id]
            save_current_user_orders(updated_list)
            st.session_state.selected_order_id = None
            st.rerun()
    else:
        st.session_state.selected_order_id = None
        st.rerun()

else:
    st.markdown('<div class="momo-header">MOMO FASHION</div>', unsafe_allow_html=True)

    tab_orders, tab_calc, tab_admin = st.tabs(["🛍️ Orders & Management", "🧮 Calculator", "👑 Admin Panel"])

    with tab_orders:
        with st.expander("➕ Add New Order", expanded=False):
            with st.form("order_form", clear_on_submit=True):
                customer_name = st.text_input("Customer Name")
                phone_number = st.text_input("Phone Number (Optional)")
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    total_price = st.number_input("Total Price ($)", min_value=0.0, value=0.0, step=10.0, format="%g")
                with col_p2:
                    advance_paid = st.number_input("Advance Paid ($)", min_value=0.0, value=0.0, step=10.0, format="%g")
                
                order_status = st.selectbox("Order Status", ["Pending", "In Progress", "Ready to Dispatch", "Completed"])
                
                st.markdown("<p style='margin-bottom:0px; font-weight:600; font-size:0.9rem; color:#ffffff;'>Due Date</p>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                    month_val = st.selectbox("Month", months, index=now.month - 1, label_visibility="collapsed")
                with col2:
                    day_val = st.selectbox("Day", list(range(1, 32)), index=now.day - 1, label_visibility="collapsed")
                with col3:
                    years = list(range(2024, 2035))
                    year_val = st.selectbox("Year", years, index=years.index(now.year), label_visibility="collapsed")
                
                order_notes = st.text_area("Measurements, design details, notes")
                uploaded_file = st.file_uploader("Upload Reference Photo / Swatch", type=["png", "jpg", "jpeg"])
                
                submitted = st.form_submit_button("Save Order")
                if submitted:
                    if customer_name.strip() == "":
                        st.warning("Please enter a customer name.")
                    else:
                        month_index = months.index(month_val) + 1
                        formatted_date = f"{month_index:02d}/{day_val:02d}/{year_val}"
                        
                        saved_img_path = None
                        if uploaded_file is not None:
                            file_extension = uploaded_file.name.split(".")[-1]
                            file_name = f"{datetime.datetime.now().timestamp()}_.{file_extension}"
                            saved_img_path = os.path.join(UPLOAD_DIR, file_name)
                            with open(saved_img_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                        
                        new_order_id = str(datetime.datetime.now().timestamp())
                        new_order = {
                            "id": new_order_id,
                            "name": customer_name,
                            "phone": phone_number,
                            "date": formatted_date,
                            "notes": order_notes,
                            "total_price": total_price,
                            "advance_paid": advance_paid,
                            "status": order_status,
                            "image_path": saved_img_path
                        }
                        user_orders.insert(0, new_order)
                        save_current_user_orders(user_orders)
                        trigger_confetti()
                        st.success("Order saved successfully!")
                        st.rerun()

        st.markdown("---")

        search_query = st.text_input("🔍 Search orders (Name, Phone, Notes, ID)...", "").lower()
        sort_option = st.selectbox("Sort Orders By", ["Closest Due Date", "Newest Added", "Customer Name"], label_visibility="collapsed")

        status_tab = st.radio("Filter Status", ["Pending", "In Progress", "Ready to Dispatch", "Completed"], horizontal=True)

        filtered_orders = []
        for o in user_orders:
            status_match = (o.get("status", "Pending")) == status_tab
            short_id = str(o.get("id", ""))[-6:]
            search_match = (
                search_query in o.get("name", "").lower() or
                search_query in o.get("phone", "").lower() or
                search_query in o.get("notes", "").lower() or
                search_query in short_id
            )
            if status_match and search_match:
                filtered_orders.append(o)

        if sort_option == "Closest Due Date":
            filtered_orders.sort(key=lambda x: x.get("date", "01/01/2026"))
        elif sort_option == "Newest Added":
            filtered_orders.sort(key=lambda x: float(x.get("id", 0)), reverse=True)
        else:
            filtered_orders.sort(key=lambda x: x.get("name", ""))

        if not filtered_orders:
            st.info(f"No {status_tab.lower()} orders found.")
        else:
            for o in filtered_orders:
                short_id = str(o["id"])[-6:]
                status_class = {
                    "Pending": "status-pending",
                    "In Progress": "status-progress",
                    "Ready to Dispatch": "status-dispatch",
                    "Completed": "status-completed"
                }.get(o.get("status", "Pending"), "status-pending")
                
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #ffffff;">👤 {o.get('name', 'Customer')} (ID: #{short_id})</h3>
                            <span class="status-badge {status_class}">{o.get('status', 'Pending')}</span>
                        </div>
                        <p style="font-size: 0.9rem; font-weight: 600; color: #ffffff; margin-bottom: 10px;">📞 Phone: {o.get('phone', 'None')} &nbsp;|&nbsp; 📅 Due Date: {o.get('date', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button(f"👁️ Open Full Details (#{short_id})", key=f"open_detail_{o['id']}"):
                            st.session_state.selected_order_id = o["id"]
                            st.rerun()
                    with col_act2:
                        if st.button(f"🗑️ Delete (#{short_id})", key=f"del_{o['id']}"):
                            img_path = o.get("image_path")
                            if img_path and os.path.exists(img_path):
                                try:
                                    os.remove(img_path)
                                except:
                                    pass
                            updated_list = [item for item in user_orders if item["id"] != o["id"]]
                            save_current_user_orders(updated_list)
                            st.success("Order deleted successfully!")
                            st.rerun()

    with tab_calc:
        st.markdown("<h3 style='color: #ffffff; text-align: center; margin-bottom: 15px; text-shadow: 0 0 15px #ffffff;'>Momo Calculator</h3>", unsafe_allow_html=True)
        
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&display=swap');
            body {
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: transparent;
                margin: 0;
                padding: 10px;
                display: flex;
                justify-content: center;
            }
            @keyframes floatBounce {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-5px); }
            }
            .calc-box {
                width: 100%;
                max-width: 380px;
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                padding: 22px;
                border-radius: 28px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 255, 255, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.6);
                animation: floatBounce 4s ease-in-out infinite;
            }
            .calc-screen {
                background: #121212;
                color: #ffffff;
                padding: 18px 22px;
                border-radius: 20px;
                font-size: 2.3rem;
                text-align: right;
                font-weight: 700;
                margin-bottom: 16px;
                word-break: break-all;
                box-shadow: inset 0 4px 12px rgba(0,0,0,0.8), 0 0 15px rgba(255, 255, 255, 0.5);
                letter-spacing: 1px;
                min-height: 55px;
            }
            .calc-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
            }
            .calc-btn {
                background: rgba(255, 255, 255, 0.25);
                color: #ffffff;
                font-size: 1.25rem;
                font-weight: 700;
                border-radius: 16px;
                min-height: 56px;
                border: 2px solid rgba(255, 255, 255, 0.5);
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 255, 255, 0.3);
                text-shadow: 0 0 8px #ffffff;
                user-select: none;
            }
            .calc-btn:hover {
                background: #ffffff;
                color: #ff1aff;
                border-color: #ffffff;
                transform: translateY(-4px) scale(1.05);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 25px #ffffff;
                text-shadow: none;
            }
            .calc-btn:active {
                transform: scale(0.92);
            }
            .span-2 {
                grid-column: span 2;
            }
        </style>
        </head>
        <body>
            <div class="calc-box">
                <div id="screen" class="calc-screen">0</div>
                <div class="calc-grid">
                    <button class="calc-btn" onclick="press('C')">C</button>
                    <button class="calc-btn" onclick="press('⌫')">⌫</button>
                    <button class="calc-btn" onclick="press('/')">/</button>
                    <button class="calc-btn" onclick="press('*')">*</button>
                    
                    <button class="calc-btn" onclick="press('7')">7</button>
                    <button class="calc-btn" onclick="press('8')">8</button>
                    <button class="calc-btn" onclick="press('9')">9</button>
                    <button class="calc-btn" onclick="press('-')">-</button>
                    
                    <button class="calc-btn" onclick="press('4')">4</button>
                    <button class="calc-btn" onclick="press('5')">5</button>
                    <button class="calc-btn" onclick="press('6')">6</button>
                    <button class="calc-btn" onclick="press('+')">+</button>
                    
                    <button class="calc-btn" onclick="press('1')">1</button>
                    <button class="calc-btn" onclick="press('2')">2</button>
                    <button class="calc-btn" onclick="press('3')">3</button>
                    <button class="calc-btn" onclick="press('=')">=</button>
                    
                    <button class="calc-btn span-2" onclick="press('0')">0</button>
                    <button class="calc-btn span-2" onclick="press('.')">.</button>
                </div>
            </div>

            <script>
                let currentVal = "0";
                const screen = document.getElementById("screen");

                function press(val) {
                    if (val === 'C') {
                        currentVal = "0";
                    } else if (val === '⌫') {
                        currentVal = currentVal.length > 1 ? currentVal.slice(0, -1) : "0";
                    } else if (val === '=') {
                        try {
                            let sanitized = currentVal.replace(/×/g, '*').replace(/÷/g, '/');
                            let result = eval(sanitized);
                            currentVal = String(result);
                        } catch (e) {
                            currentVal = "Error";
                        }
                    } else {
                        if (currentVal === "0" || currentVal === "Error") {
                            currentVal = val;
                        } else {
                            currentVal += val;
                        }
                    }
                    screen.innerText = currentVal;
                }
            </script>
        </body>
        </html>
        """, height=420)

    with tab_admin:
        st.markdown("<h3 style='color: #ffffff; text-align: center; margin-bottom: 15px; text-shadow: 0 0 15px #ffffff;'>👑 Admin Panel</h3>", unsafe_allow_html=True)
        
        if not st.session_state.get("admin_logged_in", False):
            with st.form("admin_login_form"):
                admin_pass_input = st.text_input("Enter Admin Password", type="password")
                admin_login_submitted = st.form_submit_button("Login")
                if admin_login_submitted:
                    if admin_pass_input == "123312":
                        st.session_state.admin_logged_in = True
                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect admin password. Please try again.")
        else:
            st.success("Authenticated as Administrator")
            if st.button("Logout Admin"):
                st.session_state.admin_logged_in = False
                st.rerun()
                
            st.markdown("---")
            current_admin_config = load_admin_config()
            
            with st.form("admin_config_form"):
                is_globally_locked = st.toggle("🔒 Lock App for Everyone", value=current_admin_config.get("is_locked", False))
                new_unlock_code = st.text_input("Current Unlock Code (Edit to change)", value=current_admin_config.get("unlock_code", "1234"))
                
                admin_save_sub = st.form_submit_button("Save Admin Settings")
                if admin_save_sub:
                    current_admin_config["is_locked"] = is_globally_locked
                    current_admin_config["unlock_code"] = new_unlock_code
                    if is_globally_locked:
                        current_admin_config["lock_id"] = str(datetime.datetime.now().timestamp())
                    else:
                        current_admin_config["lock_id"] = "1"
                    save_admin_config(current_admin_config)
                    st.success("Admin settings updated successfully!")
                    st.rerun()
