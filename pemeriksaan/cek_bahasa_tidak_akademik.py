from docx import Document
import re
import os # Pastikan baris ini ada

def detect_non_academic_phrases(doc_path):
    # Membuka dokumen
    doc = Document(doc_path)
    
    # Mengumpulkan semua teks dari dokumen
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    full_text = ' '.join(full_text)
    
    # Memecah teks menjadi kalimat
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)
    
    # Daftar frasa tidak akademik
    non_academic_phrases = [
        "menurut saya", "saya berpendapat", "saya rasa", "saya pikir",
        "saya ingin", "saya mencoba", "saya melihat", "saya menyimpulkan",
        "saya beranggapan", "kami beranggapan", "kami menyimpulkan",
        "di sini penulis", "penulis ingin", "penulis mencoba",
        "penulis berpendapat", "dalam penelitian ini akan dicoba",
        "dalam tulisan ini", "tulisan ini mencoba", "tulisan ini bertujuan",
        "tulisan ini mencoba menjelaskan", "saya berharap", "saya menyarankan",
        "menurut kami"
    ]
    
    # Menyimpan kalimat yang mengandung frasa tidak akademik
    non_academic_sentences = []
    
    # Pola untuk mendeteksi frasa tidak akademik
    pattern = re.compile('|'.join(non_academic_phrases), re.IGNORECASE)
    
    for sentence in sentences:
        if pattern.search(sentence):
            non_academic_sentences.append(sentence.strip())
    
    # Tentukan direktori output
    output_dir = "hasil"
    
    # Pastikan direktori 'hasil' sudah ada. Jika belum, buatlah.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tentukan path lengkap untuk file output.
    output_file_path = os.path.join(output_dir, "hasil_bahasa_tidak_akademik.txt")

    # =================================================================================
    # BAGIAN PENTING YANG DIMODIFIKASI: File selalu dibuat
    # =================================================================================
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            if non_academic_sentences:
                for i, sentence in enumerate(non_academic_sentences, 1):
                    f.write(f"Kalimat Tidak Akademik #{i}:\n")
                    f.write(f"{sentence}\n")
                    f.write("-" * 50 + "\n")
                print(f"Ditemukan {len(non_academic_sentences)} kalimat tidak akademik. Hasil disimpan di '{output_file_path}'")
            else:
                # Jika tidak ada kalimat tidak akademik, tulis pesan ke file
                f.write("Tidak ditemukan kalimat tidak akademik.\n")
                print(f"Tidak ditemukan kalimat tidak akademik. Hasil disimpan di '{output_file_path}'")
        
        # Pesan debugging ini akan muncul di terminal jika penulisan berhasil
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_bahasa_tidak_akademik.py.")
    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_bahasa_tidak_akademik.py: {e}")
        # raise # Anda bisa mengaktifkan ini jika ingin error ini menghentikan program
    # =================================================================================
    # AKHIR BAGIAN MODIFIKASI
    # =================================================================================
