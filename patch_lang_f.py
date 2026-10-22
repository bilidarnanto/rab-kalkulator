# Patch F: step-by-step UX + accountability (asumsi box, tanggal harga, gate checklist)
import io
p='build.py'
s=io.open(p,encoding='utf-8').read()
fails=[]
def rep(old,new,cnt=1,tag=''):
    global s
    n=s.count(old)
    if n<cnt or (cnt==1 and n!=1): fails.append(tag+'(found %d)'%n); return
    s=s.replace(old,new,cnt)

# ---------- 1) CSS stepper + kotak asumsi ----------
rep('.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}',
""".tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.steps{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}
.sb{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;font-size:12.5px;cursor:pointer;color:#334155}
.sb.ok{border-color:var(--acc);color:var(--bch);background:#eef7ef}
.sb .pop{opacity:.55;font-size:11.5px}
.gob{margin-top:10px}
.src{border:1px dashed var(--line);border-radius:9px;padding:8px 12px;margin:10px 0;background:#fff;font-size:13px}
.src summary{cursor:pointer;font-weight:600;font-size:13px;color:var(--bch)}
.src ul{margin:6px 0 2px 18px;padding:0}
.src li{margin:2px 0;line-height:1.45;font-size:12.5px;color:#475569}
body.dark .sb{background:#122031;border-color:#243449;color:#dbe6f1}
body.dark .sb.ok{background:#15331f;border-color:var(--acc);color:#8fdca3}
body.dark .src{background:#122031;border-color:#243449;color:#dbe6f1}
body.dark .src li{color:#9db1c5}""",1,'css steps')

# ---------- 2) HTML: id kartu + stepBar + tombol lanjut ----------
rep('<div id="tab-conf">', '<div id="tab-conf">\n  <div id="stepBar" class="steps no-print"></div>',1,'stepBar div')
rep('''<section class="card pst">
      <h2 data-tr="1 · Tipe & paket|1 · Type & package">''','''<section class="card pst" id="st1">
      <h2 data-tr="1 · Tipe & paket|1 · Type & package">''',1,'st1 id')
rep('''<section class="card pst">
      <h2 data-tr="2 · Kelengkapan (add-on)|2 · Extras (add-ons)">''','''<section class="card pst" id="st2">
      <h2 data-tr="2 · Kelengkapan (add-on)|2 · Extras (add-ons)">''',1,'st2 id')
rep('''<section class="card pst">
      <h2 data-tr="3 · Kebutuhan listrik harian|3 · Daily power needs">''','''<section class="card pst" id="st3">
      <h2 data-tr="3 · Kebutuhan listrik harian|3 · Daily power needs">''',1,'st3 id')

# tombol lanjut: ujung st1 (setelah chk optSizing)
rep('''        <div class="mut" data-tr="Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.|Find the cheapest unit mix (lowest Rp/Wh & Rp/Wp) that meets the demand.">Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.</div></div></div>
    </section>''','''        <div class="mut" data-tr="Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.|Find the cheapest unit mix (lowest Rp/Wh & Rp/Wp) that meets the demand.">Cari kombinasi unit terhemat (Rp/Wh & Rp/Wp terendah) yang memenuhi kebutuhan.</div></div></div>
      <div class="gob no-print"><button class="btn ghost mini" onclick="goStep('st2')" data-tr="Lanjut ke langkah 2: kelengkapan →|Continue to step 2: extras →">Lanjut ke langkah 2: kelengkapan →</button></div>
    </section>''',1,'gob st1')

# lanjut st2 -> st3
rep('''      <div id="addons"></div>
    </section>''','''      <div id="addons"></div>
      <div class="gob no-print"><button class="btn ghost mini" onclick="goStep('st3')" data-tr="Lanjut ke langkah 3: kebutuhan listrik →|Continue to step 3: power needs →">Lanjut ke langkah 3: kebutuhan listrik →</button></div>
    </section>''',1,'gob st2')

