# Patch J: audit — anti-duplikasi add-on vs checklist, keselamatan PV/campervan
import io
p='build.py'
s=io.open(p,encoding='utf-8').read()
fails=[]
def rep(old,new,cnt=1,tag=''):
    global s
    n=s.count(old)
    if n<cnt or (cnt==1 and n!=1): fails.append(tag+'(found %d)'%n); return
    s=s.replace(old,new,cnt)

# ---------- 1) push engine: gabung baris kode sama (anti-duplikasi add-on + chip) ----------
rep("""  const push=(code,group,q=1)=>{const c=A_MAP[code];if(!c)return;i++;lines.push({...c,group,qty:q,subtotal:Math.round(q*c.price)});};""",
"""  const push=(code,group,q=1)=>{const c=A_MAP[code];if(!c)return;
    const ex=lines.find(x=>x.code===code&&x.group===group&&x.group!=='JASA');
    if(ex){ex.qty+=q;ex.subtotal=Math.round(ex.qty*ex.price);return;}   /* anti-duplikasi: add-on langkah-2 + chip langkah-3 digabung, qty dijumlah */
    i++;lines.push({...c,group,qty:q,subtotal:Math.round(q*c.price)});};""",1,'push dedupe')

# ---------- 2) BOS PLTS: fuse dinamis + spec proteksi sesuai standar ----------
rep("""  add(A_MAP['PLTS-BOS-DC'],'kabel DC 6 mm² — 3/baris panel + 2/unit baterai',null,3*pQty+2*bat.qty);""",
"""  add(A_MAP['PLTS-BOS-DC'],'kabel DC 6 mm² (sisi charge) — 3/baris panel + 2/unit baterai; kabel inverter disesuaikan arus & panjang saat instalasi (drop <3%)',null,3*pQty+2*bat.qty);""",1,'BOS DC spec')
rep("""  for(const k of ['PLTS-BOS-FUSE','PLTS-BOS-DCBRK','PLTS-BOS-ACBRK','PLTS-BOS-BUSBAR','PLTS-BOS-GND','PLTS-BOS-MOUNT','PLTS-BOS-JBOX']){
    const c=A_MAP[k]; if(c) lines.push({...c,spec:'',qty:1,subtotal:Math.round(c.price)});
  }""",
"""  { /* proteksi sesuai standar: fuse string bila >2 string paralel (NEC 690), fuse utama baterai dekat baterai */
    const sf=Math.max(0,pQty-2);
    for(const k of ['PLTS-BOS-FUSE','PLTS-BOS-DCBRK','PLTS-BOS-ACBRK','PLTS-BOS-BUSBAR','PLTS-BOS-GND','PLTS-BOS-MOUNT','PLTS-BOS-JBOX']){
      const c=A_MAP[k]; if(!c)continue;
      let sp='',q=1;
      if(k==='PLTS-BOS-FUSE'){q=1+sf;
        sp=(sf>0?sf+'× fuse string PV (paralel >2 string) + ':'')+'fuse utama baterai — ≤0,5 m dari baterai, rating ≥1,25× arus inverter (dipasang petugas)';}
      if(k==='PLTS-BOS-DCBRK')sp='breaker DC sisi panel (proteksi input MPPT)';
      if(k==='PLTS-BOS-ACBRK')sp='breaker AC keluaran inverter';
      if(k==='PLTS-BOS-GND')sp='grounding bodi kendaraan & sistem DC (negatif ter-grounding satu titik)';
      lines.push({...c,spec:sp,qty:q,subtotal:Math.round(q*c.price)});
    }
  }""",1,'BOS proteksi')

# ---------- 3) optimNotes: tips 24V utk inverter besar (arus baterai besar = bahaya) ----------
rep("""  if(plts.inverter&&num(spec(plts.inverter),'watts')>2.2*plts.peakW)""",
"""  if(plts.inverter&&num(spec(plts.inverter),'watts')>=2000)
    n.push(T('⚠️ Keselamatan: inverter ≥2000 W pada sistem 12 V menarik arus baterai >170 A — untuk sistem ukuran ini pertimbangkan tegangan 24 V (kabel & fuse lebih kecil, efisiensi naik); konfigurasi 24 V ditawarkan admin.|⚠️ Safety: a ≥2000 W inverter on 12 V draws >170 A from the battery — for this size consider a 24 V system (smaller cables & fuses, better efficiency); the admin can quote a 24 V configuration.'));
  if(plts.inverter&&num(spec(plts.inverter),'watts')>2.2*plts.peakW)""",1,'24V tip')

