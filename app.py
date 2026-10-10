import streamlit as st
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
                Bertindaklah sebagai desainer kurikulum dan ahli pedagogi tingkat lanjut.
                Buatkan Modul Ajar / RPP lengkap berbasis Deep Learning (wajib memuat skenario yang Mindful, Meaningful, dan Joyful) serta terintegrasi TPACK (Technological Pedagogical Content Knowledge).
                
                Gunakan data berikut:
                - Nama Penyusun: {nama_guru if nama_guru else 'Guru Kelas'}
                - Satuan Pendidikan: {sekolah if sekolah else 'Sekolah Dasar'}
                - Mata Pelajaran: {mapel}
                - Fase / Kelas: {kelas}
                - Topik Materi: {topik}
                - Alokasi Waktu: {durasi if durasi else 'Menyesuaikan'}
                
                Struktur dokumen harus mencakup:
                1. IDENTITAS PEMBELAJARAN
                2. TUJUAN PEMBELAJARAN & PEMAHAMAN BERMAKNA
                3. INTEGRASI TPACK & PEMANFAATAN DIGITAL
                4. SKENARIO PENGALAMAN BELAJAR (Detailkan Kegiatan Awal, Inti, dan Penutup dengan tag [Mindful], [Meaningful], dan [Joyful] di setiap aktivitasnya secara otomatis).
                5. PREDIKSI MISKONSEPSI & DIFERENSIASI
                6. ASESMEN PEMBELAJARAN
                
                Tuliskan dalam format Markdown yang rapi, profesional, dan siap pakai.
                """
                
                # Meminta jawaban dari AI
                response = model.generate_content(prompt)
                
                # Menampilkan Hasil
                st.success("✅ Modul Ajar Berhasil Dibuat!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Tombol Download
                st.download_button(
                    label="📥 Unduh Modul Ajar (Format .txt/.md)",
                    data=response.text,
                    file_name=f"Modul_Ajar_{mapel}_{kelas}.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan pada sistem AI: {e}")
