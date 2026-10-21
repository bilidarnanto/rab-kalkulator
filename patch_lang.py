# Patch A: LANG/T helper, dark CSS, boot control, UI strings (non-SOW)
import io
p='build.py'
s=io.open(p,encoding='utf-8').read()
fails=[]
def rep(old,new,cnt=1,tag=''):
    global s
    if old not in s:
        fails.append(tag); return
    s=s.replace(old,new if cnt==1 else new,cnt)

# 1 helper LANG & T
rep("/* ===== WhatsApp admin ===== */",
"""/* ===== bahasa & dark mode ===== */
const LANG=(location.search.match(/[?&]lang=(en|id)\\b/)||[])[1]||(function(){try{return localStorage.getItem('rab.lang')||'id';}catch(e){return 'id';}})();
function T(p){const i=p.indexOf('|');return LANG==='en'&&i>=0?p.slice(i+1):p.slice(0,i<0?p.length:i);}

/* ===== WhatsApp admin ===== */""",1,'T helper')

# 2 CSS dark + tombol header
rep('.only-print{display:none}',
""".lang{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:8px;font-size:12.5px;padding:6px 10px;cursor:pointer}
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
.only-print{display:none}""",1,'css dark')

# 3 warna header grup via class gw + terjemahan
rep("""h+='<tr><td colspan="4" style="background:#f8fafc;font-weight:700">'+gk+'</td><td class="r" style="background:#f8fafc;font-weight:700">'+fmt(g.reduce((a,L)=>a+L.subtotal,0))+'</td></tr>';""",
"""const gkT=({STRUKTUR:'Struktur|Structure',INTERIOR:'Interior',PERALATAN:'Peralatan|Equipment',PLTS:'PLTS',LISTRIK:'Listrik|Electrical',PLUMBING:'Plumbing',JASA:'Jasa|Services'})[gk]||gk;
    h+='<tr><td colspan="4" class="gw" style="font-weight:700">'+T(gkT)+'</td><td class="r" style="font-weight:700">'+fmt(g.reduce((a,L)=>a+L.subtotal,0))+'</td></tr>';""",1,'group hdr')

# 4 boot dark/lang
rep('bindManual(); renderAll(); renderCat(); updateEst(); renderRiwayat();',
"""bindManual(); renderAll(); renderCat(); updateEst(); renderRiwayat();
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
}catch(e){}})();""",1,'boot dark/lang')

# 5 VEH + renderVeh
rep("d:'van konversi 1–4 orang'", "d:'van konversi 1–4 orang|1–4 seater van conversion'",1,'veh1')
rep("d:'rumah berjalan 4–8 orang'", "d:'rumah berjalan 4–8 orang|rolling home for 4–8 people'",1,'veh2')
rep("d:'dapur di atas roda'", "d:'dapur di atas roda|kitchen on wheels'",1,'veh3')
rep("d:'tanpa paket kendaraan'", "d:'tanpa paket kendaraan|no vehicle package'",1,'veh4')
rep("nm:'☀️ PLTS (rumah/lainnya)'", "nm:'☀️ PLTS (rumah/lainnya)|☀️ Solar system (home/other)'",1,'veh5')
rep("""lab.innerHTML='<input type="radio" name="veh" value="'+v.id+'" '+(S.vehicleType===v.id?'checked':'')+'> '+v.nm;
    lab.title=v.d;""","""lab.innerHTML='<input type="radio" name="veh" value="'+v.id+'" '+(S.vehicleType===v.id?'checked':'')+'> '+T(v.nm);
    lab.title=T(v.d);""",1,'renderVeh T')

# 6 fillSelect placeholders
rep("S.packageCode,'— tanpa paket —');", "S.packageCode,T('— tanpa paket —|— no package —'));",1,'ph pkg')
rep("S.layoutCode,'— pilih layout —');", "S.layoutCode,T('— pilih layout —|— choose layout —'));",1,'ph lay')
rep("S.materialCode,'— tanpa finishing —');", "S.materialCode,T('— tanpa finishing —|— no finish —'));",1,'ph mat')

