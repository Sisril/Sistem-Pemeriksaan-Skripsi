from docx import Document
import re
import os

def detect_passive_sentences(doc_path):
    doc = Document(doc_path)
    full_text = ' '.join([para.text for para in doc.paragraphs])
    
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)
    
    # Pola dasar untuk mendeteksi kalimat pasif dalam Bahasa Indonesia
    # Ini adalah pola sederhana dan mungkin tidak 100% akurat untuk semua kasus
    passive_pattern = re.compile(r'\b(di|ter)\w*\s+\w+', re.IGNORECASE)
    
    passive_sentences = []
    for sentence in sentences:
        if passive_pattern.search(sentence):
            passive_sentences.append(sentence.strip())
            
    # =====================================
    # Tentukan direktori dan path file output
    # =====================================
    output_dir = "hasil"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, "hasil_kalimat_pasif.txt")

    total_passive_sentences = len(passive_sentences)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN KALIMAT PASIF:\n\n")
            if total_passive_sentences > 0:
                f.write(f"Ditemukan {total_passive_sentences} kalimat pasif:\n\n")
                for i, sentence in enumerate(passive_sentences, 1):
                    f.write(f"Kalimat Pasif #{i}:\n")
                    f.write(f"{sentence}\n")
                    f.write("-" * 50 + "\n")
                f.write("\nCATATAN REVISI:\n")
                f.write("- Pertimbangkan untuk mengubah kalimat pasif menjadi kalimat aktif agar tulisan lebih lugas dan jelas.\n")
            else:
                f.write("Tidak ditemukan kalimat pasif.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_kalimat_pasif.py.")
        print(f"Ditemukan {total_passive_sentences} kalimat pasif. Hasil disimpan di '{output_file_path}'")
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_kalimat_pasif.py: {e}")
        total_passive_sentences = 0

    # <--- Mengembalikan jumlah kalimat pasif
    return total_passive_sentences
