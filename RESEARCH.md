# RESEARCH — Riset harga real untuk Kalkulator RAB (GitHub Pages)

Tanggal riset: **21 Okt 2026**. Metode: crawling pasif — situs referensi (vendor EcoPower ID), artikel daftar harga suryaqua.com (Mei–Jul 2026), marketplace (Tokopedia/Lazada/Shopee via snippet mesin pencari), toko panelsuryajakarta.com. Bukti mentah: `research/*.html`, `artifacts/*`.
> Semua angka dalam Rp. Lempeng [marketplace] = harga e-commerce; [premium] = brand tier-1; [vendor] = katalog EcoPower ID (survei harga kerja, Aug 2026).

## A. Mesin hitung situs referensi (dari chunk JS, bukan tebakan)

Ambil asal: `/tmp/.../js/3fjm0izpw6m7p.js` → modul `buildRab`, `buildPltsRab`, `calculatePlts`; dan siteConfig di `37ic64dze6wvb.js`:
`marginPct 15`, `ppnPct 11`, `includePpn true`, `plts{sunHours 4.5, derating 0.75, batteryDoD 0.8, batteryVoltage 12, inverterOversize 1.25, sccOversize 1.25, jasaPerWp 2000}`.

Urutan operasi (`buildAdvancedRabBreakdown`):
```
d = Σ subtotal garis                      (qty × harga)
waste_g = Σ price_subtotal × waste%g      (per kelompok, gas di bawah)
e = d + waste                             (subtotal + waste)
I  = d  (base material)
volumediscount = 3% jika d ≥ 100jt; else 2% jika d ≥ 50jt; else 1% jika d ≥ 25jt
labor = max(workDays dikatalog linier ini) × 8 jam × Rp75.000
S = (d + waste) × skorKompleksitas        (kompleksitas 0,8–1,3, basis 1)
X = S + labor − volumeDiscount
Kontingensi = pct(S) → 3–10% (basis 5%, +3 skor ≥1.2, +2 skor ≥1.1, −2 jika <1)
B (sebelum pajak) = X + Kontingensi
P = 11% × B  (saat includePpn)
Grand Total = B + P
```
Waste% per kelompok: `STRUKTUR .12, INTERIOR .08, PERALATAN .03, PLTS .02, LISTRIK .05, PLUMBING .05, JASA 0`.
Skor kompleksitas:
```
basis 1; motorhome +.15; foodtruck +.10; paket PRM +.10; DLX +.05;
add-on ≥5 +.10 / ≥3 +.05; PLTS +.08; layout kode 'LAY-3' +.10; clamp [0.8, 1.3]
```
Tenaga kerja dikalikan `workDays` dari spesifikasi paket: CV-STD 21, CV-DLX 28, CV-PRM 35; FT-STD 21, FT-DLX 28, FT-PRM 35; MH-STD 42, MH-DLX 56, MH-PRM 70.
RAB hanya PLTS (`buildPltsRab`): `total = (d + margin 15%)(1 + PPN 11%)`.
PLTS BOS default (`pltsLinesToRab`): kabel DC 6mm² = `3×qty panel + 2×qty baterai` meter; NYM 2,5mm² = 10 m; MC4 = `qty panel + 2` pasang; fuse set, DC breaker, AC breaker, busbar, grounding, mounting, JBox masing-masing 1.
Sizing PLTS:
```
required Wp   = ⌈Wh/hari ÷ (sun × 0.75)⌉
panel             = model Wp terbesar, qty = ⌈requiredWp / Wp unit⌉
Ah butuh          = ⌈Wh × 2hari ÷ (DoD 0.8 × 12V)⌉, bat = model Ah terbesar, qty = ⌈/Ah unit⌉
inverter          = pilih terkecil ≥ 1.25 × W beban puncak
SCC (A)           = pilih terkecil ≥ ⌈Wp total / 12V × 1.25⌉
```

## B. Harga pasar PLTS (terverifikasi 2026)

### Panel surya (per unit)
| Wp | Marketplace [grosir/ritel] | [Premium] toko | Katalog vendor | Kesimpulan nilai vendor |
|---|---|---|---|---|
| 100 poly lokal | Rp 400–700 rb (Tokopedia; suryaqua Mei-2026) | — | 950 rb | di atas marketplace mono lokal; ok premium band |
| 100 mono tier-1 | Rp 585–750 rb (Tokopedia; Solana Mei/Jul-2026) | Rp 750–1.100 rb (suryaqua; Canadian/JA/Trina) | 950 rb | tepat band premium |
| 200 mono | Rp 1.5 jt (Tokopedia Solana Jul-2026); Rp 1.2–2.8 jt band | — | 1.65 jt | sedikit di atas marketplace; wajar ritel |
| 450 | Rp 2.25–2.9 jt (Shopee/Tokopedia Aug-2026) | LONGi 450: ≈ Rp 2.7–3.5 jt (indeks suryaqua Mei-2026) | 2.3 jt | asimetris, vendor lebih murah |
| 550 | Rp 2.95 jt (Chint); Rp 3.43–4.0 jt (Solana Tokopedia Jul-2026); Rp 0.85–1.65 jt (claim termurah suryaqua Jul-2026, non-SNI) | — | 2.8 jt | di bawah premium SNI, OK |
→ Rp/Wp nominal: 100 = 9.5rb; 200 = 8.25rb; 450 = 5.1rb; 550 = 5.1rb.
**Optimasi**: 100/200 Wp hanya untuk rooftop sempit/mobil kecil; ≥450 Wp pakai 550/450 (hemat 35–55% per Wp). 1.65jt/2.8jt konsisten dengan suryaqua per-rumah 2.2 kWp (Rp 13–18 jt; 6×400W; egal catatan panel ~50–55% dari total biaya).

