#!/usr/bin/env python3
"""Generate index.html (GitHub Pages RAB calculator) dari artifacts/catalog.json.

Satu file HTML mandiri (vanilla JS, tanpa dependensi). Harga diambil dari katalog
vendor EcoPower ID (real, update 2026-08) — lihat RESEARCH.md untuk verifikasi
pasar & analisis optimasi. Jalankan ulang ``python3 build.py`` setelah katalog
diperbarui.
"""
import datetime, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CAT = json.loads((ROOT / "artifacts" / "catalog.json").read_text(encoding="utf-8"))["components"]

APPLIANCES = [
    ("APL-LAMP", "Lampu LED", 5, 5),
    ("APL-FAN", "Kipas Angin", 10, 6),
    ("APL-TV", "TV / Monitor", 30, 4),
    ("APL-FRIDGE", "Kulkas 12V", 45, 24),
    ("APL-PUMP", "Pompa Air", 40, 1),
    ("APL-LAPTOP", "Laptop", 65, 4),
    ("APL-PHONE", "HP / Gadget", 10, 3),
    ("APL-AC", "AC (½–¾ PK)", 500, 8),
    ("APL-RICECOOKER", "Rice Cooker", 400, 1),
    ("APL-MICROWAVE", "Microwave", 800, 0.5),
    ("APL-WATERHEATER", "Pemanas Air", 1200, 0.5),
    ("APL-FRYER", "Deep Fryer", 2000, 6),
    ("APL-GRILL", "Grill / Bakar", 1500, 6),
    ("APL-COFFEE", "Mesin Kopi", 800, 6),
    ("APL-REFRIGDISPLAY", "Kulkas Display", 200, 24),
    ("APL-BLENDER", "Blender", 350, 1),
    ("APL-TOASTER", "Toaster / Oven Kecil", 800, 2),
    ("APL-FREEZER", "Freezer", 150, 24),
    ("APL-EXHAUST", "Exhaust / Blower Dapur", 200, 6),
]

AP_EN = {
    "APL-LAMP": "LED lights", "APL-FAN": "Fan", "APL-TV": "TV / monitor",
    "APL-FRIDGE": "12V refrigerator", "APL-PUMP": "Water pump", "APL-LAPTOP": "Laptop",
    "APL-PHONE": "Phone / gadget", "APL-AC": "Air conditioner (½–¾ PK)",
    "APL-RICECOOKER": "Rice cooker", "APL-MICROWAVE": "Microwave",
    "APL-WATERHEATER": "Water heater", "APL-FRYER": "Deep fryer",
    "APL-GRILL": "Grill / barbecue", "APL-COFFEE": "Coffee machine",
    "APL-REFRIGDISPLAY": "Display refrigerator", "APL-BLENDER": "Blender",
    "APL-TOASTER": "Toaster / small oven", "APL-FREEZER": "Freezer",
    "APL-EXHAUST": "Kitchen exhaust / blower",
}

