import streamlit as st
import google.generativeai as genai
import docx
from io import BytesIO

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

# Judul Aplikasi
st.title("🤖 Web Generator Modul Ajar Otomatis")
st.markdown("Aplikasi ini membantu guru menyusun rancangan pembelajaran mendalam (*Deep Learning*) yang memuat unsur **Mindful, Meaningful, dan Joyful** serta terintegrasi **TPACK**.")

# Mengambil API Key dari brankas rahasia Streamlit
try:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Sistem belum dikonfigurasi. Pemilik aplikasi harus memasukkan API_KEY di pengaturan rahasia (Secrets) Streamlit.")
    st.stop()

# Formulir Isian Guru
with st.form("form_rpp"):
    st.subheader("📝 Masukkan Data Pembelajaran")
    
    col1, col2 = st.columns(2)
    with col1:
        nama_guru = st.text_input("Nama Penyusun", placeholder="Misal: Budi Santoso, S.Pd.")
        sekolah = st.text_input("Satuan Pendidikan", placeholder="Misal: SDN 1 Kediri")
        mapel = st.text_input("Mata Pelajaran *", placeholder="Misal: Matematika")
    with col2:
        kelas = st.text_input("Fase / Kelas *", placeholder="Misal: Fase C / Kelas 6")
        topik = st.text_input("Topik / Materi *", placeholder="Misal: Diagram Alir")
        durasi = st.text_input("Alokasi Waktu", placeholder="Misal: 2 x 35 Menit")
        
    st.markdown("*Kolom dengan tanda bintang (*) wajib diisi.*")
    
    # Tombol Submit
    submit = st.form_submit_button("✨ Buat Modul Ajar Otomatis")

# Logika Pemrosesan AI
if submit:
    if not mapel or not kelas or not topik:
        st.warning("⚠️ Mohon lengkapi Mata Pelajaran, Fase / Kelas, dan Topik / Materi!")
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Bertindaklah sebagai ahli kurikulum pendidikan dan guru profesional. Buatlah Modul Ajar (RPP) yang mendalam (Deep Learning), memuat unsur Mindful, Meaningful, dan Joyful, serta terintegrasi teknologi (TPACK).

            Berikut adalah data pembelajarannya:
            - Nama Penyusun: {nama_guru}
            - Satuan Pendidikan: {sekolah}
            - Mata Pelajaran: {mapel}
            - Fase / Kelas: {kelas}
            - Topik / Materi: {topik}
            - Alokasi Waktu: {durasi}

            Berdasarkan data di atas, susunlah modul ajar yang mengacu pada regulasi terbaru dengan struktur wajib berikut:
            1. INFORMASI UMUM: Berisi identitas dan data pembelajaran di atas.
            2. CAPAIAN PEMBELAJARAN (CP) & TUJUAN PEMBELAJARAN (TP): Susun CP dan TP secara akurat berdasarkan regulasi kurikulum terbaru yang sesuai dengan materi dan fase tersebut.
            3. INTEGRASI 8 PROFIL LULUSAN: Cantumkan dan deskripsikan bagaimana aktivitas ini memenuhi komponen dari 8 Profil Lulusan.
            4. PRAKTIK PEDAGOGIS: Jelaskan secara spesifik pendekatan, strategi, atau praktik pedagogis mutakhir apa yang diterapkan dalam rancangan ini untuk mencapai tujuan.
            5. PEMAHAMAN BERMAKNA & PERTANYAAN PEMANTIK: Buat pertanyaan yang menggugah nalar kritis siswa.
            6. SKENARIO PEMBELAJARAN (DEEP LEARNING & TPACK):
               - Pendahuluan (Sertakan unsur Mindful)
               - Kegiatan Inti (Sertakan unsur Meaningful, Joyful, dan integrasi TPACK/Teknologi)
               - Penutup (Refleksi dan kesimpulan)
            7. ASESMEN/PENILAIAN: Sertakan instrumen atau rubrik penilaian yang relevan.
            """
            
            with st.spinner("🤖 AI sedang merancang Modul Ajar Anda. Mohon tunggu sekitar 10-20 detik..."):
                response = model.generate_content(prompt)
                
            st.success("✅ Modul Ajar berhasil dibuat!")
            st.markdown(response.text)
            
            doc = docx.Document()
            for baris in response.text.split('\n'):
                doc.add_paragraph(baris)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Modul Ajar (Format Word / .docx)",
                data=buffer,
                file_name=f"Modul_Ajar_{mapel}_{kelas}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan pada sistem AI: {e}")
