from docx import Document
import re
import os

def analyze_sentences(doc_path, max_length=25): # Default max_length
    # Inisialisasi default count jika terjadi error
    total_long_sentences = 0

    try:
        # --- MULAI BLOK TRY UNTUK PEMROSESAN DOKUMEN ---
        doc = Document(doc_path)
        full_text = ' '.join([para.text for para in doc.paragraphs])
        
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)
        
        long_sentences = []
        for sentence in sentences:
            words = sentence.split()
            if len(words) > max_length:
                long_sentences.append(sentence.strip())
                
        output_dir = "hasil"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file_path = os.path.join(output_dir, "hasil_kalimat_panjang.txt")

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("HASIL PEMERIKSAAN KALIMAT PANJANG:\n\n")
            if len(long_sentences) > 0:
                f.write(f"Ditemukan {len(long_sentences)} kalimat yang melebihi {max_length} kata:\n\n")
                for i, sentence in enumerate(long_sentences, 1):
                    f.write(f"Kalimat Panjang #{i}:\n")
                    f.write(f"{sentence}\n")
                    f.write("-" * 50 + "\n")
                f.write("\nCATATAN REVISI:\n")
                f.write("- Pertimbangkan untuk memecah kalimat-kalimat ini menjadi beberapa kalimat yang lebih pendek dan mudah dipahami.\n")
            else:
                f.write(f"Tidak ditemukan kalimat yang melebihi {max_length} kata.\n")
        
        print(f"DEBUG: File '{output_file_path}' berhasil ditulis oleh cek_kalimat_panjang.py.")
        print(f"Ditemukan {len(long_sentences)} kalimat panjang. Hasil disimpan di '{output_file_path}'")

        # Setel nilai yang akan dikembalikan jika semua proses berhasil
        total_long_sentences = len(long_sentences)

    except Exception as e:
        # Jika terjadi error, cetak error dan kembalikan nilai default
        print(f"ERROR: Terjadi kesalahan di cek_kalimat_panjang.py: {e}")
        # total_long_sentences sudah 0 dari inisialisasi awal

    return total_long_sentences
