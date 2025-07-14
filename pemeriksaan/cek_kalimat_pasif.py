from docx import Document
import re

def detect_passive_sentences(doc_path):
    # Membuka dokumen
    doc = Document(doc_path)
    
    # Mengumpulkan semua teks dari dokumen
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    full_text = ' '.join(full_text)
    
    # Memecah teks menjadi kalimat
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)
    
    # Menyimpan kalimat pasif
    passive_sentences = []
    
    # Pola untuk mendeteksi kalimat pasif
    passive_pattern = re.compile(r'\boleh\b|\bdi\w*|telah dilakukan|dapat dilakukan|sedang dilakukan', re.IGNORECASE)
    
    for sentence in sentences:
        if passive_pattern.search(sentence):
            passive_sentences.append(sentence.strip())
    
    # Menyimpan hasil ke file
    if passive_sentences:
        with open('hasil_kalimat_pasif.txt', 'w', encoding='utf-8') as f:
            for i, sentence in enumerate(passive_sentences, 1):
                f.write(f"Kalimat Pasif #{i}:\n")
                f.write(f"{sentence}\n")
                f.write("-" * 50 + "\n")
        print(f"Ditemukan {len(passive_sentences)} kalimat pasif. Hasil disimpan di 'hasil_kalimat_pasif.txt'")
    else:
        print("Tidak ditemukan kalimat pasif.")