"""Membuat index.html statis, robots.txt, dan sitemap.xml dari data/semua_link.csv.

Pemakaian:
    python3 scripts/build_site.py https://username.github.io/nama-repo
"""
import csv
import html
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://USERNAME.github.io/NAMA-REPO").rstrip("/")
CSV_PATH = os.path.join(ROOT, "data", "semua_link.csv")


def e(s):
    return html.escape(str(s), quote=True)


rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8-sig")))
for r in rows:
    r["judul"] = (r.get("judul") or "").strip() or r["url"].strip()
    r["tanggal"] = (r.get("tanggal") or "")[:10]
    r["labels"] = [x.strip() for x in (r.get("label") or "").split(",") if x.strip()]
    r["url"] = r["url"].strip()
rows.sort(key=lambda r: r["tanggal"], reverse=True)
total = len(rows)

per_tahun = defaultdict(list)
for r in rows:
    per_tahun[r["tanggal"][:4] or "Lainnya"].append(r)
tahun_urut = sorted(per_tahun, reverse=True)

sections = []
for th in tahun_urut:
    items = []
    for r in per_tahun[th]:
        tgl = f'<time datetime="{e(r["tanggal"])}">{e(r["tanggal"])}</time>' if r["tanggal"] else ""
        cari = e((r["judul"] + " " + " ".join(r["labels"])).lower())
        items.append(
            f'      <li data-cari="{cari}"><a href="{e(r["url"])}" rel="noopener">{e(r["judul"])}</a> {tgl}</li>'
        )
    sections.append(
        f'  <section id="tahun-{th}">\n'
        f'    <h2>{e(th)} <span class="jml">({len(per_tahun[th])})</span></h2>\n'
        f"    <ul>\n" + "\n".join(items) + "\n    </ul>\n  </section>"
    )

nav_links = " ".join(f'<a href="#tahun-{th}">{e(th)}</a>' for th in tahun_urut)

TEKS = {
    "id": {
        "judul": "Arsip Lengkap Artikel Kang Ruli",
        "lead": "Daftar {n} artikel dan halaman dari kangruli.web.id, dari yang terbaru.",
        "ringkas": "Tulisan dikelompokkan per tahun. Gunakan kolom pencarian untuk menemukan judul tertentu, atau pilih tahun di bawah.",
        "label": "Cari judul atau topik",
        "ph": "Contoh: AI, investasi, SMK, shortcut Word",
        "lompat": "Lompat ke tahun",
        "hasil": "{a} dari {b} tulisan cocok.",
        "footer": "Arsip ini dibuat dari daftar resmi tautan blog. Sumber asli setiap tulisan ada di kangruli.web.id.",
        "tombol": "English",
    },
    "en": {
        "judul": "Complete Article Archive by Kang Ruli",
        "lead": "List of {n} articles and pages from kangruli.web.id, newest first.",
        "ringkas": "Articles are grouped by year. Use the search box to find a specific title, or jump to a year below.",
        "label": "Search title or topic",
        "ph": "Example: AI, investing, vocational school, Word shortcuts",
        "lompat": "Jump to year",
        "hasil": "{a} of {b} articles match.",
        "footer": "This archive is built from the official list of blog links. The original source of each article is kangruli.web.id. Article titles remain in Indonesian.",
        "tombol": "Bahasa Indonesia",
    },
}
ID = TEKS["id"]
desk = (
    f"Arsip lengkap {total} artikel dan halaman Kang Ruli dari kangruli.web.id, dikelompokkan per tahun "
    f"dari {tahun_urut[-1]} sampai {tahun_urut[0]}. Cari tulisan tentang AI, keuangan, pendidikan, teknologi, dan lainnya."
)
judul_meta = f"Arsip Lengkap Artikel Kang Ruli: Daftar {total} Tulisan"
jsonld = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": judul_meta,
    "description": desk,
    "url": BASE + "/",
    "inLanguage": ["id", "en"],
    "about": {"@type": "Blog", "name": "Kang Ruli", "url": "https://www.kangruli.web.id/"},
    "numberOfItems": total,
}

TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__JUDUL_META__</title>
<meta name="description" content="__DESK__">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="__BASE__/">
<link rel="alternate" hreflang="id" href="__BASE__/">
<link rel="alternate" hreflang="en" href="__BASE__/">
<link rel="alternate" hreflang="x-default" href="__BASE__/">
<meta property="og:type" content="website">
<meta property="og:title" content="__JUDUL_META__">
<meta property="og:description" content="__DESK__">
<meta property="og:url" content="__BASE__/">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">__JSONLD__</script>
<style>
:root{--fg:#111827;--muted:#6b7280;--line:#e5e7eb;--bg:#fff;--accent:#1d4ed8;--soft:#f3f4f6}
@media (prefers-color-scheme:dark){:root{--fg:#f3f4f6;--muted:#9ca3af;--line:#374151;--bg:#111827;--accent:#93c5fd;--soft:#1f2937}}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--fg);line-height:1.6}
.wrap{max-width:860px;margin:0 auto;padding:32px 20px 64px}
.atas{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}
h1{font-size:1.9rem;margin:0 0 8px;line-height:1.25}
.lead{color:var(--muted);margin:0 0 20px}
.ringkas{color:var(--muted);font-size:.95rem;margin-bottom:24px}
.tombol-bahasa{border:1px solid var(--line);background:transparent;color:var(--accent);padding:6px 12px;border-radius:8px;font:inherit;font-size:.9rem;cursor:pointer}
label{display:block;font-weight:600;margin-bottom:6px}
input[type=search]{width:100%;padding:12px 14px;font:inherit;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}
input[type=search]:focus{outline:2px solid var(--accent);outline-offset:1px}
.lompat{margin:20px 0 8px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.lompat .teks{color:var(--muted);font-size:.92rem}
.lompat a{color:var(--accent);font-size:.92rem;border:1px solid var(--line);padding:3px 10px;border-radius:6px;text-decoration:none}
#hasil{color:var(--muted);font-size:.9rem;min-height:1.4em;margin:8px 0 0}
section{margin-top:28px}
h2{font-size:1.2rem;margin:0 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h2 .jml{color:var(--muted);font-weight:400;font-size:.9rem}
ul{list-style:none;margin:0;padding:0}
li{padding:8px 0;border-bottom:1px solid var(--soft);display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline}
li a{color:var(--accent);text-decoration:none;flex:1 1 360px}
li a:hover{text-decoration:underline}
time{color:var(--muted);font-size:.85rem;white-space:nowrap}
li[hidden],section[hidden]{display:none}
footer{margin-top:40px;color:var(--muted);font-size:.9rem;border-top:1px solid var(--line);padding-top:16px}
</style>
</head>
<body>
<main class="wrap">
<div class="atas">
  <div>
    <h1 data-i18n="judul">__JUDUL_ID__</h1>
    <p class="lead" data-i18n="lead" data-n="__TOTAL__">__LEAD_ID__</p>
  </div>
  <button class="tombol-bahasa" id="ganti-bahasa" type="button" data-bahasa-tujuan="en">__TOMBOL_EN__</button>
</div>
<p class="ringkas" data-i18n="ringkas">__RINGKAS_ID__</p>

<label for="cari" data-i18n="label">__LABEL_ID__</label>
<input id="cari" type="search" data-i18n-ph="ph" placeholder="__PH_ID__" autocomplete="off">
<div id="hasil" aria-live="polite"></div>
<nav class="lompat" aria-label="__LOMPAT_ID__"><span class="teks" data-i18n="lompat">__LOMPAT_ID__:</span> __NAV__</nav>

__SECTIONS__

<footer>
<p data-i18n="footer">__FOOTER_ID__</p>
</footer>
</main>

<script>
(function () {
  var TEKS = __TEKS_JSON__;
  var JUDUL_TITLE = { id: "__JUDUL_META_JS__", en: "__JUDUL_EN_TITLE_JS__" };
  var CACHE_KEY = "lokasi_bahasa";
  var CACHE_HARI = 7;
  // Ubah ke false jika tidak ingin memanggil layanan geolokasi pihak ketiga.
  var DETEKSI_IP = true;

  function dariBrowser() {
    var daftar = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || "en"];
    for (var i = 0; i < daftar.length; i++) {
      if (/^id/i.test(daftar[i])) return "id";
    }
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      if (/^Asia\\/(Jakarta|Pontianak|Makassar|Jayapura)$/.test(tz)) return "id";
    } catch (x) {}
    return "en";
  }

  function bacaCache() {
    try {
      var c = JSON.parse(localStorage.getItem(CACHE_KEY) || "null");
      if (c && c.bahasa && Date.now() - c.waktu < CACHE_HARI * 86400000) return c.bahasa;
    } catch (x) {}
    return null;
  }

  function simpanCache(bahasa) {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ bahasa: bahasa, waktu: Date.now() })); } catch (x) {}
  }

  function deteksiIP(callback) {
    if (!DETEKSI_IP || typeof fetch !== "function") return callback(null);
    var ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); callback(null); }, 2000);
    fetch("https://ipapi.co/json/", ctrl ? { signal: ctrl.signal } : {})
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        clearTimeout(timer);
        callback(d && d.country_code ? (d.country_code === "ID" ? "id" : "en") : null);
      })
      .catch(function () { clearTimeout(timer); callback(null); });
  }

  var input = document.getElementById("cari");
  var hasilEl = document.getElementById("hasil");
  var tombol = document.getElementById("ganti-bahasa");
  var items = document.querySelectorAll("li[data-cari]");
  var sections = document.querySelectorAll("section");
  var total = items.length;
  var bahasaAktif = "id";

  function perbaruiHasil() {
    var q = input.value.trim().toLowerCase();
    var n = 0;
    items.forEach(function (li) {
      var cocok = !q || li.getAttribute("data-cari").indexOf(q) !== -1;
      li.hidden = !cocok;
      if (cocok) n++;
    });
    sections.forEach(function (s) { s.hidden = !s.querySelector("li:not([hidden])"); });
    hasilEl.textContent = q ? TEKS[bahasaAktif].hasil.replace("{a}", n).replace("{b}", total) : "";
  }

  function terapkan(bahasa) {
    var t = TEKS[bahasa];
    bahasaAktif = bahasa;
    document.documentElement.lang = bahasa;
    document.title = JUDUL_TITLE[bahasa];
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      if (k === "lead") el.textContent = t.lead.replace("{n}", el.getAttribute("data-n"));
      else if (t[k] !== undefined) el.textContent = t[k];
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      el.placeholder = t[el.getAttribute("data-i18n-ph")];
    });
    var tujuan = bahasa === "en" ? "id" : "en";
    tombol.textContent = TEKS[tujuan].tombol;
    tombol.setAttribute("data-bahasa-tujuan", tujuan);
    document.querySelector("nav.lompat").setAttribute("aria-label", t.lompat);
    perbaruiHasil();
  }

  input.addEventListener("input", perbaruiHasil);

  tombol.addEventListener("click", function () {
    var tujuan = this.getAttribute("data-bahasa-tujuan");
    try { localStorage.setItem("bahasa_pilihan", tujuan); } catch (x) {}
    terapkan(tujuan);
  });

  var pilihan = null;
  try { pilihan = localStorage.getItem("bahasa_pilihan"); } catch (x) {}

  if (pilihan === "id" || pilihan === "en") {
    terapkan(pilihan);
    return;
  }

  var cache = bacaCache();
  if (cache) {
    terapkan(cache);
    return;
  }

  terapkan(dariBrowser());
  deteksiIP(function (hasilIP) {
    if (!hasilIP) return;
    simpanCache(hasilIP);
    var sudahDipilih = null;
    try { sudahDipilih = localStorage.getItem("bahasa_pilihan"); } catch (x) {}
    if (!sudahDipilih) terapkan(hasilIP);
  });
})();
</script>
</body>
</html>
"""

replacements = {
    "__JUDUL_META__": e(judul_meta),
    "__DESK__": e(desk),
    "__BASE__": e(BASE),
    "__JSONLD__": json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/"),
    "__JUDUL_ID__": e(ID["judul"]),
    "__TOTAL__": str(total),
    "__LEAD_ID__": e(ID["lead"].replace("{n}", str(total))),
    "__TOMBOL_EN__": e(TEKS["en"]["tombol"]),
    "__RINGKAS_ID__": e(ID["ringkas"]),
    "__LABEL_ID__": e(ID["label"]),
    "__PH_ID__": e(ID["ph"]),
    "__LOMPAT_ID__": e(ID["lompat"]),
    "__NAV__": nav_links,
    "__SECTIONS__": "\n".join(sections),
    "__FOOTER_ID__": e(ID["footer"]),
    "__TEKS_JSON__": json.dumps(TEKS, ensure_ascii=False).replace("</", "<\\/"),
    "__JUDUL_META_JS__": judul_meta.replace('"', '\\"'),
    "__JUDUL_EN_TITLE_JS__": "Complete Article Archive by Kang Ruli",
}
page = TEMPLATE
for k, v in replacements.items():
    page = page.replace(k, v)

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(page)
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{BASE}/</loc></url>\n"
        "</urlset>\n"
    )

print(f"tulisan: {total} | tahun: {len(tahun_urut)} | KB: {round(len(page.encode()) / 1024)}")
