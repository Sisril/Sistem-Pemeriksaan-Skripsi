from docx import Document
import re
import os

def analyze_apa_citations(doc_path):
    # Inisialisasi default counts jika terjadi error saat pemrosesan
    len_proper_citations = 0
    len_incomplete_citations = 0

    try:
        # --- MULAI BLOK TRY UNTUK PEMROSESAN DOKUMEN ---
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

        output_dir = "hasil"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        hasil_kutipan_path = os.path.join(output_dir, "hasil_kutipan.txt")
        kutipan_revisi_path = os.path.join(output_dir, "kutipan_revisi.txt")

        with open(hasil_kutipan_path, 'w', encoding='utf-8') as f1:
            f1.write("DAFTAR KUTIPAN APA YANG BENAR:\n\n")
            if proper_citations:
                for i, (n1, n2, yr) in enumerate(proper_citations, 1):
                    citation = f"{n1} & {n2}, {yr}" if n2 else f"{n1}, {yr}"
                    f1.write(f"{i}. ({citation})\n")
            else:
                f1.write("Tidak ditemukan kutipan APA yang benar.\n")

        with open(kutipan_revisi_path, 'w', encoding='utf-8') as f2:
            f2.write("DAFTAR KUTIPAN YANG MEMERLUKAN REVISI:\n\n")
            f2.write("Berikut adalah kutipan yang hanya menyebutkan nama tanpa tahun:\n\n")
            if incomplete_citations:
                for i, cit in enumerate(incomplete_citations, 1):
                    f2.write(f"{i}. {cit}\n")
            else:
                f2.write("Tidak ditemukan kutipan yang memerlukan revisi.\n")
            f2.write("\nCATATAN REVISI:\n")
            f2.write("- Tambahkan tahun publikasi setelah nama penulis\n")
            f2.write("- Pastikan format mengikuti pola (Penulis, Tahun)\n")
            f2.write("- Untuk beberapa penulis: (Penulis1 & Penulis2, Tahun)\n")
            f2.write("- Untuk lebih dari 2 penulis: (Penulis1 et al., Tahun)\n")

        print(f"DEBUG: File '{hasil_kutipan_path}' berhasil ditulis oleh cek_kutipan.py.")
        print(f"DEBUG: File '{kutipan_revisi_path}' berhasil ditulis oleh cek_kutipan.py.")

        # Setel nilai yang akan dikembalikan jika semua proses berhasil
        len_proper_citations = len(proper_citations)
        len_incomplete_citations = len(incomplete_citations)

    except Exception as e:
        # Jika terjadi error di mana pun dalam blok try, cetak error dan kembalikan nilai default
        print(f"ERROR: Terjadi kesalahan di cek_kutipan.py: {e}")
        # len_proper_citations dan len_incomplete_citations sudah 0 dari inisialisasi awal

    print("Hasil tersimpan dalam:")
    print(f"- {hasil_kutipan_path}")
    print(f"- {kutipan_revisi_path}")

    return len_proper_citations, len_incomplete_citations
