# Arsip Kang Ruli

Halaman arsip lengkap tautan kangruli.web.id, dengan dua fitur:

1. **Bahasa otomatis.** Halaman mendeteksi lokasi pengunjung (IP) lalu menampilkan Bahasa Indonesia atau English. Jika lokasi tidak bisa dideteksi, halaman memakai bahasa browser dan zona waktu. Pengunjung bisa mengganti bahasa lewat tombol, dan pilihannya diingat di browser.
2. **Pengecekan link aktif.** GitHub Actions memeriksa setiap link setiap 6 jam dan menyimpan hasilnya di `data/status.csv` dan `data/status.json`.

## Struktur

```
index.html              halaman arsip (dibuat oleh scripts/build_site.py)
robots.txt              aturan untuk mesin pencari
sitemap.xml             peta situs halaman arsip
data/semua_link.csv     sumber daftar link
data/status.csv         hasil pengecekan per link (dibuat otomatis)
data/status.json        ringkasan pengecekan (dibuat otomatis)
scripts/build_site.py   membuat ulang index.html dari CSV
scripts/ping.py         memeriksa link aktif
.github/workflows/ping.yml  jadwal pengecekan di GitHub Actions
```

## Cara memasang

1. Buat repositori baru di GitHub, misalnya `arsip-kangruli`, lalu upload seluruh isi folder ini.
2. Buka **Settings → Pages**, pilih **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. Buka **Settings → Actions → General**, lalu di bagian *Workflow permissions* pilih **Read and write permissions**. Ini diperlukan agar workflow bisa menyimpan hasil pengecekan.
4. Ganti alamat dasar di `index.html`, `robots.txt`, dan `sitemap.xml` dengan alamat GitHub Pages Anda:
   ```
   python3 scripts/build_site.py https://USERNAME.github.io/arsip-kangruli
   ```
   Lalu commit dan push.
5. Jalankan pengecekan pertama secara manual: buka tab **Actions → Cek link aktif → Run workflow**.

## Menjalankan secara lokal

```
python3 scripts/ping.py
python3 scripts/build_site.py https://USERNAME.github.io/arsip-kangruli
```

Untuk mengurangi beban server, jumlah koneksi paralel dan jeda bisa diatur lewat variabel `PING_WORKERS` (default 4) dan `PING_JEDA` (default 0.25 detik).

## Catatan

- Deteksi lokasi memanggil layanan `ipapi.co` dari browser pengunjung. Jika tidak ingin itu, ubah `DETEKSI_IP = true` menjadi `false` di `scripts/build_site.py`, lalu jalankan ulang build.
- Judul artikel tetap dalam bahasa Indonesia, karena itu judul asli tulisan. Yang berubah hanya teks antarmuka.
- Setiap kali workflow menyimpan hasil, GitHub Pages ikut dibangun ulang. Ini normal dan tidak memerlukan langkah tambahan.
