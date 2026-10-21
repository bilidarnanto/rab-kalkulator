# README — Kalkulator RAB (GitHub Pages)

Kalkulator RAB sederhana: konversi **campervan / motorhome / food truck / instalasi PLTS**,
berbasis satu file `index.html` (tanpa build, tanpa dependensi).

## Run lokal
Buka `index.html` langsung di browser (double-click / `file://`), tanpa server.

## Deploy GitHub Pages
1. Buat repo (mis. `rab-kalkulator`).
2. Upload/salin: `index.html`, `.nojekyll`, `README.md`, `RESEARCH.md`, `PROGRESS.md`.
3. **Settings → Pages → Branch `main` / folder `/ (root)` → Save.**
4. Akses: `https://<user>.github.io/<repo>/`.

Catatan: file `index.html` gratis semua logic-nya di sisi browser (state tersimpan di
`localStorage`), jadi tidak butuh backend atau secrets.

## Struktur
- `index.html` — aplikasi (kalkulator + RAB + tabel harga; cetak/PDF tersedia via tombol).
- `build.py` — generator: mengambil `artifacts/catalog.json` (79 komponen real) dan menulis
  `index.html`. Jalankan `python3 build.py` bila katalog harga berubah.
- `artifacts/` — snapshot katalog & mesin hitung situs referensi (EcoPower ID, Aug 2026).
- `research/` — bukti riset harga pasar (Oktober 2026).
- `RESEARCH.md` — ringkasan riset & analisis optimasi komponen.
- `PROGRESS.md` — log progres pengerjaan.

## Perhatian data
Harga menuju katalog vendor asli (terverifikasi pasar Okt 2026 untuk komponen PLTS).
Fitur "Optimasi sizing komponen" mencari kombinasi unit terhemat; mode **referensi**
mengikuti perilaku situs asli (unit terbesar dulu).
