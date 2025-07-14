from docx import Document
import re
import os

def detect_phrases(doc_path):
    doc = Document(doc_path)
    full_text = ' '.join([para.text for para in doc.paragraphs])

    # Daftar frasa yang harus ada (contoh)
    required_phrases = [
        "Halaman Pengesahan", "Pernyataan Keaslian Skripsi", "Abstrak",
        "Kata Pengantar", "Daftar Isi", "Daftar Tabel", "Daftar Gambar",
        "Daftar Pustaka", "Lampiran"
    ]

    found_phrases = []
    not_found_phrases = []

    for phrase in required_phrases:
        if re.search(r'\b' + re.escape(phrase) + r'\b', full_text, re.IGNORECASE):
            found_phrases.append(phrase)
        else:
            not_found_phrases.append(phrase)

    # =====================================
    # Tentukan direktori dan path file output
    # =====================================
    output_dir = "hasil"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, "hasil_format_teknis.txt")

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN FORMAT TEKNIS:\n\n")
            f.write("✅ Ditemukan: " + str(found_phrases) + "\n")
            f.write("❌ Tidak ditemukan: " + str(not_found_phrases) + "\n\n")
            if "Lampiran" in not_found_phrases:
                f.write("Catatan: Periksa apakah Lampiran diperlukan dan sudah disertakan.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_format_teknis.py.")
        print(f"✅ Ditemukan: {found_phrases}")
        print(f"❌ Tidak ditemukan: {not_found_phrases}")
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_format_teknis.py: {e}")
        # Jika terjadi error, set counts to 0
        found_phrases = []
        not_found_phrases = []

    # <--- Mengembalikan jumlah frasa yang ditemukan dan tidak ditemukan
    return len(found_phrases), len(not_found_phrases)
