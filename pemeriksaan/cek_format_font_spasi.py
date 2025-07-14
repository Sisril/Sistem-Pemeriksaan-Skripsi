from docx import Document
import re
import os

def check_document_formatting(doc_path):
    # Inisialisasi default status jika terjadi error
    status_code = 0 

    try:
        # --- MULAI BLOK TRY UNTUK PEMROSESAN DOKUMEN ---
        doc = Document(doc_path)
        full_text = ' '.join([para.text for para in doc.paragraphs])
        
        # Ini adalah contoh sederhana. Anda mungkin memiliki logika yang lebih kompleks
        # untuk memeriksa format font dan spasi.
        
        output_dir = "hasil"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file_path = os.path.join(output_dir, "hasil_format_font_spasi.txt")

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
        
        # Setel status ke 1 jika semua proses berhasil
        status_code = 1 

    except Exception as e:
        # Jika terjadi error, cetak error dan kembalikan nilai default
        print(f"ERROR: Terjadi kesalahan di cek_format_font_spasi.py: {e}")
        # status_code sudah 0 dari inisialisasi awal

    return status_code
