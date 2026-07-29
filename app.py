import datetime
import json
import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup & Full Vibrant Pink Background with White Glowing Text Outlines
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
            --vibrant-pink: #ff1aff;
            --glass-bg: rgba(255, 255, 255, 0.12);
            --glass-border: rgba(255, 255, 255, 0.35);
            --text-main: #ffffff;
        }

        .stApp {
            background: linear-gradient(135deg, #ff1aff 0%, #e600e6 50%, #b300b3 100%);
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* 3D Floating Glowing Header - Vibrant Pink Text with White Glow Outline */
        .momo-header {
            text-align: center;
            font-size: clamp(2.4rem, 8vw, 3.4rem);
            font-weight: 800;
            color: #ff1aff;
            margin-bottom: 25px;
            letter-spacing: -1px;
            -webkit-text-stroke: 1.5px #ffffff;
            text-shadow: 0 0 10px #ffffff, 0 0 20px #ffffff, 0 0 35px rgba(255, 255, 255, 0.8), 0 4px 15px rgba(0,0,0,0.3);
            animation: float3D 4s ease-in-out infinite;
            transform-style: preserve-3d;
        }

        @keyframes float3D {
            0%, 100% { transform: translateY(0px) rotateX(0deg); text-shadow: 0 0 10px #ffffff, 0 0 20px #ffffff, 0 0 35px rgba(255, 255, 255, 0.8), 0 4px 15px rgba(0,0,0,0.3); }
            50% { transform: translateY(-8px) rotateX(4deg); text-shadow: 0 0 15px #ffffff, 0 0 30px #ffffff, 0 0 50px rgba(255, 255, 255, 1), 0 10px 25px rgba(0,0,0,0.4); }
        }

        /* General Headings and Labels with White Glow Outline */
        h1, h2, h3, h4, h5, h6, label, .stMarkdown p, span {
            color: #ffffff;
        }

        h3, h2 {
            -webkit-text-stroke: 0.5px #ffffff;
            text-shadow: 0 0 8px #ffffff, 0 0 15px rgba(255, 255, 255, 0.6);
        }

        /* 3D Glassmorphism Cards on Full Pink Background */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 18px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2), inset 0 0 15px rgba(255, 255, 255, 0.15);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            transform: perspective(1000px) rotateX(0deg) translateZ(0px);
        }

        .glass-card:hover {
            transform: perspective(1000px) translateY(-6px) rotateX(2deg) translateZ(10px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), 0 0 25px rgba(255, 255, 255, 0.4);
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
        }

        /* 3D High-End Interactive Buttons with White Glow */
        div.stButton > button {
            background: rgba(255, 255, 255, 0.15);
            color: #ffffff;
            border-radius: 16px;
            font-weight: 700;
            border: 2px solid rgba(255, 255, 255, 0.6);
            width: 100%;
            padding: 14px;
            min-height: 52px;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2), 0 0 10px rgba(255, 255, 255, 0.2);
            text-shadow: 0 0 8px #ffffff;
            transform: perspective(1000px) translateZ(0px);
        }

        div.stButton > button:hover {
            background: #ffffff;
            color: #ff1aff;
            border-color: #ffffff;
            transform: perspective(1000px) translateY(-4px) translateZ(15px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 30px #ffffff;
            text-shadow: none;
        }

        div.stButton > button:active {
            transform: scale(0.95) translateY(0);
        }

        /* Status Badges */
        .status-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
        }
        .status-pending { background: rgba(255, 255, 255, 0.2); color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.6); }
        .status-progress { background: rgba(255, 193, 7, 0.3); color: #fff3cd; border: 1px solid #ffeeba; }
        .status-fitting { background: rgba(0, 123, 255, 0.3); color: #cce5ff; border: 1px solid #b8daff; }
        .status-completed { background: rgba(40, 167, 69, 0.3); color: #d4edda; border: 1px solid #c3e6cb; }

        /* Inputs & Fields */
        input, textarea, select {
            font-size: 16px !important;
            border-radius: 14px !important;
            border: 2px solid rgba(255, 255, 255, 0.5) !important;
            background: rgba(255, 255, 255, 0.15) !important;
            color: #ffffff !important;
            transition: all 0.25s ease !important;
        }

        input:focus, textarea:focus, select:focus {
            border-color: #ffffff !important;
            box-shadow: 0 0 20px #ffffff, 0 0 0 3px rgba(255, 255, 255, 0.3) !important;
            background: rgba(255, 255, 255, 0.25) !important;
        }

        /* Seamless Modern 3D Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.15);
            padding: 8px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), inset 0 0 15px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            border-radius: 14px;
            font-weight: 700;
            color: #ffffff;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            text-shadow: 0 0 6px rgba(255, 255, 255, 0.6);
        }

        .stTabs [aria-selected="true"] {
            background: #ffffff !important;
            color: #ff1aff !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(255,255,255,0.8);
            text-shadow: none;
            -webkit-text-stroke: 0.5px #ff1aff;
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
      "<h2 style='text-align: center; color: #ffffff; text-shadow: 0 0 15px"
      " #ffffff;'>🔒 App Locked</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #f0f0f0;'>New billing cycle"
      " started. Enter code to unlock.</p>",
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
        "Fitting Ready": "status-fitting",
        "Completed": "status-completed",
    }.get(status, "status-pending")

    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                <h3 style="margin:0; color: #ffffff; font-size: 1.3rem;">👤 {current_order['name']}</h3>
                <span class="status-badge {status_class}">{status}</span>
            </div>
            <p style="font-size: 1.05rem; margin-bottom: 8px; color: #ffffff;"><b>📞 Phone:</b> {current_order['phone'] if current_order['phone'] else 'None'}</p>
            <p style="font-size: 1.05rem; margin-bottom: 12px; color: #ffffff; text-shadow: 0 0 8px #ffffff;"><b>📅 Due Date:</b> {current_order['date']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                    <h3 style="margin: 0; color: #ffffff; font-size: 1.15rem;">👤 {order['name']}</h3>
                    <span class="status-badge {status_class}">{status}</span>
                </div>
                <p style="font-size: 0.9rem; color: #ffffff; font-weight: 600; margin-bottom: 0px; text-shadow: 0 0 6px #ffffff;">📅 Due Date: {order['date']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("📄 View Details & Notes", key=f"view_{order['id']}"):
          st.session_state.selected_order_id = order["id"]
          st.rerun()

  with tab_calc:
    st.markdown(
        "<h3 style='color: #ffffff; text-align: center; margin-bottom: 15px;"
        " text-shadow: 0 0 10px #ffffff;'>Momo Calculator</h3>",
        unsafe_allow_html=True,
    )

    # Zero-Latency Client-Side 3D Glowing Calculator Component
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
            .calc-box {
                width: 100%;
                max-width: 380px;
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                padding: 22px;
                border-radius: 28px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), 0 0 25px rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.5);
                transform: perspective(1000px) rotateX(2deg);
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
                box-shadow: inset 0 4px 12px rgba(0,0,0,0.8), 0 0 10px rgba(255, 255, 255, 0.4);
                letter-spacing: 1px;
                min-height: 55px;
            }
            .calc-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
            }
            .calc-btn {
                background: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-size: 1.25rem;
                font-weight: 700;
                border-radius: 16px;
                min-height: 56px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                cursor: pointer;
                transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2), 0 0 5px rgba(255, 255, 255, 0.2);
                text-shadow: 0 0 6px #ffffff;
                user-select: none;
                transform: perspective(1000px) translateZ(0px);
            }
            .calc-btn:hover {
                background: #ffffff;
                color: #ff1aff;
                border-color: #ffffff;
                transform: perspective(1000px) translateY(-3px) translateZ(10px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px #ffffff;
                text-shadow: none;
            }
            .calc-btn:active {
                transform: scale(0.93) translateY(0);
                background: #e0e0e0;
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
