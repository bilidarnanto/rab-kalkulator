# PROGRESS — Kalkulator RAB GitHub Pages (referensi: nasbpfsby.duckdns.org:8444)

**Status: live + riwayat, perbandingan, dark mode & bahasa EN/ID. Terakhir: 2026-10-21 ~15:55 WIB**

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

## Deployment
- Repo `bilidarnanto/rab-kalkulator` dibuat (token user, PAT), push 4 commit, GitHub Pages diaktifkan (branch main, root).
- URL: https://bilidarnanto.github.io/rab-kalkulator/
- Catatan: skrip putaran perbaikan riset menuliskan ulang 18 bukti HTML antrian (all captcha 73,9 KB)
  seluruh temuan harga sudah direkam teks di `RESEARCH.md §C/§B`; bukti panel/baterai/kulkas utuh.

## Iterasi 2 (timbal balik user, ~16:20 WIB)
- Tombol "Kirim estimasi ke Admin (WhatsApp)" — no. 6285334398681, isi pesan: tipe/paket/
  layout/material/add-on, speck PLTS, estimasi grand total; tinggal tekan kirim di WhatsApp.
- SEO untuk Google: meta robots/canonical/OG/Twitter, favicon SVG, JSON-LD WebApplication,
  robots.txt + sitemap.xml (di-produce oleh build.py), sitemap ping ke Google.
- Sitemap ping g:api.google.com? = status diproses; pengindeksan organik saat ini terjadi
  beberapa hari (GitHub Pages telah di-crawl robot Google karena domain tsb aktif).

## Iterasi 3 (Okt 2026 ~14:45)
- **Permalink konfigurasi**: tombol "🔗 Salin link konfigurasi" (RAB + PLTS tab) → URL `?cfg=<base64url S>`;
  load-terima via `decodeCfg` di boot (menimpa localStorage), tes jsdom restore ✓; pesan WA kini
  menyertakan link konfigurasi sehingga admin membuka & mengedit state yang sama persis.
- **Cek kelayakan sistem** (badge OK ✓ / PERIKSA ✗): produksi panel vs kebutuhan Wh/hari
  (Wp×sun×0.75), otonomi baterai (batWh×0.8/kebutuhan vs target ≥1 hari), inverter vs beban puncak
  (margin %), MPPT vs arus (Wp/V×1.25) — jalur negatif teruji (manual 30.000 Wh/9.000 W → 2 PERIKSA + warn).
- **Unduh CSV** RAB (semicolon + BOM utf-8, termasuk tenaga kerja/kompleksitas/diskon/kontingensi/PPN/grand).
- **SOW — Lingkup Pekerjaan & Kesepakatan** (sowHtml, dinamis sesuai konfigurasi): lingkup
  (desain/struktur/interior/kelistrikan/peralatan/PLTS sesuai item yang dipilih), jangka waktu estimasi
  (workDays atau 2–3 hari PLTS + lead-time 7–14 hari), komitmen bengkel (garansi pengerjaan 90 hari,
  progres+foto, handover bersih), hak & kewajiban konsumen, daftar di luar lingkup, catatan 30 hari.
  Humanis, tercetak di PDF (bagian .sow ikut print).
- Berat komponen (kg) ditampilkan di RAB & PLTS.
- File 57,4 KB; node --check ✓; smoke jsdom t4/t5/t7 lulus.

## Iterasi 4 (Okt 2026 ~15:10)
- **Riwayat penawaran** (localStorage `rab.hist`, maks 30): tombol "💾 Simpan ke Riwayat" di RAB & PLTS —
  snapshot S (merged base64 cfg) + label otomatis + grand total + Wp/kWh/inverter/MPPT + workDays +
  kompleksitas + berat kg. Panel "🗂️ Riwayat" di bawah RAB: Muat (restore state + re-render), salin link
  snapshot, hapus.
- **Perbandingan penawaran**: pilih 2–3 entri (⚖️) → tabel side-by-side; grand total termurah diberi
  kelas .win (hijau tebal). Catatan pedoman di bawah tabel.