# catatan estimasi + lanjut ke hasil di st3
rep('''      <div id="apls"></div>
      <div class="grid" style="margin-top:10px">''','''      <p class="mut mini" data-tr="Watts & jam pemakaian default = estimasi pemakaian standar bengkel — sesuaikan angka jam dengan kebiasaan Anda, agar estimasi benar-benar pas.|Watts & default hours are standard workshop-use estimates — adjust the hours to your real habits so the estimate truly fits.">Watts & jam pemakaian default = estimasi pemakaian standar bengkel — sesuaikan angka jam dengan kebiasaan Anda, agar estimasi benar-benar pas.</p>
      <div id="apls"></div>
      <div class="grid" style="margin-top:10px">''',1,'st3 note')
rep('''🔄 Reset beban & input manual</button></div>
    </section>''','''🔄 Reset beban & input manual</button></div>
      <div class="gob no-print"><button class="btn ghost mini" onclick="goStep('rabOut')" data-tr="Lihat hasil estimasi RAB ↓|View the RAB estimate ↓">Lihat hasil estimasi RAB ↓</button></div>
    </section>''',1,'gob st3')

# ---------- 3) JS: _upd, goStep, renderStepBar, update() ----------
rep("""const _EN={};(DATA.components||[]).forEach(c=>{if(c.nameEn)_EN[c.name]=c.nameEn;});""",
"""const _EN={};const _upd={};(DATA.components||[]).forEach(c=>{if(c.nameEn)_EN[c.name]=c.nameEn;if(c.updated)_upd[c.code]=String(c.updated).slice(0,10);});""",1,'_upd map')
rep('function update(){$(\'#rabOut\').innerHTML=rabHtml();updateEst();}',
"""function goStep(id){const el=document.getElementById(id);if(el)el.scrollIntoView({behavior:'smooth',block:'start'});}
function renderStepBar(){
  const bar=$('#stepBar'); if(!bar)return;
  const e=energyOf(S);
  const ok1=!!(S.vehicleType==='plts'||(S.packageCode&&A_MAP[S.packageCode]));
  const ok3=e.dailyWh>0;
  const its=[[1,'Tipe & paket|Vehicle & package',ok1,'st1'],
    [2,'Kelengkapan (opsional)|Extras (optional)',S.addonCodes.length>0,'st2'],
    [3,'Kebutuhan listrik|Power needs',ok3,'st3']];
  bar.innerHTML=its.map(it=>'<button class="sb'+(it[2]?' ok':'')+'" onclick="goStep(\\''+it[3]+'\\')">'+
    (it[2]?'✓ ':'● ')+it[0]+'. '+T(it[1])+(it[2]?'':' <span class=\\'pop\\'>'+T('isi duluan|fill this first')+'</span>')+'</button>').join('');
}
function update(){$('#rabOut').innerHTML=rabHtml();updateEst();renderStepBar();}""",1,'renderStepBar+update')

# ---------- 4) rabHtml: gate checklist + kotak dasar perhitungan ----------
rep("""if(!lines.length){return h+'<div class="warn">'+T('Pilih paket konversi atau aktifkan PLTS dahulu.|Choose a conversion package or enable solar first.')+'</div>';}""",
"""if(!lines.length){
    const ok1=!!(S.vehicleType==='plts'||(S.packageCode&&A_MAP[S.packageCode])),ok3=energyOf(S).dailyWh>0;
    return h+'<div class="warn">'+T('Estimasi muncul otomatis setelah 2 langkah ini:|The estimate appears automatically after these 2 steps:')+
      '<div style="margin-top:4px">'+(ok1?'✓':'☐')+T(' Langkah 1: pilih paket konversi (atau tipe & PLTS).| Step 1: pick a conversion package (or vehicle type + solar).')+'</div>'+
      '<div>'+(ok3?'✓':'☐')+T(' Langkah 3: isi jumlah unit & jam pemakaian minimal 1 peralatan (atau total manual).| Step 3: enter units & hours for at least one appliance (or a manual total).')+'</div>'+
      '<div class="mut mini" style="margin-top:4px">'+T('Gunakan tombol “Lanjut ke langkah …” agar urutannya jelas.|Use the “Continue to step …” buttons to keep the order clear.')+'</div></div>';}""",1,'gate checklist')
