# Panduan Lengkap: Arsip Kang Ruli di GitHub Pages

Panduan ini menjelaskan cara memasang, menjalankan, memverifikasi, dan merawat arsip tautan kangruli.web.id. Ikuti urutannya dari awal. Setiap bagian punya langkah uji, sehingga Anda tahu kapan sebuah tahap sudah berhasil.

---

## Daftar isi

1. Yang perlu disiapkan
2. Memahami isi folder
3. Membuat repositori di GitHub
4. Mengunggah file
5. Mengaktifkan GitHub Pages
6. Mengizinkan GitHub Actions menyimpan hasil
7. Mengatur alamat dasar (base URL)
8. Menjalankan pengecekan link pertama
9. Memverifikasi halaman dan fitur bahasa
10. Mendaftarkan ke mesin pencari
11. Perawatan rutin
12. Pemecahan masalah
13. Hal yang perlu diperhatikan

---

## 1. Yang perlu disiapkan

| Kebutuhan | Keterangan |
|---|---|
| Akun GitHub | Gratis. Daftar di https://github.com/signup |
| Browser | Chrome, Edge, Firefox, atau Safari versi terbaru |
| Python 3.9 atau lebih baru | Hanya diperlukan jika ingin menjalankan skrip di komputer sendiri. Tidak wajib, karena GitHub Actions sudah menjalankannya |
| Folder `repo/` | Hasil dari paket yang sudah disiapkan |

Repositori harus berstatus **public** agar GitHub Pages dan GitHub Actions gratis dipakai tanpa batasan tambahan.

---

## 2. Memahami isi folder

```
repo/
├── index.html                    Halaman arsip utama (sudah dibuat, 4608 tautan)
├── robots.txt                    Aturan untuk mesin pencari
├── sitemap.xml                   Peta situs halaman arsip
├── README.md                     Ringkasan singkat
├── PANDUAN.md                    Dokumen ini
├── data/
│   ├── semua_link.csv            Sumber daftar tautan (4608 baris)
│   ├── status.csv                Hasil pengecekan per tautan (dibuat otomatis)
│   └── status.json               Ringkasan pengecekan (dibuat otomatis)
├── scripts/
│   ├── build_site.py             Membuat ulang index.html, robots.txt, sitemap.xml
│   └── ping.py                   Memeriksa setiap tautan apakah masih aktif
└── .github/
    └── workflows/
        └── ping.yml              Jadwal pengecekan otomatis di GitHub Actions
```

Yang perlu Anda pahami:

- **`index.html`** adalah halaman yang dibaca pengunjung dan mesin pencari. Isinya dibuat dari `data/semua_link.csv` oleh `build_site.py`.
- **`status.csv` dan `status.json`** belum ada sampai pengecekan pertama dijalankan. Keduanya diperbarui otomatis oleh GitHub Actions.
- **Folder `.github`** diawali titik. Pastikan folder ini ikut terunggah (lihat bagian 4).

---

## 3. Membuat repositori di GitHub

1. Login ke https://github.com.
2. Klik tanda **+** di pojok kanan atas, lalu pilih **New repository**.
3. Isi kolom berikut:
   - **Repository name:** `arsip-kangruli` (boleh nama lain, tetapi catat karena dipakai di alamat)
   - **Description:** opsional, misalnya "Arsip tautan kangruli.web.id"
   - **Visibility:** pilih **Public**
   - Jangan centang *Add a README* atau *.gitignore*, karena repositori kosong lebih mudah diisi.
4. Klik **Create repository**.

**Uji:** halaman repositori kosong muncul dengan instruksi "Quick setup". Ini berarti repositori sudah siap.

---

## 4. Mengunggah file

Ada dua cara. Pilih salah satu.

### Cara A: lewat browser (paling mudah)

1. Di halaman repositori, klik **Add file → Upload files**.
2. Seret **seluruh isi** folder `repo/` ke area unggah. Pastikan yang diunggah adalah isi folder, bukan folder `repo` itu sendiri, sehingga `index.html` berada di root repositori.
3. Pastikan folder `.github`, `data`, dan `scripts` ikut terunggah. Jika `.github` tidak terlihat, lihat catatan di bawah.
4. Di bagian **Commit changes**, tulis pesan singkat seperti "Unggah arsip awal", lalu klik **Commit changes**.

