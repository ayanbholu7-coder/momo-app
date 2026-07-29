import datetime
import json
import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup & Animated Full Pink Theme
st.set_page_config(
    page_title="Momo Fashion",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# 2. Optimized Permanent Server-Side JSON Storage
DB_FILE = "momo_persistent_orders.json"
UPLOAD_DIR = "momo_uploads"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)


@st.cache_data(ttl=60)
def load_orders_cached():
  if os.path.exists(DB_FILE):
    try:
      with open(DB_FILE, "r") as f:
        return json.load(f)
    except:
      return []
  return []


def save_orders(orders_list):
  with open(DB_FILE, "w") as f:
    json.dump(orders_list, f)
  st.cache_data.clear()


if "orders" not in st.session_state:
  st.session_state.orders = load_orders_cached()

if "selected_order_id" not in st.session_state:
  st.session_state.selected_order_id = None


def trigger_confetti():
  components.html(
      """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 120,
                spread: 80,
                origin: { y: 0.6 },
                colors: ['#ffffff', '#ff1aff', '#ff66cc', '#ff99ff']
            });
        </script>
        """,
      height=0,
  )


now = datetime.datetime.now()

# 4. Routing: Detail Page vs Main Dashboard
if st.session_state.selected_order_id is not None:
  current_order = next(
      (
          o
          for o in st.session_state.orders
          if o["id"] == st.session_state.selected_order_id
      ),
      None,
  )

  if current_order:
    if st.button("← Back to Dashboard"):
      st.session_state.selected_order_id = None
      st.rerun()

    st.markdown(
        f'<div class="momo-header">✨ {current_order["name"]} ✨</div>',
        unsafe_allow_html=True,
    )

    total_p = current_order.get("total_price", 0.0)
    advance_p = current_order.get("advance_paid", 0.0)
    remaining_p = total_p - advance_p

    status = current_order.get("status", "Pending")
    status_class = {
        "Pending": "status-pending",
        "In Progress": "status-progress",
        "Ready to Dispatch": "status-dispatch",
        "Completed": "status-completed",
    }.get(status, "status-pending")

    phone_val = current_order.get("phone", "")

    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                <h3 style="margin:0; color: #ffffff; font-size: 1.3rem;">👤 {current_order['name']}</h3>
                <span class="status-badge {status_class}">{status}</span>
            </div>
            <p style="font-size: 1.05rem; margin-bottom: 8px; color: #ffffff;"><b>📞 Phone:</b> {phone_val if phone_val else 'None'}</p>
            <p style="font-size: 1.05rem; margin-bottom: 12px; color: #ffffff; text-shadow: 0 0 10px #ffffff;"><b>📅 Due Date:</b> {current_order['date']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h3 style='color: #ffffff;'>⚡ Update Status</h3>",
        unsafe_allow_html=True,
    )
    status_options = [
        "Pending",
        "In Progress",
        "Ready to Dispatch",
        "Completed",
    ]
    current_status_index = (
        status_options.index(status) if status in status_options else 0
    )
    new_status_val = st.selectbox(
        "Change Order Status",
        status_options,
        index=current_status_index,
        key=f"status_select_{current_order['id']}",
    )
    if new_status_val != status:
      current_order["status"] = new_status_val
      save_orders(st.session_state.orders)
      st.success(f"Status updated to {new_status_val}!")
      st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color: #ffffff;'>💰 Financial Breakdown</h3>",
        unsafe_allow_html=True,
    )
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
      st.metric("Total Bill", f"${total_p:.2f}")
    with f_col2:
      st.metric("Paid Advance", f"${advance_p:.2f}")
    with f_col3:
      st.metric("Balance Due", f"${remaining_p:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color: #ffffff;'>📝 Notes & Measurements</h3>",
        unsafe_allow_html=True,
    )
    st.info(
        current_order["notes"]
        if current_order["notes"]
        else "No special notes recorded."
    )

    img_path = current_order.get("image_path")
    if img_path and os.path.exists(img_path):
      st.markdown(
          "<br><h3 style='color: #ffffff; font-size: 1.1rem;'>📸 Design /"
          " Swatch Reference</h3>",
          unsafe_allow_html=True,
      )
      st.image(img_path, caption="Reference Photo", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Delete Order Record"):
      if img_path and os.path.exists(img_path):
        try:
          os.remove(img_path)
        except:
          pass
      st.session_state.orders = [
          o
          for o in st.session_state.orders
          if o["id"] != st.session_state.selected_order_id
      ]
      save_orders(st.session_state.orders)
      st.session_state.selected_order_id = None
      st.rerun()
  else:
    st.session_state.selected_order_id = None
    st.rerun()

else:
  st.markdown(
      '<div class="momo-header">MOMO FASHION</div>', unsafe_allow_html=True
  )

  tab_orders, tab_calc = st.tabs(["🛍️ Orders & Management", "🧮 Calculator"])

  with tab_orders:
    with st.expander("➕ Add New Order", expanded=False):
      with st.form("order_form", clear_on_submit=True):
        customer_name = st.text_input("Customer Name")
        phone_number = st.text_input("Phone Number (Optional)")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
          total_price = st.number_input(
              "Total Price ($)", min_value=0.0, value=0.0, step=10.0, format="%g"
          )
        with col_p2:
          advance_paid = st.number_input(
              "Advance Paid ($)",
              min_value=0.0,
              value=0.0,
              step=10.0,
              format="%g",
          )

        order_status = st.selectbox(
            "Order Status",
            ["Pending", "In Progress", "Ready to Dispatch", "Completed"],
        )

        st.markdown(
            "<p"
            " style='margin-bottom:0px; font-weight:600; font-size:0.9rem;"
            " color:#ffffff;'>Due Date</p>",
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns(3)
        with col1:
          months = [
              "January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December",
          ]
          month_val = st.selectbox(
              "Month",
              months,
              index=now.month - 1,
              label_visibility="collapsed",
          )
        with col2:
          day_val = st.selectbox(
              "Day",
              list(range(1, 32)),
              index=now.day - 1,
              label_visibility="collapsed",
          )
        with col3:
          years = list(range(2024, 2035))
          year_val = st.selectbox(
              "Year",
              years,
              index=years.index(now.year),
              label_visibility="collapsed",
          )

        order_notes = st.text_area(
            "Measurements, design details, notes (Phone number optional here)"
        )
        uploaded_file = st.file_uploader(
            "Upload Reference Photo / Swatch", type=["png", "jpg", "jpeg"]
        )

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
              file_name = (
                  f"{datetime.datetime.now().timestamp()}_.{file_extension}"
              )
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
                "image_path": saved_img_path,
            }
            st.session_state.orders.insert(0, new_order)
            save_orders(st.session_state.orders)
            trigger_confetti()
            st.success("Order & Barcode ID generated successfully!")
            st.rerun()

    st.markdown("---")

    orders_json_string = json.dumps(st.session_state.orders)

    html_template = """
        <!DOCTYPE html>
        <html>
        <head>
        <script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
            body {
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: transparent;
                margin: 0;
                padding: 10px;
                color: #ffffff;
            }
            .toolbar {
                display: flex;
                gap: 12px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            .search-input, .sort-select {
                flex: 1;
                min-width: 200px;
                padding: 14px 18px;
                font-size: 16px;
                font-weight: 700;
                border-radius: 16px;
                border: 2px solid rgba(255, 255, 255, 0.6);
                background: rgba(255, 255, 255, 0.9);
                color: #ff1aff;
                outline: none;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }
            .search-input::placeholder {
                color: #ff66cc;
                opacity: 0.8;
            }
            .search-input:focus, .sort-select:focus {
                border-color: #ffffff;
                box-shadow: 0 0 25px #ffffff;
                background: #ffffff;
            }
            .tabs-header {
                display: flex;
                gap: 8px;
                background: rgba(255, 255, 255, 0.2);
                padding: 8px;
                border-radius: 20px;
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.5);
                margin-bottom: 20px;
                overflow-x: auto;
            }
            .tab-btn {
                flex: 1;
                min-width: 120px;
                height: 48px;
                background: transparent;
                border: none;
                border-radius: 14px;
                font-weight: 700;
                color: #ffffff;
                cursor: pointer;
                transition: all 0.25s ease;
                text-shadow: 0 0 8px #ffffff;
                font-size: 0.95rem;
            }
            .tab-btn.active {
                background: #ffffff;
                color: #ff1aff;
                box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                text-shadow: none;
                transform: scale(1.03);
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.18);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 24px;
                padding: 22px;
                margin-bottom: 18px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;
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
            }
            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                flex-wrap: wrap;
                gap: 8px;
            }
            .card-title {
                margin: 0;
                font-size: 1.2rem;
                font-weight: 800;
                color: #ffffff;
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
            }
            .status-Pending { background: rgba(255, 255, 255, 0.3); color: #ffffff; border: 1px solid #ffffff; }
            .status-In-Progress { background: rgba(255, 193, 7, 0.4); color: #fff3cd; border: 1px solid #ffeeba; }
            .status-Ready-to-Dispatch { background: rgba(0, 123, 255, 0.4); color: #cce5ff; border: 1px solid #b8daff; }
            .status-Completed { background: rgba(40, 167, 69, 0.4); color: #d4edda; border: 1px solid #c3e6cb; }

            .meta-text {
                font-size: 0.9rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 12px;
                text-shadow: 0 0 8px #ffffff;
            }
            .notes-textarea {
                width: 100%;
                min-height: 55px;
                max-height: 120px;
                padding: 8px 12px;
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.6);
                background: rgba(255, 255, 255, 0.9);
                color: #ff1aff;
                font-weight: 700;
                font-size: 0.9rem;
                line-height: 1.3;
                resize: vertical;
                box-sizing: border-box;
                outline: none;
                margin-bottom: 10px;
            }
            .notes-textarea::placeholder {
                color: #ff66cc;
                opacity: 0.8;
            }
            .notes-textarea:focus {
                border-color: #ffffff;
                background: #ffffff;
                box-shadow: 0 0 20px #ffffff;
            }
            .action-row {
                display: flex;
                gap: 10px;
                align-items: center;
                flex-wrap: wrap;
                margin-top: 10px;
            }
            .action-select {
                padding: 10px 14px;
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.6);
                background: #ffffff;
                color: #ff1aff;
                font-weight: 700;
                font-size: 0.9rem;
                outline: none;
                cursor: pointer;
            }
            .save-note-btn {
                background: rgba(255, 255, 255, 0.9);
                color: #ff1aff;
                border: 2px solid #ffffff;
                padding: 10px 18px;
                border-radius: 12px;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.2s ease;
            }
            .save-note-btn:hover {
                background: #ff1aff;
                color: #ffffff;
                box-shadow: 0 0 20px #ff1aff;
            }
            .delete-note-btn {
                background: rgba(255, 77, 77, 0.3);
                color: #ffffff;
                border: 2px solid #ff4d4d;
                padding: 10px 16px;
                border-radius: 12px;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.2s ease;
            }
            .delete-note-btn:hover {
                background: #ff4d4d;
                color: #ffffff;
                box-shadow: 0 0 20px #ff4d4d;
            }
            .barcode-container {
                background: #ffffff;
                padding: 10px;
                border-radius: 12px;
                display: inline-block;
                margin-top: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .empty-state {
                text-align: center;
                padding: 30px;
                font-weight: 700;
                color: #ffffff;
                font-size: 1.1rem;
                text-shadow: 0 0 10px #ffffff;
            }
        </style>
        </head>
        <body>
            <div class="toolbar">
                <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search orders, notes, phone, ID..." oninput="renderOrders()">
                <select id="sortSelect" class="sort-select" onchange="renderOrders()">
                    <option value="due">Sort: Closest Due Date</option>
                    <option value="newest">Sort: Newest Added</option>
                    <option value="name">Sort: Customer Name</option>
                </select>
            </div>

            <div class="tabs-header">
                <button class="tab-btn active" id="tab_Pending" onclick="switchTab('Pending')">⏳ Pending</button>
                <button class="tab-btn" id="tab_In_Progress" onclick="switchTab('In Progress')">🚀 In Progress</button>
                <button class="tab-btn" id="tab_Ready_to_Dispatch" onclick="switchTab('Ready to Dispatch')">📦 Ready to Dispatch</button>
                <button class="tab-btn" id="tab_Completed" onclick="switchTab('Completed')">✅ Completed</button>
            </div>

            <div id="ordersContainer"></div>

            <script>
                const serverOrders = __ORDERS_JSON__;
                const storageKey = "momo_permanent_client_orders_v1";
                
                function getOrders() {
                    const localData = localStorage.getItem(storageKey);
                    if (localData) {
                        try {
                            const parsed = JSON.parse(localData);
                            if (Array.isArray(parsed) && parsed.length >= serverOrders.length) {
                                return parsed;
                            }
                        } catch(e) {}
                    }
                    localStorage.setItem(storageKey, JSON.stringify(serverOrders));
                    return serverOrders;
                }

                let orders = getOrders();
                let currentTab = "Pending";

                function switchTab(tabName) {
                    currentTab = tabName;
                    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                    const activeBtnId = 'tab_' + tabName.replace(/ /g, '_');
                    const targetBtn = document.getElementById(activeBtnId);
                    if (targetBtn) targetBtn.classList.add('active');
                    renderOrders();
                }

                function updateOrderField(id, field, value) {
                    const idx = orders.findIndex(o => o.id === id);
                    if (idx !== -1) {
                        orders[idx][field] = value;
                        localStorage.setItem(storageKey, JSON.stringify(orders));
                    }
                }

                function saveNoteAndStatus(id) {
                    const noteEl = document.getElementById('note_' + id);
                    const statusEl = document.getElementById('status_' + id);
                    if (noteEl && statusEl) {
                        const idx = orders.findIndex(o => o.id === id);
                        if (idx !== -1) {
                            orders[idx].notes = noteEl.value;
                            orders[idx].status = statusEl.value;
                            localStorage.setItem(storageKey, JSON.stringify(orders));
                            renderOrders();
                        }
                    }
                }

                function deleteOrderRecord(id) {
                    orders = orders.filter(o => o.id !== id);
                    localStorage.setItem(storageKey, JSON.stringify(orders));
                    renderOrders();
                }

                function renderOrders() {
                    const search = document.getElementById('searchInput').value.toLowerCase();
                    const sort = document.getElementById('sortSelect').value;
                    const container = document.getElementById('ordersContainer');

                    const filtered = orders.filter(o => {
                        const matchesTab = (o.status || "Pending") === currentTab;
                        const shortId = String(o.id).slice(-6);
                        const matchesSearch = (o.name || "").toLowerCase().includes(search) ||
                                          (o.phone || "").toLowerCase().includes(search) ||
                                          (o.notes || "").toLowerCase().includes(search) ||
                                          shortId.includes(search);
                        return matchesTab && matchesSearch;
                    });

                    filtered.sort((a, b) => {
                        if (sort === 'due') {
                            const dateA = new Date(a.date || '01/01/2026');
                            const dateB = new Date(b.date || '01/01/2026');
                            return dateA - dateB;
                        } else if (sort === 'newest') {
                            return parseFloat(b.id || 0) - parseFloat(a.id || 0);
                        } else {
                            return (a.name || "").localeCompare(b.name || "");
                        }
                    });

                    if (filtered.length === 0) {
                        container.innerHTML = `<div class="empty-state">No ${currentTab.toLowerCase()} orders found.</div>`;
                        return;
                    }

                    let html = '';
                    filtered.forEach(o => {
                        const badgeClass = 'status-' + (o.status || "Pending").replace(/ /g, '-');
                        const shortId = String(o.id).slice(-6);
                        const customerNameSafe = o.name || 'Customer';
                        const orderDateSafe = o.date || 'N/A';

                        html += `
                            <div class="glass-card">
                                <div class="card-header">
                                    <h3 class="card-title">👤 ${customerNameSafe} (ID: #${shortId})</h3>
                                    <span class="status-badge ${badgeClass}">${o.status || 'Pending'}</span>
                                </div>
                                <div class="meta-text">📞 Phone: ${o.phone || 'None'} &nbsp;|&nbsp; 📅 Due Date: ${orderDateSafe}</div>
                                
                                <div style="margin-bottom: 12px;">
                                    <div class="barcode-container">
                                        <svg id="barcode_${o.id}"></svg>
                                    </div>
                                </div>

                                <textarea id="note_${o.id}" class="notes-textarea" placeholder="Add measurements, notes, or design instructions..." oninput="updateOrderField('${o.id}', 'notes', this.value)">${o.notes || ''}</textarea>
                                <div class="action-row">
                                    <select id="status_${o.id}" class="action-select" onchange="updateOrderField('${o.id}', 'status', this.value)">
                                        <option value="Pending" ${o.status === 'Pending' ? 'selected' : ''}>⏳ Pending</option>
                                        <option value="In Progress" ${o.status === 'In Progress' ? 'selected' : ''}>🚀 In Progress</option>
                                        <option value="Ready to Dispatch" ${o.status === 'Ready to Dispatch' ? 'selected' : ''}>📦 Ready to Dispatch</option>
                                        <option value="Completed" ${o.status === 'Completed' ? 'selected' : ''}>✅ Completed</option>
                                    </select>
                                    <button class="save-note-btn" onclick="saveNoteAndStatus('${o.id}')">💾 Save Note & Status</button>
                                    <button class="delete-note-btn" onclick="deleteOrderRecord('${o.id}')">🗑️ Delete Order</button>
                                </div>
                            </div>
                        `;
                    });
                    container.innerHTML = html;

                    filtered.forEach(o => {
                        const shortId = String(o.id).slice(-6);
                        try {
                            JsBarcode("#barcode_" + o.id, shortId, {
                                format: "CODE128",
                                width: 1.5,
                                height: 40,
                                displayValue: true,
                                fontSize: 12
                            });
                        } catch(e) {}
                    });
                }

                renderOrders();
            </script>
        </body>
        </html>
        """

    final_html = html_template.replace("__ORDERS_JSON__", orders_json_string)
    components.html(final_html, height=700)

  with tab_calc:
    st.markdown(
        "<h3 style='color: #ffffff; text-align: center; margin-bottom: 15px;"
        " text-shadow: 0 0 15px #ffffff;'>Momo Calculator</h3>",
        unsafe_allow_html=True,
    )

    components.html(
        """
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
        """,
        height=420,
    )
