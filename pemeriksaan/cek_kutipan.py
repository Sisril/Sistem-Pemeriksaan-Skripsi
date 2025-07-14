from docx import Document
import re
import os # <--- PASTIKAN BARIS INI ADA

def analyze_apa_citations(doc_path):
    # Membuka dokumen
    doc = Document(doc_path)
    full_text = ' '.join([para.text for para in doc.paragraphs])
    
    # Pola untuk kutipan APA lengkap
    apa_pattern = re.compile(
        r'\((?P<nama1>[A-Z][a-zA-Z]+)(?: & (?P<nama2>[A-Z][a-zA-Z]+))?(?: et al\.)?, (?P<tahun>\d{4})\)',
        re.IGNORECASE
    )
    
    # Pola untuk kutipan tidak lengkap (hanya nama)
    incomplete_pattern = re.compile(
        r'\((?P<nama1>[A-Z][a-zA-Z]+)(?: & (?P<nama2>[A-Z][a-zA-Z]+))?(?: et al\.)?(?:, [^0-9]+)?\)',
        re.IGNORECASE
    )
    
    # Mendeteksi kutipan
    proper_citations = sorted(set(apa_pattern.findall(full_text)), key=lambda x: (x[0], x[2]))
    incomplete_citations = sorted(set(m[0] for m in incomplete_pattern.finditer(full_text) 
                                     if not re.search(r', \d{4}\)', m[0])))

    # =================================================================================
    # BAGIAN PENTING YANG HARUS ADA DAN BENAR DI SINI
    # =================================================================================
    # Tentukan direktori output yang diinginkan (harus 'hasil' sesuai dengan app.py)
    output_dir = "hasil"
    
    # Periksa apakah direktori 'hasil' sudah ada. Jika belum, buatlah.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tentukan path lengkap untuk kedua file yang akan dibuat.
    # INI YANG AKAN MEMASTIKAN FILE DISIMPAN DENGAN NAMA DAN LOKASI YANG BENAR
    hasil_kutipan_path = os.path.join(output_dir, "hasil_kutipan.txt")
    kutipan_revisi_path = os.path.join(output_dir, "kutipan_revisi.txt")
    # =================================================================================
    # AKHIR BAGIAN PENTING
    # =================================================================================

    # Menyimpan hasil
    # PASTIKAN ANDA MENGGUNAKAN hasil_kutipan_path DAN kutipan_revisi_path DI SINI
    try: # <--- try-except ini untuk debugging tambahan, bisa dipertahankan
        with open(hasil_kutipan_path, 'w', encoding='utf-8') as f1, \
             open(kutipan_revisi_path, 'w', encoding='utf-8') as f2:
            
            # File 1: Kutipan APA lengkap (sekarang akan disimpan sebagai hasil_kutipan.txt di folder hasil)
            f1.write("DAFTAR KUTIPAN APA YANG BENAR:\n\n")
            for i, (n1, n2, yr) in enumerate(proper_citations, 1):
                citation = f"{n1} & {n2}, {yr}" if n2 else f"{n1}, {yr}"
                f1.write(f"{i}. ({citation})\n")
            
            # File 2: Catatan revisi (akan disimpan sebagai kutipan_revisi.txt di folder hasil)
            f2.write("DAFTAR KUTIPAN YANG MEMERLUKAN REVISI:\n\n")
            f2.write("Berikut adalah kutipan yang hanya menyebutkan nama tanpa tahun:\n\n")
            for i, cit in enumerate(incomplete_citations, 1):
                f2.write(f"{i}. {cit}\n")
            f2.write("\nCATATAN REVISI:\n")
            f2.write("- Tambahkan tahun publikasi setelah nama penulis\n")
            f2.write("- Pastikan format mengikuti pola (Penulis, Tahun)\n")
            f2.write("- Untuk beberapa penulis: (Penulis1 & Penulis2, Tahun)\n")
            f2.write("- Untuk lebih dari 2 penulis: (Penulis1 et al., Tahun)\n")
        
        # Pesan debugging ini akan muncul di terminal jika penulisan berhasil
        print(f"DEBUG: File '{hasil_kutipan_path}' berhasil ditulis oleh cek_kutipan.py.")
        print(f"DEBUG: File '{kutipan_revisi_path}' berhasil ditulis oleh cek_kutipan.py.")

    except Exception as e:
        print(f"ERROR: Gagal menulis file di cek_kutipan.py: {e}")
        # raise # Anda bisa mengaktifkan ini jika ingin error ini menghentikan program

    # Output hasil (pesan di terminal VSCode Anda)
    # PASTIKAN ANDA MENGGUNAKAN hasil_kutipan_path DAN kutipan_revisi_path DI SINI
    print("Hasil tersimpan dalam:")
    print(f"- {hasil_kutipan_path}") # <--- PASTIKAN INI MENUNJUKKAN PATH YANG BENAR
    print(f"- {kutipan_revisi_path}") # <--- PASTIKAN INI MENUNJUKKAN PATH YANG BENAR
