import streamlit as st
from engine import WaguriBrain
from dotenv import load_dotenv

# Memuat kunci rahasia
load_dotenv()

# ==========================================
# 1. KONFIGURASI HALAMAN WEB
# ==========================================
st.set_page_config(
    page_title="Waguri AI", 
    page_icon="🌸", 
    layout="centered"
)

st.title("🌸 Waguri AI Assistant")
st.caption("Asisten Portofolio Interaktif oleh Haitamim Jahran Mahendra")
st.divider()

# ==========================================
# 2. INISIALISASI MESIN & MEMORI (Session State)
# ==========================================
# Streamlit memuat ulang halaman setiap kali ada interaksi. 
# Kita gunakan session_state agar memori dan otak Waguri tidak ter-reset terus-menerus.

if "waguri_engine" not in st.session_state:
    # Memanggil Class OOP kita HANYA sekali di awal
    st.session_state.waguri_engine = WaguriBrain(file_portofolio="portofolio.txt")

if "messages" not in st.session_state:
    # Pesan sapaan pertama saat web dibuka
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya Waguri. Ada yang ingin Anda ketahui tentang portofolio atau keahlian teknis Haitamim?"}
    ]

# ==========================================
# 3. MENAMPILKAN RIWAYAT OBROLAN DI LAYAR
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 4. LOGIKA INPUT PENGGUNA (Kolom Chat)
# ==========================================
if prompt := st.chat_input("Ketikkan pertanyaanmu di sini..."):
    
    # 4a. Tampilkan pesan user ke layar
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 4b. Simpan pesan user ke memori web
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 4c. Panggil Waguri untuk menjawab (dengan animasi loading)
    with st.chat_message("assistant"):
        with st.spinner("Waguri sedang berpikir..."):
            jawaban = st.session_state.waguri_engine.jawab_pertanyaan(prompt)
            st.markdown(jawaban)
    
    # 4d. Simpan jawaban Waguri ke memori web
    st.session_state.messages.append({"role": "assistant", "content": jawaban})