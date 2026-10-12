import streamlit as st
import google.generativeai as genai
import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
from io import BytesIO

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

st.title("🤖 Web Generator Modul Ajar (Format Pengawas - Fast Split Mode)")
st.markdown("Menggunakan teknik **Generasi 2 Tahap (Split Mode)** untuk menghasilkan Modul Ajar + LKPD super lengkap secara **cepat, stabil, dan bebas error**.")

# Mengambil API Key dari brankas rahasia Streamlit (Secrets)
try:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Sistem belum dikonfigurasi. Masukkan API_KEY di pengaturan Secrets Streamlit.")
    st.stop()

with st.form("form_rpp"):
    st.subheader("📝 Masukkan Data Pembelajaran")
    col1, col2 = st.columns(2)
    with col1:
        nama_guru = st.text_input("Nama Penyusun", placeholder="Misal: Budi Santoso, S.Pd.")
        sekolah = st.text_input("Satuan Pendidikan", placeholder="Misal: SDN 1 Kediri")
        mapel = st.text_input("Mata Pelajaran *", placeholder="Misal: Matematika")
    with col2:
        kelas = st.text_input("Fase / Kelas / Semester *", placeholder="Misal: C / VI / I")
        topik = st.text_input("Bab / Topik *", placeholder="Misal: Pecahan dan Desimal")
        durasi = st.text_input("Durasi & Jumlah Siswa", placeholder="Misal: 2 JP (28 Siswa)")
    submit = st.form_submit_button("✨ Buat Modul Ajar Super Lengkap (Cepat)")

