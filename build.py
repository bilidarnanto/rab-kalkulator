#!/usr/bin/env python3
"""Generate index.html (GitHub Pages RAB calculator) dari artifacts/catalog.json.

Satu file HTML mandiri (vanilla JS, tanpa dependensi). Harga diambil dari katalog
vendor EcoPower ID (real, update 2026-08) — lihat RESEARCH.md untuk verifikasi
pasar & analisis optimasi. Jalankan ulang ``python3 build.py`` setelah katalog
diperbarui.
"""
import json
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

DATA = {
    "components": [
        {
            "code": c["code"], "name": c["nameId"], "category": c["category"],
            "unit": c["unit"], "price": c["price"], "specs": c.get("specs") or {},
        }
        for c in CAT
    ],
    "appliances": [{"code": a, "name": n, "watts": w, "hours": h} for (a, n, w, h) in APPLIANCES],
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
<meta name="description" content="Kalkulator RAB konversi campervan, motorhome, food truck dan instalasi PLTS. Harga real katalog vendor (Aug 2026) + verifikasi pasar Okt 2026.">
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
@media print{header,nav,.no-print{display:none!important}body{background:#fff}
section.card{border:0;padding:0;margin:0 0 12px}.sticky{position:static}
}
</style>
</head>
<body>
<header>
  <h1>⚡ Kalkulator RAB</h1>
  <small>Campervan · Motorhome · Food Truck · PLTS — harga real katalog vendor (Aug 2026), verifikasi pasar Okt 2026</small>
</header>
<main>
<nav class="no-print">
  <button data-tab="conf" class="on">Konfigurator RAB</button>
  <button data-tab="apl">Kalkulator PLTS</button>
  <button data-tab="cat">Tabel Harga</button>
</nav>

<div id="tab-conf">
  <div class="grid">
    <section class="card">
      <h2>1 · Tipe & paket</h2>
      <div class="opt" id="vehList"></div>
      <label>Paket konversi</label><select id="pkg"></select>
      <label>Layout interior</label><select id="lay"></select>
      <label>Material finishing</label><select id="mat"></select>
      <div class="chk" style="margin-top:10px"><input type="checkbox" id="incPlts">
        <div><b>Sistem PLTS (listrik mandiri)</b>
        <div class="mut">Panel solar + baterai LiFePO4 + inverter + MPPT + proteksi + jasa.</div></div></div>
      <div class="chk"><input type="checkbox" id="optSizing">
        <div><b>Optimasi sizing komponen PLTS</b>
        <div class="mut">Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.</div></div></div>
    </section>
    <section class="card">
      <h2>2 · Kelengkapan (add-on)</h2>
      <div id="addons"></div>
    </section>
    <section class="card">
      <h2>3 · Kebutuhan listrik harian</h2>
      <div id="apls"></div>
      <div class="grid" style="margin-top:10px">
        <div><label>Total harian manual (Wh)</label><input id="mWh" type="number" min="0" placeholder="otomatis"></div>
        <div><label>Beban puncak manual (W)</label><input id="mPeak" type="number" min="0" placeholder="otomatis"></div>
        <div><label>Peak sun hour harian (1–7)</label><input id="sun" type="number" step="0.1" min="1" max="7" value="4.5"></div>
      </div>
      <div class="note" id="espEst"></div>
    </section>
  </div>
  <section class="card sticky" id="rabOut"></section>
</div>

<div id="tab-apl" hidden>
  <section class="card">
    <h2>Kalkulator PLTS (sistem mandiri)</h2>
    <div id="apls2"></div>
    <div class="grid" style="margin-top:10px">
      <div><label>Total harian manual (Wh)</label><input id="mWh2" type="number" min="0" placeholder="otomatis"></div>
      <div><label>Beban puncak manual (W)</label><input id="mPeak2" type="number" min="0" placeholder="otomatis"></div>
      <div><label>Peak sun hour harian (1–7)</label><input id="sun2" type="number" step="0.1" min="1" max="7" value="4.5"></div>
    </div>
    <button class="btn" id="btnPlts" style="margin-top:12px">Hitung & susun RAB PLTS</button>
  </section>
  <section class="card" id="pltsOut"><div class="mut">Isi jumlah unit & jam pemakaian, lalu tekan hitung.</div></section>
</div>

<div id="tab-cat" hidden>
  <section class="card">
    <h2>Harga komponen — katalog vendor (real, Aug 2026)</h2>
    <input id="catQ" type="text" placeholder="Cari nama / kode…">
    <div id="catFilter" style="margin:10px 0"></div>
    <table><thead><tr><th style="width:112px">Kode</th><th class="r">Harga satuan</th><th style="width:66px">Satuan</th><th>Nama</th><th style="width:96px">Kategori</th></tr></thead><tbody id="catBody"></tbody></table>
    <p class="mut">Sumber: API <code>/api/catalog</code> situs referensi (Aug 2026) · banding riset & optimasi: <code>RESEARCH.md</code>.</p>
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
  if(!best){ // fallback: unit terbesar dengan cap
    const l=catBy(cat).filter(c=>num(c.specs,key)>0).sort((a,b)=>num(b.specs,key)-num(a.specs,key));
    best={comp:l[0],qty:cap,cost:l[0].price*cap};
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
  n.push('Indikator Rp/Wp panel: '+fmt(rpWp)+' — unit 450–550 Wp ~Rp5.100/Wp, unit 100 Wp Rp9.500/Wp (2× lipat).');
  n.push('Indikator Rp/Wh baterai: '+fmt(rpWh)+' — unit 200–300 Ah paling hemat per kWh.');
  n.push('Indikator Rp/W inverter: '+fmt(rpW)+' — jaga beban puncak agar tidak terloncat ke kelas yang lebih besar.');
  n.push('Indikator Rp/A MPPT: '+fmt(rpA)+' — bila panel dibagi 2 string, 2×30 A sering lebih murah daripada 1×60 A.');
  if(plts.panel.comp!==smallPickDesc('PLTS_PANEL','wp'))
    n.push('Sizing hemat aktif: '+plts.pQty+'× '+num(spec(plts.panel.comp),'wp')+' Wp ('+fmt(plts.panel.comp.price)+'/unit) — lihat catatan Rp/Wp di atas.');
  if(plts.bQty===PLTS.maxBatteryUnits)
    n.push('Baterai mencapai batas '+PLTS.maxBatteryUnits+' unit — pertimbangkan baterai kapasitas lebih besar atau turunkan otonomi.');
  if(plts.inverter&&num(spec(plts.inverter),'watts')>2.2*plts.peakW)
    n.push('Inverter melebihi 2× beban puncak — elemen beban bisa dilakukan bertahap (stagger) agar inverter lebih kecil.');
  if(plts.scc&&num(spec(plts.scc),'amps')<=30)
    n.push('MPPT 30 A cukup — nilai arus: '+plts.scc.code.replace('PLTS-SCC-','')+' A.');
  return n;
}

/* ===== UI ===== */
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));

