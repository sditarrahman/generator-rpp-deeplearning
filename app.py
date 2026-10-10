import streamlit as st
import google.generativeai as genai
import docx
from io import BytesIO

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="centered")

# Judul Aplikasi
st.title("🤖 Web Generator Modul Ajar Otomatis")
st.markdown("Aplikasi ini membantu guru menyusun rancangan pembelajaran mendalam (*Deep Learning*) yang memuat unsur **Mindful, Meaningful, dan Joyful** serta terintegrasi **TPACK**.")

# Mengambil API Key dari brankas rahasia Streamlit (Secrets)
try:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
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
    # Cek kelengkapan data wajib
    if not mapel or not kelas or not topik:
        st.warning("⚠️ Mohon lengkapi Mata Pelajaran, Fase / Kelas, dan Topik / Materi!")
    else:
        try:
            # Menggunakan model Gemini paling update
            model = genai.GenerativeModel('gemini-flash-latest')
            
            # Perintah (Prompt) AI Skala Makro berstandar Pengawas dengan 3 Jenis LKPD Variatif
            prompt = f"""
            Bertindaklah sebagai Pengawas Sekolah dan Ahli Kurikulum Merdeka tingkat mahir. Buatlah Perencanaan Pembelajaran Mendalam (Deep Learning) atau Modul Ajar yang komprehensif, terstruktur, dan berstandar tinggi.

            Berikut adalah data pembelajarannya:
            - Nama Penyusun: {nama_guru}
            - Satuan Pendidikan: {sekolah}
            - Mata Pelajaran: {mapel}
            - Fase / Kelas: {kelas}
            - Topik / Materi: {topik}
            - Alokasi Waktu: {durasi}

            Berdasarkan data di atas, susunlah modul ajar dengan struktur detail dan wajib persis seperti kerangka berikut:

            1. IDENTITAS MODUL: Sajikan dalam bentuk daftar yang rapi.
            2. IDENTIFIKASI MURID:
               - Pengetahuan Awal.
               - Minat Belajar & Pertanyaan Pemantik.
               - Latar Belakang & Kebutuhan Belajar: Uraikan pembagian berdasarkan gaya belajar Visual, Auditori, dan Kinestetik.
            3. MATA PELAJARAN:
               - Jenis Pengetahuan yang Akan Dicapai (Faktual, Konseptual, Prosedural).
               - Relevansi dengan Kehidupan Nyata.
               - Struktur Materi.
            4. DIMENSI PROFIL LULUSAN: Cantumkan minimal 4 dimensi karakter yang relevan.
            5. DESAIN PEMBELAJARAN:
               - Capaian Pembelajaran (Sesuaikan dengan fase dan mapel).
               - Lintas Disiplin Ilmu (Kaitkan dengan mapel lain).
               - Pemahaman Bermakna.
               - Tujuan Pembelajaran: WAJIB gunakan Taksonomi Bloom berurutan dari C1 (Mengingat/Mengidentifikasi) sampai C6 (Mengevaluasi/Mencipta).
               - Indikator Ketercapaian Tujuan Pembelajaran (IKTP).
            6. PRAKTIK PEDAGOGIS & LINGKUNGAN BELAJAR:
               - Pendekatan (Deep Learning), Metode, dan Model Pembelajaran: WAJIB gunakan Problem-Based Learning (PBL).
               - Lingkungan Belajar: Jelaskan desain Ruang Fisik (tata letak bangku, pojok belajar), Ruang Virtual, dan Budaya Belajar (Growth Mindset).
               - Pemanfaatan Digital (TPACK).
            7. PENGALAMAN BELAJAR (SKENARIO KEGIATAN):
               - Susun skenario dengan sangat rinci (Kegiatan Awal, Inti, dan Penutup).
               - Kegiatan Inti WAJIB memuat 5 Sintaks PBL secara berurutan: (1) Orientasi siswa pada masalah, (2) Mengorganisasikan siswa untuk belajar, (3) Membimbing penyelidikan individu/kelompok, (4) Mengembangkan dan menyajikan hasil karya/solusi, (5) Menganalisis dan mengevaluasi proses pemecahan masalah.
               - ATURAN WAJIB: Di setiap akhir kalimat aktivitas guru/siswa, cantumkan tag/label Deep Learning persis seperti ini: [Tahap: (Sebutkan tahapnya), Prinsip: Mindful / Meaningful / Joyful]. Pastikan ketiga prinsip tersebut terdistribusi merata.
            8. ASESMEN PEMBELAJARAN: Jelaskan pelaksanaan asesmen Awal, Proses (Formatif), dan Akhir (Sumatif). Lengkapi dengan indikator yang jelas, bukan sekadar template kosong.
            9. PENGAYAAN DAN REMEDIAL.
            10. REFLEKSI PEMBELAJARAN: Susun daftar pertanyaan refleksi untuk Guru dan Murid.
            11. LAMPIRAN (WAJIB ADA): 
                - Rangkuman ringkas Bahan Ajar dan Media Pembelajaran. 
                - KISI-KISI RUBRIK PENILAIAN yang berisi indikator konkret. 
                - SEBAGAI SOLUSI KETIADAAN BUKU LKS, WAJIB BUATKAN 3 (TIGA) JENIS LEMBAR KERJA PESERTA DIDIK (LKPD) FULL DAN SIAP CETAK. Ketiga LKPD tersebut harus bervariasi:
                  * LKPD 1: PEMAHAMAN KONSEP DASAR. Berisi soal-soal terstruktur untuk memastikan murid memahami teori dasar dari materi.
                  * LKPD 2: SOAL HOTS (Higher Order Thinking Skills). Berisi studi kasus pemecahan masalah tingkat tinggi (menganalisis dan mengevaluasi).
                  * LKPD 3: EKSPLORASI TERBUKA (Open-Ended) / PENALARAN KRITIS. Berisi pertanyaan esai pemantik di mana jawabannya membebaskan murid untuk berpendapat berdasarkan pemahaman, imajinasi, dan logika kritis mereka sendiri (tidak ada jawaban baku).
                  Setiap LKPD harus memuat: Identitas (Nama), Tujuan, Petunjuk Pengerjaan, Narasi Masalah, dan Ruang/Tabel Isian yang siap dijawab oleh siswa.
            
            Gunakan gaya bahasa formal, akademis, inovatif, dan berpusat pada peserta didik sesuai standar regulasi terbaru. Gunakan format Markdown (bold, italic, list) yang sangat rapi agar saat dikonversi ke Microsoft Word hasilnya memukau.
            """
            
            # Menampilkan animasi loading
            with st.spinner("🤖 AI sedang merancang Modul Ajar dan 3 Jenis LKPD Anda. Mohon tunggu sekitar 15-25 detik..."):
                response = model.generate_content(prompt)
                
            st.success("✅ Modul Ajar dan LKPD variatif berhasil dibuat!")
            st.markdown(response.text)
            
            # --- PROSES MEMBUAT FILE WORD OTOMATIS ---
            doc = docx.Document()
            for baris in response.text.split('\n'):
                doc.add_paragraph(baris)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            # Menampilkan tombol Download Word (.docx)
            st.download_button(
                label="📥 Download Modul Ajar + 3 LKPD (Format Word / .docx)",
                data=buffer,
                file_name=f"Modul_Ajar_Lengkap_{mapel}_{kelas}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan pada sistem AI: {e}")
