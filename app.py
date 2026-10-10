import streamlit as st
import docx
from io import BytesIO
import google.generativeai as genai

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

# Judul Aplikasi
st.title("🤖 Web Generator Modul Ajar Otomatis")
st.markdown("Aplikasi ini membantu guru menyusun rancangan pembelajaran mendalam (*Deep Learning*) yang memuat unsur **Mindful, Meaningful, dan Joyful** serta terintegrasi **TPACK**.")

# Menu Samping (Sidebar) untuk API Key
with st.sidebar:
    st.header("⚙️ Pengaturan Sistem")
    st.markdown("Untuk menggunakan aplikasi ini, masukkan API Key Google Gemini Anda.")
    api_key = st.text_input("Masukkan API Key:", type="password")
    st.markdown("[Klik di sini untuk mendapatkan API Key Gratis](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    st.caption("Dibuat untuk memudahkan guru di Indonesia.")

# Formulir Isian Guru (Bisa disesuaikan dengan form Canva Anda)
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
    submit_button = st.form_submit_button("✨ Buat Modul Ajar Otomatis")

# Logika ketika tombol ditekan
if submit_button:
    if not api_key:
        st.error("⚠️ Gagal: Silakan masukkan API Key di menu sebelah kiri terlebih dahulu!")
    elif not mapel or not kelas or not topik:
        st.warning("⚠️ Gagal: Mata Pelajaran, Kelas, dan Topik wajib diisi!")
    else:
        with st.spinner("🧠 AI sedang menyusun Pengalaman Belajar Mendalam untuk Anda. Mohon tunggu sekitar 10-20 detik..."):
            try:
                # Menghubungkan ke AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                
                # Instruksi Rahasia (Prompt) untuk AI
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
                              
                Tuliskan dalam format Markdown yang rapi, profesional, dan siap pakai.
                """
                
                # Meminta jawaban dari AI
                response = model.generate_content(prompt)
                
                # Menampilkan Hasil
                st.success("✅ Modul Ajar Berhasil Dibuat!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Tombol Download
                st.download_button
                # (Kode di atasnya biarkan saja)
if submit:
        try:
            # Meminta AI membuat modul ajar
            response = model.generate_content(prompt)
            
            # Menampilkan hasil teks di layar web
            st.markdown(response.text)
            
            # --- PROSES MEMBUAT FILE WORD OTOMATIS ---
            doc = docx.Document()
            for baris in response.text.split('\n'):
                doc.add_paragraph(baris)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            # Menampilkan tombol Download Word
            st.download_button(
                label="📥 Download Modul Ajar (Word / .docx)",
                data=buffer,
                file_name="Modul_Ajar.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"Terjadi kesalahan pada sistem AI: {e}")