Catatan untuk folder `.github`: beberapa browser atau sistem operasi menyembunyikan folder yang diawali titik. Jika tidak yakin, gunakan Cara B.

Batas unggah lewat browser adalah 25 MB per unggahan. Total paket ini sekitar 2,5 MB, jadi aman.

### Cara B: lewat Git (untuk yang sudah terbiasa)

```bash
cd repo
git init -b main
git add .
git commit -m "Unggah arsip awal"
git remote add origin https://github.com/USERNAME/arsip-kangruli.git
git push -u origin main
```

Ganti `USERNAME` dengan nama akun GitHub Anda. Saat diminta login, gunakan token akses pribadi (Personal Access Token), bukan kata sandi.

**Uji:** di halaman repositori, Anda harus melihat folder `data`, `scripts`, dan `.github`, serta file `index.html`, `robots.txt`, dan `sitemap.xml` di root.

---

## 5. Mengaktifkan GitHub Pages

1. Di repositori, buka tab **Settings**.
2. Di menu kiri, pilih **Pages** (di bagian *Code and automation*).
3. Di bagian **Build and deployment**:
   - **Source:** pilih **Deploy from a branch**
   - **Branch:** pilih **main**, lalu folder **/ (root)**
4. Klik **Save**.
5. Tunggu 1 sampai 5 menit. Halaman ini akan menampilkan alamat seperti:
   `https://USERNAME.github.io/arsip-kangruli/`

**Uji:** buka alamat tersebut. Halaman arsip harus tampil dengan judul "Arsip Lengkap Artikel Kang Ruli".

Jika muncul 404, lihat bagian 12.

---

## 6. Mengizinkan GitHub Actions menyimpan hasil

Workflow pengecekan link perlu izin untuk menulis ke repositori. Tanpa izin ini, langkah terakhir akan gagal.

1. Di repositori, buka **Settings → Actions → General**.
2. Gulir ke bagian **Workflow permissions**.
3. Pilih **Read and write permissions**.
4. Klik **Save**.

**Uji:** pengaturan tersimpan dan pilihan tersebut terlihat aktif.

---

## 7. Mengatur alamat dasar (base URL)

Beberapa bagian file memakai alamat lengkap halaman, yaitu `index.html` (untuk canonical dan hreflang), `robots.txt`, dan `sitemap.xml`. Saat ini isinya masih berupa placeholder. Perbaiki dengan menjalankan skrip di komputer Anda.

### Langkah

1. Pastikan Python sudah terpasang. Cek dengan perintah:
   ```
   python3 --version
   ```
   Di Windows, gunakan `python --version` atau `py --version`.

2. Buka terminal di folder `repo/`:
   - **Windows:** buka folder di File Explorer, ketik `cmd` di kotak alamat, lalu Enter.
   - **Mac:** klik kanan folder, pilih **New Terminal at Folder**. Jika tidak ada, buka Terminal lalu ketik `cd ` (dengan spasi) dan seret folder ke jendela Terminal.
   - **Linux:** klik kanan folder, pilih **Open in Terminal**.

3. Jalankan perintah ini, dengan mengganti alamat sesuai akun dan nama repositori Anda:
   ```
   python3 scripts/build_site.py https://USERNAME.github.io/arsip-kangruli
   ```
   Di Windows, gunakan `python` sebagai ganti `python3`.

4. Keluaran akan menampilkan jumlah tulisan dan ukuran file, misalnya:
   ```
   tulisan: 4608 | tahun: 20 | KB: 1535
   ```

5. Di GitHub Desktop atau dengan Git, commit dan push perubahan. Jika Anda mengunggah lewat browser, unggah ulang tiga file ini: `index.html`, `robots.txt`, dan `sitemap.xml`.

