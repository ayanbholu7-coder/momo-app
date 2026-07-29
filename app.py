import datetime
import json
import os
import streamlit as st

# 1. Page Setup & Cool AF Styling / Animations
st.set_page_config(
    page_title="Momo Fashion", page_icon="✨", layout="centered"
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
        }

        .momo-header {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(45deg, #ff1a75, #ff66b2, #ff3385);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 25px;
            letter-spacing: -1px;
            animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            text-shadow: 0 10px 30px rgba(255, 51, 133, 0.2);
        }

        .order-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 20px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            margin-bottom: 16px;
            box-shadow: 0 15px 35px rgba(255, 51, 133, 0.08);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
            animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        .order-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(255, 51, 133, 0.15);
        }

        div.stButton > button {
            background: linear-gradient(135deg, #1a1a1a, #333333);
            color: white;
            border-radius: 14px;
            font-weight: 600;
            border: none;
            width: 100%;
            padding: 12px;
            transition: all 0.2s ease;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        div.stButton > button:hover {
            background: linear-gradient(135deg, #ff1a75, #ff3385);
            color: white;
            transform: scale(1.02);
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Permanent Server-Side JSON Storage
DB_FILE = "momo_persistent_orders.json"


def load_orders():
  if os.path.exists(DB_FILE):
    try:
      with open(DB_FILE, "r") as f:
        return json.load(f)
    except:
      return []
  return []


def save_orders(orders_list):
  with open(DB_FILE, "w") as f:
    json.dump(orders_list, f, indent=4)


if "orders" not in st.session_state:
  st.session_state.orders = load_orders()

if "selected_order_id" not in st.session_state:
  st.session_state.selected_order_id = None

# 3. Monthly Lock System (Triggers on 1st of the month)
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

# 4. Routing: Detail Page vs Main List Page
if st.session_state.selected_order_id is not None:
  # Find the selected order
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

    st.markdown(
        f"""
        <div class="order-card" style="padding: 25px;">
            <p style="font-size: 1.1rem; margin-bottom: 15px;"><b>👤 Customer Name:</b> {current_order['name']}</p>
            <p style="font-size: 1.1rem; margin-bottom: 15px;"><b>📞 Phone Number:</b> {current_order['phone'] if current_order['phone'] else 'None'}</p>
            <p style="font-size: 1.1rem; margin-bottom: 15px; color: #ff1a75;"><b>📅 Due Date:</b> {current_order['date']}</p>
            <p style="font-size: 1.1rem; margin-bottom: 5px;"><b>📝 Notes & Measurements:</b></p>
            <div style="background: #fff; padding: 15px; border-radius: 12px; border: 1px solid #ffb3d1; color: #333; font-size: 1rem; white-space: pre-wrap;">{current_order['notes'] if current_order['notes'] else 'No notes added.'}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗑️ Delete This Order"):
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
  # Main App Interface
  st.markdown(
      '<div class="momo-header">✨ MOMO FASHION ✨</div>', unsafe_allow_html=True
  )

  with st.expander("➕ Add New Order", expanded=False):
    with st.form("order_form", clear_on_submit=True):
      customer_name = st.text_input("Customer Name")
      phone_number = st.text_input("Phone Number")

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

      order_notes = st.text_area("Measurements, design details, price...")

      submitted = st.form_submit_button("Save Order")
      if submitted:
        if customer_name.strip() == "":
          st.warning("Please enter a customer name.")
        else:
          month_index = months.index(month_val) + 1
          formatted_date = f"{month_index:02d}/{day_val:02d}/{year_val}"
          new_order = {
              "id": str(datetime.datetime.now().timestamp()),
              "name": customer_name,
              "phone": phone_number,
              "date": formatted_date,
              "notes": order_notes,
          }
          st.session_state.orders.insert(0, new_order)
          save_orders(st.session_state.orders)
          st.success("Saved permanently!")
          st.rerun()

  st.markdown("---")

  search_term = st.text_input(
      "🔍 Search orders...", placeholder="Type name, phone, or notes..."
  ).lower()

  filtered_orders = [
      o
      for o in st.session_state.orders
      if search_term in o["name"].lower()
      or search_term in o["phone"].lower()
      or search_term in o["notes"].lower()
  ]

  if not filtered_orders:
    st.info("No orders found.")
  else:
    for order in filtered_orders:
      st.markdown(
          f"""
            <div class="order-card">
                <h3 style="margin-bottom: 4px; color: #1a1a1a;">👤 {order['name']}</h3>
                <p style="font-size: 0.9rem; color: #ff1a75; font-weight: 600; margin-bottom: 0px;">📅 Due Date: {order['date']}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      if st.button("📄 View Details & Notes", key=f"view_{order['id']}"):
        st.session_state.selected_order_id = order["id"]
        st.rerun()
