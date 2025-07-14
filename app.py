import streamlit as st
import os
# Import semua modul pemeriksaan yang ada
from pemeriksaan import cek_format_teknis, cek_kutipan, cek_kalimat_panjang, cek_kalimat_pasif, cek_bahasa_tidak_akademik, cek_format_font_spasi
# Import modul pemeriksaan ejaan dan tata bahasa yang baru
from pemeriksaan import cek_ejaan_tata_bahasa

import nltk # <--- BARIS INI TETAP ADA
# from nltk.downloader import DownloadError # <--- BARIS INI DIHAPUS/DIKOMENTARI

# =====================================
# Konfigurasi Halaman Streamlit
# =====================================
st.set_page_config(
    page_title="Sistem Pemeriksaan Naskah Skripsi",
    layout="wide", # Mengatur tata letak halaman menjadi lebar
    initial_sidebar_state="collapsed" # Sidebar bisa dibuka/ditutup
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
st.markdown("<h1 style='color:#002147;'>Sistem Pemeriksaan Naskah Skripsi</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#555555;'>Program Studi Ilmu Pemerintahan - FISIP Universitas Tadulako</h4>", unsafe_allow_html=True)
st.markdown("---")

# =====================================
# Upload File
# =====================================
st.markdown("📥 Silakan unggah file skripsi (.docx)")
uploaded_file = st.file_uploader("", type=["docx"], label_visibility="collapsed")

if uploaded_file is not None:
    temp_docx_path = "skripsi_temp.docx"
    with open(temp_docx_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File **{uploaded_file.name}** berhasil diunggah. Siap diperiksa!")

    # =====================================
    # Download NLTK data for TextBlob (hanya sekali)
    # Ini penting agar TextBlob bisa berfungsi di Streamlit Cloud
    # =====================================
    # <--- BAGIAN INI DIMODIFIKASI
    try:
        nltk.data.find('corpora/punkt')
    except nltk.downloader.DownloadError: # <--- Menggunakan path lengkap untuk DownloadError
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except nltk.downloader.DownloadError: # <--- Menggunakan path lengkap untuk DownloadError
        nltk.download('averaged_perceptron_tagger')
    # =====================================

    # =====================================
    # Jalankan semua pemeriksaan dan kumpulkan hasilnya untuk ringkasan
    # =====================================
    # Inisialisasi dictionary untuk menyimpan ringkasan hasil
    summary_results = {}

    # Pemeriksaan Format Teknis
    found_phrases_count, not_found_phrases_count = cek_format_teknis.detect_phrases(temp_docx_path)
    summary_results['Format Teknis'] = f"Ditemukan: {found_phrases_count}, Tidak Ditemukan: {not_found_phrases_count}"

    # Pemeriksaan Kutipan
    proper_citations_count, incomplete_citations_count = cek_kutipan.analyze_apa_citations(temp_docx_path)
    summary_results['Kutipan APA'] = f"Benar: {proper_citations_count}, Perlu Revisi: {incomplete_citations_count}"

    # Pemeriksaan Kalimat Panjang
    long_sentences_count = cek_kalimat_panjang.analyze_sentences(temp_docx_path)
    summary_results['Kalimat Panjang'] = f"Ditemukan: {long_sentences_count}"

    # Pemeriksaan Kalimat Pasif
    passive_sentences_count = cek_kalimat_pasif.detect_passive_sentences(temp_docx_path)
    summary_results['Kalimat Pasif'] = f"Ditemukan: {passive_sentences_count}"

    # Pemeriksaan Bahasa Tidak Akademik
    non_academic_phrases_count = cek_bahasa_tidak_akademik.detect_non_academic_phrases(temp_docx_path)
    summary_results['Bahasa Tidak Akademik'] = f"Ditemukan: {non_academic_phrases_count}"

    # Pemeriksaan Ejaan dan Tata Bahasa (MODUL BARU)
    spelling_grammar_issues_count = cek_ejaan_tata_bahasa.analyze_spelling_grammar(temp_docx_path)
    summary_results['Ejaan & Tata Bahasa'] = f"Potensi Kesalahan: {spelling_grammar_issues_count}"

    # Pemeriksaan Format Font dan Spasi
    format_font_spasi_status = cek_format_font_spasi.check_document_formatting(temp_docx_path)
    summary_results['Format Font & Spasi'] = "Pemeriksaan Selesai" if format_font_spasi_status > 0 else "Tidak Ada Laporan Spesifik"


    # =====================================
    # Tampilkan Ringkasan Hasil di Bagian Atas
    # =====================================
    st.markdown("<h2>📊 Ringkasan Hasil Pemeriksaan:</h2>", unsafe_allow_html=True)
    cols = st.columns(3)

    col_idx = 0
    for key, value in summary_results.items():
        with cols[col_idx]:
            st.metric(label=key, value=value)
        col_idx = (col_idx + 1) % 3

    st.markdown("---")


    # =====================================
    # Tampilkan hasil pemeriksaan detail
    # =====================================
    st.markdown("<h2>📄 Detail Hasil Pemeriksaan:</h2>", unsafe_allow_html=True)

    hasil_files = [
        "hasil/hasil_format_teknis.txt",
        "hasil/hasil_kutipan.txt",
        "hasil/kutipan_revisi.txt",
        "hasil/hasil_kalimat_panjang.txt",
        "hasil/hasil_kalimat_pasif.txt",
        "hasil/hasil_bahasa_tidak_akademik.txt",
        "hasil/hasil_ejaan_tata_bahasa.txt",
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
        clean_file_name = os.path.basename(file_path).replace('_', ' ').replace('.txt', '').title()
        st.markdown(f"<h3>🔎 {clean_file_name}</h3>", unsafe_allow_html=True)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                isi = f.read()

            st.code(isi, language="markdown")

            st.download_button(
                label=f"⬇️ Unduh {clean_file_name}.txt",
                data=isi,
                file_name=os.path.basename(file_path),
                mime="text/plain"
            )
        except FileNotFoundError:
            st.error(f"File hasil '{clean_file_name}.txt' tidak ditemukan. Pastikan modul pemeriksaan terkait berhasil membuatnya.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file '{clean_file_name}.txt': {e}")

        st.markdown("---")

    st.success("✅ Pemeriksaan selesai. Anda bisa membaca atau mengunduh semua hasil di atas.")

    # Opsional: Hapus file sementara setelah selesai
    # if os.path.exists(temp_docx_path):
    #     os.remove(temp_docx_path)