**Uji:** buka `robots.txt` di alamat repositori Anda. Isinya harus memuat baris `Sitemap: https://USERNAME.github.io/arsip-kangruli/sitemap.xml`.

---

## 8. Menjalankan pengecekan link pertama

Pengecekan berjalan otomatis setiap 6 jam, tetapi pengecekan pertama sebaiknya dijalankan manual agar Anda bisa melihat hasilnya.

1. Buka tab **Actions** di repositori.
2. Jika muncul pesan bahwa workflow dinonaktifkan, klik tombol untuk mengaktifkannya.
3. Di daftar sebelah kiri, pilih **Cek link aktif**.
4. Klik **Run workflow**, pilih branch **main**, lalu klik tombol hijau **Run workflow**.
5. Klik baris run yang baru muncul untuk melihat lognya.

Estimasi waktu: sekitar 20 sampai 60 menit untuk 4608 tautan, tergantung respons server.

Setelah selesai:
- Di tab **Code**, folder `data` akan berisi `status.csv` dan `status.json`.
- Commit otomatis bernama "Pengecekan link: ..." muncul di riwayat.

**Uji:** buka `data/status.json`. Anda akan melihat angka `total`, `aktif`, dan `tidak_aktif`, serta daftar tautan yang bermasalah.

### Mengubah jadwal

Jadwal diatur di `.github/workflows/ping.yml`, pada baris `cron`. Contohnya:

- Setiap 6 jam (default): `"17 */6 * * *"`
- Sekali sehari pukul 03.00 UTC (pukul 10.00 WIB): `"0 3 * * *"`

Pengecekan sekali sehari sudah cukup untuk sebagian besar kebutuhan dan lebih ringan bagi server blog.

---

## 9. Memverifikasi halaman dan fitur bahasa

### Uji pencarian

1. Buka halaman arsip.
2. Ketik kata seperti `AI` atau `shortcut`.
3. Daftar harus langsung terfilter, dan teks di bawah kolom menampilkan jumlah hasil.

### Uji bahasa otomatis

Bahasa ditentukan oleh lokasi IP pengunjung, jadi perlu diuji dari dua lokasi jika memungkinkan.

**Uji dari Indonesia:**
1. Buka halaman di jendela incognito (agar tidak terpengaruh riwayat).
2. Halaman harus tampil dalam Bahasa Indonesia.

**Uji dari luar Indonesia:**
- Gunakan VPN yang berlokasi di negara lain, atau minta teman di luar negeri membukanya.
- Halaman harus tampil dalam English.

**Uji tombol bahasa:**
1. Klik tombol **English** atau **Bahasa Indonesia** di pojok kanan atas.
2. Bahasa berubah dan pilihan Anda disimpan di browser.

**Mengatur ulang pilihan bahasa:**
- Buka halaman, tekan F12, pilih tab **Console**, lalu ketik:
  ```
  localStorage.clear()
  ```
  Tekan Enter, lalu muat ulang halaman.

**Hal yang bisa membuat bahasa tidak sesuai:**
- Pemblokir iklan atau pelindung privasi bisa memblokir `ipapi.co`. Dalam kasus ini halaman akan memakai bahasa browser sebagai gantinya.
- Layanan `ipapi.co` memiliki batas penggunaan gratis (sekitar 1000 permintaan per hari). Jika batas tercapai, fitur ini juga akan memakai cadangan bahasa browser.
- Pengunjung yang sudah pernah membuka halaman dalam 7 hari terakhir memakai hasil yang disimpan, bukan panggilan baru.

**Uji teknis (opsional):** jika Anda ingin memastikan logika bahasa tidak rusak setelah perubahan kode, jalankan `node` terhadap bagian JavaScript di `index.html`. Ini sudah diuji sebelumnya dengan enam skenario.

---

## 10. Mendaftarkan ke mesin pencari

Halaman ini bisa ditemukan mesin pencari tanpa pendaftaran, tetapi pendaftaran mempercepat proses pengindeksan dan memberi Anda data performa.

### Google Search Console

