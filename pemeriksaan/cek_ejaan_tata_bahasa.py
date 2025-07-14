from docx import Document
import os
from textblob import TextBlob
import nltk

def analyze_spelling_grammar(doc_path):
    # Inisialisasi default count jika terjadi error
    total_issues = 0

    try:
        # --- MULAI BLOK TRY UNTUK PEMROSESAN DOKUMEN ---
        doc = Document(doc_path)
        full_text = ' '.join([para.text for para in doc.paragraphs])
        
        blob = TextBlob(full_text)
        
        misspelled_words = []
        for word, tag in blob.tags:
            if word.isalpha() and word.lower() != word.correct().lower():
                misspelled_words.append(f"Kata salah eja: '{word}' -> Saran: '{word.correct()}'")

        output_dir = "hasil"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file_path = os.path.join(output_dir, "hasil_ejaan_tata_bahasa.txt")
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN EJAAN DAN TATA BAHASA:\n\n")
            if len(misspelled_words) > 0:
                f.write(f"Ditemukan {len(misspelled_words)} potensi kesalahan ejaan:\n\n")
                for i, issue in enumerate(misspelled_words, 1):
                    f.write(f"{i}. {issue}\n")
                f.write("\nCATATAN REVISI:\n")
                f.write("- Periksa kembali ejaan kata-kata yang disarankan.\n")
                f.write("- Perbaiki kesalahan tata bahasa jika ada.\n")
            else:
                f.write("Tidak ditemukan potensi kesalahan ejaan atau tata bahasa dasar.\n")
                f.write("Pastikan untuk tetap melakukan peninjauan manual.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_ejaan_tata_bahasa.py.")
        print(f"Ditemukan {len(misspelled_words)} potensi kesalahan ejaan. Hasil disimpan di '{output_file_path}'.")

        # Setel nilai yang akan dikembalikan jika semua proses berhasil
        total_issues = len(misspelled_words)

    except Exception as e:
        # Jika terjadi error, cetak error dan kembalikan nilai default
        print(f"ERROR: Terjadi kesalahan di cek_ejaan_tata_bahasa.py: {e}")
        # total_issues sudah 0 dari inisialisasi awal

    return total_issues
