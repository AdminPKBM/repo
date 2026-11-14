"""Memeriksa setiap URL di data/semua_link.csv dan menyimpan hasilnya.

Keluaran:
    data/status.csv   status tiap link (kode HTTP, aktif/tidak, waktu cek)
    data/status.json  ringkasan dan daftar link yang tidak aktif

Dirancang untuk berjalan terjadwal di GitHub Actions. Pemeriksaan dibuat
pelan (beberapa koneksi paralel, jeda antar permintaan) agar tidak membebani
server blog.
"""
import csv
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "semua_link.csv")
OUT_CSV = os.path.join(ROOT, "data", "status.csv")
OUT_JSON = os.path.join(ROOT, "data", "status.json")

WORKERS = int(os.environ.get("PING_WORKERS", "4"))
JEDA = float(os.environ.get("PING_JEDA", "0.25"))
TIMEOUT = 20
COBA_ULANG = 2  # untuk link yang gagal, coba ulang agar tidak salah tandai
USER_AGENT = "Mozilla/5.0 (compatible; KangRuliLinkCheck/1.0; +https://www.kangruli.web.id/)"
KONTEKS = ssl.create_default_context()


def permintaan(url, metode):
    req = urllib.request.Request(url, method=metode, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=KONTEKS) as r:
        return r.status, r.geturl()


def cek_sekali(url):
    """Kembalikan (kode, alamat_akhir, keterangan)."""
    ket = ""
    try:
        status, akhir = permintaan(url, "HEAD")
        return status, akhir, ""
    except urllib.error.HTTPError as e:
        if e.code not in (403, 405, 501):
            return e.code, "", e.reason
        ket = f"HEAD ditolak ({e.code}), dicoba GET"
    except Exception as e:
        ket = str(e)[:160]
    # Sebagian server menolak HEAD, jadi coba GET.
    try:
        status, akhir = permintaan(url, "GET")
        return status, akhir, ""
    except urllib.error.HTTPError as e:
        return e.code, "", e.reason
    except Exception as e:
        return 0, "", str(e)[:160] or ket


def cek(url):
    hasil = (0, "", "belum dicek")
    for percobaan in range(COBA_ULANG + 1):
        hasil = cek_sekali(url)
        if 200 <= hasil[0] < 400:
            break
        time.sleep(1.5 * (percobaan + 1))
    time.sleep(JEDA)
    return hasil


def main():
    with open(SRC, encoding="utf-8-sig") as f:
        baris = list(csv.DictReader(f))
    urls = []
    seen = set()
    for r in baris:
        u = (r.get("url") or "").strip()
        if u and u not in seen:
            seen.add(u)
            urls.append((r.get("judul", "").strip(), u))

    print(f"Memeriksa {len(urls)} link dengan {WORKERS} koneksi...", flush=True)
    waktu = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    hasil = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, ((judul, url), (kode, akhir, ket)) in enumerate(zip(urls, ex.map(lambda x: cek(x[1]), urls)), 1):
            aktif = 200 <= kode < 400
            hasil.append({
                "judul": judul,
                "url": url,
                "status": kode,
                "aktif": "ya" if aktif else "tidak",
                "alamat_akhir": akhir if akhir and akhir != url else "",
                "keterangan": ket,
                "diperiksa": waktu,
            })
            if i % 250 == 0:
                print(f"  {i}/{len(urls)} diperiksa", flush=True)

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(hasil[0].keys()))
        w.writeheader()
        w.writerows(hasil)

    tidak_aktif = [h for h in hasil if h["aktif"] == "tidak"]
    ringkasan = {
        "diperiksa_pada": waktu,
        "total": len(hasil),
        "aktif": len(hasil) - len(tidak_aktif),
        "tidak_aktif": len(tidak_aktif),
        "tidak_aktif_daftar": [
            {"url": h["url"], "status": h["status"], "keterangan": h["keterangan"]}
            for h in tidak_aktif
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ringkasan, f, ensure_ascii=False, indent=2)

    print(f"\nSelesai. Aktif: {ringkasan['aktif']} | Tidak aktif: {ringkasan['tidak_aktif']}")
    print(f"Hasil: data/status.csv dan data/status.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