- Teruji jsdom (t8): simpan 2 snapshot, banding, muat newest (foodtruck + manual 6000 restored), salin,
  hapus. File 63,5 KB — masih satu file.

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

## Iterasi 5 — Dark mode + Bahasa EN/ID (Okt 21, ~15:50 WIB)
- **Mode gelap**: tombol 🌙 di header; warna via `body.dark` (bg #0c1420, kartu #122031, input/nama tabel/catatan/warning/SOW/toast), disimpan `localStorage rab.dark`,
  default mengikuti `prefers-color-scheme`; cetak dipaksa terang (`@media print body.dark` reset).
- **Bahasa ID/EN**: tombol `EN`/`ID` di header; `?lang=en|id` URL param (boleh digabung `?cfg=`) → `localStorage rab.lang` → default `id`.
  - Renderer: helper `T('ID|EN')` inline di semua label dinamis (nav, kartu langkah, daftar kendaraan, RAB + penjabaran vendor, header grup STRUKTUR→Structure dst.,
    cek kelayakan, SOW penuh (scope/komitmen/hak-kewajiban/di-luar-lingkup/durasi), catatan optimasi, hasil PLTS, CSV, riwayat + perbandingan,
    toasts/alerts/prompt, pesan & greeting WhatsApp "Type: / Package: / Send the final pricing…").
  - HTML statis: `data-tr="ID|EN"` + loop boot; placeholder pencarian katalog diterjemahkan.
- **Uji jsdom (t9/t10/t11) 8/8 ✓**: nav/h2/grup/udi kendaraan/updateEst EN; badge kelayakan EN;
  SOW h4 EN penuh; riwayat EN tersimpan; WA EN `Type:` ✓; dark on/off ✓; 0 error jsdom.
  Sweep leftovers EN: hanya nama katalog Indonesia (sengaja — nama barang vendor).
- Catatan teknis: bug kuot ala `('|` diperbaiki global; helper T sendiri `indexOf('|')` dipulihkan manual.
- Ukuran: build.py 64,6 KB → index.html ~75 KB.

## Iterasi 6 — Nama katalog EN (Okt 21, ~16:10 WIB)
- 79 komponen katalog kini memakai `nameEn` asli dari API referensi (bukan terjemahan buatan) — DATA components kini membawa
  `nameEn`; 19 nama alat listrik diterjemahkan manual (`AP_EN`: LED lights, 12V refrigerator, Kitchen exhaust / blower, dst.).
- Helper `T('ID|EN')` + `tn(x)` (nama by `nameId` → `nameEn`, fallback passthrough) diterapkan di 11 titik render:
  select paket/layout/material, kartu add-on, daftar alat (apls), baris RAB konfigurator, baris RAB PLTS, tabel harga
  (+ filter pencarian juga mencari `nameEn`, jadi EN "fridge"/ID "kulkas" dua-duanya tembus), CSV, string SOW join,
  snapLabel paket, perbandingan penawaran, pesan/`nm()` WhatsApp.
- Uji jsdom (t12/t13) ✓: tabel harga EN, pencarian EN/ID, opsi paket EN, add-on EN, alat EN, baris RAB EN;
  regresi ID tidak berubah (masih "Paket Konversi Campervan Deluxe", dll.); t9 8/8 tetap hijau.
- Ukuran: build.py 64,8 KB → index.html ~78,7 KB.

## Iterasi 7 — Mobile view (request admin, Okt 21, ~16:35 WIB)
- **Blok `@media (max-width:640px)`**: header ringkas (subjudul disembunyikan di HP), padding kartu/teks lebih rapat,
  **input font 16px** (mencegah auto-zoom iOS), tombol hasil (`Send/CSV/Copy/History/Print`) **stack full-width**,
  chrome kendaraan min 140px, `.sticky` hasil jadi statis (tak memakan layar), toast max 92vw.
- **Tabel scroll horizontal** rapi via `.tw{overflow-x:auto}`: tabel RAB/PLTS/harga/kelayakan/perbandingan otomatis
  dibungkus `div.tw` saat boot (MutationObserver, idempotent — diuji: `tw count 2`, tanpa `tw .tw`, tanpa loop).
- Bonus: empty-state kalkulator PLTS ditranslasi EN (`data-tr`).
- Uji jsdom t14 ✓ (wrap tabel) + regresi t9 8/8 & t12 (nama EN) tetap hijau; `node --check` OK.
- Catatan: grid formulir sudah auto-fit (memecah jadi 1 kolom di <~460px) sejak awal — tidak perlu diubah.

## Iterasi 8 — Bugfix: total harian tidak berjalan meski qty>0 (Okt 22, ~10:00 WIB)
- **Akar masalah**: state versi lama menyimpan `S.appliances[code]` sebagai angka. Boot memakai fallback
  `S.appliances[code]||{qty:0,hours:a.hours}` → primitif angka terpakai; penulisan `o.qty=v` pada number **gagal diam-diam** —
  jadi meski user mengetik qty>0, total & beban puncak tetap 0. **Direproduksi jsdom** (skenario A t17: est tetap 0).
- **Perbaikan 3 lapis**: (1) normalizer boot — angka → `{qty, hours default}` & objek tak lengkap → lengkap;
  (2) handler input memaksa objek (`cur&&typeof cur==='object'`); (3) `energyOf` menerima angka-lama sebagai qty.
- **Tombol Reset** 🔄 di kartu 3 & kartu PLTS: mengosongkan alat + input manual Wh/W + sun 4.5 (jsdom t18: 2.160→0 ✓).
- Perilaku pamungkas yang bisa membingungkan juga ditangani: bila **total manual (Wh)** pernah diisi, angka alat tidak
  mengubah tampilan (override). Label sudah mengindikasikan; kini ada cara reset yang jelas.
- Guard kecil `toast()`: `requestAnimationFrame` di-fallback agar tidak pernah error.
- Uji: t17 ✓ (A/B/C), t18 ✓, t9 8/8 ✓; `node --check` OK.

## Iterasi 9 — Alur step-by-step + akuntabilitas data (request admin, Okt 22, ~11:15 WIB)
- **Stepper**: strip `#stepBar` di atas kartu — 3 langkah ber-status live (✓/●): "1. Tipe & paket" pilih paket/PLTS,
  "2. Kelengkapan (opsional)", "3. Kebutuhan listrik" update live saat pengguna mengisi; chip yang belum lengkap
  diberi label "isi duluan"; klik chip → scroll ke kartu. EN/ID penuh (T()).
- **Tombol "Lanjut ke langkah N →"** di ujung tiap kartu (1→2→3→hasil, scroll smooth) — urutan isian jelas.
- **Gate-checklist** saat RAB masih kosong: warn berisi ☐/✓ kriteria minimum (paket + beban > 0) + petunjuk pakai tombol lanjut.
- **Kotak "📋 Dasar & asumsi perhitungan"** (details, 7 butir) di atas hasil RAB: sumber harga katalog vendor Aug 2026
  + verifikasi pasar Okt 2026, formula kerja Rp75rb×8j, waste per kelompok, kompleksitas 0,80–1,30, diskon volume,
  kontingensi 3–10% (final oleh admin), PPN 11%, margin PLTS 15%, validitas 30 hari.
- **Tanggal harga per komponen** kini tampil: kolom "Tgl harga" di tab Tabel Harga (`priceUpdatedAt`, real 2026-08-18 dst.)
  + DATA membawa `updated`; tooltip `uph` di sel harga baris RAB via `_upd`.
- Catatan penggunaan alat: "W & jam default = estimasi standar bengkel; sesuaikan jam kebiasaan Anda".
- Uji jsdom t19 ✓ (chips live, gate ☐/✓, 7 butir asumsi, kolom tanggal, EN penuh); regresi t9/t18/t12 tetap hijau.
