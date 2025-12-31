import streamlit as st
import json
import hashlib
import cloudinary
import cloudinary.uploader
import os

# ---------------- CONFIG ----------------
cloudinary.config(
    cloud_name=st.secrets.get("CLOUDINARY_NAME"),
    api_key=st.secrets.get("CLOUDINARY_API_KEY"),
    api_secret=st.secrets.get("CLOUDINARY_API_SECRET"),
)
DATA_FILE = "data.json"
PROFILE_FILE = "admin_profile.json"


# ---------------- UTILS ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()


# ---------------- LOGIN ----------------
with open(PROFILE_FILE) as f:
    profile = json.load(f)

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 Admin Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == profile["username"] and hash_pass(p) == profile["password"]:
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()


# ---------------- SIDEBAR ----------------
st.sidebar.image(
    profile.get("photo", "https://cdn-icons-png.flaticon.com/512/149/149071.png"),
    width=120
)
st.sidebar.markdown(f"### {profile['name']}")

if st.sidebar.button("Logout"):
    st.session_state.logged = False
    st.rerun()


# ---------------- LOAD DATA ----------------
vehicles = load_data()

for v in vehicles:
    v.setdefault("status", "Available")
    v.setdefault("images", [])


# ---------------- ADD VEHICLE ----------------
st.title("🚛 Admin Panel")
st.subheader("➕ Add Vehicle")

name = st.text_input("Vehicle Name")
year = st.text_input("Model Year")
capacity = st.text_input("Capacity")
fuel = st.selectbox("Fuel Type", ["Diesel", "Petrol", "CNG"])
price = st.text_input("Price")
phone = st.text_input("Phone")

images = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if st.button("Add Vehicle"):
    image_urls = []

    if images:
        for img in images:
            res = cloudinary.uploader.upload(img)
            image_urls.append(res["secure_url"])

    vehicles.append({
        "name": name,
        "year": year,
        "capacity": capacity,
        "fuel": fuel,
        "price": price,
        "phone": phone,
        "images": image_urls,
        "status": "Available"
    })

    save_data(vehicles)
    st.success("✅ Vehicle Added Successfully")
    st.rerun()


# ---------------- MANAGE VEHICLES ----------------
st.subheader("🛠 Manage Vehicles")

for i, v in enumerate(vehicles):
    with st.expander(f"{v['name']} ({v['status']})"):

        # Images
        if v["images"]:
            cols = st.columns(len(v["images"]))
            for idx, img in enumerate(v["images"]):
                with cols[idx]:
                    st.image(img, use_container_width=True)
                    if st.button("❌ Remove", key=f"img_{i}_{idx}"):
                        v["images"].pop(idx)
                        save_data(vehicles)
                        st.rerun()
        else:
            st.info("No images uploaded")

        st.divider()

        # Status
        status = st.selectbox(
            "Status",
            ["Available", "SOLD"],
            index=0 if v["status"] == "Available" else 1,
            key=f"status_{i}"
        )

        if st.button("Update Status", key=f"update_{i}"):
            vehicles[i]["status"] = status
            save_data(vehicles)
            st.success("Status Updated")
            st.rerun()

        if st.button("🗑 Delete Vehicle", key=f"delete_{i}"):
            vehicles.pop(i)
            save_data(vehicles)
            st.warning("Vehicle Deleted")
            st.rerun()