let S={vehicleType:'campervan',packageCode:'CV-PKG-STD',layoutCode:'',materialCode:'',addonCodes:[],
  includePlts:false,optSizing:true,appliances:{},manualDailyWh:null,manualPeakW:null,sunIncome:4.5};
try{Object.assign(S,JSON.parse(localStorage.getItem('rab.state')||'{}'));}catch(e){}
const save=()=>{try{localStorage.setItem('rab.state',JSON.stringify(S));}catch(e){}};

const VEH=[{id:'campervan',nm:'🚐 Campervan',d:'van konversi 1–4 orang'},
  {id:'motorhome',nm:'🚌 Motorhome',d:'rumah berjalan 4–8 orang'},
  {id:'foodtruck',nm:'🍔 Food Truck',d:'dapur di atas roda'},
  {id:'plts',nm:'☀️ PLTS (rumah/lainnya)',d:'tanpa paket kendaraan'}];
const suf=v=>({campervan:'CV',motorhome:'MH',foodtruck:'FT'}[v]||'');

function renderVeh(){
  const L=$('#vehList'); L.innerHTML='';
  for(const v of VEH){
    const lab=document.createElement('label');
    lab.innerHTML='<input type="radio" name="veh" value="'+v.id+'" '+(S.vehicleType===v.id?'checked':'')+'> '+v.nm;
    lab.title=v.d;
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
  sel.innerHTML='<option value="">'+ph+'</option>'+list.map(c=>'<option value="'+c.code+'">'+esc(c.name)+' — '+fmt(c.price)+'</option>').join('');
  sel.value=list.some(c=>c.code===cur)?cur:'';
}
function renderSteps(){
  const t=suf(S.vehicleType);
  const pltsMode=S.vehicleType==='plts';
  for(const id of ['pkg','lay','mat'])$('#'+id).disabled=pltsMode;
  $('#incPlts').disabled=pltsMode;
  $('#pkg').style.opacity=$('#pkg').disabled?.5:1;
  fillSelect($('#pkg'),catBy('STRUKTUR').filter(c=>c.code.startsWith(t+'-PKG')),S.packageCode,'— tanpa paket —');
  fillSelect($('#lay'),catBy('INTERIOR').filter(c=>c.code.startsWith(t+'-LAY')),S.layoutCode,'— pilih layout —');
  fillSelect($('#mat'),catBy('INTERIOR').filter(c=>c.code.startsWith('MAT-')),S.materialCode,'— tanpa finishing —');
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
  if(S.vehicleType==='plts'){box.innerHTML='<div class="mut">— tidak berlaku untuk mode PLTS —</div>';return;}
  const t=suf(S.vehicleType);
  const list=[...catBy('PERALATAN').filter(c=>c.code.startsWith(t+'-AD')),
              ...catBy('LISTRIK').filter(c=>c.code.startsWith(t+'-'))];
  if(!list.length){box.innerHTML='<div class="mut">— tidak ada add-on —</div>';return;}
  for(const c of list){
    const row=document.createElement('div');row.className='chk';
    row.innerHTML='<input type="checkbox" '+(S.addonCodes.includes(c.code)?'checked':'')+
      '><div><b>'+esc(c.name)+'</b><div class="mut">'+fmt(c.price)+' / '+esc(c.unit)+' · '+esc(c.code)+'</div></div>';
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
      '<div class="apl"><span class="nm">'+esc(a.name)+'</span><span class="w">'+a.watts+' W</span>'+
      '<input type="number" min="0" value="'+(st&&st.qty>0?st.qty:0)+'" data-q="'+a.code+'" title="unit">'+
      '<span class="w">unit ×</span>'+
      '<input type="number" min="0" step="0.5" value="'+(st&&st.hours>0?st.hours:a.hours)+'" data-h="'+a.code+'" title="jam/hari">'+
      '<span class="w">jam</span></div>');
  }
  box.oninput=e=>{
    if(e.target.matches('input')) save(); updateEst();
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
  const t='Otomatis: '+e.dailyWh.toLocaleString('id-ID')+' Wh/hari · beban puncak '+e.peakW.toLocaleString('id-ID')+' W (ditimpa bila kolom manual diisi).';
  const a=$('#espEst'); if(a)a.innerHTML=t;
}

function summLine(label,val,cls=''){return '<div class="tot '+cls+'"><span>'+label+'</span><b>'+val+'</b></div>';}
function summStmt(a){return summLine('Faktor bengkel (margin '+CFG.marginPct+'%)','+'+fmt(a.margin));}

function rabHtml(){
  const {lines,plts}=buildRabLines(S);
  let h='<h2>Rincian RAB <span class="tag mode">'+(S.vehicleType==='plts'?'PLTS':({
    campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck'}[S.vehicleType]))+'</span></h2>';
  if(!lines.length){return h+'<div class="warn">Pilih paket konversi atau aktfnkan PLTS dahulu.</div>';}
  const groups={};
  for(const L of lines)(groups[L.group]=groups[L.group]||[]).push(L);
  h+='<h3>Rincian per kelompok</h3><table><thead><tr><th style="text-align:left">Komponen</th><th class="r">Harga</th><th class="r" width="52">Qty</th><th class="r" width="70">Satuan</th><th class="r">Subtotal</th></tr></thead><tbody>';
  for(const gk of ['STRUKTUR','INTERIOR','PERALATAN','PLTS','LISTRIK','PLUMBING','JASA']){
    const g=groups[gk]; if(!g)continue;
    h+='<tr><td colspan="4" style="background:#f8fafc;font-weight:700">'+gk+'</td><td class="r" style="background:#f8fafc;font-weight:700">'+fmt(g.reduce((a,L)=>a+L.subtotal,0))+'</td></tr>';
    for(const L of g){
      h+='<tr><td>'+esc(L.name)+'<div class="mut">'+esc(L.code)+(L.spec?' · '+esc(L.spec):'')+'</div></td>'+
        '<td class="r">'+fmt(L.price)+'</td><td class="r">'+L.qty+'</td><td class="r mut">'+esc(L.unit)+'</td><td class="r">'+fmt(L.subtotal)+'</td></tr>';
    }
  }
  h+='</tbody></table>';
  const adv=S.vehicleType==='plts'?null:advancedBreakdown(S,lines);
  if(adv){
    const a=adv;
    h+='<h3>Penjabaran biaya (radil vendor)</h3>';
    h+=summLine('Material dasar (katalog)',fmt(a.material));
    for(const [k,v] of Object.entries(a.waste.per))if(v.val>0)h+=summLine('Waste '+k+' ('+Math.round(v.pct*100)+'%)','+'+fmt(v.val));
    h+=summLine('Kompleksitas', '<span class="tag">'+a.cx.label+'</span> × '+a.cx.score.toFixed(2));
    if(a.workDays>0)h+=summLine('Tenaga kerja ('+a.workDays+' hari × '+CFG.hoursPerDay+' jam × '+fmt(CFG.laborRate)+'/jam)','+'+fmt(a.labor));
    if(a.vol.amount>0)h+=summLine('Diskon volume ('+a.vol.pct+'%)','−'+fmt(a.vol.amount));
    h+=summLine('Kontingensi ('+a.cont.pct+'% — '+esc(a.cont.reason)+')','+'+fmt(a.cont.amount));
    h+=summLine('Total sebelum PPN',fmt(a.beforeTax),'grand');
    h+=summLine('PPN ('+a.ppnPct+'%)','+'+fmt(a.ppn));
    h+=summLine('Grand total','<b>'+fmt(a.grand)+'</b>','grand');
  } else {
    const t=simpleTotals(lines);
    h+=summLine('Subtotal',fmt(t.subtotal));
    h+=summLine('Margin bengkel ('+t.marginPct+'%)','+'+fmt(t.margin));
    h+=summLine('PPN ('+t.ppnPct+'%)','+'+fmt(t.ppn));
    h+=summLine('Grand total','<b>'+fmt(t.total)+'</b>','grand');
  }
  if(plts){
    h+='<h3>Sistem PLTS terpilih</h3><div class="note">'+esc(plts.pWp)+' Wp ('+plts.pQty+'× '+num(plts.panel.comp.specs,'wp')+' Wp) · '+
      plts.bQty+'× '+plts.bAh+' Ah ≈ '+(plts.batWh/1000).toFixed(1)+' kWh · inverter '+num(plts.inverter.specs,'watts')+' W · MPPT '+num(plts.scc.specs,'amps')+' A</div>';
    const n=optimNotes(plts);
    if(n.length)h+='<h3>Catatan optimasi komponen</h3><div class="note">'+n.map(x=>'• '+esc(x)).join('<br>')+'</div>';
  }
  h+='<p class="mut">Estimasi berlaku 30 hari; harga final diverifikasi admin sebelum penawaran resmi.</p>'+
     '<button class="btn ghost no-print" onclick="window.print()">🖨️ Cetak / simpan PDF</button>';
  return h;
}
function update(){$('#rabOut').innerHTML=rabHtml();updateEst();}

function renderAll(){renderVeh();renderSteps();renderAddons();update();}

function renderCat(){
  const cats=['ALL',...new Set(C.map(c=>c.category))], box=$('#catFilter');
  box.innerHTML='<div class="opt">'+cats.map((c,i)=>'<label><input type="radio" name="cf" value="'+c+'" '+(i===0?'checked':'')+'>'+c+'</label>').join('')+'</div>';
  const draw=()=>{
    const cat=box.querySelector('input[type=radio]:checked')?.value||'ALL', q=$('#catQ').value.toLowerCase();
    $('#catBody').innerHTML=C.filter(c=>(cat==='ALL'||c.category===cat)&&(!q||c.name.toLowerCase().includes(q)||c.code.toLowerCase().includes(q)))
      .map(c=>'<tr><td class="mut">'+esc(c.code)+'</td><td class="r">'+fmt(c.price)+'</td><td class="mut">'+esc(c.unit)+'</td><td>'+esc(c.name)+'</td><td class="mut">'+esc(c.category)+'</td></tr>').join('');
  };
  $('#catQ').oninput=draw; box.onchange=draw; draw();
}

document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
  for(const id of ['conf','apl','cat'])$('#tab-'+id).hidden=(b.dataset.tab!==id);
});

$('#btnPlts').onclick=()=>{
  const e=energyOf({...S,manualDailyWh:S.manualDailyWh,manualPeakW:S.manualPeakW});
  if(e.dailyWh<=0||e.peakW<=0){$('#pltsOut').innerHTML='<div class="warn">Isi minimal 1 alat (unit & jam > 0) atau isi angka manual.</div>';return;}
  const plts=calculatePlts({dailyWh:e.dailyWh,peakW:e.peakW,sunHours:Number($('#sun2').value)||PLTS.sunHours},!!S.optSizing);
  const t=simpleTotals(plts.lines);
  let h='<h2>Hasil & RAB PLTS</h2><div class="note">'+plts.pWp+' Wp ('+plts.pQty+'× '+num(plts.panel.comp.specs,'wp')+' Wp) · '+
    plts.bQty+'× '+plts.bAh+' Ah ≈ '+(plts.batWh/1000).toFixed(1)+' kWh · inverter '+num(plts.inverter.specs,'watts')+' W · MPPT '+num(plts.scc.specs,'amps')+' A</div>';
  h+='<h3>RAB PLTS</h3><table><thead><tr><th style="text-align:left">Item</th><th class="r">Qty (satuan)</th><th class="r">Harga</th><th class="r">Subtotal</th></tr></thead><tbody>';
  for(const L of plts.lines)h+='<tr><td>'+esc(L.name)+'<div class="mut">'+esc(L.spec||L.code)+'</div></td><td class="r">'+L.qty+' '+esc(L.unit)+'</td><td class="r">'+fmt(L.price)+'</td><td class="r">'+fmt(L.subtotal)+'</td></tr>';
  h+='</tbody></table>';
  h+=summLine('Subtotal',fmt(t.subtotal));
  h+=summLine('Margin bengkel ('+t.marginPct+'%)','+'+fmt(t.margin));
  h+=summLine('PPN ('+t.ppnPct+'%)','+'+fmt(t.ppn));
  h+=summLine('Grand total','<b>'+fmt(t.total)+'</b>','grand');
  const n=optimNotes(plts);
  if(n.length)h+='<h3>Catatan optimasi komponen</h3><div class="note">'+n.map(x=>'• '+esc(x)).join('<br>')+'</div>';
  h+='<p class="mut"><button class="btn ghost" onclick="window.print()">🖨️ Cetak / simpan PDF</button></p>';
  $('#pltsOut').innerHTML=h;
};

renderApls('#apls'); renderApls('#apls2');
S.sunIncome=Number(S.sunIncome)||4.5;
bindManual(); renderAll(); renderCat(); updateEst();
</script>
</body>
</html>
"""

html_out = TEMPLATE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
out = ROOT / "index.html"
out.write_text(html_out, encoding="utf-8")
print("wrote", out, len(html_out), "bytes")