### Baterai LiFePO4 12V
| Ah | Katalog vendor Rp | Pasar |
|---|---|---|
| 100 | 2.5 jt | marketplace mentor Rp 2–3.5 jt (OEM China BMS); premium Pylontech/BYD Rp 7–10 jt [suryaqua Mei-2026] |
| 200 | 4.8 jt | Rp 2.4–3.0 jt/segmen (brand lokal/China); suryaqua: 200Ah/12V Rp 14–19 jt [premium Felicity/BYD] |
| 300 | 7.2 jt | segmen China: ~Rp 3.5–5.5 jt/300Ah 12V; premium ≥ Rp 15 jt |
Per Wh: vendor 1.95 rb; premium 5.5–7.8 rb. Katalog vendor = segmen OEM komersial, **jangan samakan dengan premium retail**; dipilih karena umum untuk retrofit kendaraan.
**Optimasi**: 200/300 Ah lebih efektif per kWh (Rp 1.875/Wh vs 1.953); hindari banyak unit kecil.

### Inverter pure sine (off-grid)
| W | Katalog Rp | Pasar (off-grid PSW) |
|---|---|---|
| 1000 | 1.5 jt | Rp 1.0–2.0 jt (Toko/China) |
| 1500 | 2.2 jt | Rp 1.6–2.6 jt |
| 2000 | 2.8 jt | Rp 2.0–3.5 jt |
| 3000 | 4.2 jt | Rp 3.0–5.0 jt |
| 5000 | 6.5 jt | Rp 4.5–7.5 jt |
Per W: 1.50 / 1.47 / 1.40 / 1.40 / 1.30 rb.
Konfirmasi: on-grid 1 kW Growatt Rp 2–3 jt; hybrid 3 kW Rp 8–13 jt [suryaqua Mei-2026] — vendor pakai off-grid PSW jauh lebih murah.
**Optimasi**: jaga beban puncak → 1 unit inverter besar murah per W; hindari over-size >2× kebutuhan; jangan over-drive > 80% kontinu.

### Solar Charge Controller (MPPT)
| A | Katalog Rp | Pasar MPPT [suryaqua Jun-2026] |
|---|---|---|
| 30 | 1.4 jt | 1.3–2.5 jt (Epever/Renogy) |
| 40 | 1.9 jt | 2.0–3.5 jt (Epever Tracer) |
| 60 | 2.9 jt | 3.0–5.5 jt (Victron SmartSolar) |
| 80 | 4.2 jt | ~Rp 4–6 jt (band antar kapasitas) |
| 100 | 5.5 jt | 6–10 jt (Victron/Outback) |
Per A: 46.7 / 47.5 / 48.3 / 52.5 / 55 ribu → vendor versi OEM non-Victron.
**Optimasi**: pilih melalui arus = ⌈(Wp total / 12V) × 1.25⌉; 2×30A sering lebih murah + redundan daripada 1×60A (2×1.4 = 2.8 jt vs 2.9 jt), tapi butuh panel 2 string.

### BOS (Balance of System)
Vendor: kabel DC 6mm 25 rb/m; NYM 2.5 12 rb/m; MC4 30 rb/pasang; Fuse set 150 rb; DC breaker 250 rb; AC breaker 180 rb; Busbar 350 rb; Grounding kit 400 rb; Mounting 1.2 jt; JBox 300 rb.
Verifikasi (suryaqua Mei-2026, 2200 Wp rumah): kabel DC + MC4 Rp 0.5–1 jt; MCB AC/DC Rp 0.5–1.2 jt; surge Rp 0.5–1 jt; conduit+box Rp 0.3–0.5 jt; **jasa instalasi Rp 3–5 jt** untuk 2.2 kWp (≈ Rp 1.4–2.3/Wp) → vendor jasa 2.000/Wp di dalam band.

## C. Perlengkapan & material — *riset berjalan*
(antrian Brave: berjalan di background; hasil akan diupdate di bagian ini saat fetch selesai)
- Prioritas: kulkas 12V, kompor, pompa+tangki, toilet, water heater 12V, solar vent, mesin kopi, deep fryer, griddle, hood, kulkas display, freezer 200 L, plywood 12 mm, ACM/Alucobond 3 mm, HPL, kabel NYA/NYM per meter, MC4, MCB, roof rack, awning, upah tukang per hari.

## D. Belum terverifikasi / ketidakpastian
- AC 12V 12000 BTU & Roof AC — produk niche, harga pasar sangat bervariasi.
- Toilet campervan wet-cell & Smart Home System — indicator harga premium, tidak ada referensi pasar stabil.
- Upah tukang — engine memakai Rp 75.000/jam (x8 jam), perlu cek upah harian harian (UMK Bangil/Pasuruan 2026) untuk konteks.
