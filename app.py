import streamlit as st
import os
from pemeriksaan import cek_format_teknis, cek_kutipan, cek_kalimat_panjang, cek_kalimat_pasif, cek_bahasa_tidak_akademik, cek_format_font_spasi

# =====================================
# Konfigurasi Halaman Streamlit
# =====================================
st.set_page_config(
    page_title="Sistem Pemeriksaan Naskah Skripsi",
    # page_icon="📚", # <--- IKON BUKU DIHILANGKAN
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# CSS Kustom untuk Mempercantik Tampilan (Tema Putih)
# =====================================
st.markdown("""
    <style>
    /* Mengatur font global dan warna latar belakang */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="st-emotion"] {
        font-family: 'Inter', sans-serif;
        color: #333333; /* Warna teks utama: Hitam gelap */
        background-color: #FFFFFF; /* Warna latar belakang: Putih */
    }

    /* Header Utama */
    h1 {
        color: #002147 !important; /* Warna biru tua untuk judul utama */
        text-align: center;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Sub-header */
    h4 {
        color: #555555 !important; /* Warna abu-abu gelap untuk sub-header */
        text-align: center;
        font-weight: 400;
    }

    /* Garis Pemisah */
    hr {
        border-top: 2px solid #DDDDDD; /* Garis pemisah lebih tebal dan berwarna terang */
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* Kotak Unggah File */
    .stFileUploader {
        border: 2px dashed #002147; /* Border putus-putus warna biru tua */
        border-radius: 15px; /* Sudut membulat */
        padding: 20px;
        background-color: #F8F8F8; /* Latar belakang kotak unggah lebih terang */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Bayangan lembut */
    }
    .stFileUploader > div > div > button {
        background-color: #002147; /* Warna tombol Browse files: Biru tua */
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stFileUploader > div > div > button:hover {
        background-color: #003366; /* Warna hover tombol */
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }

    /* Pesan Sukses */
    .stSuccess {
        background-color: #d4edda; /* Warna hijau muda untuk sukses */
        color: #155724; /* Warna teks hijau gelap */
        border-radius: 10px;
        padding: 15px;
        margin-top: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Header Hasil Pemeriksaan */
    h2 {
        color: #002147 !important; /* Warna biru tua untuk judul hasil */
        font-weight: 600;
        margin-top: 2rem;
    }

    /* Sub-header untuk setiap file hasil */
    h3 {
        color: #002147 !important; /* Warna biru tua untuk sub-judul file */
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Kotak Kode (untuk menampilkan isi file) */
    .stCode {
        background-color: #F0F0F0; /* Latar belakang kotak kode lebih terang */
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #DDDDDD;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-height: 400px;
        overflow-y: auto;
        color: #333333; /* Warna teks di kotak kode */
    }

    /* Tombol Download */
    .stDownloadButton > button {
        background-color: #002147; /* Warna biru tua untuk tombol download */
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    .stDownloadButton > button:hover {
        background-color: #003366; /* Warna hover tombol download */
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }

    /* Pesan Error (jika ada) */
    .stError {
        background-color: #f8d7da; /* Warna merah muda untuk error */
        color: #721c24; /* Warna teks merah gelap */
        border-radius: 10px;
        padding: 15px;
        margin-top: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# =====================================
# Tampilan Header
# =====================================
# <--- IKON BUKU DIHILANGKAN DARI SINI
st.markdown("<h1 style='color:#002147;'>Sistem Pemeriksaan Naskah Skripsi</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#555555;'>Program Studi Ilmu Pemerintahan - FISIP Universitas Tadulako</h4>", unsafe_allow_html=True)
st.markdown("---")

# =====================================
# Upload File
# =====================================
st.markdown("📥 Silakan unggah file skripsi (.docx)") # Mengubah ini menjadi markdown biasa untuk styling
uploaded_file = st.file_uploader("", type=["docx"], label_visibility="collapsed") # Label visibility collapsed untuk menghilangkan label default

if uploaded_file is not None:
    # Simpan file yang diunggah sementara
    temp_docx_path = "skripsi_temp.docx"
    with open(temp_docx_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File **{uploaded_file.name}** berhasil diunggah. Siap diperiksa!")

    # =====================================
    # Jalankan semua pemeriksaan
    # =====================================
    cek_format_teknis.detect_phrases(temp_docx_path)
    cek_kutipan.analyze_apa_citations(temp_docx_path)
    cek_kalimat_panjang.analyze_sentences(temp_docx_path)
    cek_kalimat_pasif.detect_passive_sentences(temp_docx_path)
    cek_bahasa_tidak_akademik.detect_non_academic_phrases(temp_docx_path)
    cek_format_font_spasi.check_document_formatting(temp_docx_path)

    # =====================================
    # Tampilkan hasil pemeriksaan
    # =====================================
    st.markdown("<h2>📄 Hasil Pemeriksaan Naskah:</h2>", unsafe_allow_html=True) # Menggunakan h2 dengan unsafe_allow_html

    # Daftar file hasil yang diharapkan ada di folder 'hasil/'
    hasil_files = [
        "hasil/hasil_format_teknis.txt",
        "hasil/hasil_kutipan.txt",
        "hasil/kutipan_revisi.txt",
        "hasil/hasil_kalimat_panjang.txt",
        "hasil/hasil_kalimat_pasif.txt",
        "hasil/hasil_bahasa_tidak_akademik.txt",
        "hasil/hasil_format_font_spasi.txt",
    ]

    # Debugging: Tampilkan direktori kerja dan status file (opsional, bisa dihapus setelah yakin)
    st.write(f"Direktori Kerja Saat Ini: `{os.getcwd()}`")
    for debug_file in hasil_files:
        full_debug_path = os.path.join(os.getcwd(), debug_file)
        if os.path.exists(full_debug_path):
            st.success(f"DEBUG: File `{debug_file}` DITEMUKAN di `{full_debug_path}`.")
        else:
            st.error(f"DEBUG: File `{debug_file}` TIDAK DITEMUKAN di `{full_debug_path}`.")

    # Loop untuk menampilkan setiap file hasil
    for file_path in hasil_files:
        st.markdown(f"<h3>🔎 {os.path.basename(file_path).replace('_', ' ').replace('.txt', '').title()}</h3>", unsafe_allow_html=True) # Tampilan judul lebih rapi dan kapitalisasi

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                isi = f.read()

            st.code(isi, language="markdown")

            st.download_button(
                label=f"⬇️ Unduh {os.path.basename(file_path).replace('_', ' ').replace('.txt', '').title()}",
                data=isi,
                file_name=os.path.basename(file_path),
                mime="text/plain"
            )
        except FileNotFoundError:
            st.error(f"File hasil '{os.path.basename(file_path)}' tidak ditemukan. Pastikan modul pemeriksaan terkait berhasil membuatnya.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file '{os.path.basename(file_path)}': {e}")

        st.markdown("---")

    st.success("✅ Pemeriksaan selesai. Anda bisa membaca atau mengunduh semua hasil di atas.")

    # Opsional: Hapus file sementara setelah selesai
    # if os.path.exists(temp_docx_path):
    #     os.remove(temp_docx_path)
