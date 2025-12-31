import streamlit as st
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Matoshree Vehicle Resellers",
    layout="wide"
)

DATA_FILE = "data.json"

# ---------------- LOAD DATA ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

vehicles = load_data()

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color:#0b1220; }

.header {
    background: linear-gradient(135deg,#0e2a3a,#143c4b);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
}

.card {
    background: #0f1c2e;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
<h1>🚛 Matoshree Vehicle Resellers</h1>
<p>Trusted Transport Vehicle Dealers Since 1999</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FILTERS ----------------
col1, col2, col3 = st.columns(3)

search = col1.text_input("🔍 Search vehicle")
fuel = col2.selectbox("Fuel Type", ["All", "Diesel", "Petrol", "CNG"])
price = col3.selectbox("Price Range", ["All", "Below 5L", "5L–10L", "10L+"])

# ---------------- VEHICLE DISPLAY ----------------
for i, v in enumerate(vehicles):

    if search and search.lower() not in v.get("name", "").lower():
        continue

    if fuel != "All" and v.get("fuel") != fuel:
        continue

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col_img, col_info = st.columns([1, 2])

    # ---------- IMAGE SLIDER ----------
    with col_img:
        if "images" in v and isinstance(v["images"], list) and len(v["images"]) > 0:

            img_key = f"img_{i}"

            if img_key not in st.session_state:
                st.session_state[img_key] = 0

            st.image(
                v["images"][st.session_state[img_key]],
                use_container_width=True
            )

            p, n = st.columns(2)

            if p.button("⬅ Prev", key=f"p{i}"):
                if st.session_state[img_key] > 0:
                    st.session_state[img_key] -= 1

            if n.button("Next ➡", key=f"n{i}"):
                if st.session_state[img_key] < len(v["images"]) - 1:
                    st.session_state[img_key] += 1

    # ---------- DETAILS ----------
    with col_info:
        st.subheader(v.get("name", "Vehicle"))

        st.write(f"**Model:** {v.get('model', 'N/A')}")
        st.write(f"**Fuel:** {v.get('fuel', 'N/A')}")
        st.write(f"**Capacity:** {v.get('capacity', 'N/A')}")
        st.write(f"**Price:** ₹ {v.get('price', 'N/A')}")

        st.markdown(
            f"""
            <a href="https://wa.me/91XXXXXXXXXX?text=I am interested in {v.get('name','vehicle')}"
               target="_blank">
               <button style="background:#25D366;color:white;
               padding:10px 20px;border:none;border-radius:8px;">
               WhatsApp Enquiry
               </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
