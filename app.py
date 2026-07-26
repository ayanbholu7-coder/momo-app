import json
import sqlite3
from google import genai
import streamlit as st

# Setup local database inside the app
conn = sqlite3.connect("momo_orders.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS orders 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT, items TEXT, price TEXT)"""
)
conn.commit()

st.set_page_config(
    page_title="Momo Fashion Orders", layout="centered", page_icon="👗"
)

# Custom pink theme styling
st.markdown(
    """
    <style>
    .stApp { background-color: #FFF5F7; }
    h1, h2, h3 { color: #E91E63; text-align: center; }
    .stButton>button { background-color: #E91E63; color: white; border-radius: 12px; height: 50px; font-weight: bold; width: 100%; border: none; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("👗 Momo Fashion Orders")

# Sidebar for your Google AI key
gemini_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

tab1, tab2 = st.tabs(["✨ New Order", "📋 Saved Orders"])

# Tab 1: Extract and Save Order
with tab1:
    st.subheader("Paste Customer Message")
    raw_text = st.text_area(
        "Paste WhatsApp message here (Roman Urdu / English):", height=120
    )

    if st.button("✨ Extract Details with AI"):
        if not gemini_key:
            st.error("Please enter your Gemini API Key in the left sidebar!")
        elif not raw_text:
            st.warning("Please paste a text message first.")
        else:
            try:
                client = genai.Client(api_key=gemini_key)
                prompt = f"""
                Extract customer details from this message: "{raw_text}".
                Return ONLY a raw JSON object with these exact keys:
                "name", "phone", "address", "items", "price"
                Do NOT include markdown backticks or block formatting.
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt
                )

                clean_text = (
                    response.text.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )
                data = json.loads(clean_text)

                st.session_state["extracted"] = data
                st.success("Details Extracted Successfully!")
            except Exception as e:
                st.error(f"Extraction Error: {e}")

    st.divider()

    ext = st.session_state.get("extracted", {})

    with st.form("save_order_form"):
        name = st.text_input("Customer Name", value=ext.get("name", ""))
        phone = st.text_input("Phone Number", value=ext.get("phone", ""))
        address = st.text_input(
            "Delivery Address", value=ext.get("address", "")
        )
        items = st.text_area("Order Items", value=ext.get("items", ""))
        price = st.text_input("Price (PKR)", value=str(ext.get("price", "")))

        submitted = st.form_submit_button("SAVE ORDER")
        if submitted:
            c.execute(
                "INSERT INTO orders (name, phone, address, items, price) VALUES (?, ?, ?, ?, ?)",
                (name, phone, address, items, price),
            )
            conn.commit()
            st.success("Order Saved Successfully!")
            st.session_state["extracted"] = {}

# Tab 2: Dashboard
with tab2:
    st.subheader("Customer Orders")
    c.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = c.fetchall()

    if not orders:
        st.info("No orders saved yet.")
    else:
        for order in orders:
            with st.container(border=True):
                st.markdown(f"### {order[1]} — **PKR {order[5]}**")
                st.write(f"📞 **Phone:** {order[2]}")
                st.write(f"📍 **Address:** {order[3]}")
                st.write(f"📦 **Items:** {order[4]}")

                clean_phone = "".join(filter(str.isdigit, str(order[2])))
                if clean_phone:
                    st.markdown(
                        f"[💬 Open WhatsApp Chat](https://wa.me/{clean_phone})",
                        unsafe_allow_html=True,
                    )