1. Buka https://search.google.com/search-console.
2. Pilih **Add property**, lalu pilih **URL prefix**.
3. Masukkan alamat halaman, misalnya `https://USERNAME.github.io/arsip-kangruli/`.
4. Pilih metode verifikasi **HTML file**. Google akan memberi satu file, misalnya `google1234abcd.html`.
5. Unduh file itu, letakkan di root repositori (sejajar dengan `index.html`), lalu commit dan push.
6. Kembali ke Search Console dan klik **Verify**.
7. Setelah terverifikasi, buka menu **Sitemaps**, masukkan `sitemap.xml`, lalu klik **Submit**.
8. Buka menu **URL Inspection**, tempel alamat halaman, lalu klik **Request indexing**.

### Bing Webmaster Tools

1. Buka https://www.bing.com/webmasters.
2. Anda bisa mengimpor data dari Search Console agar tidak perlu verifikasi ulang.
3. Atau pilih verifikasi dengan file XML atau meta tag, lalu kirimkan `sitemap.xml`.

### Catatan penting

- Sitemap ini hanya berisi halaman arsip itu sendiri. Tulisan-tulisan di blog sudah memiliki sitemap sendiri di `https://www.kangruli.web.id/sitemap.xml`, dan itulah yang dipakai mesin pencari untuk mengindeks tulisan.
- Untuk membantu mesin pencari menemukan halaman arsip, tambahkan tautan ke halaman tersebut dari blog kangruli.web.id, misalnya di menu atau halaman Sitemap.
- Pengindeksan membutuhkan waktu, biasanya beberapa hari sampai beberapa minggu. Tidak ada jaminan halaman akan berada di peringkat tertentu.

---

## 11. Perawatan rutin

| Frekuensi | Yang dilakukan |
|---|---|
| Otomatis tiap 6 jam (atau sesuai jadwal) | Pengecekan link oleh GitHub Actions |
| Seminggu sekali | Buka `data/status.json`, periksa jumlah tidak aktif |
| Setiap ada tulisan baru | Perbarui daftar (lihat langkah di bawah) |
| Setiap sebulan | Cek Search Console untuk error pengindeksan |

### Memperbarui daftar tautan

Saat ada tulisan baru atau daftar lama perlu diperbarui:

1. Perbarui `data/semua_link.csv` dengan daftar terbaru. Format kolomnya: `tipe,judul,tanggal,label,url`.
2. Jalankan ulang pembuatan halaman:
   ```
   python3 scripts/build_site.py https://USERNAME.github.io/arsip-kangruli
   ```
3. Unggah ulang `index.html`, `robots.txt`, dan `sitemap.xml`, atau commit dan push.

### Menangani tautan yang tidak aktif

1. Buka `data/status.csv`, lalu filter kolom `aktif` dengan nilai `tidak`.
2. Untuk tiap tautan, periksa apakah tulisannya dihapus, dipindah, atau hanya gagal sementara.
3. Jika tulisannya dipindah, perbarui URL di `semua_link.csv`, lalu bangun ulang halaman.
4. Jika tulisannya dihapus, hapus barisnya dari `semua_link.csv`.

Kode status yang sering muncul:

| Kode | Arti | Tindakan |
|---|---|---|
| 200 | Aktif | Tidak perlu tindakan |
| 301 / 302 | Dialihkan | Biasanya aman, tetapi bisa diperbarui ke alamat akhir |
| 403 | Akses ditolak | Sering karena server membatasi bot. Cek manual |
| 404 | Tidak ditemukan | Perlu diperbaiki atau dihapus |
| 410 | Sudah dihapus permanen | Hapus dari daftar |
| 5xx | Error server | Biasanya sementara. Coba lagi nanti |
| 0 | Koneksi gagal | Sering sementara. Coba lagi nanti |

---

## 12. Pemecahan masalah

### Halaman GitHub Pages menampilkan 404

- Tunggu beberapa menit setelah mengaktifkan Pages.
- Pastikan file `index.html` ada di root repositori, bukan di dalam folder.
- Buka tab **Actions** dan cari workflow **pages build and deployment**. Pastikan statusnya berhasil.
- Cek kembali pengaturan di **Settings → Pages**.

