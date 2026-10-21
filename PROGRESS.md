# PROGRESS — Kalkulator RAB GitHub Pages (referensi: nasbpfsby.duckdns.org:8444)

**Status: SELESAI (aplikasi + riset yang memungkinkan). Terakhir: 2026-10-21 ~15:35 WIB**

## Target
- Satu `index.html` GitHub Pages: kalkulator RAB campervan/motorhome/food-truck/PLTS.
- Harga **real** (katalog vendor + verifikasi pasar), mesin hitung = engine referensi (port 1:1).
- Simpel & ringan: vanilla JS, tanpa dependensi, ~41 KB total.

## Selesai
1. **Baseline situs referensi** — SSR HTML + 14 chunk JS; disimpan di `artifacts/`.
2. **Katalog real vendor** — `GET /api/catalog` = 79 komponen, harga Aug 2026 → `artifacts/catalog.json`.
3. **Mesin hitung reverse-engineered** (bukan tebakan — lihat `RESEARCH.md §A`):
   - waste % per kelompok, tenaga kerja `workDays×8×Rp75rb`, kompleksitas 0,8–1,3,
     diskon volume 1/2/3%, kontingensi 3–10%, PPN 11%, margin PLTS 15%.
4. **Sizing PLTS** — `Wp=⌈Wh/(sun×0,75)⌉`, baterai otonomi 2 hari DoD 0,8, inverter 1,25×puncak, SCC 1,25×Wp/12V.
5. **Riset pasar PLTS lengkap** (panel 100–550 Wp, baterai LiFePO4/VRLA, MPPT, inverter, BOS, jasa per Wp) → `RESEARCH.md §B`.
6. **Aplikasi `index.html`** — dibangun via `build.py`; mesin tetap 1:1 dengan referensi:
   - Tab Konfigurator: tipe kendaraan → paket/layout/material/add-on → beban listrik (19 alat) → RAB per kelompok + penjabaran biaya + cetak PDF.
   - Tab PLTS: kalkulator beban mandiri → sizing → RAB (margin 15% + PPN seperti `buildPltsRab`).
   - Tab Tabel Harga: filter + pencarian 79 komponen.
   - Autosave `localStorage`; nada UI mengikuti situs referensi (estimasi 30 hari, verifikasi admin).
   - `node --check` lolos; smoke test engine di Node: 20 baris RAB, bilangan wajar (CV-STD penuh ≈ Rp140 jt, PLTS mandiri contoh ≈ Rp23,8 jt).
7. **Optimasi sizing komponen (mode hemat, default ON)** — formulasi "packPick" (min biaya, qty ≤ batas):
   - Contoh hasil: kebutuhan 3.000 Wh/hari & 800 W → referensi Rp39,77 jt vs hemat **Rp36,02 jt (−9,4%)**
     (2×450 Wp + 4×200 Ah vs rekomendasi situs 2×550 Wp + 3×300 Ah).
   - kebutuhan 700 Wh / 400 W: Rp18,67 jt → **Rp15,57 jt (−16,6%)**.
   - Catatan hidup di UI: Rp/Wp, Rp/Wh, Rp/W inverter, Rp/A MPPT;peringatan bila inverter >2× beban, baterai mentok batas, dll.
8. **README + langkah deploy GitHub Pages** sudah disiapkan.

## Sedang berjalan
- [riset] Perlengkapan & material (18 query Brave, pacing 50 s) — kulkas 12V 60 L terkonfirmasi
  Rp4,49 jt (Taffware T60, Tokopedia) ≈ harga katalog Rp4,5 jt ✅. Selebihnya menunggu file selesai lalu diagregasi.

## Hasil riset putaran perbaikan
- Brave mengaktifkan **captcha tingkat IP** pada putaran appliance — 12 item sisanya
  **tidak terverifikasi eksternal** (pompa, toilet, water-heater, vent, mesin kopi, fryer,
  griddle, hood, kulkas display, freezer, kompor, upah). Bensin harga tetap harga katalog
  vendor asli (real seller), keterbatasan dicatat di `RESEARCH.md §D`. Query yang berhasil:
  panel 100/200/450/550 Wp, baterai LiFePO4 100/200 Ah, inverter, MPPT, MCB AC/DC, kabel NYM,
  plywood, ACM, HPL, kulkas 12V, MC4 §umum.

## Keputusan akhir harga
- Aplikasi memakai **harga katalog vendor asli** untuk semua 79 komponen (real seller, Aug 2026).
- Rentang pasar Okt 2026 dicatat sebagai pembanding di `RESEARCH.md` (bukan diaplikasi),
  selisih paling reduksi ~10–15% pada premium retail vs harga katalog.
- Mode "Optimasi sizing" mencari paket terhemat; mode referensi mengikuti situs asli persis.

## Uji fungsional (jsdom, Okt 21)
- Load, tab switch, pilih paket PRM + add-on → Rp190,4 jt (CV-PRM penuh, yaw delta wajar).
- Motorhome PRM + layout + PLTS: Rp529,7 jt; kompleksitas mentok cap 1,30 (perilaku referensi).
- Food truck default STD: Rp103,7 jt.
- Tabel harga: 79 baris, pencarian "baterai" → 3 baris PLTS_BATTERY.
- Kalkulator PLTS: 6×450 Wp + 7×300 Ah untuk 8.000 Wh/hari & 1.000 W; margin 15% + PPN 11%.
- Bug fix: (1) handler qty alat tidak menyimpan state; (2) fallback sizing baterai men-undersize
  (4×300Ah untuk kebutuhan 1.667Ah) → sekarang fallback qty unlimited seperti referensi.
- [ ] Final `PROGRESS.md`.
