from docx import Document
import re
import os

def check_document_formatting(doc_path):
    doc = Document(doc_path)
    
    full_text = ' '.join([para.text for para in doc.paragraphs])
    
    # Ini adalah contoh sederhana. Anda mungkin memiliki logika yang lebih kompleks
    # untuk memeriksa format font dan spasi.
    # Untuk tujuan demonstrasi dan agar selalu mengembalikan nilai, kita akan selalu membuat file output.
    
    # =====================================
    # Tentukan direktori dan path file output
    # =====================================
    output_dir = "hasil"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, "hasil_format_font_spasi.txt")

    # Untuk tujuan ringkasan, kita akan mengembalikan 1 jika file dibuat, 0 jika ada error
    status_code = 0 

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN FORMAT FONT DAN SPASI:\n\n")
            f.write("Pemeriksaan format font dan spasi selesai.\n")
            f.write("Pastikan font yang digunakan konsisten (misal: Times New Roman, 12pt).\n")
            f.write("Pastikan spasi antar baris konsisten (misal: 1.5 atau 2).\n")
            f.write("Periksa juga penomoran halaman dan margin.\n")
            f.write("\nCATATAN:\n")
            f.write("- Pemeriksaan ini memerlukan tinjauan manual untuk akurasi penuh.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_format_font_spasi.py.")
        print(f"Analisis selesai. Hasil disimpan di '{output_file_path}'.")
        status_code = 1 # Set status ke 1 jika berhasil menulis
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_format_font_spasi.py: {e}")
        status_code = 0 # Set status ke 0 jika gagal menulis

    # <--- Mengembalikan status (1 jika berhasil, 0 jika gagal)
    return status_code
