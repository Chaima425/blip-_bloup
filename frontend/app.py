#frontend/app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# URL du backend (Azure plus tard)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Blip Bloup", page_icon="🤖", layout="centered")

st.title("🤖 Blip Bloup")

st.markdown("Clique sur le bouton pour envoyer un **Ping** au robot.")

# BOUTON PING
if st.button("🔔 Ping"):
    try:
        response = requests.post(f"{BACKEND_URL}/ping")

        if response.status_code == 200:
            data = response.json()
            st.success(f"Blip envoyé ✅ | IP : {data['ip']}")
        else:
            st.error("Erreur lors du ping")

    except Exception as e:
        st.error(f"Backend inaccessible : {e}")

st.divider()

# HISTORIQUE
st.subheader("📜 Historique des Pings")

page = st.number_input("Page", min_value=1, value=1, step=1)
limit = st.selectbox("Nombre par page", [10, 25, 50, 100])

if st.button("🔄 Actualiser l'historique"):
    try:
        response = requests.get(f"{BACKEND_URL}/pings?page={page}&limit={limit}")

        if response.status_code == 200:
            data = response.json()

            if data["data"]:
                for ping in data["data"]:
                    st.write(f"📍 {ping['ip']} — {ping['created_at']}")
            else:
                st.warning("Aucun ping enregistré")
        else:
            st.error("Erreur récupération historique")

    except Exception as e:
        st.error(f"Erreur : {e}")
