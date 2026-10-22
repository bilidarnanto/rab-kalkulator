# Patch H: checklist beli alat (langkah-3) -> item RAB dari katalog add-on
import io
p='build.py'
s=io.open(p,encoding='utf-8').read()
fails=[]
def rep(old,new,cnt=1,tag=''):
    global s
    n=s.count(old)
    if n<cnt or (cnt==1 and n!=1): fails.append(tag+'(found %d)'%n); return
    s=s.replace(old,new,cnt)

# 1) CSS chip beli
rep('.gob{margin-top:10px}',
""".gob{margin-top:10px}
.buychk{display:inline-flex;align-items:center;gap:4px;font-size:11.5px;color:var(--bch);border:1px solid var(--acc);border-radius:6px;padding:2px 7px;cursor:pointer;white-space:nowrap;user-select:none}
.buychk input{width:auto;margin:0;cursor:pointer}
.buychk:has(input:checked){background:var(--bch);color:#fff}
body.dark .buychk{color:#8fdca3;border-color:var(--acc)}
body.dark .buychk:has(input:checked){color:#fff}""",1,'css buychk')

# 2) peta pembelian APL -> katalog (per tipe kendaraan, fallback CV)
rep("const A_MAP = Object.fromEntries(C.map(c=>[c.code,c]));",
"""const A_MAP = Object.fromEntries(C.map(c=>[c.code,c]));
/* memetakan alat langkah-3 (beli?) -> komponen katalog yang dijual per tipe kendaraan */
const APL_BUY={
  APL-TV:{CV:'CV-AD-TV',MH:'MH-AD-TV'},
  APL-FRIDGE:{CV:'CV-AD-FRIDGE',MH:'MH-AD-FRIDGE',FT:'FT-AD-REFRIG'},
  APL-PUMP:{CV:'CV-AD-PUMP',FT:'FT-AD-WATER'},
  APL-AC:{CV:'CV-AD-AC',MH:'MH-AD-AC'},
  APL-WATERHEATER:{CV:'CV-AD-WATERHEATER',MH:'MH-AD-WATERHEATER'},
  APL-FREEZER:{FT:'FT-AD-FREEZER'},
  APL-FRYER:{FT:'FT-AD-FRYER'},
  APL-GRILL:{FT:'FT-AD-GRILL'},
  APL-COFFEE:{FT:'FT-AD-COFFEE'},
  APL-REFRIGDISPLAY:{FT:'FT-AD-REFRIG'},
  APL-EXHAUST:{FT:'FT-AD-HOOD'}
};
function buyAdCode(apl,vt){const o=APL_BUY[apl]; if(!o)return null; return o[vt]||o.CV||Object.values(o)[0]||null;}""",1,'APL_BUY map')

# 3) baris alat dapat chip 🛒 + handler
rep("""  for(const a of DATA.appliances){
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
    const cur=S.appliances[code];const o=S.appliances[code]=(cur&&typeof cur==='object')?cur:{qty:0,hours:a.hours};
    const v=Math.max(0,Number(t.value)||0);
    if(q)o.qty=v; else o.hours=v;
    save(); updateEst();
    if(id==='#apls') update();
  };
  box.onchange=e=>update();
}""",
"""  for(const a of DATA.appliances){
    const st=S.appliances[a.code];
    const bcode=S.vehicleType==='plts'?buyAdCode(a.code,'CV'):buyAdCode(a.code,suf(S.vehicleType));
    const buyChip=bcode?'<label class="buychk" title="'+(A_MAP[bcode]?T('🛒 belanja item ini: |🛒 purchase this item: ')+fmt(A_MAP[bcode].price)+' / '+esc(A_MAP[bcode].unit)+' (+'+(a.watts)+' W)':'')+'">'+
      '<input type="checkbox" data-buy="'+a.code+'" '+(st&&st.buy?'checked':'')+'>'+T('🛒 ke RAB|🛒 to RAB')+'</label>':'';
    box.insertAdjacentHTML('beforeend',
      '<div class="apl"><span class="nm">'+esc(tn(a))+buyChip+'</span><span class="w">'+a.watts+' W</span>'+
      '<input type="number" min="0" value="'+(st&&st.qty>0?st.qty:0)+'" data-q="'+a.code+'" title="unit">'+
      '<span class="w">unit ×</span>'+
      '<input type="number" min="0" step="0.5" value="'+(st&&st.hours>0?st.hours:a.hours)+'" data-h="'+a.code+'" title="'+T('jam/hari|hours/day')+'">'+
      '<span class="w">'+T('jam|hrs')+'</span></div>');
  }
  const pick=e=>{
    if(!e.target.matches||!e.target.matches('input'))return;
    const t=e.target, q=t.dataset.q, h=t.dataset.h;
    const code=q||h; if(!code)return;
    const a=DATA.appliances.find(x=>x.code===code);
    const cur=S.appliances[code];const o=S.appliances[code]=(cur&&typeof cur==='object')?cur:{qty:0,hours:a.hours};
    if(t.dataset.buy){o.buy=t.checked;}
    else{const v=Math.max(0,Number(t.value)||0); if(q)o.qty=v; else o.hours=v;}
    save(); updateEst();
    if(id==='#apls') update();
  };
  box.oninput=pick; box.onchange=pick;
}""",1,'renderApls buy chip')

# 4) buildRabLines: cek masukkan belanjaan alat sebagai item PERALATAN
rep("""    for(const a of s.addonCodes)push(a,GRP[A_MAP[a]?.category]??'PERALATAN');
  }""",
"""    for(const a of s.addonCodes)push(a,GRP[A_MAP[a]?.category]??'PERALATAN');
    for(const a of DATA.appliances||[]){const st=s.appliances&&s.appliances[a.code];
      if(st&&st.buy){const code=buyAdCode(a.code,vehicleT(s.vehicleType));if(code&&A_MAP[code])push(code,'PERALATAN',Math.max(1,st.qty||1));}}
  }""",1,'buildRabLines buy')

# vehicleT helper (suf tanpa plts-edge)
rep("const suf=v=>({campervan:'CV',motorhome:'MH',foodtruck:'FT'}[v]||'');",
"""const suf=v=>({campervan:'CV',motorhome:'MH',foodtruck:'FT'}[v]||'');
const vehicleT=v=>({campervan:'CV',motorhome:'MH',foodtruck:'FT'}[v]||'CV');""",1,'vehicleT')

# 5) kotak asumsi: butir bahasa belanja
rep("""'<li>'+T('Daftar alat (langkah 3) bukan biaya: hanya menentukan sizing PLTS. Belanja peralatan (dibayar per unit) dicentang di langkah 2.|The appliance list (step 3) is not a cost: it only sizes the solar system. Equipment purchases (paid per unit) are ticked in step 2.')+'</li>'+""",
"""'<li>'+T('Cara belanja peralatan: centang 🛒 pada baris alat (langkah 3) — diperhitungkan sebagai item PERALATAN dengan harga katalog per unit × jumlah; atau centang add-on di langkah 2.|To purchase equipment: tick 🛒 on the appliance row (step 3) — it is billed as an EQUIPMENT line at catalog price × units; or tick add-ons in step 2.')+'</li>'+""",1,'src bullet update')

io.open(p,'w',encoding='utf-8').write(s)
print('PATCH H WROTE. FAILS:',fails if fails else 'none')
