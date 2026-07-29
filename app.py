import datetime
import json
import os
import streamlit as st

# 1. Page Setup & Branding (Pink, White, Black)
st.set_page_config(
    page_title="Momo Fashion", page_icon="✨", layout="centered"
)

st.markdown(
    """
    <style>
        :root {
            --bg-color: #fff5f7;
            --card-bg: #ffffff;
            --text-primary: #111111;
            --text-secondary: #666666;
            --accent-pink: #ff69b4;
            --border-color: #ffd1dc;
        }
        .stApp {
            background-color: var(--bg-color);
        }
        h1, h2, h3 {
            color: var(--text-primary) !important;
        }
        .order-card {
            background: var(--card-bg);
            padding: 16px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            margin-bottom: 12px;
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.08);
        }
        div.stButton > button {
            background-color: var(--text-primary);
            color: white;
            border-radius: 12px;
            font-weight: 600;
            border: none;
            width: 100%;
            padding: 10px;
        }
        div.stButton > button:hover {
            background-color: var(--accent-pink);
            color: white;
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


# Initialize orders from file
if "orders" not in st.session_state:
  st.session_state.orders = load_orders()

# 3. Monthly Paywall / Lock System
SECRET_CODE = "momo2026"  # Change this password whenever you want
now = datetime.datetime.now()
current_month_year = f"{now.month}-{now.getFullYear()}"

if "unlocked_month" not in st.session_state:
  st.session_state.unlocked_month = ""

# Trigger Lock Screen on the 1st of the month
if now.day >= 1 and st.session_state.unlocked_month != current_month_year:
  st.markdown("---")
  st.markdown("<h2 style='text-align: center;'>🔒 App Locked</h2>", unsafe_allow_html=True)
  st.markdown(
      "<p style='text-align: center; color: #666;'>A new billing cycle has"
      " started. Enter the code to unlock.</p>",
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

# 4. Main App Interface
st.title("✨ Momo Fashion")

# Add New Order Expander
with st.expander("➕ Add New Order", expanded=False):
  with st.form("order_form", clear_on_submit=True):
    customer_name = st.text_input("Customer Name")
    phone_number = st.text_input("Phone Number")
    order_date = st.date_input("Due Date", datetime.date.today())
    order_notes = st.text_area("Measurements, design details, price...")

    submitted = st.form_submit_button("Save Order")
    if submitted:
      if customer_name.strip() == "":
        st.warning("Please enter a customer name.")
      else:
        new_order = {
            "id": str(datetime.datetime.now().timestamp()),
            "name": customer_name,
            "phone": phone_number,
            "date": str(order_date),
            "notes": order_notes,
        }
        st.session_state.orders.insert(0, new_order)
        save_orders(st.session_state.orders)
        st.success("Order saved permanently!")
        st.rerun()

st.markdown("---")

# Search Filter
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

# Display Orders
if not filtered_orders:
  st.info("No orders found.")
else:
  for order in filtered_orders:
    st.markdown(
        f"""
        <div class="order-card">
            <h3>{order['name']}</h3>
            <p><b>📞 Phone:</b> {order['phone'] if order['phone'] else 'None'}</p>
            <p><b>📝 Notes:</b> {order['notes'] if order['notes'] else 'None'}</p>
            <p style="font-size: 0.85rem; color: #ff479b; margin-top: 8px;"><b>Due Date:</b> {order['date']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Delete", key=f"del_{order['id']}"):
      st.session_state.orders = [
          o for o in st.session_state.orders if o["id"] != order["id"]
      ]
      save_orders(st.session_state.orders)
      st.rerun()
