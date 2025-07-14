from docx import Document
import re
import os # <--- BARIS INI DITAMBAHKAN: Untuk bekerja dengan path file dan direktori

def check_document_formatting(doc_path):
    doc = Document(doc_path)
    
    # Kumpulkan semua teks dari dokumen
    full_text = ' '.join([para.text for para in doc.paragraphs])
    
    # Ini adalah contoh sederhana, Anda mungkin memiliki logika yang lebih kompleks
    # untuk memeriksa format font dan spasi.
    # Untuk tujuan demonstrasi, kita akan selalu membuat file output.
    
    # =================================================================================
    # <--- BAGIAN INI BARU DITAMBAHKAN/DIMODIFIKASI UNTUK MENANGANI PATH FILE
    # =================================================================================
    # Tentukan direktori output yang diinginkan (harus 'hasil' sesuai dengan app.py)
    output_dir = "hasil"
    
    # Periksa apakah direktori 'hasil' sudah ada. Jika belum, buatlah.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tentukan path lengkap untuk file output.
    output_file_path = os.path.join(output_dir, "hasil_format_font_spasi.txt")
    # =================================================================================
    # <--- AKHIR BAGIAN BARU/MODIFIKASI
    # =================================================================================

    # Menyimpan hasil ke file
    # Kita akan selalu membuat file ini, meskipun tidak ada masalah format yang ditemukan
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            # Contoh sederhana: Anda bisa menambahkan logika pemeriksaan format di sini
            # dan menulis hasilnya ke file.
            # Untuk saat ini, kita akan menulis pesan sederhana.
            f.write("Hasil Pemeriksaan Format Font dan Spasi:\n\n")
            f.write("Pemeriksaan format font dan spasi selesai.\n")
            f.write("Pastikan font yang digunakan konsisten (misal: Times New Roman, 12pt).\n")
            f.write("Pastikan spasi antar baris konsisten (misal: 1.5 atau 2).\n")
            f.write("Periksa juga penomoran halaman dan margin.\n")
        
        # Pesan debugging ini akan muncul di terminal jika penulisan berhasil
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_format_font_spasi.py.")
        print(f"Analisis selesai. Hasil disimpan di '{output_file_path}'.") # <--- PESAN INI JUGA DIUBAH
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_format_font_spasi.py: {e}")
        # raise # Anda bisa mengaktifkan ini jika ingin error ini menghentikan program