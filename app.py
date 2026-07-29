import datetime
import json
import os
import streamlit as st

# 1. Page Setup & Ultra-Mobile-Responsive Glassmorphism Styling
st.set_page_config(
    page_title="Momo Fashion",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

        :root {
            --bg-gradient: linear-gradient(135deg, #fff0f3 0%, #ffe3ec 50%, #ffd1dc 100%);
            --card-bg: rgba(255, 255, 255, 0.85);
            --text-primary: #1a1a1a;
            --accent-pink: #ff3385;
            --accent-hover: #ff1a75;
            --border-color: #ffb3d1;
        }

        .stApp {
            background: var(--bg-gradient);
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', sans-serif;
            animation: fadeInApp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes fadeInApp {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Fixed letter spacing: tighter and normal padding */
        .momo-header {
            text-align: center;
            font-size: clamp(2rem, 7vw, 2.8rem);
            font-weight: 800;
            background: linear-gradient(45deg, #ff1a75, #ff66b2, #ff3385, #ff1a75);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
            animation: gradientShift 8s ease infinite;
            text-shadow: 0 5px 15px rgba(255, 51, 133, 0.08);
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Butter-smooth card hover and entry animations */
        .order-card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 16px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.9);
            margin-bottom: 14px;
            box-shadow: 0 8px 25px rgba(255, 51, 133, 0.05);
            position: relative;
            overflow: hidden;
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        .order-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(255, 51, 133, 0.12);
        }

        @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .order-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: #ff1a75;
        }

        /* High-Impact Touch Buttons with fluid micro-interactions */
        div.stButton > button {
            background: #1a1a1a;
            color: white;
            border-radius: 14px;
            font-weight: 600;
            border: none;
            width: 100%;
            padding: 12px;
            min-height: 48px;
            font-size: 1rem;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        div.stButton > button:hover {
            background: #ff1a75;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(255, 51, 133, 0.25);
        }

        div.stButton > button:active {
            transform: scale(0.96) translateY(0);
        }

        /* Calculator Specific Button Styling & Layout Fix */
        .calc-btn-container div.stButton > button {
            background: #2a2a2a !important;
            color: #ffffff !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            border-radius: 14px !important;
            min-height: 54px !important;
            border: 1px solid rgba(255, 51, 133, 0.2) !important;
            transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }

        .calc-btn-container div.stButton > button:hover {
            background: #ff1a75 !important;
            border-color: #ff1a75 !important;
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 20px rgba(255, 26, 117, 0.3) !important;
        }

        /* Responsive Detail Card */
        .detail-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(12px);
            padding: 22px;
            border-radius: 22px;
            border: 1px solid #ffb3d1;
            box-shadow: 0 12px 35px rgba(255, 51, 133, 0.1);
            animation: scaleIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.97); }
            to { opacity: 1; transform: scale(1); }
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .status-pending { background: #ffe6eb; color: #ff1a75; }
        .status-progress { background: #fff3cd; color: #856404; }
        .status-fitting { background: #cce5ff; color: #004085; }
        .status-completed { background: #d4edda; color: #155724; }

        input, textarea, select {
            font-size: 16px !important;
            border-radius: 12px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        input:focus, textarea:focus {
            border-color: #ff3385 !important;
            box-shadow: 0 0 0 3px rgba(255, 51, 133, 0.15) !important;
        }

        /* Custom Streamlit Tabs Styling for Smooth Feel */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(255, 255, 255, 0.6);
            padding: 6px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(255, 51, 133, 0.04);
        }

        .stTabs [data-baseweb="tab"] {
            height: 46px;
            border-radius: 12px;
            font-weight: 700;
            color: #1a1a1a;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background-color: #ff1a75 !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(255, 26, 117, 0.3);
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

if "calc_input" not in st.session_state:
  st.session_state.calc_input = "0"

# 3. Monthly Lock System
SECRET_CODE = "momo2026"
now = datetime.datetime.now()
current_month_year = f"{now.month}-{now.year}"

if "unlocked_month" not in st.session_state:
  st.session_state.unlocked_month = ""

is_first_of_month = now.day == 1
needs_unlock = (
    is_first_of_month and st.session_state.unlocked_month != current_month_year
)

if needs_unlock:
  st.markdown("---")
  st.markdown(
      "<h2 style='text-align: center; color: #ff1a75;'>🔒 App Locked</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #666;'>New billing cycle started."
      " Enter code to unlock.</p>",
      unsafe_allow_html=True,
  )

  entered_code = st.text_input("Unlock Code", type="password")
  if st.button("Unlock App"):
    if entered_code == SECRET_CODE:
      st.session_state.unlocked_month = current_month_year
      st.success("Unlocked successfully!")
      st.rerun()
    else:
      st.error("Incorrect code!")
  st.stop()


# 4. Calculator Action Handler via Callbacks
def press_calc(val):
  current = st.session_state.calc_input
  if val == "C":
    st.session_state.calc_input = "0"
  elif val == "⌫":
    st.session_state.calc_input = current[:-1] if len(current) > 1 else "0"
  elif val == "=":
    try:
      # Safe evaluation of basic math expression
      allowed_chars = set("0123456789+-*. /")
      if all(c in allowed_chars for c in current):
        res = eval(current)
        st.session_state.calc_input = str(res)
      else:
        st.session_state.calc_input = "Error"
    except Exception:
      st.session_state.calc_input = "Error"
  else:
    if current == "0" or current == "Error":
      st.session_state.calc_input = val
    else:
      st.session_state.calc_input += val


# 5. Routing: Detail Page vs Main Tabs Interface
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
    if st.button("← Back to Orders"):
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
        "Fitting Ready": "status-fitting",
        "Completed": "status-completed",
    }.get(status, "status-pending")

    st.markdown(
        f"""
        <div class="detail-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <h3 style="margin:0; color: #1a1a1a; font-size: 1.2rem;">👤 {current_order['name']}</h3>
                <span class="status-badge {status_class}">{status}</span>
            </div>
            <p style="font-size: 1rem; margin-bottom: 8px; color: #1a1a1a;"><b>📞 Phone:</b> {current_order['phone'] if current_order['phone'] else 'None'}</p>
            <p style="font-size: 1rem; margin-bottom: 12px; color: #ff1a75;"><b>📅 Due Date:</b> {current_order['date']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💰 Financials")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
      st.metric("Total", f"${total_p:.2f}")
    with f_col2:
      st.metric("Paid", f"${advance_p:.2f}")
    with f_col3:
      st.metric("Left", f"${remaining_p:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📝 Notes & Measurements")
    st.info(
        current_order["notes"]
        if current_order["notes"]
        else "No notes added."
    )

    img_path = current_order.get("image_path")
    if img_path and os.path.exists(img_path):
      st.markdown(
          "<br><h3 style='color: #ff1a75; font-size: 1.1rem;'>📸 Design /"
          " Swatch Reference</h3>",
          unsafe_allow_html=True,
      )
      st.image(img_path, caption="Reference Photo", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Delete This Order"):
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

  # Top-Level Tabs for Orders Management vs Calculator
  tab_orders, tab_calc = st.tabs(["🛍️ Orders & Management", "🧮 Calculator"])

  with tab_orders:
    with st.expander("➕ Add New Order", expanded=False):
      with st.form("order_form", clear_on_submit=True):
        customer_name = st.text_input("Customer Name")
        phone_number = st.text_input("Phone Number")

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
            ["Pending", "In Progress", "Fitting Ready", "Completed"],
        )

        st.markdown(
            "<p"
            " style='margin-bottom:0px; font-weight:600; font-size:0.9rem;'>Due"
            " Date</p>",
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

        order_notes = st.text_area("Measurements, design details...")
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

            new_order = {
                "id": str(datetime.datetime.now().timestamp()),
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
            st.success("Saved permanently!")
            st.rerun()

    st.markdown("---")

    # Search and Filter Toolbar
    search_term = st.text_input(
        "🔍 Search orders...", placeholder="Type name, phone, or notes..."
    ).lower()
    sort_option = st.selectbox(
        "Sort By", ["Closest Due Date", "Newest Added", "Customer Name"]
    )

    filtered_orders = [
        o
        for o in st.session_state.orders
        if search_term in o["name"].lower()
        or search_term in o["phone"].lower()
        or search_term in o["notes"].lower()
    ]


    def get_sorting_key(order_item):
      if sort_option == "Closest Due Date":
        try:
          return datetime.datetime.strptime(order_item["date"], "%m/%d/%Y")
        except:
          return datetime.datetime.max
      elif sort_option == "Newest Added":
        return -float(order_item["id"])
      else:
        return order_item["name"].lower()


    filtered_orders.sort(key=get_sorting_key)

    if not filtered_orders:
      st.info("No orders found.")
    else:
      for order in filtered_orders:
        status = order.get("status", "Pending")
        status_class = {
            "Pending": "status-pending",
            "In Progress": "status-progress",
            "Fitting Ready": "status-fitting",
            "Completed": "status-completed",
        }.get(status, "status-pending")

        st.markdown(
            f"""
            <div class="order-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">
                    <h3 style="margin: 0; color: #1a1a1a; font-size: 1.1rem;">👤 {order['name']}</h3>
                    <span class="status-badge {status_class}">{status}</span>
                </div>
                <p style="font-size: 0.85rem; color: #ff1a75; font-weight: 600; margin-bottom: 0px;">📅 Due Date: {order['date']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("📄 View Details & Notes", key=f"view_{order['id']}"):
          st.session_state.selected_order_id = order["id"]
          st.rerun()

  with tab_calc:
    st.markdown(
        "<h3 style='color: #ff1a75; text-align: center; margin-bottom:"
        " 15px;'>Momo Calculator</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background: #1a1a1a; color: #fff; padding: 18px; border-radius: 16px; font-size: 2rem; text-align: right; font-weight: 700; margin-bottom: 15px; word-break: break-all; box-shadow: inset 0 2px 6px rgba(0,0,0,0.4);">
            {st.session_state.calc_input}
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_rows = [
        ["C", "⌫", "/", "*"],
        ["7", "8", "9", "-"],
        ["4", "5", "6", "+"],
        ["1", "2", "3", "="],
        ["0", "."],
    ]

    st.markdown('<div class="calc-btn-container">', unsafe_allow_html=True)
    for row in c_rows:
      cols = st.columns(len(row))
      for idx, btn_label in enumerate(row):
        with cols[idx]:
          st.button(
              btn_label,
              key=f"calc_key_{btn_label}_{idx}",
              on_click=press_calc,
              args=(btn_label,),
          )
    st.markdown("</div>", unsafe_allow_html=True)
