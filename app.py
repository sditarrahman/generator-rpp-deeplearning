import streamlit as st
import google.generativeai as genai
import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
from io import BytesIO

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

st.title("🤖 Web Generator Modul Ajar (Format Pengawas)")
st.markdown("Versi ini memadukan **Google Gemini JSON Mode** dengan format Block-Rendering untuk meniru 100% struktur dari dokumen pengawas secara rapi dan bebas *error*.")

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
        nama_guru = st.text_input("Nama Penyusun", placeholder="Misal: Budi, S.Pd.")
        sekolah = st.text_input("Satuan Pendidikan", placeholder="Misal: SDN 1 Kediri")
        mapel = st.text_input("Mata Pelajaran *", placeholder="Misal: Matematika")
    with col2:
        kelas = st.text_input("Fase / Kelas / Semester *", placeholder="Misal: C / VI / I")
        topik = st.text_input("Bab / Topik *", placeholder="Misal: Pecahan dan Desimal")
        durasi = st.text_input("Durasi & Jumlah Siswa", placeholder="Misal: 2 JP (28 Siswa)")
    submit = st.form_submit_button("✨ Buat Modul Ajar (Sesuai Standar Pengawas)")

if submit:
    if not mapel or not kelas or not topik:
        st.warning("⚠️ Mohon lengkapi Mata Pelajaran, Kelas, dan Topik!")
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Anda adalah Ahli Kurikulum Merdeka. Buatlah Modul Ajar Deep Learning berbasis Problem-Based Learning (PBL).
            Data: Guru: {nama_guru}, Sekolah: {sekolah}, Mapel: {mapel}, Kelas: {kelas}, Topik: {topik}, Waktu: {durasi}.

            WAJIB tiru struktur KERANGKA PENGAWAS ini secara berurutan:
            1. PERENCANAAN PEMBELAJARAN MENDALAM (DEEP LEARNING) (Judul Utama)
            2. IDENTITAS MODUL
            3. IDENTIFIKASI MURID (Pengetahuan Awal, Minat Belajar, Latar Belakang, Kebutuhan Belajar Visual/Auditori/Kinestetik)
            4. MATA PELAJARAN (Jenis Pengetahuan Faktual/Konseptual/Prosedural, Relevansi, Struktur Materi)
            5. DIMENSI PROFIL LULUSAN
            6. DESAIN PEMBELAJARAN (Capaian Pembelajaran, Lintas Disiplin Ilmu, Pemahaman Bermakna, Tujuan Pembelajaran C1-C6, IKTP)
            7. PRAKTIK PEDAGOGIS (Pendekatan, Metode, Model Pembelajaran WAJIB PBL)
            8. KEMITRAAN PEMBELAJARAN
            9. LINGKUNGAN BELAJAR (Ruang Fisik, Ruang Virtual, Budaya Belajar)
            10. PEMANFAATAN DIGITAL
            11. PENGALAMAN BELAJAR (KEGIATAN AWAL, INTI dgn 5 Sintaks PBL, PENUTUP. Wajib beri tag [Tahap: ..., Prinsip: Mindful/Meaningful/Joyful])
            12. ASESMEN PEMBELAJARAN (Awal, Proses, Akhir)
            13. PENGAYAAN DAN REMIDIAL
            14. REFLEKSI PEMBELAJARAN (Guru, Murid)
            15. LAMPIRAN
                - LAMPIRAN 1: BAHAN AJAR
                - LAMPIRAN 2: MEDIA PEMBELAJARAN
                - LAMPIRAN 3: 3 JENIS LKPD (Dasar, HOTS, Terbuka). Wajib ada [AREA GAMBAR: deskripsi] di dalam tabel LKPD.
                - LAMPIRAN 4: INSTRUMEN PENILAIAN (Rubrik Sikap, Keterampilan, Pengetahuan HARUS TERISI INDIKATORNYA, jangan kosong).

            OUTPUT HARUS BERUPA JSON STRICT dengan format "blocks". DILARANG KERAS menggunakan markdown atau tag HTML di dalam teks JSON.
            Contoh Format JSON:
            {{
              "blocks": [
                {{"type": "heading1", "text": "PERENCANAAN PEMBELAJARAN MENDALAM"}},
                {{"type": "heading1", "text": "IDENTITAS MODUL"}},
                {{"type": "table", "data": [["Nama Penyusun", ":", "{nama_guru}"], ["Mata Pelajaran", ":", "{mapel}"]]}},
                {{"type": "heading2", "text": "Pengetahuan Awal"}},
                {{"type": "paragraph", "text": "Peserta didik telah..."}},
                {{"type": "bullet", "text": "Poin list pertama..."}}
              ]
            }}
            Pilihan type yang diizinkan HANYA: "heading1", "heading2", "heading3", "paragraph", "bullet", "number", "table".
            """
            
            with st.spinner("🤖 Gemini sedang merancang Modul standar Pengawas (Anti-Error)..."):
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.4
                    )
                )
                
            data = json.loads(response.text)
            st.success("✅ Modul berhasil digenerate! Menyusun dokumen Word...")
            
            # --- MULAI MENYUSUN WORD BERDASARKAN BLOK ---
            doc = docx.Document()
            
            for block in data.get("blocks", []):
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
                        doc.add_paragraph() # Spasi ekstra setelah tabel
                    
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Modul Ajar Format Pengawas (Word)",
                data=buffer,
                file_name=f"Modul_Pengawas_{mapel}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except json.JSONDecodeError:
            st.error("❌ Gagal membaca format data dari AI. Silakan coba tekan tombol buat lagi.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan sistem: {e}")
