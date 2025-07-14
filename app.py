import streamlit as st
import os
from pemeriksaan import cek_format_teknis, cek_kutipan, cek_kalimat_panjang, cek_kalimat_pasif, cek_bahasa_tidak_akademik, cek_format_font_spasi

# =====================================
# Tampilan Header
# =====================================
st.markdown("<h1 style='color:#002147;'>📚 Sistem Pemeriksaan Naskah Skripsi</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#444;'>Program Studi Ilmu Pemerintahan - FISIP Universitas Tadulako</h4>", unsafe_allow_html=True)
st.markdown("---")

# =====================================
# Upload File
# =====================================
uploaded_file = st.file_uploader("📥 Silakan unggah file skripsi (.docx)", type=["docx"])

if uploaded_file is not None:
    with open("skripsi_temp.docx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File **{uploaded_file.name}** berhasil diunggah. Siap diperiksa!")

    # =====================================
    # Jalankan semua pemeriksaan
    # =====================================
    cek_format_teknis.detect_phrases("skripsi_temp.docx")
    cek_kutipan.analyze_apa_citations("skripsi_temp.docx")
    cek_kalimat_panjang.analyze_sentences("skripsi_temp.docx")
    cek_kalimat_pasif.detect_passive_sentences("skripsi_temp.docx")
    cek_bahasa_tidak_akademik.detect_non_academic_phrases("skripsi_temp.docx")
    cek_format_font_spasi.check_document_formatting("skripsi_temp.docx")

    # =================================================================================
    # <--- BAGIAN INI OPSIONAL (DEBUGGING): Untuk memeriksa direktori kerja dan keberadaan file
    # <--- Anda bisa menghapusnya setelah yakin semuanya berfungsi
    # =================================================================================
    st.write(f"Direktori Kerja Saat Ini: `{os.getcwd()}`")
    print(f"DEBUG: Direktori Kerja: {os.getcwd()}") # Ini muncul di terminal VSCode Anda

    # Coba cek path spesifik untuk hasil_kutipan.txt
    debug_hasil_kutipan_path = os.path.join(os.getcwd(), "hasil", "hasil_kutipan.txt")
    st.write(f"Mencoba mencari file: `{debug_hasil_kutipan_path}`")
    print(f"DEBUG: Mencoba mencari file: {debug_hasil_kutipan_path}") # Ini muncul di terminal VSCode Anda

    if os.path.exists(debug_hasil_kutipan_path):
        st.success(f"DEBUG: File `hasil_kutipan.txt` DITEMUKAN di `{debug_hasil_kutipan_path}`.")
    else:
        st.error(f"DEBUG: File `hasil_kutipan.txt` TIDAK DITEMUKAN di `{debug_hasil_kutipan_path}`.")
    # =================================================================================
    # <--- AKHIR BAGIAN OPSIONAL (DEBUGGING)
    # =================================================================================

    # =====================================
    # Tampilkan hasil pemeriksaan
    # =====================================
    st.markdown("## 📄 Hasil Pemeriksaan Naskah:")

    hasil_files = [
        "hasil/hasil_format_teknis.txt",
        "hasil/hasil_kutipan.txt",
        "hasil/kutipan_revisi.txt", # <--- BARIS INI DITAMBAHKAN: Untuk menampilkan hasil revisi kutipan
        "hasil/hasil_kalimat_panjang.txt",
        "hasil/hasil_kalimat_pasif.txt",
        "hasil/hasil_bahasa_tidak_akademik.txt",
        "hasil/hasil_format_font_spasi.txt",
    ]

    # <--- BAGIAN INI DIMODIFIKASI: Perbaikan cara membaca file untuk menghindari f.read() ganda
    for file in hasil_files:
        st.markdown(f"### 🔎 {os.path.basename(file)}")
        
        # Buka file HANYA SEKALI untuk membaca isinya
        with open(file, "r", encoding="utf-8") as f:
            isi = f.read() # <--- BACA SELURUH ISI FILE KE DALAM VARIABEL 'isi'

        # Tampilkan isi file menggunakan st.code
        st.code(isi, language="markdown")

        # Gunakan variabel 'isi' yang sudah dibaca untuk tombol download
        # TIDAK PERLU MEMBUKA FILE LAGI ATAU MEMANGGIL f.read() LAGI
        st.download_button(
            label="⬇️ Download Hasil Ini",
            data=isi, # <--- GUNAKAN VARIABEL 'isi' DI SINI
            file_name=os.path.basename(file),
            mime="text/plain"
        )

        st.markdown("---") # Garis pemisah setelah setiap hasil
    # <--- AKHIR BAGIAN MODIFIKASI

    st.success("✅ Pemeriksaan selesai. Anda bisa membaca atau mengunduh semua hasil di atas.")