### Workflow gagal dengan pesan "Permission denied" atau "refusing to allow"

- Izin tulis belum diatur. Ulangi bagian 6.

### Push ditolak saat commit otomatis

- Kemungkinan Anda dan workflow mengubah file bersamaan. Di komputer, jalankan `git pull` lalu `git push` lagi.
- Workflow sudah memakai `concurrency` untuk mencegah dua run berjalan bersamaan.

### Pengecekan berjalan sangat lama

- Itu normal untuk 4608 tautan. Jika lebih dari 3 jam, workflow akan dihentikan oleh batas `timeout-minutes`.
- Untuk mengurangi waktu, Anda bisa menambah `PING_WORKERS` ke 6, tetapi jangan terlalu tinggi agar server blog tidak terbebani.

### Banyak tautan ditandai tidak aktif padahal halaman bisa dibuka

- Sebagian server membatasi bot dan menolak permintaan dari GitHub Actions, sehingga muncul kode 403 atau 429. Cek beberapa tautan secara manual.
- Jika angka 429 (terlalu banyak permintaan) muncul, kurangi `PING_WORKERS` ke 2 dan naikkan `PING_JEDA` ke 1.

### Halaman tidak berubah bahasa

- Lihat bagian 9, bagian "Hal yang bisa membuat bahasa tidak sesuai".

### Script Python error saat dijalankan di komputer

- Pastikan memakai Python 3.9 atau lebih baru.
- Jalankan dari dalam folder `repo/`, bukan dari folder lain. Skrip membaca `data/semua_link.csv` berdasarkan lokasi skrip itu sendiri, jadi seharusnya tidak bermasalah, tetapi tetap pastikan.

---

## 13. Hal yang perlu diperhatikan

**Keterbatasan yang sudah diketahui:**

- Saya tidak bisa menjalankan GitHub Actions atau mengakses domain blog dari lingkungan kerja saya. Karena itu, pengecekan link dan pengujian di browser belum dilakukan secara langsung. Logika bahasa sudah diuji dengan simulasi, dan script ping sudah diuji dengan server lokal.
- Daftar tautan di `semua_link.csv` berisi 4608 baris, sedangkan total yang Anda sebut 5447. Selisih sekitar 839 tautan belum terkonfirmasi. Periksa jumlah total di bagian awal output `ping.py` atau di dashboard Blogger.
- Halaman arsip hanya memuat tautan yang ada di daftar. Tulisan yang belum masuk daftar tidak akan muncul.

**Privasi:**

- Deteksi lokasi memanggil `ipapi.co` dari browser pengunjung, sehingga alamat IP mereka dikirim ke layanan tersebut. Jika itu tidak diinginkan, ubah `DETEKSI_IP` menjadi `false` di `scripts/build_site.py`.
- Jika Anda memasang halaman privasi di blog, sebutkan penggunaan layanan ini.

**Keamanan dan kepatuhan:**

- Pengecekan link menggunakan `User-Agent` yang jelas dan jeda antar permintaan. Ini membuat aktivitas tersebut mudah dikenali dan tidak membebani server.
- Jangan menjalankan pengecekan lebih sering dari yang diperlukan.

**Lisensi dan konten:**

- Arsip ini hanya berisi tautan dan judul, bukan isi artikel. Namun tetap cantumkan sumber asal dan jangan menyalin isi tulisan tanpa izin.

---

## Ringkasan langkah cepat

1. Buat repositori **public** di GitHub.
2. Unggah seluruh isi folder `repo/`.
3. **Settings → Pages**: branch `main`, folder `/ (root)`.
4. **Settings → Actions → General**: *Read and write permissions*.
5. Jalankan `python3 scripts/build_site.py https://USERNAME.github.io/arsip-kangruli`, lalu unggah ulang file yang berubah.
6. **Actions → Cek link aktif → Run workflow**.
7. Daftarkan di Google Search Console dan Bing Webmaster Tools.
8. Rutin cek `data/status.json`.