DATA = {
    "components": [
        {
            "code": c["code"], "name": c["nameId"], "nameEn": c.get("nameEn") or "", "category": c["category"],
            "unit": c["unit"], "price": c["price"], "specs": c.get("specs") or {},
        }
        for c in CAT
    ],
    "appliances": [{"code": a, "name": n, "nameEn": AP_EN.get(a, n), "watts": w, "hours": h} for (a, n, w, h) in APPLIANCES],
    "cfg": {
        "marginPct": 15, "ppnPct": 11, "includePpn": True,
        "laborRate": 75000, "hoursPerDay": 8,
        "batteryAutonomyDays": 2,
        "plts": {"sunHours": 4.5, "derating": 0.75, "batteryDoD": 0.8, "batteryVoltage": 12,
                 "inverterOversize": 1.25, "sccOversize": 1.25, "jasaPerWp": 2000, "maxBatteryUnits": 4},
    },
}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kalkulator RAB — Campervan · Motorhome · Food Truck · PLTS</title>
<meta name="description" content="Hitung RAB konversi campervan, motorhome, food truck dan instalasi PLTS secara online. Harga real katalog vendor (Aug 2026), rincian per komponen, hasil bisa dikirim ke admin WhatsApp.">
<meta name="robots" content="index,follow">
<meta name="author" content="EcoPower ID">
<meta name="theme-color" content="#275b31">
<meta property="og:type" content="website">
<meta property="og:title" content="Kalkulator RAB — Campervan · Motorhome · Food Truck · PLTS">
<meta property="og:description" content="Konfigurasi online, angka real per komponen, estimasi RAB otomatis + kirim ke admin via WhatsApp.">
<meta property="og:url" content="https://bilidarnanto.github.io/rab-kalkulator/">
<meta property="og:site_name" content="Kalkulator RAB">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="https://bilidarnanto.github.io/rab-kalkulator/">
<meta name="google-site-verification" content="qOh3prb1Smavfyra9wRaYZVwQyn4cc-QYFbsiTVeUkE">
<meta property="og:image" content="https://bilidarnanto.github.io/rab-kalkulator/logo.jpg">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="1024">
<meta property="og:image:alt" content="EcoPower ID — bengkel konversi campervan & instalasi PLTS">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://bilidarnanto.github.io/rab-kalkulator/logo.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E⚡%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Kalkulator RAB — EcoPower ID","url":"https://bilidarnanto.github.io/rab-kalkulator/","applicationCategory":"BusinessApplication","operatingSystem":"Any","inLanguage":"id","description":"Kalkulator RAB konversi campervan, motorhome, food truck dan instalasi PLTS","image":"https://bilidarnanto.github.io/rab-kalkulator/logo.jpg","offers":{"@type":"Offer","price":"0","priceCurrency":"IDR"}}
</script>
<style>
:root{--bch:#275b31;--acc:#2f7d3f;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#1e293b;background:var(--bg)}
header{background:var(--bch);color:#fff;padding:14px 18px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:17px;margin:0;font-weight:700}
header small{opacity:.85;font-size:12px}
main{max-width:1080px;margin:0 auto;padding:18px 14px 70px}
nav{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}
nav button{border:1px solid var(--line);background:#fff;border-radius:9px;padding:9px 14px;font-size:14px;cursor:pointer}
nav button.on{background:var(--acc);border-color:var(--acc);color:#fff}
section.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:14px}
h2{font-size:16px;margin:0 0 10px}h3{font-size:14px;margin:14px 0 8px}
label{font-size:13px;color:var(--mut);display:block;margin:10px 0 4px}
select,input[type=number],input[type=text]{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font-size:14px;background:#fff}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f1f5f9;font-weight:600}
td.r,th.r{text-align:right;white-space:nowrap}
.btn{background:var(--acc);color:#fff;border:0;border-radius:9px;padding:10px 16px;font-size:14px;cursor:pointer}
.btn.ghost{background:#fff;color:#1e293b;border:1px solid var(--line)}
.mut{color:var(--mut);font-size:12.5px}
.tot{display:flex;justify-content:space-between;gap:8px;padding:3px 0;font-size:14px;font-weight:400}
.tot b{white-space:nowrap;font-weight:700}
.grand{border-top:2px solid #1e293b;margin-top:6px;padding-top:8px;font-size:16px}
.tag{display:inline-block;background:#eef7ef;color:var(--bch);border-radius:6px;padding:2px 8px;font-size:12px}
.chk{display:flex;align-items:flex-start;gap:8px;padding:7px 0;border-bottom:1px dashed var(--line)}
input[type=checkbox]{width:16px;height:16px;flex:none;margin-top:4px}
.opt{display:flex;gap:3px;border:1px solid var(--line);border-radius:9px;padding:3px;flex-wrap:wrap}
.opt label{flex:1 1 120px;margin:0;padding:8px 10px;border-radius:7px;font-size:13.5px;color:#1e293b;cursor:pointer;position:relative}
.opt input{position:absolute;opacity:0}
.opt label:has(input:checked){background:var(--bch);color:#fff}
.apl{display:flex;gap:6px;align-items:center;padding:5px 0;border-bottom:1px dashed var(--line)}
.apl .nm{flex:1 1 140px;font-size:13.5px}
.apl .w{width:64px;text-align:right;font-size:12.5px;color:var(--mut)}
.apl input{width:60px;padding:4px 6px}
.warn{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:8px;padding:8px 12px;font-size:13px;margin:8px 0}
.note{background:#f0fdf4;border:1px solid #bbf7d0;color:#166534;border-radius:8px;padding:8px 12px;font-size:13px;margin:8px 0}
.sticky{position:sticky;top:10px}
.badge{display:inline-block;border-radius:6px;padding:1px 8px;font-size:12.5px;font-weight:600}
.badge.ok{background:#dcfce7;color:#166534}
.badge.warn{background:#fef3c7;color:#92400e}
.badge.bad{background:#fee2e2;color:#991b1b}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#1e293b;color:#fff;border-radius:10px;padding:10px 18px;font-size:14px;opacity:0;pointer-events:none;transition:opacity .25s;z-index:60}
.toast.show{opacity:.95}
.viab{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 2px}
.viab th,.viab td{padding:6px 8px;border-bottom:1px solid var(--line)}
.viab th{font-size:11.5px;text-transform:uppercase;letter-spacing:.3px;color:var(--mut)}
.sow{background:#f8fafc;border:1px solid var(--line);border-radius:10px;padding:10px 14px;font-size:13.5px;margin:10px 0}
.sow h4{margin:10px 0 3px;font-size:13.5px;color:#334155}
.sow ul{margin:2px 0 4px 18px;padding:0}
.sow li{margin:3px 0;line-height:1.45}
.sow .grow{display:grid;grid-template-columns:1.15fr 1fr;gap:0 20px}
.sow .luar{border-top:1px dashed var(--line);margin-top:8px;padding-top:2px}
@media print{.grow{grid-template-columns:1fr 1fr}}
.hist{display:flex;gap:8px;align-items:center;padding:7px 0;border-bottom:1px dashed var(--line);flex-wrap:wrap}
.hist:last-child{border-bottom:0}
.hist .nm{flex:1 1 230px;min-width:0}
.hist .btn.mini{padding:3px 9px;font-size:12.5px}
.mini{font-size:12px}
.cmp{width:100%;border-collapse:collapse;font-size:13.5px;margin:4px 0 10px}
.cmp th,.cmp td{padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
.cmp .win{color:#166534;font-weight:800}
.lang{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:8px;font-size:12.5px;padding:6px 10px;cursor:pointer}
body.dark{background:#0c1420;color:#dbe6f1}
body.dark .card{background:#122031;border-color:#243449}
body.dark nav button{background:#122031;border-color:#243449;color:#dbe6f1}
body.dark nav button.on{background:var(--acc);border-color:var(--acc);color:#fff}
body.dark select,body.dark input[type=number],body.dark input[type=text]{background:#0d1826;color:#dbe6f1;border-color:#243449}
body.dark .btn.ghost{background:#122031;color:#dbe6f1;border-color:#243449}
body.dark .opt{border-color:#243449}
body.dark .opt label{color:#dbe6f1}
body.dark .tag{background:#15331f;color:#8fdca3}
body.dark th{background:#152635;color:#aebfd2}
body.dark .gw{background:#152635;color:#dbe6f1}
body.dark .note{background:#0f2418;border-color:#22503a;color:#9fe0ae}
body.dark .warn{background:#271a0d;border-color:#5c4015;color:#f0c07f}
body.dark .sow{background:#0f1a29;border-color:#243449;color:#dbe6f1}
body.dark .sow h4{color:#b9cadb}
body.dark .grand{border-top-color:#dbe6f1}
body.dark .toast{outline:1px solid #334155}
@media print{body.dark{background:#fff!important;color:#1e293b}
body.dark .card,body.dark th,body.dark .gw{background:#fff!important;color:#1e293b!important}}
.only-print{display:none}
@media print{header,nav,.no-print{display:none!important}body{background:#fff}
.only-print{display:flex!important}
section.card{border:0;padding:0;margin:0 0 12px}.sticky{position:static}
body[data-tab="conf"] #tab-apl,body[data-tab="conf"] #tab-cat{display:none!important}
body[data-tab="apl"] #tab-conf,body[data-tab="apl"] .pst{display:none!important}
body[data-tab="cat"] #tab-conf,body[data-tab="cat"] #tab-apl{display:none!important}
.pst{display:none!important}
}
</style>
</head>
<body data-tab="conf">
<header>
  <img src="logo.jpg" alt="logo EcoPower ID" style="height:34px;width:34px;object-fit:cover;border-radius:9px;flex:none">
  <h1>Kalkulator RAB <span style="font-weight:400;opacity:.8;font-size:13px">· EcoPower ID</span></h1>
  <small data-tr="Campervan · Motorhome · Food Truck · PLTS — harga real katalog vendor (Aug 2026), verifikasi pasar Okt 2026|Campervan · Motorhome · Food Truck · Solar — real vendor catalog prices (Aug 2026), market-checked Oct 2026">Campervan · Motorhome · Food Truck · PLTS — harga real katalog vendor (Aug 2026), verifikasi pasar Okt 2026</small>
  <div style="margin-left:auto;display:flex;gap:6px;flex:none">
    <button id="langBtn" title="Ganti bahasa / switch language">EN</button>
    <button id="darkBtn" title="Mode gelap / dark mode">🌙</button>
  </div>
</header>
<main>
<div id="kop" class="only-print" style="display:flex;gap:10px;align-items:center;margin-bottom:14px">
  <img src="logo.jpg" alt="EcoPower ID" style="height:64px;width:64px;object-fit:cover;border-radius:12px">
  <div>
    <div style="font-weight:800;font-size:17px">EcoPower ID</div>
    <div style="font-size:12.5px">Bengkel Konversi Campervan, Motorhome, Food Truck & Instalasi PLTS</div>
    <div style="font-size:12px;color:#475569">Perum Permata Indah A9 No.10, Bangil, Pasuruan · WA +62 853-3439-8681 · projectigniter@gmail.com</div>
  </div>
</div>
<nav class="no-print">
  <button data-tab="conf" class="on" data-tr="Konfigurator RAB|RAB Configurator">Konfigurator RAB</button>
  <button data-tab="apl" data-tr="Kalkulator PLTS|Solar Calculator">Kalkulator PLTS</button>
  <button data-tab="cat" data-tr="Tabel Harga|Price List">Tabel Harga</button>
</nav>

<div id="tab-conf">
  <div class="grid">
    <section class="card pst">
      <h2 data-tr="1 · Tipe & paket|1 · Type & package">1 · Tipe & paket</h2>
      <div class="opt" id="vehList"></div>
      <label data-tr="Paket konversi|Conversion package">Paket konversi</label><select id="pkg"></select>
      <label data-tr="Layout interior|Interior layout">Layout interior</label><select id="lay"></select>
      <label data-tr="Material finishing|Finish material">Material finishing</label><select id="mat"></select>
      <div class="chk" style="margin-top:10px"><input type="checkbox" id="incPlts">
        <div><b data-tr="Sistem PLTS (listrik mandiri)|Solar system (independent power)">Sistem PLTS (listrik mandiri)</b>
        <div class="mut" data-tr="Panel solar + baterai LiFePO4 + inverter + MPPT + proteksi + jasa.|Solar panels + LiFePO4 battery + inverter + MPPT + protection + install service.">Panel solar + baterai LiFePO4 + inverter + MPPT + proteksi + jasa.</div></div></div>
      <div class="chk"><input type="checkbox" id="optSizing">
        <div><b data-tr="Optimasi sizing komponen PLTS|Optimize solar component sizing">Optimasi sizing komponen PLTS</b>
        <div class="mut" data-tr="Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.|Find the cheapest unit mix (lowest Rp/Wh & Rp/Wp) that meets the demand.">Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.</div></div></div>
    </section>
    <section class="card pst">
      <h2 data-tr="2 · Kelengkapan (add-on)|2 · Extras (add-ons)">2 · Kelengkapan (add-on)</h2>
      <div id="addons"></div>
    </section>
    <section class="card pst">
      <h2 data-tr="3 · Kebutuhan listrik harian|3 · Daily power needs">3 · Kebutuhan listrik harian</h2>
      <div id="apls"></div>
      <div class="grid" style="margin-top:10px">
        <div><label data-tr="Total harian manual (Wh)|Manual daily total (Wh)">Total harian manual (Wh)</label><input id="mWh" type="number" min="0" placeholder="otomatis"></div>
        <div><label data-tr="Beban puncak manual (W)|Manual peak load (W)">Beban puncak manual (W)</label><input id="mPeak" type="number" min="0" placeholder="otomatis"></div>
        <div><label data-tr="Peak sun hour harian (1–7)|Daily peak sun hours (1–7)">Peak sun hour harian (1–7)</label><input id="sun" type="number" step="0.1" min="1" max="7" value="4.5"></div>
      </div>
      <div class="note" id="espEst"></div>
    </section>
  </div>
  <section class="card sticky" id="rabOut"></section>
  <section class="card no-print" id="histBox"></section>
</div>

<div id="tab-apl" hidden>
  <section class="card pst">
    <h2 data-tr="Kalkulator PLTS (sistem mandiri)|Solar calculator (standalone)">Kalkulator PLTS (sistem mandiri)</h2>
    <div id="apls2"></div>
    <div class="grid" style="margin-top:10px">
      <div><label data-tr="Total harian manual (Wh)|Manual daily total (Wh)">Total harian manual (Wh)</label><input id="mWh2" type="number" min="0" placeholder="otomatis"></div>
      <div><label data-tr="Beban puncak manual (W)|Manual peak load (W)">Beban puncak manual (W)</label><input id="mPeak2" type="number" min="0" placeholder="otomatis"></div>
      <div><label data-tr="Peak sun hour harian (1–7)|Daily peak sun hours (1–7)">Peak sun hour harian (1–7)</label><input id="sun2" type="number" step="0.1" min="1" max="7" value="4.5"></div>
    </div>
    <button class="btn" id="btnPlts" style="margin-top:12px" data-tr="Hitung & susun RAB PLTS|Calculate & build solar RAB">Hitung & susun RAB PLTS</button>
  </section>
  <section class="card" id="pltsOut"><div class="mut">Isi jumlah unit & jam pemakaian, lalu tekan hitung.</div></section>
</div>

<div id="tab-cat" hidden>
  <section class="card">
    <h2 data-tr="Harga komponen — katalog vendor (real, Aug 2026)|Component prices — vendor catalog (real, Aug 2026)">Harga komponen — katalog vendor (real, Aug 2026)</h2>
    <input id="catQ" type="text" placeholder="Cari nama / kode…">
    <div id="catFilter" style="margin:10px 0"></div>
    <table><thead><tr><th style="width:112px" data-tr="Kode|Code">Kode</th><th class="r" data-tr="Harga satuan|Unit price">Harga satuan</th><th style="width:66px" data-tr="Satuan|Unit">Satuan</th><th data-tr="Nama|Name">Nama</th><th style="width:96px" data-tr="Kategori|Category">Kategori</th></tr></thead><tbody id="catBody"></tbody></table>
    <p class="mut" data-tr="Sumber: API /api/catalog situs referensi (Aug 2026) · banding riset & optimasi: RESEARCH.md.|Source: /api/catalog API of the reference site (Aug 2026) · price research & optimization: see RESEARCH.md.">Sumber: API <code>/api/catalog</code> situs referensi (Aug 2026) · banding riset & optimasi: <code>RESEARCH.md</code>.</p>
  </section>
</div>
</main>
<script>
const DATA = __DATA__;
const C = DATA.components, CFG = DATA.cfg, PLTS = CFG.plts;
const A_MAP = Object.fromEntries(C.map(c=>[c.code,c]));
const catBy = cat => C.filter(c=>c.category===cat);
const fmt = n => 'Rp' + Math.round(n).toLocaleString('id-ID');
const num = (o,k)=>{const v=o?.[k];return 'number'===typeof v?v:Number(v??0)||0;};
const spec = c => c?.specs ?? {};

/* ===== mesin hitung — port 1:1 dari chunk referensi ===== */
const WASTE = {STRUKTUR:.12,INTERIOR:.08,PERALATAN:.03,PLTS:.02,LISTRIK:.05,PLUMBING:.05,JASA:0};
const GRP = {STRUKTUR:'STRUKTUR',INTERIOR:'INTERIOR',PERALATAN:'PERALATAN',PLTS_PANEL:'PLTS',PLTS_BATTERY:'PLTS',
  PLTS_INVERTER:'PLTS',PLTS_SCC:'PLTS',PLTS_BOS:'PLTS',LISTRIK:'LISTRIK',PLUMBING:'PLUMBING',JASA:'JASA'};

function energyOf(s){
  let wh=0, W=0;
  for(const a of DATA.appliances){
    const st=s.appliances?.[a.code]||null;
    const q=st?Math.max(0,st.qty||0):0, h=st&&st.hours>0?st.hours:a.hours;
    if(q>0&&h>0){ wh+=a.watts*h*q; W+=a.watts*q; }
  }
  const dailyWh = s.manualDailyWh>0?Math.round(s.manualDailyWh):Math.round(wh);
  const peakW   = s.manualPeakW>0 ?Math.round(s.manualPeakW) :Math.round(W);
  return {dailyWh,peakW};
}

/* pemilih komponen: mode referensi (unit terbesar/terkecil cukup) vs optimasi hemat */
function packPick(cat, need, key){      // optimasi: minimum biaya, qty ≤ batas
  const cap = cat==='PLTS_BATTERY'?PLTS.maxBatteryUnits:6;
  let best=null;
  for(const c of catBy(cat)){
    const u=num(c.specs,key); if(u<=0)continue;
    const q=Math.ceil(need/u); if(q>cap)continue;
    const cost=c.price*q;
    if(!best||cost<best.cost||(cost===best.cost&&q<best.qty))best={comp:c,qty:q,cost};
  }
  if(!best){ // fallback: unit terbesar, qty tanpa batas (perilaku referensi)
    const l=catBy(cat).filter(c=>num(c.specs,key)>0).sort((a,b)=>num(b.specs,key)-num(a.specs,key));
    const u=num(l[0].specs,key);
    best={comp:l[0],qty:Math.max(1,Math.ceil(need/u))};
  }
  return best;
}
function refPanel(need){               // referensi: unit Wp terbesar
  const l=catBy('PLTS_PANEL').filter(c=>num(c.specs,'wp')>0).sort((a,b)=>num(b.specs,'wp')-num(a.specs,'wp'));
  return {comp:l[0],qty:Math.max(1,Math.ceil(need/num(l[0].specs,'wp')))};
}
function smallPickDesc(cat,key){return catBy(cat).filter(c=>num(c.specs,key)>0).sort((a,b)=>num(b.specs,key)-num(a.specs,key))[0];}
function downPick(cat,need,key){
  const l=catBy(cat).filter(c=>num(c.specs,key)>0).sort((a,b)=>num(a.specs,key)-num(b.specs,key));
  return l.find(c=>num(c.specs,key)>=need)??l[l.length-1];
}

function calculatePlts(inp, optim){
  const sun=inp.sunHours>0?inp.sunHours:PLTS.sunHours, V=PLTS.batteryVoltage;
  const dailyWh=Math.max(1,Math.round(inp.dailyWh||0)), peakW=Math.max(1,Math.round(inp.peakW||0));
  const reqWp=Math.ceil(dailyWh/(sun*PLTS.derating));
  const panel=optim?packPick('PLTS_PANEL',reqWp,'wp'):refPanel(reqWp);
  const wp=num(spec(panel.comp),'wp'), pQty=panel.qty, pWp=pQty*wp;
  const batNeed=Math.ceil(dailyWh*CFG.batteryAutonomyDays/(PLTS.batteryDoD*V));
  const bat=optim?packPick('PLTS_BATTERY',batNeed,'ah')
               :(()=>{const b=smallPickDesc('PLTS_BATTERY','ah');return {comp:b,qty:Math.max(1,Math.ceil(batNeed/num(spec(b),'ah')))};})();
  const inverter=downPick('PLTS_INVERTER',Math.ceil(peakW*PLTS.inverterOversize),'watts');
  const scc=downPick('PLTS_SCC',Math.ceil(pWp/V*PLTS.sccOversize),'amps');
  const lines=[];
  const add=(c,stxt,unit,qty)=>{if(!c||!qty)return; lines.push({...c,spec:stxt,unit:unit||c.unit,qty,subtotal:Math.round(qty*c.price),weightKg:num(c.specs,'weightKg')||undefined});};
  add(panel.comp,wp+' Wp; '+fmt(panel.comp.price)+'/unit',null,pQty);
  add(bat.comp,num(spec(bat.comp),'ah')+' Ah / '+V+' V',null,bat.qty);
  add(inverter,num(spec(inverter),'watts')+' W pure sine',null,1);
  add(scc,'MPPT '+num(spec(scc),'amps')+' A',null,1);
  add(A_MAP['PLTS-BOS-DC'],'kabel DC 6 mm² — 3/baris panel + 2/unit baterai',null,3*pQty+2*bat.qty);
  add(A_MAP['PLTS-BOS-AC'],'NYM 2,5 mm² panel instalasi AC',null,10);
  add(A_MAP['PLTS-BOS-MC4'],'konektor',null,pQty+2);
  for(const k of ['PLTS-BOS-FUSE','PLTS-BOS-DCBRK','PLTS-BOS-ACBRK','PLTS-BOS-BUSBAR','PLTS-BOS-GND','PLTS-BOS-MOUNT','PLTS-BOS-JBOX']){
    const c=A_MAP[k]; if(c) lines.push({...c,spec:'',qty:1,subtotal:Math.round(c.price)});
  }
  add(A_MAP['PLTS-JASA-INSTALL'],pWp+' Wp × '+fmt(PLTS.jasaPerWp)+'/Wp',null,pWp);
  const bAh=num(spec(bat.comp),'ah'), batWh=bat.qty*bAh*V;
  return {dailyWh,peakW,reqWp,pQty,pWp,bQty:bat.qty,bAh,batWh,panel,bat,inverter,scc,sun,lines};
}

function complexityOf(s){
  let n=1, why=[];
  const p=s.packageCode||'', lay=s.layoutCode||'', x=s.addonCodes||[];
  if(s.vehicleType==='motorhome'){n+=.15;why.push('motorhome lebih kompleks');}
  if(s.vehicleType==='foodtruck'){n+=.10;why.push('food truck instalasi khusus');}
  if(p.includes('PRM')){n+=.10;why.push('paket premium');}else if(p.includes('DLX')){n+=.05;why.push('paket deluxe');}
  if(x.length>=5){n+=.10;why.push(x.length+' add-on (banyak)');}else if(x.length>=3){n+=.05;why.push(x.length+' add-on');}
  if(s.includePlts){n+=.08;why.push('instalasi PLTS');}
  if(lay.includes('LAY-3')){n+=.10;why.push('layout custom');}
  n=Math.min(1.3,Math.max(.8,n));
  const label=n>=1.2?'Sangat kompleks':n>=1.1?'Kompleks':n>=1?'Standar':'Sederhana';
  return {score:n,label,why};
}

function buildRabLines(s){
  const lines=[]; let i=0;
  const push=(code,group,q=1)=>{const c=A_MAP[code];if(!c)return;i++;lines.push({...c,group,qty:q,subtotal:Math.round(q*c.price)});};
  if(s.vehicleType!=='plts'){
    if(s.packageCode)push(s.packageCode,'STRUKTUR');
    if(s.layoutCode)push(s.layoutCode,'INTERIOR');
    if(s.materialCode)push(s.materialCode,'INTERIOR');
    for(const a of s.addonCodes)push(a,GRP[A_MAP[a]?.category]??'PERALATAN');
  }
  const e=energyOf(s); let plts=null;
  if((s.includePlts&&s.vehicleType!=='plts')||s.vehicleType==='plts'){
    if(e.dailyWh>0&&e.peakW>0){
      plts=calculatePlts({dailyWh:e.dailyWh,peakW:e.peakW,sunHours:s.sunIncome},!!s.optSizing);
      for(const L of plts.lines)lines.push({...L,group:'PLTS'});
    }
  }
  return {lines,plts};
}

function simpleTotals(lines){
  const d=lines.reduce((a,L)=>a+L.subtotal,0), m=Math.round(CFG.marginPct/100*d),
    ppnP=CFG.includePpn?CFG.ppnPct:0, ppn=Math.round(ppnP/100*(d+m)),
    kg=lines.reduce((a,L)=>a+(L.weightKg??0)*L.qty,0);
  return {subtotal:d,margin:m,ppnPct:ppnP,ppn,total:d+m+ppn,marginPct:CFG.marginPct,weightKg:kg};
}

function advancedBreakdown(s,lines){
  const d=lines.reduce((a,L)=>a+L.subtotal,0);
  const wmap={};
  for(const L of lines){const pct=WASTE[L.group]??.05;wmap[L.group]=(wmap[L.group]??0)+Math.round(L.subtotal*pct);}
  const wasteTotal=Object.values(wmap).reduce((a,b)=>a+b,0);
  const waste={per:Object.fromEntries(Object.entries(wmap).map(([k,v])=>[k,{pct:WASTE[k]||0,val:v}])),total:wasteTotal,
    avg:d>0?Math.round(wasteTotal/d*1000)/10:0};
  const cx=complexityOf(s);
  const workDays=Math.max(0,...lines.map(L=>('number'===typeof L.specs?.workDays)?L.specs.workDays:0));
  const hours=CFG.hoursPerDay*workDays, labor=hours*CFG.laborRate;
  const volPct=d>=1e8?3:d>=5e7?2:d>=25e6?1:0, vol={pct:volPct,amount:Math.round(volPct/100*d)};
  const Sbase=Math.round((d+wasteTotal)*cx.score), X=Sbase+labor-vol.amount;
  let ctp=5,why=[];
  if(cx.score>=1.2){ctp+=3;why.push('kompleksitas tinggi');}else if(cx.score>=1.1){ctp+=2;why.push('kompleksitas sedang');}
  else if(cx.score<1){ctp-=2;why.push('proyek sederhana');}
  ctp=Math.max(3,Math.min(10,ctp));
  const cont={pct:ctp,amount:Math.round(ctp/100*Sbase),reason:why.join(', ')||'standar industri'};
  const beforeTax=X+cont.amount, ppnP=CFG.includePpn?CFG.ppnPct:0, ppn=Math.round(ppnP/100*beforeTax);
  return {material:d,waste,cx,workDays,hours,labor,vol,cont,beforeTax,ppnPct:ppnP,ppn,grand:beforeTax+ppn};
}

/* ===== catatan optimasi komponen ===== */
function optimNotes(plts){
  const n=[];
  if(!plts)return n;
  const rpWp=plts.panel?plts.panel.comp.price/Math.max(1,num(spec(plts.panel.comp),'wp')):0;
  const rpWh=plts.bat?plts.bat.comp.price/(num(spec(plts.bat.comp),'ah')*PLTS.batteryVoltage):0;
  const rpW=plts.inverter?plts.inverter.price/Math.max(1,num(spec(plts.inverter),'watts')):0;
  const rpA=plts.scc?plts.scc.price/Math.max(1,num(spec(plts.scc),'amps')):0;
  n.push(T('Indikator Rp/Wp panel: |Panel price check: ')+fmt(rpWp)+T(' — unit 450–550 Wp ~Rp5.100/Wp, unit 100 Wp Rp9.500/Wp (2× lipat).| — 450–550 Wp panels run ~Rp5,100/Wp vs 100 Wp at Rp9,500/Wp (2× the price).'));
  n.push(T('Indikator Rp/Wh baterai: |Battery price check: ')+fmt(rpWh)+T(' — unit 200–300 Ah paling hemat per kWh.| — 200–300 Ah units give the best value per kWh.'));
  n.push(T('Indikator Rp/W inverter: |Inverter price check: ')+fmt(rpW)+T(' — jaga beban puncak agar tidak terloncat ke kelas yang lebih besar.| — keep the peak load below the tier threshold so you stay in this class.'));
  n.push(T('Indikator Rp/A MPPT: |MPPT price check: ')+fmt(rpA)+T(' — bila panel dibagi 2 string, 2×30 A sering lebih murah daripada 1×60 A.| — if the panels split into 2 strings, 2×30 A is often cheaper than 1×60 A.'));
  if(plts.panel.comp!==smallPickDesc('PLTS_PANEL','wp'))
    n.push(T('Sizing hemat aktif: |Cost-optimized sizing: ')+plts.pQty+'× '+num(spec(plts.panel.comp),'wp')+' Wp ('+fmt(plts.panel.comp.price)+T('/unit) — lihat catatan Rp/Wp di atas.|/unit) — see the Rp/Wp check above.'));
  if(plts.bQty>=4)
    n.push(T('Baterai |Battery ')+plts.bQty+T(' unit (| unit (')+((plts.batWh/1000).toFixed(1))+T(' kWh) — untuk aplikasi kendaraan pertimbangkan tegangan sistem lebih tinggi (24/48 V) atau kurangi konsumsi listrik malam hari.| kWh) — for vehicles consider a higher system voltage (24/48 V) or cut night-time loads.'));
  if(plts.inverter&&num(spec(plts.inverter),'watts')>2.2*plts.peakW)
    n.push(T('Inverter melebihi 2× beban puncak — elemen beban bisa dilakukan bertahap (stagger) agar inverter lebih kecil.|The inverter exceeds 2× the peak load — staggering loads in stages lets you use a smaller inverter.'));
  if(plts.scc&&num(spec(plts.scc),'amps')<=30)
    n.push(T('MPPT 30 A cukup — nilai arus: |MPPT 30 A is enough — computed current: ')+plts.scc.code.replace('PLTS-SCC-','')+' A.');
  return n;
}

/* ===== UI ===== */
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));

let S={vehicleType:'campervan',packageCode:'CV-PKG-STD',layoutCode:'',materialCode:'',addonCodes:[],
  includePlts:false,optSizing:true,appliances:{},manualDailyWh:null,manualPeakW:null,sunIncome:4.5};
try{Object.assign(S,JSON.parse(localStorage.getItem('rab.state')||'{}'));}catch(e){}
try{const mc=location.search.match(/[?&]cfg=([^&]+)/);if(mc){const cf=decodeCfg(mc[1]);if(cf)Object.assign(S,cf);}}catch(e){}
const save=()=>{try{localStorage.setItem('rab.state',JSON.stringify(S));}catch(e){}};

const VEH=[{id:'campervan',nm:'🚐 Campervan',d:'van konversi 1–4 orang|1–4 seater van conversion'},
  {id:'motorhome',nm:'🚌 Motorhome',d:'rumah berjalan 4–8 orang|rolling home for 4–8 people'},
  {id:'foodtruck',nm:'🍔 Food Truck',d:'dapur di atas roda|kitchen on wheels'},
  {id:'plts',nm:'☀️ PLTS (rumah/lainnya)|☀️ Solar system (home/other)',d:'tanpa paket kendaraan|no vehicle package'}];
const suf=v=>({campervan:'CV',motorhome:'MH',foodtruck:'FT'}[v]||'');

function renderVeh(){
  const L=$('#vehList'); L.innerHTML='';
  for(const v of VEH){
    const lab=document.createElement('label');
    lab.innerHTML='<input type="radio" name="veh" value="'+v.id+'" '+(S.vehicleType===v.id?'checked':'')+'> '+T(v.nm);
    lab.title=T(v.d);
    lab.onclick=()=>{
      S.vehicleType=v.id;
      S.addonCodes=[];S.layoutCode='';S.materialCode='';
      if(v.id==='plts'){S.packageCode='';S.includePlts=false;}
      else{const p=suf(v.id)+'-PKG-STD'; S.packageCode=A_MAP[p]?p:'';}
      save(); renderAll();
    };
    L.appendChild(lab);
  }
}

function fillSelect(sel,list,cur,ph){
  sel.innerHTML='<option value="">'+ph+'</option>'+list.map(c=>'<option value="'+c.code+'">'+esc(tn(c))+' — '+fmt(c.price)+'</option>').join('');
  sel.value=list.some(c=>c.code===cur)?cur:'';
}
function renderSteps(){
  const t=suf(S.vehicleType);
  const pltsMode=S.vehicleType==='plts';
  for(const id of ['pkg','lay','mat'])$('#'+id).disabled=pltsMode;
  $('#incPlts').disabled=pltsMode;
  $('#pkg').style.opacity=$('#pkg').disabled?.5:1;
  fillSelect($('#pkg'),catBy('STRUKTUR').filter(c=>c.code.startsWith(t+'-PKG')),S.packageCode,T('— tanpa paket —|— no package —'));
  fillSelect($('#lay'),catBy('INTERIOR').filter(c=>c.code.startsWith(t+'-LAY')),S.layoutCode,T('— pilih layout —|— choose layout —'));
  fillSelect($('#mat'),catBy('INTERIOR').filter(c=>c.code.startsWith('MAT-')),S.materialCode,T('— tanpa finishing —|— no finish —'));
  $('#pkg').onchange=e=>{S.packageCode=e.target.value;save();renderAll();};
  $('#lay').onchange=e=>{S.layoutCode=e.target.value;save();renderAll();};
  $('#mat').onchange=e=>{S.materialCode=e.target.value;save();renderAll();};
  $('#incPlts').checked=pltsMode?false:!!S.includePlts;
  $('#incPlts').onchange=e=>{S.includePlts=e.target.checked;save();renderAll();};
  $('#optSizing').checked=!!S.optSizing;
  $('#optSizing').onchange=e=>{S.optSizing=e.target.checked;save();renderAll();};
}

function renderAddons(){
  const box=$('#addons'); box.innerHTML='';
  if(S.vehicleType==='plts'){box.innerHTML='<div class="mut">'+T('— tidak berlaku untuk mode PLTS —|— not applicable in solar mode —')+'</div>';return;}
  const t=suf(S.vehicleType);
  const list=[...catBy('PERALATAN').filter(c=>c.code.startsWith(t+'-AD')),
              ...catBy('LISTRIK').filter(c=>c.code.startsWith(t+'-'))];
  if(!list.length){box.innerHTML='<div class="mut">'+T('— tidak ada add-on —|— no add-ons —')+'</div>';return;}
  for(const c of list){
    const row=document.createElement('div');row.className='chk';
    row.innerHTML='<input type="checkbox" '+(S.addonCodes.includes(c.code)?'checked':'')+
      '><div><b>'+esc(tn(c))+'</b><div class="mut">'+fmt(c.price)+' / '+esc(c.unit)+' · '+esc(c.code)+'</div></div>';
    row.querySelector('input').onchange=e=>{
      S.addonCodes=S.addonCodes.filter(x=>x!==c.code);
      if(e.target.checked)S.addonCodes.push(c.code);
      save();renderAll();
    };
    box.appendChild(row);
  }
}

function renderApls(id){
  const box=$(id); if(!box)return;
  box.innerHTML='';
  for(const a of DATA.appliances){
    const st=S.appliances[a.code];
    box.insertAdjacentHTML('beforeend',
      '<div class="apl"><span class="nm">'+esc(tn(a))+'</span><span class="w">'+a.watts+' W</span>'+
      '<input type="number" min="0" value="'+(st&&st.qty>0?st.qty:0)+'" data-q="'+a.code+'" title="unit">'+
      '<span class="w">unit ×</span>'+
      '<input type="number" min="0" step="0.5" value="'+(st&&st.hours>0?st.hours:a.hours)+'" data-h="'+a.code+'" title="'+T('jam/hari|hours/day')+'">'+
      '<span class="w">'+T('jam|hrs')+'</span></div>');
  }
  box.oninput=e=>{
    if(!e.target.matches('input'))return;
    const t=e.target, q=t.dataset.q, h=t.dataset.h;
    const code=q||h; if(!code)return;
    const a=DATA.appliances.find(x=>x.code===code);
    const o=S.appliances[code]=S.appliances[code]||{qty:0,hours:a.hours};
    const v=Math.max(0,Number(t.value)||0);
    if(q)o.qty=v; else o.hours=v;
    save(); updateEst();
    if(id==='#apls') update();
  };
  box.onchange=e=>update();
}

function bindManual(){
  const pairs=[[ '#mWh','manualDailyWh','#mWh2'],['#mPeak','manualPeakW','#mPeak2'],
               ['#sun','sunIncome','#sun2']];
  for(const [sel,key,other] of pairs){
    const e1=$(sel),e2=$(other);
    if(e1)e1.value=S[key]??(key==='sunIncome'?4.5:'');
    if(e2&&e2!==e1)e2.value=S[key]??(key==='sunIncome'?4.5:'');
    e1&&(e1.oninput=()=>{S[key]=e1.value===''?null:Number(e1.value)||0;if(e2)e2.value=e1.value;save();updateEst();update();});
  }
}
function updateEst(){
  const e=energyOf(S);
  const t=T('Otomatis: |Auto: ')+e.dailyWh.toLocaleString('id-ID')+T(' Wh/hari · beban puncak | Wh/day · peak load ')+e.peakW.toLocaleString('id-ID')+T(' W (ditimpa bila kolom manual diisi).| W (overridden by the manual fields).');
  const a=$('#espEst'); if(a)a.innerHTML=t;
}

function summLine(label,val,cls=''){return '<div class="tot '+cls+'"><span>'+label+'</span><b>'+val+'</b></div>';}
function summStmt(a){return summLine('Faktor bengkel (margin '+CFG.marginPct+'%)','+'+fmt(a.margin));}

function rabHtml(){
  const {lines,plts}=buildRabLines(S);
  let h='<h2>'+T('Rincian RAB |RAB breakdown ')+'<span class="tag mode">'+(S.vehicleType==='plts'?'PLTS':({
    campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck'}[S.vehicleType]))+'</span></h2>';
  if(!lines.length){return h+'<div class="warn">'+T('Pilih paket konversi atau aktifkan PLTS dahulu.|Choose a conversion package or enable solar first.')+'</div>';}
  const groups={};
  for(const L of lines)(groups[L.group]=groups[L.group]||[]).push(L);
  h+='<h3>'+T('Rincian per kelompok|Breakdown by group')+'</h3><table><thead><tr><th style="text-align:left">'+T('Komponen|Component')+'</th><th class="r">'+T('Harga|Price')+'</th><th class="r" width="52">Qty</th><th class="r" width="70">'+T('Satuan|Unit')+'</th><th class="r">Subtotal</th></tr></thead><tbody>';
  for(const gk of ['STRUKTUR','INTERIOR','PERALATAN','PLTS','LISTRIK','PLUMBING','JASA']){
    const g=groups[gk]; if(!g)continue;
    const gkT=({STRUKTUR:'Struktur|Structure',INTERIOR:'Interior',PERALATAN:'Peralatan|Equipment',PLTS:'PLTS',LISTRIK:'Listrik|Electrical',PLUMBING:'Plumbing',JASA:'Jasa|Services'})[gk]||gk;
    h+='<tr><td colspan="4" class="gw" style="font-weight:700">'+T(gkT)+'</td><td class="r" style="font-weight:700">'+fmt(g.reduce((a,L)=>a+L.subtotal,0))+'</td></tr>';
    for(const L of g){
      h+='<tr><td>'+esc(tn(L.name))+'<div class="mut">'+esc(L.code)+(L.spec?' · '+esc(L.spec):'')+'</div></td>'+
        '<td class="r">'+fmt(L.price)+'</td><td class="r">'+L.qty+'</td><td class="r mut">'+esc(L.unit)+'</td><td class="r">'+fmt(L.subtotal)+'</td></tr>';
    }
  }
  h+='</tbody></table>';
  const adv=S.vehicleType==='plts'?null:advancedBreakdown(S,lines);
  if(adv){
    const a=adv;
    h+='<h3>'+T('Penjabaran biaya (rincian vendor)|Cost derivation (vendor detail)')+'</h3>';
    h+=summLine(T('Material dasar (katalog)|Base materials (catalog)'),fmt(a.material));
    for(const [k,v] of Object.entries(a.waste.per))if(v.val>0)h+=summLine('Waste '+k+' ('+Math.round(v.pct*100)+'%)','+'+fmt(v.val));
    h+=summLine(T('Kompleksitas|Complexity'), '<span class="tag">'+a.cx.label+'</span> × '+a.cx.score.toFixed(2));
    if(a.workDays>0)h+=summLine(T('Tenaga kerja (|Labor (')+a.workDays+T(' hari × | d × ')+CFG.hoursPerDay+T(' jam × | h × ')+fmt(CFG.laborRate)+T('/jam)|/hr)'),'+'+fmt(a.labor));
    if(a.vol.amount>0)h+=summLine(T('Diskon volume (|Volume discount (')+a.vol.pct+'%)','−'+fmt(a.vol.amount));
    h+=summLine(T('Kontingensi |Contingency (')+a.cont.pct+'% — '+esc(a.cont.reason)+')','+'+fmt(a.cont.amount));
    h+=summLine(T('Total sebelum PPN|Total before VAT'),fmt(a.beforeTax),'grand');
    h+=summLine(T('PPN |VAT (')+a.ppnPct+'%)','+'+fmt(a.ppn));
    h+=summLine('Grand total','<b>'+fmt(a.grand)+'</b>','grand');
  } else {
    const t=simpleTotals(lines);
    h+=summLine('Subtotal',fmt(t.subtotal));
    h+=summLine(T('Margin bengkel (|Workshop margin (')+t.marginPct+'%)','+'+fmt(t.margin));
    h+=summLine(T('PPN |VAT (')+t.ppnPct+'%)','+'+fmt(t.ppn));
    h+=summLine('Grand total','<b>'+fmt(t.total)+'</b>','grand');
  }
  if(plts){
    const kgn=lines.reduce((a,L)=>a+(L.weightKg||0)*L.qty,0);
    h+='<h3>Sistem PLTS terpilih</h3><div class="note">'+esc(plts.pWp)+' Wp ('+plts.pQty+'× '+num(plts.panel.comp.specs,'wp')+' Wp) · '+
      plts.bQty+'× '+plts.bAh+' Ah ≈ '+(plts.batWh/1000).toFixed(1)+' kWh · inverter '+num(plts.inverter.specs,'watts')+' W · MPPT '+num(plts.scc.specs,'amps')+' A'+(kgn?T(' · berat ±| · weight ±')+fmt0(kgn)+' kg':'')+'</div>';
    h+=viabilityHtml(plts);
    const n=optimNotes(plts);
    if(n.length)h+='<h3>Catatan optimasi komponen</h3><div class="note">'+n.map(x=>'• '+esc(x)).join('<br>')+'</div>';
  } else {
    const kgn=lines.reduce((a,L)=>a+(L.weightKg||0)*L.qty,0);
    if(kgn)h+='<div class="mut" style="margin:6px 0">'+T('Berat komponen (alat+material): ±|Component weight (tools+materials): ±')+fmt0(kgn)+T(' kg — belum termasuk bobot dasar kendaraan.| kg — excluding the base vehicle weight.')+'</div>';
  }
  h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+sowHtml(S,lines,adv,plts);
  h+='<p class="mut">Estimasi berlaku 30 hari; harga final diverifikasi admin sebelum penawaran resmi.</p>'+
     '<button class="btn no-print" onclick="kirimWa()">'+T('📱 Kirim estimasi ke Admin (WhatsApp)|📱 Send estimate to Admin (WhatsApp)')+'</button> '+
     '<button class="btn ghost no-print" onclick="copyCfg()">'+T('🔗 Salin link konfigurasi|🔗 Copy configuration link')+'</button> '+
     '<button class="btn ghost no-print" onclick="unduhCsv()">'+T('⬇️ Unduh CSV|⬇️ Download CSV')+'</button> '+
     '<button class="btn ghost no-print" onclick="simpanRiwayat()">'+T('💾 Simpan ke Riwayat|💾 Save to History')+'</button> '+
     '<button class="btn ghost no-print" onclick="window.print()">'+T('🖨️ Cetak / simpan PDF|🖨️ Print / save PDF')+'</button>';
  return h;
}
function update(){$('#rabOut').innerHTML=rabHtml();updateEst();}

function renderAll(){renderVeh();renderSteps();renderAddons();update();}

function renderCat(){
  const cats=['ALL',...new Set(C.map(c=>c.category))], box=$('#catFilter');
  box.innerHTML='<div class="opt">'+cats.map((c,i)=>'<label><input type="radio" name="cf" value="'+c+'" '+(i===0?'checked':'')+'>'+c+'</label>').join('')+'</div>';
  const draw=()=>{
    const cat=box.querySelector('input[type=radio]:checked')?.value||'ALL', q=$('#catQ').value.toLowerCase();
    $('#catBody').innerHTML=C.filter(c=>(cat==='ALL'||c.category===cat)&&(!q||c.name.toLowerCase().includes(q)||(c.nameEn||'').toLowerCase().includes(q)||c.code.toLowerCase().includes(q)))
      .map(c=>'<tr><td class="mut">'+esc(c.code)+'</td><td class="r">'+fmt(c.price)+'</td><td class="mut">'+esc(c.unit)+'</td><td>'+esc(tn(c))+'</td><td class="mut">'+esc(c.category)+'</td></tr>').join('');
  };
  $('#catQ').oninput=draw; box.onchange=draw; draw();
}

document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
  document.body.dataset.tab=b.dataset.tab;
  for(const id of ['conf','apl','cat'])$('#tab-'+id).hidden=(b.dataset.tab!==id);
});

$('#btnPlts').onclick=()=>{
  const e=energyOf({...S,manualDailyWh:S.manualDailyWh,manualPeakW:S.manualPeakW});
  if(e.dailyWh<=0||e.peakW<=0){$('#pltsOut').innerHTML='<div class="warn">'+T('Isi minimal 1 alat (unit & jam > 0) atau isi angka manual.|Fill at least one appliance (units & hours > 0) or use the manual fields.')+'</div>';return;}
  const plts=calculatePlts({dailyWh:e.dailyWh,peakW:e.peakW,sunHours:Number($('#sun2').value)||PLTS.sunHours},!!S.optSizing);
  const t=simpleTotals(plts.lines);
  let h='<h2>'+T('Hasil & RAB PLTS|Solar result & RAB')+'</h2><div class="note">'+plts.pWp+' Wp ('+plts.pQty+'× '+num(plts.panel.comp.specs,'wp')+' Wp) · '+
    plts.bQty+'× '+plts.bAh+' Ah ≈ '+(plts.batWh/1000).toFixed(1)+' kWh · inverter '+num(plts.inverter.specs,'watts')+' W · MPPT '+num(plts.scc.specs,'amps')+' A</div>';
  h+='<h3>'+T('RAB PLTS|Solar RAB')+'</h3><table><thead><tr><th style="text-align:left">'+T('Item|Item')+'</th><th class="r">'+T('Qty (satuan)|Qty (unit)')+'</th><th class="r">'+T('Harga|Price')+'</th><th class="r">Subtotal</th></tr></thead><tbody>';
  for(const L of plts.lines)h+='<tr><td>'+esc(tn(L.name))+'<div class="mut">'+esc(L.spec||L.code)+'</div></td><td class="r">'+L.qty+' '+esc(L.unit)+'</td><td class="r">'+fmt(L.price)+'</td><td class="r">'+fmt(L.subtotal)+'</td></tr>';
  h+='</tbody></table>';
  h+=summLine('Subtotal',fmt(t.subtotal));
  h+=summLine(T('Margin bengkel (|Workshop margin (')+t.marginPct+'%)','+'+fmt(t.margin));
  h+=summLine(T('PPN |VAT (')+t.ppnPct+'%)','+'+fmt(t.ppn));
  h+=summLine('Grand total','<b>'+fmt(t.total)+'</b>','grand');
  h+=viabilityHtml(plts);
  const kgn=plts.lines.reduce((a,L)=>a+(L.weightKg||0)*L.qty,0);
  if(kgn)h+='<div class="mut" style="margin:8px 0">'+T('Berat total komponen: ±|Total component weight: ±')+fmt0(kgn)+T(' kg (panel+baterai+BOS, belum termasuk rak/mounting tambahan).| kg (panels+battery+BOS, excluding extra mounting racks).')+'</div>';
  const n=optimNotes(plts);
  if(n.length)h+='<h3>Catatan optimasi komponen</h3><div class="note">'+n.map(x=>'• '+esc(x)).join('<br>')+'</div>';
  h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+sowHtml({vehicleType:'plts'},plts.lines,null,plts);
  h+='<p class="mut"><button class="btn no-print" onclick="kirimWa()">'+T('📱 Kirim ke Admin (WhatsApp)|📱 Send to Admin (WhatsApp)')+'</button> '+
     '<button class="btn ghost no-print" onclick="copyCfg()">'+T('🔗 Salin link konfigurasi|🔗 Copy configuration link')+'</button> '+
     '<button class="btn ghost no-print" onclick="unduhCsv()">'+T('⬇️ Unduh CSV|⬇️ Download CSV')+'</button> '+
     '<button class="btn ghost no-print" onclick="simpanRiwayat()">'+T('💾 Simpan ke Riwayat|💾 Save to History')+'</button> '+
     '<button class="btn ghost no-print" onclick="window.print()">'+T('🖨️ Cetak / simpan PDF|🖨️ Print / save PDF')+'</button></p>';
  $('#pltsOut').innerHTML=h;
};

/* ===== util kelayakan & share-link ===== */
const fmt0=n=>Math.round(n).toLocaleString('id-ID');
let toastT=null;
function toast(msg){
  const t=document.createElement('div');t.className='toast';t.textContent=msg;
  document.body.appendChild(t);
  requestAnimationFrame(()=>t.classList.add('show'));
  clearTimeout(toastT);toastT=setTimeout(()=>{t.classList.remove('show');setTimeout(()=>t.remove(),300);},2200);
}
function encodeCfg(){return btoa(unescape(encodeURIComponent(JSON.stringify(S)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function decodeCfg(str){
  if(!str)return null;
  try{
    let t=str.replace(/-/g,'+').replace(/_/g,'/');
    while(t.length%4)t+='=';
    return JSON.parse(decodeURIComponent(escape(atob(t))));
  }catch(e){return null;}
}
function shareLink(){try{return location.origin+location.pathname+'?cfg='+encodeCfg();}catch(e){return '';}}
function copyCfg(){
  const link=shareLink(); if(!link){toast(T('Tidak bisa membuat link|Cannot create a link'));return;}
  const done=()=>toast(T('Link konfigurasi disalin — tempel di WhatsApp/chat|Config link copied — paste it in WhatsApp/chat'));
  const fallback=()=>{if(window.prompt(T('Salin link konfigurasi ini:|Copy this configuration link:'),link))done();};
  if(navigator.clipboard&&navigator.clipboard.writeText)
    navigator.clipboard.writeText(link).then(done).catch(fallback);
  else fallback();
}
function unduhCsv(){
  const {lines}=buildRabLines(S);
  if(!lines.length){alert(T('Susun dulu paket / add-on / kebutuhan listrik.|Build a package / add-on / power needs first.'));return;}
  const q=c=>'"'+String(c).replace(/"/g,'""')+'"';
  const row=(a,b,c2,d,e,f,g)=>[a,b||'',c2||'',d||'',e||'',f||'',g||''];
  const rows=[row(T('Komponen|Component'),T('Kode|Code'),T('Kelompok|Group'),'Qty',T('Satuan|Unit'),T('Harga|Price'),'Subtotal')];
  for(const L of lines)rows.push(row(tn(L.name),L.code,L.group||'',L.qty,L.unit,L.price,L.subtotal));
  const adv=S.vehicleType==='plts'?null:advancedBreakdown(S,lines);
  const tot=adv?adv.grand:simpleTotals(lines).total;
  if(adv){
    rows.push(row(T('Limbah material ±|Material waste ±')+adv.waste.avg+'%','','','','','',adv.waste.total));
    if(adv.workDays>0)rows.push(row(T('Tenaga kerja (|Labor (')+adv.workDays+T(' hari × | d × ')+CFG.hoursPerDay+T(' jam × | h × ')+CFG.laborRate+T(' /jam)| /hr)'),'','',adv.workDays+T(' hari| d'),'','',adv.labor));
    rows.push(row(T('Kompleksitas: |Complexity: ')+adv.cx.label+' (×'+adv.cx.score.toFixed(2)+')'));
    if(adv.vol.amount>0)rows.push(row(T('Diskon volume (|Volume discount (')+adv.vol.pct+'%)','','','','','',-adv.vol.amount));
    rows.push(row(T('Kontingensi |Contingency ')+adv.cont.pct+'% — '+adv.cont.reason,'','','','','',adv.cont.amount));
    rows.push(row(T('PPN |VAT ')+adv.ppnPct+'%','','','','','',adv.ppn));
  }else{
    const t=simpleTotals(lines);
    rows.push(row(T('Margin bengkel |Workshop margin ')+t.marginPct+'%','','','','','',t.margin));
    rows.push(row(T('PPN |VAT ')+t.ppnPct+'%','','','','','',t.ppn));
  }
  rows.push(row('GRAND TOTAL','','','','','',tot));
  const blob=new Blob(['\ufeff'+rows.map(r=>r.map(q).join(';')).join('\r\n')],{type:'text/csv;charset=utf-8'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download='RAB-'+(S.vehicleType||'proyek')+'.csv';
  document.body.appendChild(a); a.click(); a.remove();
  toast(T('CSV RAB terunduh ✓|RAB CSV downloaded ✓'));
}
function viabilityHtml(plts){
  const V=PLTS.batteryVoltage;
  const prod=plts.pWp*plts.sun*PLTS.derating;
  const auto=plts.batWh*PLTS.batteryDoD/plts.dailyWh;
  const inv=num(plts.inverter.specs,'watts');
  const sccA=num(plts.scc.specs,'amps');
  const arus=Math.ceil(plts.pWp/V*PLTS.sccOversize);
  const rows=[
    [T('Produksi panel|Panel output'),'@sun '+plts.sun+T(' jam ≈ | h ≈ ')+fmt0(prod)+T(' Wh/hari| Wh/day'),T('vs kebutuhan |vs daily demand ')+fmt0(plts.dailyWh)+T(' Wh/hari| Wh/day'),prod>=plts.dailyWh],
    [T('Cadangan baterai|Battery reserve'),'autonomi '+auto.toFixed(1)+T(' hari (DoD 80%)| days of autonomy (DoD 80%)'),T('target ≥ 1 hari — sizing standar 2 hari|target ≥ 1 day — standard sizing uses 2 days'),auto>=1],
    [T('Inverter vs beban puncak|Inverter vs peak load'),fmt0(inv)+' W vs '+fmt0(plts.peakW)+' W',T('margin |margin ')+Math.max(0,Math.round((inv-plts.peakW)/Math.max(1,plts.peakW)*100))+'%'+T(' (sizing ×1.25)| (sizing ×1.25)'),inv>=plts.peakW],
    [T('MPPT vs arus panel|MPPT vs panel current'),sccA+' A vs '+fmt0(arus)+' A',T('arus = Wp ÷ |current = Wp ÷ ')+V+' V × 1.25',sccA>=arus],
  ];
  let h='<h3>'+T('Cek kelayakan sistem|System viability check')+'</h3><table class="viab"><thead><tr><th style="text-align:left">'+T('Aspek|Aspect')+'</th><th>'+T('Hitungan|Calculation')+'</th><th style="text-align:left">'+T('Acuan|Benchmark')+'</th><th style="text-align:right">'+T('Status|Status')+'</th></tr></thead><tbody>';
  for(const r of rows)h+='<tr><td>'+esc(r[0])+'</td><td class="r">'+esc(r[1])+'</td><td class="mut">'+esc(r[2])+'</td><td class="r"><span class="badge '+(r[3]?'ok':'bad')+'">'+(r[3]?'OK ✓':T('PERIKSA ✗|CHECK ✗'))+'</span></td></tr>';
  h+='</tbody></table>';
  if(rows.some(r=>!r[3]))h+='<div class="warn">'+T('Ada aspek berstatus PERIKSA. Naikkan beban/panel/baterai hingga semua OK — atau kirim link konfigurasi ini ke admin untuk penyesuaian desain.|Some aspects show CHECK. Increase the load/panels/battery until all OK — or send this config link to the admin for design help.')+'</div>';
  return h;
}

function sowHtml(s,lines,adv,plts){
  const inCat=c=>lines.some(L=>L.category===c);
  const catNames=c=>lines.filter(L=>L.category===c).map(L=>tn(L.name));
  const join=(arr,n)=>{const t=arr.slice(0,n||4).map(esc).join(', ');return t+(arr.length>(n||4)?' +'+(arr.length-(n||4))+' item lain':'')+(arr.length?'.':'');};
  const scope=[[T('Desain & persiapan|Design & preparation'),T('samakan kebutuhan, pengukuran, sketsa layout sederhana, dan daftar material — kami konfirmasi desain ke Anda sebelum mulai memotong bahan.|we align on needs, take measurements, sketch a simple layout and draft the materials list — the design is confirmed with you before any cutting starts.')]];
  const pkg=catNames('STRUKTUR');
  if(pkg.length)scope.push([T('Struktur & bodi|Structure & body'),T('pembongkaran seperlunya, penguatan rangka, pelapis dinding/lantai (|as-needed disassembly, frame reinforcement, wall/floor lining (')+join(pkg)+T('), anti-bocor & peredam seperlunya.|), leak-proofing & damping as needed.')]);
  const int=catNames('INTERIOR');
  if(int.length)scope.push([T('Interior & finishing|Interior & finish'),T('fabrikasi furniture, pelapisan/finishing (|fabricated furniture, lining & finishing (')+join(int)+T(') mengikuti gambar yang sudah disetujui.|) following the approved drawing.')]);
  if(inCat('LISTRIK'))scope.push([T('Instalasi kelistrikan kendaraan|Vehicle electrical installation'),T('titik lampu/saklar, sekuring/MCB, grounding, dan pengujian beban sebelum serah terima.|light and switch points, circuit breakers/MCB, grounding, and a load test before handover.')]);
  const alat=catNames('PERALATAN');
  if(alat.length)scope.push([T('Pemasangan peralatan & aksesori|Equipment & accessory installation'),join(alat)+T(' — dipasang, disambung, dan diuji fungsinya satu per satu.| — mounted, wired and tested one by one.')]);
  if(inCat('PLTS_PANEL')||inCat('PLTS_BATTERY')||inCat('PLTS_INVERTER')||inCat('PLTS_SCC')||(plts&&plts.pWp>0))scope.push([T('Instalasi PLTS / tenaga surya|Solar PV installation'),T('panel terpasang & kabel rapi, baterai + inverter + MPPT menyala, pengujian pengisian/pemakaian, plus pendampingan cara pakai.|panels mounted & cabled neatly, battery + inverter + MPPT powered up, charge/load testing, plus usage guidance.')]);
  let dur;
  if(s.vehicleType==='plts')dur=T('±2–3 hari kerja instalasi|±2–3 days of installation work');
  else if(adv&&adv.workDays>0)dur='±'+adv.workDays+T(' hari kerja di bengkel| days of workshop work');
  else dur=T('disesuaikan pesanan|tailored to the order');
  const kami=[
    T('Dikerjakan sesuai lingkup & material dalam dokumen ini — pembongkaran/pekerjaan di luar itu minta ijin dan persetujuan biaya lebih dahulu (cukup via WhatsApp).|We build exactly to the scope & materials in this document — any work outside it needs your prior approval and cost agreement (WhatsApp is enough).'),
    T('Menyediakan pembaruan progres + foto pada tiap tahap besar kepada WhatsApp Anda.|We send progress updates + photos to your WhatsApp at every major stage.'),
    T('Garansi pengerjaan 90 hari untuk cacat instalasi; garansi produk mengikuti ketentuan vendor masing-masing.|90-day workmanship warranty for installation defects; product warranty follows each vendor\'s own terms.'),
    T('Serah terima bersih: fungsi diuji bersama Anda, area kerja dibersihkan, cara pemakaian dijelaskan.|Clean handover: functions tested together, work area cleaned, usage explained.')];
  const Anda=[
    T('Menyampaikan kebutuhan dan perubahan desain sedini mungkin — terlebih sebelum material mulai dipotong.|Share your needs and design changes early — especially before materials are cut.'),
    T('Menyediakan akses kendaraan/lokasi yang aman selama pengerjaan berlangsung.|Provide safe access to the vehicle/site while the work is in progress.'),
    T('Melunasi termin pembayaran sesuai jadwal yang dikonfirmasi admin.|Settle the payment installments on the schedule confirmed by the admin.'),
    T('Merawat pekerjaan sesuai panduan yang kami berikan agar garansi tetap berlaku.|Maintain the work as per our guidance to keep the warranty valid.')];
  const luar=[
    T('Kerusakan tersembunyi yang baru ketahuan saat pembongkaran (karat, rapuh, bocor lama): kami foto, laporkan, dan lanjut setelah Anda menyetujui biayanya.|Hidden damage discovered during disassembly (rust, rot, old leaks): we photograph, report, and continue after you approve the cost.'),
    T('Perbaikan wajib/rutin kendaraan (mesin, kelistrikan pabrik mobil).|Mandatory/routine vehicle repairs (engine, factory wiring).'),
    T('Kerugian akibat pemakaian tidak sesuai panduan (mis. beban PLTS melebihi daya terpasang).|Damage from use contrary to our guidance (e.g. solar loads above the installed capacity).')];
  let h='<div class="sow"><div class="grow"><div><h4>'+T('🛠️ Lingkup pekerjaan|🛠️ Scope of work')+'</h4><ul>'+
    scope.map(x=>'<li><b>'+esc(x[0])+'</b> — '+x[1]+'</li>').join('')+
    '</ul><p class="mut">'+T('Jangka waktu estimasi: |Estimated duration: ')+esc(dur)+T(' (belum termasuk lead-time barang, kira-kira 7–14 hari).| (excluding material lead time, roughly 7–14 days).')+'</p></div>';
  h+='<div><h4>'+T('🤝 Komitmen kami (bengkel)|🤝 Our commitments (workshop)')+'</h4><ul>'+kami.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'+
     '<h4>'+T('🙏 Hak & kewajiban Anda (konsumen)|🙏 Your rights & duties (customer)')+'</h4><ul>'+Anda.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div></div>';
  h+='<div class="luar"><h4>'+T('⚠️ Di luar lingkup — selalu beritahu kami dahulu|⚠️ Out of scope — always tell us first')+'</h4><ul>'+luar.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>';
  h+='<p class="mut">'+T('Estimasi berlaku 30 hari: semua angka & lingkup mengacu pada dokumen ini. Jadwal, termin, dan garansi final dikonfirmasi admin EcoPower sebelum pengerjaan dimulai — konsultasinya gratis.|Estimate valid for 30 days: all figures & scope follow this document. Final schedule, installments and warranty are confirmed by the EcoPower admin before work starts — the consultation is free.')+'</p></div>';
  return h;
}

/* ===== riwayat penawaran & perbandingan ===== */
const histLoad=()=>{try{return JSON.parse(localStorage.getItem('rab.hist')||'[]')}catch(e){return []}};
const histSave=a=>{try{localStorage.setItem('rab.hist',JSON.stringify(a));}catch(e){}};
const bandSel=new Set();
function snapLabel(){
  const t={campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck'}[S.vehicleType]||'';
  const pk=S.packageCode&&A_MAP[S.packageCode]?tn(A_MAP[S.packageCode]):'';
  return (S.vehicleType==='plts'?T('PLTS mandiri|Standalone solar'):t+(pk?' · '+pk:''))+(S.addonCodes.length?' +'+S.addonCodes.length+' add-on':'');
}
function simpanRiwayat(){
  const {lines,plts}=buildRabLines(S);
  if(!lines.length){alert(T('Susun dulu paket / add-on / kebutuhan listrik.|Build a package / add-on / power needs first.'));return;}
  const adv=S.vehicleType==='plts'?null:advancedBreakdown(S,lines);
  const kgn=lines.reduce((a,L)=>a+(L.weightKg||0)*L.qty,0);
  const e={id:Date.now().toString(36)+Math.floor(Math.random()*1296).toString(36),ts:Date.now(),
    cfg:encodeCfg(),label:snapLabel(),
    tot:adv?adv.grand:simpleTotals(lines).total,
    wp:plts?plts.pWp:0,kwh:plts?+(plts.batWh/1000).toFixed(1):0,
    inv:plts?num(plts.inverter.specs,'watts'):0,scc:plts?num(plts.scc.specs,'amps'):0,
    wd:adv?adv.workDays:0,cx:adv?adv.cx.score:0,kg:Math.round(kgn),
    addons:(S.addonCodes||[]).length,veh:S.vehicleType,pkg:S.packageCode||'',lay:S.layoutCode||'',mat:S.materialCode||''};
  const a=histLoad();a.unshift(e);if(a.length>30)a.pop();
  histSave(a);renderRiwayat();toast('Disimpan ke riwayat ✓');
}
function muatRiwayat(id){
  const e=histLoad().find(x=>x.id===id);if(!e)return;
  const cf=decodeCfg(e.cfg);if(!cf){toast(T('Snapshot rusak|Broken snapshot'));return;}
  Object.assign(S,cf);save();
  renderAll();renderRiwayat();
  toast(T('Konfigurasi dimuat dari riwayat ✓|Configuration loaded from history ✓'));
  try{$('#rabOut').scrollIntoView({behavior:'smooth',block:'start'});}catch(x){}
}
function hapusRiwayat(id){histSave(histLoad().filter(x=>x.id!==id));bandSel.delete(id);renderRiwayat();toast(T('Entri dihapus|Entry deleted'));}
function salinHist(id){
  const e=histLoad().find(x=>x.id===id);if(!e)return;
  const link=location.origin+location.pathname+'?cfg='+e.cfg;
  const done=()=>toast(T('Link snapshot disalin ✓|Snapshot link copied ✓'));
  const fb=()=>{if(window.prompt(T('Salin link snapshot:|Copy the snapshot link:'),link))done();};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(link).then(done).catch(fb);
  else fb();
}
function toggleBanding(id){
  if(bandSel.has(id))bandSel.delete(id);
  else{if(bandSel.size>=3){toast(T('Bandingkan maksimal 3 penawaran|Compare up to 3 quotes'));return;}bandSel.add(id);}
  renderRiwayat();
}
function histLabel(e){
  const d=new Date(e.ts);
  return d.toLocaleDateString('id-ID',{day:'2-digit',month:'short'})+' '+d.toLocaleTimeString('id-ID',{hour:'2-digit',minute:'2-digit'});
}
function bandingHtml(list){
  const min=Math.min.apply(null,list.map(e=>e.tot));
  const rows=[
    [T('Grand total|Grand total'),e=>'<b>'+fmt(e.tot)+'</b>'],
    [T('Tipe|Type'),e=>esc({campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck',plts:T('PLTS mandiri|Standalone solar')}[e.veh]||e.veh)],
    [T('Paket|Package'),e=>e.pkg&&A_MAP[e.pkg]?esc(tn(A_MAP[e.pkg])):(e.veh==='plts'?'—':T('tanpa paket|no package'))],
    ['Add-on',e=>e.addons?'+'+e.addons:'—'],
    ['PLTS',e=>e.wp?e.wp+' Wp · '+e.kwh+' kWh':'—'],
    ['Inverter / MPPT',e=>e.wp?e.inv+' W / '+e.scc+' A':'—'],
    [T('Tenaga kerja|Labor'),e=>e.wd?e.wd+T(' hari kerja| working days'):'—'],
    [T('Kompleksitas|Complexity'),e=>e.cx?'×'+Number(e.cx).toFixed(2):'—'],
    [T('Berat komponen|Weight'),e=>e.kg?'±'+e.kg+' kg':'—'],
  ];
  let h='<h3>'+T('⚖️ Perbandingan penawaran|⚖️ Quote comparison')+'</h3><table class="cmp"><thead><tr><th style="width:110px">'+T('Aspek|Aspect')+'</th>'+
    list.map(e=>'<th>'+esc(histLabel(e))+'<div class="mut mini">'+esc(e.label)+'</div></th>').join('')+'</tr></thead><tbody>';
  for(const r of rows)h+='<tr><td class="mut" style="font-size:12.5px">'+r[0]+'</td>'+
    list.map(e=>'<td'+(r[0]==='Grand total'&&e.tot===min?' class="win"':'')+'>'+r[1](e)+'</td>').join('')+'</tr>';
  return h+'</tbody></table>';
}
function renderRiwayat(){
  const a=histLoad(),box=$('#histBox');
  if(!a.length){box.innerHTML='<h2>'+T('🗂️ Riwayat penawaran|🗂️ Quote history')+'</h2><div class="mut">'+T('Belum ada. Tekan tombol “💾 Simpan ke Riwayat” pada hasil RAB — konfigurasi & angkanya bisa dibuka ulang atau dibandingkan kapan pun (maks. 30 entri).|Empty so far. Press “Save to History” on the RAB result — the configuration & figures can be reopened or compared any time (max. 30 entries).')+'</div>';return;}
  const sel=a.filter(e=>bandSel.has(e.id));
  let h='<h2>'+T('🗂️ Riwayat penawaran|🗂️ Quote history')+'</h2>';
  if(sel.length>=2)h+=bandingHtml(sel)+'<p class="mut mini">'+T('Angka hijau = grand total termurah di antara pilihan.|Green = the lowest grand total among the selected quotes.')+'</p>';
  h+=a.map(e=>'<div class="hist"><div class="nm"><b>'+esc(e.label)+'</b> <span class="tag mini">'+esc(histLabel(e))+'</span>'+
    '<div class="mut mini">'+(e.wp?e.wp+' Wp · '+e.kwh+' kWh · ':'')+(e.wd?e.wd+T(' hari kerja · | working days · '):'')+T('berat ±|weight ±')+e.kg+' kg</div></div>'+
    '<b style="white-space:nowrap">'+fmt(e.tot)+'</b>'+
    '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-left:auto">'+
    '<button class="btn ghost mini" onclick="muatRiwayat(\'+e.id+\')">'+T('📂 Muat|📂 Load')+'</button>'+
    '<button class="btn ghost mini" onclick="toggleBanding(\''+e.id+'\')">'+(bandSel.has(e.id)?T('✅ Dipilih|✅ Selected'):T('⚖️ Bandingkan|⚖️ Compare'))+'</button>'+
    '<button class="btn ghost mini" onclick="salinHist(\''+e.id+'\')">🔗</button>'+
    '<button class="btn ghost mini" onclick="if(confirm(\''+T('Hapus entri ini?|Delete this entry?')+'\'))hapusRiwayat(\''+e.id+'\')">🗑️</button>'+
    '</div></div>').join('');
  box.innerHTML=h;
}

/* ===== bahasa & dark mode ===== */
const LANG=(location.search.match(/[?&]lang=(en|id)\b/)||[])[1]||(function(){try{return localStorage.getItem('rab.lang')||'id';}catch(e){return 'id';}})();
function T(p){const i=p.indexOf('|');return LANG==='en'&&i>=0?p.slice(i+1):p.slice(0,i<0?p.length:i);}
/* ---- nama katalog EN (nameId → nameEn dari API referensi) ---- */
const _EN={};(DATA.components||[]).forEach(c=>{if(c.nameEn)_EN[c.name]=c.nameEn;});
(DATA.appliances||[]).forEach(a=>{if(a.nameEn)_EN[a.name]=a.nameEn;});
function tn(x){if(LANG!=='en')return typeof x==='object'?(x.name||''):x;
  if(typeof x==='object')return x.nameEn||x.name||'';
  return _EN[x]||x;}

/* ===== WhatsApp admin ===== */
const WA_PHONE='6285334398681';
function waText(){
  const {lines,plts}=buildRabLines(S);
  if(!lines.length)return null;
  const adv=S.vehicleType==='plts'?null:advancedBreakdown(S,lines);
  const tot=adv?adv.grand:simpleTotals(lines).total;
  const nm=c=>A_MAP[c]?tn(A_MAP[c]):c;
  const jenis={campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck',plts:'PLTS'}[S.vehicleType]||'-';
  const akt=(
    S.vehicleType==='plts'?[]:[T('Tipe: |Type: ')+jenis,
    S.packageCode?T('Paket: |Package: ')+nm(S.packageCode):'',
    S.layoutCode?'Layout: '+nm(S.layoutCode):'',
    S.materialCode?'Material: '+nm(S.materialCode):'',
    S.addonCodes.length?'Add-on: '+S.addonCodes.map(nm).join(', '):'']
  );
  if((S.includePlts||S.vehicleType==='plts')&&plts)akt.push(
    'PLTS: '+plts.pWp+' Wp ('+plts.pQty+'× '+num(plts.panel.comp.specs,'wp')+' Wp), baterai '+
    plts.bQty+'× '+plts.bAh+' Ah ≈ '+(plts.batWh/1000).toFixed(1)+' kWh, inverter '+num(plts.inverter.specs,'watts')+' W, MPPT '+num(plts.scc.specs,'amps')+' A');
  akt.push(T('Estimasi grand total: |Estimated grand total: ')+fmt(tot)+T(' (berlaku 30 hari)| (valid for 30 days)'));
  let msg=T('Halo EcoPower ID, saya baru memakai kalkulator RAB online.|Hi EcoPower ID, I just used your online RAB calculator.')+'\n'+akt.join('\n');
  try{const L=shareLink();if(L)msg+='\n\n'+T('Link konfigurasi (bisa dibuka & diedit lagi): |Config link (open & edit it again here): ')+L;}catch(e){}
  msg+='\n'+T('Mohon info harga final & jadwal produksinya. Terima kasih.|Please send the final pricing & production schedule. Thank you.');
  return msg;
}
function kirimWa(){
  const t=waText();
  if(!t){alert(T('Susun dulu paket / add-on / kebutuhan listrik, lalu kirim.|Build a package / add-on / power needs first, then send.'));return;}
  window.open('https://wa.me/'+WA_PHONE+'?text='+encodeURIComponent(t),'_blank','noopener,noreferrer');
}

renderApls('#apls'); renderApls('#apls2');
S.sunIncome=Number(S.sunIncome)||4.5;
bindManual(); renderAll(); renderCat(); updateEst(); renderRiwayat();
(function(){try{
  const dk=localStorage.getItem('rab.dark');
  let dark=dk===null?!!(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches):dk==='1';
  const ap=()=>document.body.classList.toggle('dark',!!dark);ap();
  $('#darkBtn').onclick=()=>{dark=!dark;localStorage.setItem('rab.dark',dark?'1':'0');ap();};
  $('#langBtn').textContent=(LANG==='id'?'EN':'ID');
  $('#langBtn').onclick=()=>{try{localStorage.setItem('rab.lang',LANG==='id'?'en':'id');}catch(e){}
    location.href=location.origin+location.pathname+'?lang='+(LANG==='id'?'en':'id');};
  document.querySelectorAll('[data-tr]').forEach(el=>el.textContent=T(el.dataset.tr));
  $('#catQ').placeholder=T('Cari nama / kode…|Search name / code…');
}catch(e){}})();
</script>
</body>
</html>
"""

html_out = TEMPLATE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
out = ROOT / "index.html"
out.write_text(html_out, encoding="utf-8")

BASE = "https://bilidarnanto.github.io/rab-kalkulator/"
(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
d = datetime.date.today().isoformat()
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{BASE}</loc><lastmod>{d}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
    '</urlset>\n', encoding="utf-8")
print("wrote", out, len(html_out), "bytes")
