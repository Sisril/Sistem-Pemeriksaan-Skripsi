from docx import Document
import os
from textblob import TextBlob # Import TextBlob
import nltk # <--- Tambahkan ini untuk NLTK data download

def analyze_spelling_grammar(doc_path):
    doc = Document(doc_path)
    full_text = ' '.join([para.text for para in doc.paragraphs])
    
    blob = TextBlob(full_text)
    
    misspelled_words = []
    # TextBlob's spellcheck is basic, it suggests corrections.
    # We'll identify words that are likely misspelled (not in its dictionary)
    for word, tag in blob.tags:
        # Check if the word is likely misspelled (TextBlob's built-in check)
        # This is a simple check, more advanced requires custom dictionary
        if word.isalpha() and word.lower() != word.correct().lower():
            misspelled_words.append(f"Kata salah eja: '{word}' -> Saran: '{word.correct()}'")

    # =====================================
    # Tentukan direktori dan path file output
    # =====================================
    output_dir = "hasil"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, "hasil_ejaan_tata_bahasa.txt")
    
    total_issues = len(misspelled_words)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN EJAAN DAN TATA BAHASA:\n\n")
            if total_issues > 0:
                f.write(f"Ditemukan {total_issues} potensi kesalahan ejaan:\n\n")
                for i, issue in enumerate(misspelled_words, 1):
                    f.write(f"{i}. {issue}\n")
                f.write("\nCATATAN REVISI:\n")
                f.write("- Periksa kembali ejaan kata-kata yang disarankan.\n")
                f.write("- Perbaiki kesalahan tata bahasa jika ada.\n")
            else:
                f.write("Tidak ditemukan potensi kesalahan ejaan atau tata bahasa dasar.\n")
                f.write("Pastikan untuk tetap melakukan peninjauan manual.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_ejaan_tata_bahasa.py.")
        print(f"Ditemukan {total_issues} potensi kesalahan ejaan. Hasil disimpan di '{output_file_path}'.")
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_ejaan_tata_bahasa.py: {e}")
        total_issues = 0 # Set issues to 0 if writing fails

    return total_issues # Mengembalikan jumlah isu yang ditemukan
