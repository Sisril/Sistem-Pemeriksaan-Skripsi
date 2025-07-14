from docx import Document
import re
import os

def detect_non_academic_phrases(doc_path):
    doc = Document(doc_path)
    
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    full_text = ' '.join(full_text)
    
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)
    
    non_academic_phrases_list = [ # Rename variable to avoid conflict
        "menurut saya", "saya berpendapat", "saya rasa", "saya pikir",
        "saya ingin", "saya mencoba", "saya melihat", "saya menyimpulkan",
        "saya beranggapan", "kami beranggapan", "kami menyimpulkan",
        "di sini penulis", "penulis ingin", "penulis mencoba",
        "penulis berpendapat", "dalam penelitian ini akan dicoba",
        "dalam tulisan ini", "tulisan ini mencoba", "tulisan ini bertujuan",
        "tulisan ini mencoba menjelaskan", "saya berharap", "saya menyarankan",
        "menurut kami"
    ]
    
    non_academic_sentences = []
    
    pattern = re.compile('|'.join(non_academic_phrases_list), re.IGNORECASE) # Use renamed variable
    
    for sentence in sentences:
        if pattern.search(sentence):
            non_academic_sentences.append(sentence.strip())
    
    # =====================================
    # Tentukan direktori dan path file output
    # =====================================
    output_dir = "hasil"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, "hasil_bahasa_tidak_akademik.txt")

    total_non_academic_sentences = len(non_academic_sentences)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN BAHASA TIDAK AKADEMIK:\n\n")
            if total_non_academic_sentences > 0:
                for i, sentence in enumerate(non_academic_sentences, 1):
                    f.write(f"Kalimat Tidak Akademik #{i}:\n")
                    f.write(f"{sentence}\n")
                    f.write("-" * 50 + "\n")
                f.write("\nCATATAN REVISI:\n")
                f.write("- Hindari penggunaan frasa personal atau informal dalam penulisan akademik.\n")
                f.write("- Gunakan gaya bahasa yang objektif dan formal.\n")
            else:
                f.write("Tidak ditemukan kalimat tidak akademik.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_bahasa_tidak_akademik.py.")
        print(f"Ditemukan {total_non_academic_sentences} kalimat tidak akademik. Hasil disimpan di '{output_file_path}'.")
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_bahasa_tidak_akademik.py: {e}")
        total_non_academic_sentences = 0

    # <--- Mengembalikan jumlah kalimat tidak akademik
    return total_non_academic_sentences