rep("""  const groups={};
  for(const L of lines)(groups[L.group]=groups[L.group]||[]).push(L);""",
"""  h+='<details class="src"><summary>'+T('📋 Dasar & asumsi perhitungan (bisa diperiksa)|📋 Calculation basis & assumptions (verifiable)')+'</summary><ul>'+
    '<li>'+T('Harga: katalog vendor (Aug 2026) + verifikasi pasar (Okt 2026) — tanggal harga per komponen tertulis di tab Tabel Harga.|Prices: vendor catalog (Aug 2026) + market check (Oct 2026) — per-component price dates are listed in the Price List tab.')+'</li>'+
    '<li>'+T('Tenaga kerja: Rp75.000/jam × 8 jam/hari, jumlah hari mengikuti hari kerja vendor per paket.|Labor: Rp75,000/h × 8 h/day; day counts follow the vendor working-days per package.')+'</li>'+
    '<li>'+T('Limbah material per kelompok: Struktur 12% · Interior 8% · Peralatan 3% · PLTS 2% · Listrik & Pipa 5%.|Material waste per group: Structure 12% · Interior 8% · Equipment 3% · Solar 2% · Electrical & plumbing 5%.')+'</li>'+
    '<li>'+T('Faktor kompleksitas 0,80–1,30 (level custom layout/finishing).|Complexity factor 0.80–1.30 (custom layout/finish level).')+'</li>'+
    '<li>'+T('Diskon volume 3%/2%/1% bila subtotal grup besar; kontingensi 3–10% (besaran disepakati admin sebelum final).|Volume discount 3%/2%/1% on large group subtotals; contingency 3–10% (agreed with the admin before final).')+'</li>'+
    '<li>'+T('PPN 11%; margin bengkel sistem PLTS 15% (mencakup perakitan, pengujian, dan garansi pengerjaan).|VAT 11%; solar-system workshop margin 15% (assembly, testing and workmanship warranty).')+'</li>'+
    '<li>'+T('Estimasi berlaku 30 hari — angka final dikonfirmasi admin EcoPower.|Estimates valid 30 days — final figures are confirmed by the EcoPower admin.')+'</li></ul></details>';
  const groups={};
  for(const L of lines)(groups[L.group]=groups[L.group]||[]).push(L);""",1,'src box')

# ---------- 5) tabel harga: kolom tanggal ----------
rep('<th style="width:96px" data-tr="Kategori|Category">Kategori</th></tr>',
    '<th style="width:96px" data-tr="Kategori|Category">Kategori</th><th class="r" style="width:84px" data-tr="Tgl harga|Price date">Tgl harga</th></tr>',1,'cat th date')
rep("""'</td><td>'+esc(tn(c))+'</td><td class="mut">'+esc(c.category)+'</td></tr>').join('');""",
    """'</td><td>'+esc(tn(c))+'</td><td class="mut">'+esc(c.category)+'</td><td class="mut mini">'+(c.updated?_upd[c.code]||'':'')+'</td></tr>').join('');""",1,'cat td date')

# ---------- 6) DATA sertakan updated ----------
rep('"code": c["code"], "name": c["nameId"], "nameEn": c.get("nameEn") or "", "category": c["category"],',
    '"code": c["code"], "name": c["nameId"], "nameEn": c.get("nameEn") or "", "updated": c.get("priceUpdatedAt") or "", "category": c["category"],',1,'DATA updated')

io.open(p,'w',encoding='utf-8').write(s)
print('PATCH F WROTE. FAILS:', fails if fails else 'none')
