import streamlit as st
import google.generativeai as genai
import docx
from docx.shared import Pt, RGBColor
import re
from io import BytesIO

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

st.title("🤖 Web Generator Modul Ajar Otomatis")
st.markdown("Aplikasi ini membantu guru menyusun rancangan pembelajaran mendalam (*Deep Learning*) terintegrasi LKPD Estetik.")

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
            model = genai.GenerativeModel('gemini-flash-latest')
            
            prompt = f"""
            Buatlah Perencanaan Pembelajaran Mendalam (Deep Learning) PBL dan LKPD.
            Data: Guru: {nama_guru}, Sekolah: {sekolah}, Mapel: {mapel}, Kelas: {kelas}, Topik: {topik}, Waktu: {durasi}.

            Buat struktur 11 Poin standar RPP (Identitas hingga Refleksi).
            
            PADA POIN 11 (LAMPIRAN), BUAT 3 LKPD (Dasar, HOTS, Terbuka).
            ATURAN ESTETIKA LKPD WAJIB:
            1. Jangan gunakan ASCII Art (seperti kotak dari tanda + dan -). 
            2. Gunakan TABEL MARKDOWN ASLI (dengan tanda | ) untuk setiap kolom isian, ruang gambar, atau format soal agar rapi di MS Word.
            3. Berikan [AREA GAMBAR: Deskripsikan gambar apa yang harus dimasukkan guru di sini, misal: "Gambar anak membuang sampah"] di dalam tabel agar LKPD menarik. Gunakan emoji yang relevan pada judul dan instruksi.

            Gunakan gaya bahasa formal. Pastikan pembuatan tabel rapi.
            """
            
            with st.spinner("🤖 Merancang Modul Ajar dan LKPD Estetik (20 detik)..."):
                response = model.generate_content(prompt)
                
            st.success("✅ Selesai dibuat!")
            
            # PROSES PARSING KE WORD YANG DIPERBAIKI (BEBAS SIMBOL KOTOR)
            doc = docx.Document()
            lines = response.text.split('\n')
            
            in_table = False
            table_data = []
            
            def clean_text_for_word(text):
                # Menghapus sisa simbol markdown yang sering bocor
                text = text.replace('#', '').replace('**', '').replace('*', '').replace('`', '').replace('>', '').strip()
                return text

            for line in lines:
                line_strip = line.strip()
                
                # Deteksi Tabel
                if line_strip.startswith('|') and line_strip.endswith('|'):
                    in_table = True
                    row = [cell.strip() for cell in line_strip.split('|')[1:-1]]
                    if not all(c == '' or set(c).issubset({'-', ':', ' '}) for c in row):
                        table_data.append(row)
                    continue
                else:
                    if in_table and table_data:
                        table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
                        table.style = 'Table Grid'
                        for i, row in enumerate(table_data):
                            for j, cell_text in enumerate(row):
                                if j < len(table.columns):
                                    table.cell(i, j).text = clean_text_for_word(cell_text)
                        table_data = []
                        in_table = False
                        doc.add_paragraph() 

                if not line_strip:
                    if not in_table:
                        doc.add_paragraph()
                    continue

                # Format Teks & Bersihkan Simbol
                cleaned_line = clean_text_for_word(line_strip)
                
                if line_strip.startswith('#'):
                    # Jadikan Judul Tebal
                    p = doc.add_paragraph()
                    run = p.add_run(cleaned_line)
                    run.bold = True
                    run.font.size = Pt(14) if line_strip.startswith('# ') else Pt(12)
                elif line_strip.startswith('- ') or line_strip.startswith('* '):
                    p = doc.add_paragraph(style='List Bullet')
                    p.add_run(cleaned_line)
                elif re.match(r'^\d+\.\s', line_strip):
                    p = doc.add_paragraph(style='List Number')
                    p.add_run(re.sub(r'^\d+\.\s', '', cleaned_line))
                else:
                    p = doc.add_paragraph()
                    p.add_run(cleaned_line)
                    
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Modul Ajar + LKPD Rapi (Word)",
                data=buffer,
                file_name=f"Modul_Ajar_Rapi_{mapel}_{kelas}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