# 7 renderAddons empty texts
rep("""box.innerHTML='<div class="mut">— tidak berlaku untuk mode PLTS —</div>';""",
    """box.innerHTML='<div class="mut">'+T('— tidak berlaku untuk mode PLTS —|— not applicable in solar mode —')+'</div>';""",1,'add1')
rep("""box.innerHTML='<div class="mut">— tidak ada add-on —</div>';""",
    """box.innerHTML='<div class="mut">'+T('— tidak ada add-on —|— no add-ons —')+'</div>';""",1,'add2')

# 8 renderApls title
rep('''data-h="'+a.code+'" title="jam/hari">''', '''data-h="'+a.code+'" title="'+T('jam/hari|hours/day')+'">''',1,'apl jam')
rep("""'<span class="w">jam</span></div>'""", """'<span class="w">'+T('jam|hrs')+'</span></div>'""",1,'apl h')

# 9 updateEst
rep("""const t='Otomatis: '+e.dailyWh.toLocaleString('id-ID')+' Wh/hari · beban puncak '+e.peakW.toLocaleString('id-ID')+' W (ditimpa bila kolom manual diisi).';""",
"""const t=T('Otomatis: |Auto: ')+e.dailyWh.toLocaleString('id-ID')+T(' Wh/hari · beban puncak | Wh/day · peak load ')+e.peakW.toLocaleString('id-ID')+T(' W (ditimpa bila kolom manual diisi).| W (overridden by the manual fields).');""",1,'updateEst')

# 10 rabHtml
rep("""let h='<h2>Rincian RAB <span class="tag mode">""", """let h='<h2>'+T('Rincian RAB |RAB breakdown ')+'<span class="tag mode">""",1,'rab h2')
rep("""return h+'<div class="warn">Pilih paket konversi atau aktifkan PLTS dahulu.</div>';""",
    """return h+'<div class="warn">'+T('Pilih paket konversi atau aktifkan PLTS dahulu.|Choose a conversion package or enable solar first.')+'</div>';""",1,'rab warn')
rep("""h+='<h3>Rincian per kelompok</h3><table><thead><tr><th style="text-align:left">Komponen</th><th class="r">Harga</th><th class="r" width="52">Qty</th><th class="r" width="70">Satuan</th><th class="r">Subtotal</th></tr></thead><tbody>';""",
    """h+='<h3>'+T('Rincian per kelompok|Breakdown by group')+'</h3><table><thead><tr><th style="text-align:left">'+T('Komponen|Component')+'</th><th class="r">'+T('Harga|Price')+'</th><th class="r" width="52">Qty</th><th class="r" width="70">'+T('Satuan|Unit')+'</th><th class="r">Subtotal</th></tr></thead><tbody>';""",1,'rab tbl')
rep("""h+='<h3>Penjabaran biaya (rincian vendor)</h3>';""", """h+='<h3>'+T('Penjabaran biaya (rincian vendor)|Cost derivation (vendor detail)')+'</h3>';""",1,'rab adv h')
rep("summLine('Material dasar (katalog)',fmt(a.material));", "summLine(T('Material dasar (katalog)|Base materials (catalog)'),fmt(a.material));",1,'rab mat')
rep("""summLine('Kompleksitas', '<span class="tag">'+a.cx.label+'</span> × '+a.cx.score.toFixed(2));""",
    """summLine(T('Kompleksitas|Complexity'), '<span class="tag">'+a.cx.label+'</span> × '+a.cx.score.toFixed(2));""",1,'rab cx')
rep("if(a.workDays>0)h+=summLine('Tenaga kerja ('+a.workDays+' hari × '+CFG.hoursPerDay+' jam × '+fmt(CFG.laborRate)+'/jam)','+'+fmt(a.labor));",
    "if(a.workDays>0)h+=summLine(T('Tenaga kerja (|Labor (')+a.workDays+T(' hari × | d × ')+CFG.hoursPerDay+T(' jam × | h × ')+fmt(CFG.laborRate)+T('/jam)|/hr'),'+'+fmt(a.labor));",1,'rab labor')

s=io.open(p,'w',encoding='utf-8').write(s)
print('WROTE. FAILS:', fails if fails else 'none')
