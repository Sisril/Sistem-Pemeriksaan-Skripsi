from docx import Document

def detect_phrases(doc_path):
    # Daftar frasa yang akan dideteksi
    phrases = [
        "Halaman Pengesahan", "Pernyataan", "Abstrak", 
        "Kata Pengantar", "Daftar Isi", "Daftar Pustaka", 
        "Lampiran"
    ]

    # Membuka dokumen
    doc = Document(doc_path)
    found_phrases = []
    
    # Membaca semua teks dari dokumen
    for para in doc.paragraphs:
        text = para.text.strip()
        # Mendeteksi frasa
        for phrase in phrases:
            if phrase.lower() in text.lower():
                found_phrases.append(phrase)
                break  # Jika sudah ditemukan, tidak perlu cek frasa lain

    # Menentukan frasa yang tidak ditemukan
    not_found_phrases = [phrase for phrase in phrases if phrase not in found_phrases]

    # Menampilkan hasil deteksi
    print("✅ Ditemukan:", found_phrases)
    print("❌ Tidak ditemukan:", not_found_phrases)

    # Menyimpan hasil deteksi ke file .txt
    with open('hasil_format_teknis.txt', 'w') as f:
        f.write("✅ Ditemukan: " + ', '.join(found_phrases) + '\n')
        f.write("❌ Tidak ditemukan: " + ', '.join(not_found_phrases) + '\n')

        # Menambahkan catatan jika 'Daftar Pustaka' tidak ditemukan
        if "Daftar Pustaka" not in found_phrases:
            f.write("Catatan: Pastikan Daftar Pustaka ditulis dengan benar sebagai bagian wajib dari karya ilmiah.\n")

        # Menambahkan catatan jika 'Lampiran' tidak ditemukan
        if "Lampiran" not in found_phrases:
            f.write("Catatan: Periksa apakah Lampiran diperlukan dan sudah disertakan.\n")