# ---------- 4) kotak keselamatan & peringatan duplikasi di rabHtml ----------
rep("""  const pend=lines.filter(L=>L.pending);""",
"""  const pend=lines.filter(L=>L.pending);
  const dups=(DATA.appliances||[]).filter(a=>{const st=S.appliances&&S.appliances[a.code];
    if(!st||!st.buy)return false;const bc=buyAdCode(a.code,vehicleT(S.vehicleType));
    return bc&&(S.addonCodes||[]).includes(bc);});
  if(dups.length)h+='<p class="mut mini">'+T('⚠️ '+dups.map(a=>tn(a)).join(', ')+': tercentang di add-on (langkah 2) DAN checklist 🛒 (langkah 3) — otomatis digabung jadi satu baris, jumlah unit dijumlah (tidak ditagih dua kali).|⚠️ '+dups.map(a=>tn(a)).join(', ')+': ticked both as add-on (step 2) and checklist 🛒 (step 3) — merged into one line with combined quantity (never billed twice).')+'</p>';""",1,'dup warn')

# ---------- 5) blok "Keselamatan & standar pemasangan" ----------
rep("""document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{""",
"""function safetyHtml(){
  const it=[
   T('Fuse utama baterai ≤0,5 m dari baterai, rating ≥1,25× arus inverter; fuse string PLTS wajib bila >2 string paralel.|Main battery fuse ≤0,5 m from the battery, rated ≥1.25× inverter current; PV string fuses are mandatory when >2 parallel strings.'),
   T('MCB/fuse per sirkuit 12 V pada panel distribusi (penerangan, pompa, port USB, dsb).|One MCB/fuse per 12 V circuit on the distribution board (lighting, pump, USB etc).'),
   T('Kabel mengikuti arus & panjang (drop tegangan <3%); kabel inverter disesuaikan — ≥2000 W disarankan sistem 24 V.|Cables sized to current and length (voltage drop <3%); inverter cables upgraded as needed — ≥2000 W motors a 24 V system.'),
   T('Locker gas: ventilasi atas & bawah + drain hole, regulator & selang ber-SNI; APAR 2 kg dan detektor CO/asap dipasang bersamaan (harga konfirmasi admin).|Gas locker: top & bottom vents plus drain hole, SNI regulator & hose; a 2 kg fire extinguisher and CO/smoke detectors are fitted too (price confirmed by the admin).'),
   T('Terminal & konektor MC4 rusuk/torque benar, terlindung dari gesekan; bodi kendaraan di-grounding satu titik untuk sistem DC.|Terminals & MC4 connectors correctly crimped/torqued, protected from chafing; vehicle body grounded at one point for the DC system.'),
   T('Peralatan listrik dipasang teknisi berpengalaman; komponen yang dipakai dari katalog ber-SNI/kualitas industri.|Electrical work is done by experienced technicians; components come from the SNI/industrial-grade catalog.')];
  return '<details class="src"><summary>⚠️ '+T('Keselamatan & standar pemasangan (dipasang bengkel)|Safety & installation standards (workshop practice)')+'</summary><ul>'+it.map(x=>'<li>'+x+'</li>').join('')+'</ul></details>';
}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{""",1,'safetyHtml fn')
rep("""h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+sowHtml(S,lines,adv,plts);""",
"""h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+sowHtml(S,lines,adv,plts)+safetyHtml();""",1,'safety in rab')
rep("""h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+sowHtml({vehicleType:'plts'},plts.lines,null,plts);""",
"""h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+sowHtml({vehicleType:'plts'},plts.lines,null,plts)+safetyHtml();""",1,'safety in plts')

# ---------- 6) waText: belanja alat tidak diulang dgn add-on ----------
rep("""  const buys=(DATA.appliances||[]).filter(a=>{const st=S.appliances[a.code];return st&&st.buy;});""",
"""  const buys=(DATA.appliances||[]).filter(a=>{const st=S.appliances[a.code];if(!st||!st.buy)return false;
    const bc=buyAdCode(a.code,vehicleT(S.vehicleType));return !(bc&&(S.addonCodes||[]).includes(bc));});""",1,'wa no dup buys')

io.open(p,'w',encoding='utf-8').write(s)
print('PATCH J WROTE. FAILS:',fails if fails else 'none')
