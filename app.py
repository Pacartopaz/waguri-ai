import streamlit as st
import os
import requests
from engine import WaguriBrain
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env (Untuk mode lokal di laptop)
load_dotenv()

# Konfigurasi halaman utama Streamlit
st.set_page_config(page_title="Waguri AI", page_icon="🌸", layout="centered")

st.title("🌸 Waguri AI Assistant")
st.caption("Asisten Portofolio Interaktif oleh Haitamim Jahran Mahendra")
st.divider()

# Inisialisasi Engine AI (RAG)
if "waguri_engine" not in st.session_state:
    st.session_state.waguri_engine = WaguriBrain(file_portofolio="portofolio.txt")

# Inisialisasi Riwayat Obrolan
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya Waguri. Ada yang ingin Anda ketahui tentang portofolio atau keahlian teknis Haitamim?"}
    ]

# Menampilkan riwayat obrolan yang sudah ada
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Kolom Input Chat Pengguna
if prompt := st.chat_input("Ketikkan pertanyaanmu di sini..."):
    
    # Tampilkan pesan pengguna
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Tampilkan respons dari asisten AI
    with st.chat_message("assistant"):
        with st.spinner("Waguri sedang berpikir..."):
            # 1. Mengambil jawaban teks utama dari engine RAG
            jawaban = st.session_state.waguri_engine.jawab_pertanyaan(prompt)
            st.markdown(jawaban)
            
            # 2. Menu Tambahan (Copy & Pilihan Mendengarkan Suara)
            with st.expander("🛠️ Opsi: Salin Teks & Dengarkan Suara"):
                
                # Fitur Salin Teks
                st.caption("📝 Salin Jawaban:")
                st.code(jawaban, language="markdown")
                
                # Fitur Sintesis Suara via Fish Audio API
                st.caption("🔊 Dengarkan Suara Waguri:")
                try:
                    # Mengambil kunci dengan aman (Cek lokal .env dulu)
                    fish_api_key = os.environ.get("FISH_AUDIO_API_KEY")
                    fish_model_id = os.environ.get("FISH_AUDIO_MODEL_ID")
                    
                    # Jika di lokal tidak ada, coba ambil dari Streamlit Cloud Secrets
                    if not fish_api_key:
                        try:
                            fish_api_key = st.secrets["FISH_AUDIO_API_KEY"]
                            fish_model_id = st.secrets["FISH_AUDIO_MODEL_ID"]
                        except:
                            pass # Kunci tetap kosong jika di Streamlit Cloud tidak ada
                    
                    # Cegah eksekusi jika kunci masih kosong atau teks placeholder
                    if not fish_api_key or "isi_dengan" in fish_api_key:
                        st.error("Kunci API Fish Audio belum ditemukan di .env (Lokal) maupun Secrets (Streamlit Cloud)!")
                    else:
                        # Persiapan komunikasi dengan server Fish Audio
                        url = "https://api.fish.audio/v1/tts"
                        headers = {
                            "Authorization": f"Bearer {fish_api_key}",
                            "Content-Type": "application/json"
                        }
                        payload = {
                            "text": jawaban,
                            "reference_id": fish_model_id,
                            "format": "mp3"
                        }
                        
                        # Mengirim permintaan
                        response = requests.post(url, json=payload, headers=headers)
                        
                        # Jika sukses (200), render pemutar audio
                        if response.status_code == 200:
                            st.audio(response.content, format='audio/mp3', autoplay=False)
                        else:
                            # Menampilkan pesan error spesifik dari Fish Audio jika gagal
                            st.error(f"Pita suara Waguri sedang gangguan. Status: {response.status_code}. Detail: {response.text}")
                            
                except Exception as e:
                    st.error(f"Sistem gagal terhubung ke internet: {e}")

    # Simpan jawaban ke riwayat obrolan
    st.session_state.messages.append({"role": "assistant", "content": jawaban})

# --- SEKSI ETIKA AI & DISCLAIMER HAK CIPTA ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.caption(
    "⚠️ **Disclaimer Proyek Penggemar (Fan Project):**\n"
    "Aplikasi ini merupakan proyek portofolio akademik non-komersial dan tidak mengambil keuntungan finansial apa pun. "
    "Kloning suara AI dilatih menggunakan sampel karakter Waguri Kaoruko (Kaoru Hana wa Rin to Saku). "
    "Seluruh hak cipta kekayaan intelektual atas karakter, citra, dan suara asli sepenuhnya milik seiyuu dan studio produksi terkait."
)