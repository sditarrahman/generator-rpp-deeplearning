import streamlit as st
import google.generativeai as genai
import docx
from docx.shared import Pt
import json
from io import BytesIO

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

st.title("🤖 Web Generator Modul Ajar (JSON Mode)")
st.markdown("Versi ini menggunakan format data terstruktur untuk menjamin **0% error** pada tabel dan layout Microsoft Word.")

# Mengambil API Key dari brankas rahasia Streamlit (Secrets)
try:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Sistem belum dikonfigurasi. Masukkan API_KEY di pengaturan Secrets.")
    st.stop()

with st.form("form_rpp"):
    st.subheader("📝 Masukkan Data Pembelajaran")
    col1, col2 = st.columns(2)
    with col1:
        nama_guru = st.text_input("Nama Penyusun", placeholder="Misal: Budi, S.Pd.")
        sekolah = st.text_input("Satuan Pendidikan", placeholder="Misal: SDN 1 Kediri")
        mapel = st.text_input("Mata Pelajaran *", placeholder="Misal: Matematika")
    with col2:
        kelas = st.text_input("Fase / Kelas *", placeholder="Misal: Fase C / Kelas 6")
        topik = st.text_input("Topik / Materi *", placeholder="Misal: Diagram Alir")
        durasi = st.text_input("Alokasi Waktu", placeholder="Misal: 2 x 35 Menit")
    submit = st.form_submit_button("✨ Buat Modul Ajar & LKPD")

if submit:
    if not mapel or not kelas or not topik:
        st.warning("⚠️ Mohon lengkapi Mata Pelajaran, Fase / Kelas, dan Topik / Materi!")
    else:
        try:
            # Menggunakan JSON Mode pada Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Buatlah Perencanaan Pembelajaran Mendalam (Deep Learning) PBL dan LKPD.
            Data: Guru: {nama_guru}, Sekolah: {sekolah}, Mapel: {mapel}, Kelas: {kelas}, Topik: {topik}, Waktu: {durasi}.

            Keluarkan hasil HANYA dalam format JSON dengan struktur yang persis seperti ini:
            {{
                "modul_ajar": [
                    {{
                        "judul_bab": "1. IDENTITAS MODUL",
                        "isi_teks": ["Nama Guru: ...", "Mata Pelajaran: ..."]
                    }},
                    {{
                        "judul_bab": "2. TUJUAN PEMBELAJARAN",
                        "isi_teks": ["Tujuan 1...", "Tujuan 2..."]
                    }}
                ],
                "lkpd": [
                    {{
                        "judul_lkpd": "LKPD 1: TINGKAT DASAR",
                        "instruksi": ["Langkah 1...", "Langkah 2..."],
                        "tabel_data": [
                            ["Kolom 1", "Kolom 2", "Kolom 3"],
                            ["Baris 1 A", "Baris 1 B", "Baris 1 C"],
                            ["Baris 2 A", "[AREA GAMBAR: Deskripsi]", "Baris 2 C"]
                        ]
                    }}
                ]
            }}
            
            ATURAN PENTING:
            1. Buat 10 Poin standar RPP di dalam array "modul_ajar".
            2. Buat 3 LKPD (Dasar, HOTS, Terbuka) di dalam array "lkpd".
            3. DILARANG menggunakan kode HTML (<br>) atau markdown (*, #) di dalam nilai JSON. Gunakan teks polos (plain text).
            """
            
            with st.spinner("🤖 Menyusun Modul (Menggunakan JSON Schema, Anti-Error)..."):
                # Memaksa Gemini merespons dalam bentuk JSON
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.4 # Suhu diturunkan agar AI lebih patuh pada format
                    )
                )
                
            # Mengubah teks JSON dari Gemini menjadi Dictionary Python
            data = json.loads(response.text)
            st.success("✅ Data berhasil digenerate! Menyusun dokumen Word...")
            
            # --- MULAI MENYUSUN WORD DENGAN PYTHON ---
            doc = docx.Document()
            
            # 1. Menyusun RPP (Poin 1-10)
            for bab in data.get("modul_ajar", []):
                # Tulis Judul Bab (Bold)
                p_judul = doc.add_paragraph()
                run = p_judul.add_run(bab.get("judul_bab", ""))
                run.bold = True
                run.font.size = Pt(12)
                
                # Tulis Isi Teks
                for teks in bab.get("isi_teks", []):
                    doc.add_paragraph(teks, style='List Bullet' if len(bab.get("isi_teks")) > 1 else 'Normal')
            
            doc.add_page_break()
            
            # 2. Menyusun LKPD (Poin 11)
            p_lampiran = doc.add_paragraph()
            run_lampiran = p_lampiran.add_run("11. LAMPIRAN: LKPD")
            run_lampiran.bold = True
            run_lampiran.font.size = Pt(14)
            
            for lkpd in data.get("lkpd", []):
                doc.add_paragraph() # Spasi
                
                # Judul LKPD
                p_judul_lkpd = doc.add_paragraph()
                run_lkpd = p_judul_lkpd.add_run(lkpd.get("judul_lkpd", ""))
                run_lkpd.bold = True
                
                # Instruksi LKPD
                for inst in lkpd.get("instruksi", []):
                    doc.add_paragraph(inst)
                    
                # Menggambar Tabel LKPD
                tabel_data = lkpd.get("tabel_data", [])
                if tabel_data and len(tabel_data) > 0:
                    # Buat tabel berdasarkan jumlah baris dan kolom dari JSON
                    table = doc.add_table(rows=len(tabel_data), cols=len(tabel_data[0]))
                    table.style = 'Table Grid'
                    
                    for r_idx, row_data in enumerate(tabel_data):
                        for c_idx, cell_data in enumerate(row_data):
                            # Jika jumlah kolom konsisten
                            if c_idx < len(table.columns): 
                                table.cell(r_idx, c_idx).text = str(cell_data)
                
                doc.add_paragraph() # Spasi antar LKPD
                    
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Modul Ajar Super Rapi (Word)",
                data=buffer,
                file_name=f"Modul_Ajar_JSON_{mapel}_{kelas}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except json.JSONDecodeError:
            st.error("❌ Gagal membaca format data dari AI. Silakan coba tekan tombol buat lagi.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan sistem: {e}")