if submit:
    if not mapel or not kelas or not topik:
        st.warning("⚠️ Mohon lengkapi Mata Pelajaran, Kelas, dan Topik!")
    else:
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            gen_config = genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2, # Suhu rendah agar AI memproses teks cepat dan patuh JSON
                max_output_tokens=8192
            )

            # STATUS TRACKER UNTUK USER
            status = st.status("🚀 Memproses dokumen secara bertahap...", expanded=True)

            # ==========================================
            # TAHAP 1: GENERATE INTI RPP / MODUL (1-14)
            # ==========================================
            status.write("⏳ **Tahap 1/2:** Menyusun Inti Modul Ajar, Kajian Materi, & Skenario PBL...")
            
            prompt_tahap1 = f"""
            Anda adalah Ahli Kurikulum Merdeka. Buatlah Bagian Utama Modul Ajar Deep Learning (Poin 1-14) berbasis Problem-Based Learning (PBL) secara DETAIL dan LENGKAP.
            Data: Guru: {nama_guru}, Sekolah: {sekolah}, Mapel: {mapel}, Kelas: {kelas}, Topik: {topik}, Waktu: {durasi}.

            Struktur POIN 1 SAMPAI 14 yang WAJIB dibuat:
            1. PERENCANAAN PEMBELAJARAN MENDALAM (DEEP LEARNING) (Judul Utama)
            2. IDENTITAS MODUL
            3. IDENTIFIKASI MURID (Pengetahuan Awal, Minat Belajar, Latar Belakang, Kebutuhan Belajar Visual/Auditori/Kinestetik)
            4. MATA PELAJARAN (Sangat Luas):
               - Pengetahuan Faktual (Istilah teknis, simbol, lambang, fakta dasar)
               - Pengetahuan Konseptual (Definisi mendalam, prinsip dasar, dan analisis MISKONSEPSI UMUM peserta didik beserta solusinya)
               - Pengetahuan Prosedural (Langkah-langkah teknis, algoritma pengerjaan, dan metode pemecahan masalah)
               - Relevansi Kehidupan Nyata (Aplikasi pada kehidupan sehari-hari, belanja, teknologi, literasi finansial)
               - Struktur & Hirarki Materi (Peta alur materi dari dasar, inti, hingga pengayaan)
            5. DIMENSI PROFIL LULUSAN
            6. DESAIN PEMBELAJARAN (Capaian Pembelajaran, Lintas Disiplin Ilmu, Pemahaman Bermakna, Tujuan Pembelajaran C1-C6, IKTP)
            7. PRAKTIK PEDAGOGIS (Pendekatan Deep Learning, Metode, Model Pembelajaran WAJIB PBL)
            8. KEMITRAAN PEMBELAJARAN
            9. LINGKUNGAN BELAJAR (Ruang Fisik, Ruang Virtual, Budaya Belajar Growth Mindset)
            10. PEMANFAATAN DIGITAL (Integrasi TPACK: PhET/GeoGebra, video animasi, papan digital, kuis real-time)
            11. PENGALAMAN BELAJAR (Rinci 5 Sintaks PBL: Orientasi masalah, Pengorganisasian, Membimbing penyelidikan, Mengembangkan & menyajikan karya, Menganalisis & mengevaluasi. Cantumkan durasi dan tag [Tahap: ..., Prinsip: Mindful/Meaningful/Joyful])
            12. ASESMEN PEMBELAJARAN (Awal, Proses, Akhir)
            13. PENGAYAAN DAN REMEDIAL (Sangat Lengkap: Target, strategi bimbingan, scaffolding, tutor sebaya, dan contoh soal)
            14. REFLEKSI PEMBELAJARAN (Guru & Murid)

            OUTPUT HARUS BERUPA JSON STRICT dengan format "blocks". Tanpa markdown/HTML di dalam teks.
            Format JSON:
            {{
              "blocks": [
                {{"type": "heading1", "text": "PERENCANAAN PEMBELAJARAN MENDALAM"}},
                {{"type": "heading1", "text": "IDENTITAS MODUL"}},
                {{"type": "table", "data": [["Nama Penyusun", ":", "{nama_guru}"], ["Mata Pelajaran", ":", "{mapel}"]]}},
                {{"type": "heading2", "text": "4. MATA PELAJARAN"}},
                {{"type": "paragraph", "text": "Teks..."}},
                {{"type": "bullet", "text": "Poin..."}}
              ]
            }}
            Type yang diizinkan HANYA: "heading1", "heading2", "heading3", "paragraph", "bullet", "number", "table".
            """

            response1 = model.generate_content(prompt_tahap1, generation_config=gen_config)
            data1 = json.loads(response1.text)

            # ==========================================
            # TAHAP 2: GENERATE LAMPIRAN & LKPD (POIN 15)
            # ==========================================
            status.write("⏳ **Tahap 2/2:** Menyusun Bahan Ajar Utuh, 3 LKPD Kreatif, & Rubrik Penilaian...")

            prompt_tahap2 = f"""
            Anda adalah Ahli Kurikulum Merdeka. Buatlah POIN 15 (LAMPIRAN MODUL AJAR) berbasis Problem-Based Learning (PBL) secara KAYA, LENGKAP, DAN KREATIF.
            Data: Guru: {nama_guru}, Sekolah: {sekolah}, Mapel: {mapel}, Kelas: {kelas}, Topik: {topik}.

            Struktur POIN 15 yang WAJIB dibuat:
            15. LAMPIRAN
                - LAMPIRAN 1: BAHAN AJAR (SANGAT KAYA & LENGKAP): Rangkuman materi bacaan utuh untuk siswa, rumus/konsep penting, contoh soal cerita beserta pembahasan langkah demi langkah (step-by-step), serta tips/trik mudah memahami materi.
                - LAMPIRAN 2: MEDIA PEMBELAJARAN (Daftar alat peraga fisik, media digital, dan tabel integrasi media dalam tahapan pembelajaran).
                - LAMPIRAN 3: 3 JENIS LKPD (SEDERHANA, KREATIF, BANYAK SOAL LATIHAN):
                  * LKPD 1 (Tingkat Dasar): Petunjuk singkat, tabel isian sederhana, dan MINIMAL 4 SOAL LATIHAN KONSEPTUAL (Isian/Menjodohkan/Pilihan Singkat).
                  * LKPD 2 (Tingkat HOTS): Narasi kasus nyata, tabel analisis keputusan, dan MINIMAL 3 SOAL STUDI KASUS PEMECAHAN MASALAH.
                  * LKPD 3 (Tingkat Terbuka / Open-Ended): Tantangan proyek kreasi mandiri dan pertanyaan esai penalaran kritis.
                  * Catatan: Selalu sediakan [AREA GAMBAR: deskripsi gambar] di dalam sel tabel tempat gambar/canvas siswa berada.
                - LAMPIRAN 4: INSTRUMEN PENILAIAN (Rubrik Penilaian Sikap, Keterampilan, dan Pengetahuan HARUS TERISI INDIKATOR DAN SKORNYA SECARA LENGKAP, JANGAN KOSONG).

            OUTPUT HARUS BERUPA JSON STRICT dengan format "blocks". Tanpa markdown/HTML di dalam teks.
            Format JSON:
            {{
              "blocks": [
                {{"type": "heading1", "text": "15. LAMPIRAN"}},
                {{"type": "heading2", "text": "LAMPIRAN 1: BAHAN AJAR"}},
                {{"type": "paragraph", "text": "Teks..."}},
                {{"type": "table", "data": [["Kolom 1", "Kolom 2"], ["Data 1", "Data 2"]]}}
              ]
            }}
            Type yang diizinkan HANYA: "heading1", "heading2", "heading3", "paragraph", "bullet", "number", "table".
            """

            response2 = model.generate_content(prompt_tahap2, generation_config=gen_config)
            data2 = json.loads(response2.text)

            # ==========================================
            # PENGABUNGAN DATA & PEMBUATAN WORD (.DOCX)
            # ==========================================
            status.write("⚙️ Merangkaikan seluruh blok ke dalam dokumen Microsoft Word...")

            # Gabungkan blocks dari Tahap 1 dan Tahap 2
            all_blocks = data1.get("blocks", []) + data2.get("blocks", [])

            doc = docx.Document()

            for block in all_blocks:
                b_type = block.get("type")
                b_text = block.get("text", "")

                if b_type == "heading1":
                    p = doc.add_heading(b_text, level=1)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                elif b_type == "heading2":
                    doc.add_heading(b_text, level=2)
                elif b_type == "heading3":
                    doc.add_heading(b_text, level=3)
                elif b_type == "paragraph":
                    doc.add_paragraph(b_text)
                elif b_type == "bullet":
                    doc.add_paragraph(b_text, style='List Bullet')
                elif b_type == "number":
                    doc.add_paragraph(b_text, style='List Number')
                elif b_type == "table":
                    t_data = block.get("data", [])
                    if t_data and len(t_data) > 0:
                        table = doc.add_table(rows=len(t_data), cols=len(t_data[0]))
                        table.style = 'Table Grid'
                        for r_idx, row_data in enumerate(t_data):
                            for c_idx, cell_data in enumerate(row_data):
                                if c_idx < len(table.columns):
                                    table.cell(r_idx, c_idx).text = str(cell_data)
                        doc.add_paragraph() # Spasi setelah tabel

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            status.update(label="✅ Selesai! Modul Ajar + LKPD siap diunduh.", state="complete", expanded=False)

            st.download_button(
                label="📥 Download Modul Ajar Super Lengkap (Word)",
                data=buffer,
                file_name=f"Modul_Pengawas_Lengkap_{mapel}_{kelas}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except json.JSONDecodeError:
            st.error("❌ Gagal membaca respon dari AI. Silakan klik tombol 'Buat' sekali lagi.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan sistem: {e}")
