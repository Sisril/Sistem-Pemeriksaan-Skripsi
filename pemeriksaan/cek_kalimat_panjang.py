from docx import Document
import re

def analyze_sentences(doc_path):
    # Membuka dokumen
    doc = Document(doc_path)
    
    # Mengumpulkan semua teks dari dokumen
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    full_text = ' '.join(full_text)
    
    # Memecah teks menjadi kalimat
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)
    
    # Mengekstrak kalimat panjang (>25 kata)
    long_sentences = []
    for sentence in sentences:
        words = sentence.split()
        word_count = len(words)
        if word_count > 25:
            long_sentences.append((sentence, word_count))
    
    # Menyimpan hasil ke file
    if long_sentences:
        with open('hasil_kalimat_panjang.txt', 'w', encoding='utf-8') as f:
            for i, (sentence, count) in enumerate(long_sentences, 1):
                f.write(f"Kalimat Panjang #{i} ({count} kata):\n")
                f.write(f"\"{sentence}\"\n")
                f.write("-" * 50 + "\n\n")
        print(f"Ditemukan {len(long_sentences)} kalimat panjang. Hasil disimpan di 'hasil_kalimat_panjang.txt'")
    else:
        print("Tidak ditemukan kalimat yang melebihi 25 kata.")