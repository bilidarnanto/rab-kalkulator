# Patch B: plts handler, viability, optimNotes, toasts/CSV/WA
import io
p='build.py'
s=io.open(p,encoding='utf-8').read()
fails=[]
def rep(old,new,cnt=1,tag=''):
    global s
    n=s.count(old)
    if n<cnt or (cnt==1 and n!=1):
        fails.append(tag+'(found '+str(n)+')'); return
    s=s.replace(old,new,cnt)

# --- hasil PLTS ---
rep("""$('#pltsOut').innerHTML='<div class="warn">Isi minimal 1 alat (unit & jam > 0) atau isi angka manual.</div>';""",
    """$('#pltsOut').innerHTML='<div class="warn">'+T('Isi minimal 1 alat (unit & jam > 0) atau isi angka manual.|Fill at least one appliance (units & hours > 0) or use the manual fields.')+'</div>';""",1,'plts warn')
rep("""  let h='<h2>Hasil & RAB PLTS</h2><div class="note">'+plts.pWp+""",
    """  let h='<h2>'+T('Hasil & RAB PLTS|Solar result & RAB')+'</h2><div class="note">'+plts.pWp+""",1,'plts h2')
rep("""h+='<h3>RAB PLTS</h3><table><thead><tr><th style="text-align:left">Item</th><th class="r">Qty (satuan)</th><th class="r">Harga</th><th class="r">Subtotal</th></tr></thead><tbody>';""",
    """h+='<h3>'+T('RAB PLTS|Solar RAB')+'</h3><table><thead><tr><th style="text-align:left">'+T('Item|Item')+'</th><th class="r">'+T('Qty (satuan)|Qty (unit)')+'</th><th class="r">'+T('Harga|Price')+'</th><th class="r">Subtotal</th></tr></thead><tbody>';""",1,'plts tbl')
rep("""if(kgn)h+='<div class="mut" style="margin:8px 0">Berat total komponen: ±'+fmt0(kgn)+' kg (panel+baterai+BOS, belum termasuk rak/mounting tambahan).</div>';""",
    """if(kgn)h+='<div class="mut" style="margin:8px 0">'+T('Berat total komponen: ±|Total component weight: ±')+fmt0(kgn)+T(' kg (panel+baterai+BOS, belum termasuk rak/mounting tambahan).| kg (panels+battery+BOS, excluding extra mounting racks).')+'</div>';""",1,'plts weight')

# --- rabHtml: PLTS note & fallback weight & ringkasan ---
rep("(kgn?' · berat ±'+fmt0(kgn)+' kg':'')", "(kgn?T(' · berat ±| · weight ±')+fmt0(kgn)+' kg':'')",1,'rab plts wg')
rep("""if(kgn)h+='<div class="mut" style="margin:6px 0">Berat komponen (alat+material): ±'+fmt0(kgn)+' kg — belum termasuk bobot dasar kendaraan.</div>';""",
    """if(kgn)h+='<div class="mut" style="margin:6px 0">'+T('Berat komponen (alat+material): ±|Component weight (tools+materials): ±')+fmt0(kgn)+T(' kg — belum termasuk bobot dasar kendaraan.| kg — excluding the base vehicle weight.')+'</div>';""",1,'rab fb wg')
rep("h+=summLine('PPN ('+a.ppnPct+'%)','+'+fmt(a.ppn));", "h+=summLine(T('PPN ('|VAT (')+a.ppnPct+'%)','+'+fmt(a.ppn));",1,'ppn adv')
rep("h+=summLine('PPN ('+t.ppnPct+'%)','+'+fmt(t.ppn));", "h+=summLine(T('PPN ('|VAT (')+t.ppnPct+'%)','+'+fmt(t.ppn));",2,'ppn t')
rep("h+=summLine('Margin bengkel ('+t.marginPct+'%)','+'+fmt(t.margin));", "h+=summLine(T('Margin bengkel (|Workshop margin (')+t.marginPct+'%)','+'+fmt(t.margin));",2,'margin')
rep("h+=summLine('Diskon volume ('+a.vol.pct+'%)','−'+fmt(a.vol.amount));", "h+=summLine(T('Diskon volume (|Volume discount (')+a.vol.pct+'%)','−'+fmt(a.vol.amount));",1,'discount')
rep("h+=summLine('Kontingensi ('+a.cont.pct+'% — '+esc(a.cont.reason)+')','+'+fmt(a.cont.amount));", "h+=summLine(T('Kontingensi ('|Contingency (')+a.cont.pct+'% — '+esc(a.cont.reason)+')','+'+fmt(a.cont.amount));",1,'conting')
rep("h+=summLine('Total sebelum PPN',fmt(a.beforeTax),'grand');", "h+=summLine(T('Total sebelum PPN|Total before VAT'),fmt(a.beforeTax),'grand');",1,'beforeTax')

# --- viabilityHtml ---
rep("""const rows=[
    ['Produksi panel','@sun '+plts.sun+' jam ≈ '+fmt0(prod)+' Wh/hari','vs kebutuhan '+fmt0(plts.dailyWh)+' Wh/hari',prod>=plts.dailyWh],
    ['Cadangan baterai','autonomi '+auto.toFixed(1)+' hari (DoD 80%)','target ≥ 1 hari — sizing standar 2 hari',auto>=1],
    ['Inverter vs beban puncak',fmt0(inv)+' W vs '+fmt0(plts.peakW)+' W','margin '+Math.max(0,Math.round((inv-plts.peakW)/Math.max(1,plts.peakW)*100))+'% (sizing ×1.25)',inv>=plts.peakW],
    ['MPPT vs arus panel',sccA+' A vs '+fmt0(arus)+' A','arus = Wp ÷ '+V+' V × 1.25',sccA>=arus],
  ];""",
"""const rows=[
    [T('Produksi panel|Panel output'),'@sun '+plts.sun+T(' jam ≈ | h ≈ ')+fmt0(prod)+T(' Wh/hari| Wh/day'),T('vs kebutuhan |vs daily demand ')+fmt0(plts.dailyWh)+T(' Wh/hari| Wh/day'),prod>=plts.dailyWh],
    [T('Cadangan baterai|Battery reserve'),'autonomi '+auto.toFixed(1)+T(' hari (DoD 80%)| days of autonomy (DoD 80%)'),T('target ≥ 1 hari — sizing standar 2 hari|target ≥ 1 day — standard sizing uses 2 days'),auto>=1],
    [T('Inverter vs beban puncak|Inverter vs peak load'),fmt0(inv)+' W vs '+fmt0(plts.peakW)+' W',T('margin |margin ')+Math.max(0,Math.round((inv-plts.peakW)/Math.max(1,plts.peakW)*100))+'%'+T(' (sizing ×1.25)| (sizing ×1.25)'),inv>=plts.peakW],
    [T('MPPT vs arus panel|MPPT vs panel current'),sccA+' A vs '+fmt0(arus)+' A',T('arus = Wp ÷ |current = Wp ÷ ')+V+' V × 1.25',sccA>=arus],
  ];""",1,'viab rows')
rep("""let h='<h3>Cek kelayakan sistem</h3><table class="viab"><thead><tr><th style="text-align:left">Aspek</th><th>Hitungan</th><th style="text-align:left">Acuan</th><th style="text-align:right">Status</th></tr></thead><tbody>';""",
    """let h='<h3>'+T('Cek kelayakan sistem|System viability check')+'</h3><table class="viab"><thead><tr><th style="text-align:left">'+T('Aspek|Aspect')+'</th><th>'+T('Hitungan|Calculation')+'</th><th style="text-align:left">'+T('Acuan|Benchmark')+'</th><th style="text-align:right">'+T('Status|Status')+'</th></tr></thead><tbody>';""",1,'viab head')
rep("(r[3]?'OK ✓':'PERIKSA ✗')", "(r[3]?'OK ✓':T('PERIKSA ✗|CHECK ✗'))",1,'viab badge')
rep("""if(rows.some(r=>!r[3]))h+='<div class="warn">Ada aspek berstatus PERIKSA. Naikkan beban/panel/baterai hingga semua OK — atau kirim konfigurasi ini ke admin untuk penyesuaian desain.</div>';""",
    """if(rows.some(r=>!r[3]))h+='<div class="warn">'+T('Ada aspek berstatus PERIKSA. Naikkan beban/panel/baterai hingga semua OK — atau kirim konfigurasi ini ke admin untuk penyesuaian desain.|Some aspects show CHECK. Increase the load/panels/battery until all OK — or send this configuration to the admin for design help.')+'</div>';""",1,'viab warn')

# --- optimNotes ---
rep("""n.push('Indikator Rp/Wp panel: '+fmt(rpWp)+' — unit 450–550 Wp ~Rp5.100/Wp, unit 100 Wp Rp9.500/Wp (2× lipat).');""",
    """n.push(T('Indikator Rp/Wp panel: |Panel price check: ')+fmt(rpWp)+T(' — unit 450–550 Wp ~Rp5.100/Wp, unit 100 Wp Rp9.500/Wp (2× lipat).| — 450–550 Wp panels run ~Rp5,100/Wp vs 100 Wp at Rp9,500/Wp (2× the price).'));""",1,'opt1')
rep("""n.push('Indikator Rp/Wh baterai: '+fmt(rpWh)+' — unit 200–300 Ah paling hemat per kWh.');""",
    """n.push(T('Indikator Rp/Wh baterai: |Battery price check: ')+fmt(rpWh)+T(' — unit 200–300 Ah paling hemat per kWh.| — 200–300 Ah units give the best value per kWh.'));""",1,'opt2')
rep("""n.push('Indikator Rp/W inverter: '+fmt(rpW)+' — jaga beban puncak agar tidak terloncat ke kelas yang lebih besar.');""",
    """n.push(T('Indikator Rp/W inverter: |Inverter price check: ')+fmt(rpW)+T(' — jaga beban puncak agar tidak terloncat ke kelas yang lebih besar.| — keep the peak load below the tier threshold so you stay in this class.'));""",1,'opt3')
rep("""n.push('Indikator Rp/A MPPT: '+fmt(rpA)+' — bila panel dibagi 2 string, 2×30 A sering lebih murah daripada 1×60 A.');""",
    """n.push(T('Indikator Rp/A MPPT: |MPPT price check: ')+fmt(rpA)+T(' — bila panel dibagi 2 string, 2×30 A sering lebih murah daripada 1×60 A.| — if the panels split into 2 strings, 2×30 A is often cheaper than 1×60 A.'));""",1,'opt4')
rep("""n.push('Sizing hemat aktif: '+plts.pQty+'× '+num(spec(plts.panel.comp),'wp')+' Wp ('+fmt(plts.panel.comp.price)+'/unit) — lihat catatan Rp/Wp di atas.');""",
    """n.push(T('Sizing hemat aktif: |Cost-optimized sizing: ')+plts.pQty+'× '+num(spec(plts.panel.comp),'wp')+' Wp ('+fmt(plts.panel.comp.price)+T('/unit) — lihat catatan Rp/Wp di atas.|/unit) — see the Rp/Wp check above.'));""",1,'opt5')
rep("""n.push('Baterai '+plts.bQty+' unit ('+((plts.batWh/1000).toFixed(1))+' kWh) — untuk aplikasi kendaraan pertimbangkan tegangan sistem lebih tinggi (24/48 V) atau kurangi konsumsi listrik malam hari.');""",
    """n.push(T('Baterai |Battery ')+plts.bQty+T(' unit (| unit (')+((plts.batWh/1000).toFixed(1))+T(' kWh) — untuk aplikasi kendaraan pertimbangkan tegangan sistem lebih tinggi (24/48 V) atau kurangi konsumsi listrik malam hari.| kWh) — for vehicles consider a higher system voltage (24/48 V) or cut night-time loads.'));""",1,'opt6')
rep("""n.push('Inverter melebihi 2× beban puncak — elemen beban bisa dilakukan bertahap (stagger) agar inverter lebih kecil.');""",
    """n.push(T('Inverter melebihi 2× beban puncak — elemen beban bisa dilakukan bertahap (stagger) agar inverter lebih kecil.|The inverter exceeds 2× the peak load — staggering loads in stages lets you use a smaller inverter.'));""",1,'opt7')
rep("""n.push('MPPT 30 A cukup — nilai arus: '+plts.scc.code.replace('PLTS-SCC-','')+' A.');""",
    """n.push(T('MPPT 30 A cukup — nilai arus: |MPPT 30 A is enough — computed current: ')+plts.scc.code.replace('PLTS-SCC-','')+' A.');""",1,'opt8')

# --- toasts / alerts / prompts ---
rep("toast('Tidak bisa membuat link')", "toast(T('Tidak bisa membuat link|Cannot create a link'))",1,'t-cant')
rep("done=()=>toast('Link konfigurasi disalin — tempel di WhatsApp/chat')", "done=()=>toast(T('Link konfigurasi disalin — tempel di WhatsApp/chat|Config link copied — paste it in WhatsApp/chat'))",1,'t-copied')
rep("window.prompt('Salin link konfigurasi ini:',link)", "window.prompt(T('Salin link konfigurasi ini:|Copy this configuration link:'),link)",1,'p-cfg')
rep("alert('Susun dulu paket / add-on / kebutuhan listrik.');return;}", "alert(T('Susun dulu paket / add-on / kebutuhan listrik.|Build a package / add-on / power needs first.'));return;}",1,'a-csv')
rep("alert('Susun dulu paket / add-on / kebutuhan listrik, lalu kirim.');return;}", "alert(T('Susun dulu paket / add-on / kebutuhan listrik, lalu kirim.|Build a package / add-on / power needs first, then send.'));return;}",1,'a-wa')
rep("toast('CSV RAB terunduh ✓')", "toast(T('CSV RAB terunduh ✓|RAB CSV downloaded ✓'))",1,'t-csv')

# --- CSV headers & rows ---
rep("""const rows=[row('Komponen','Kode','Kelompok','Qty','Satuan','Harga','Subtotal')];""",
    """const rows=[row(T('Komponen|Component'),T('Kode|Code'),T('Kelompok|Group'),'Qty',T('Satuan|Unit'),T('Harga|Price'),'Subtotal')];""",1,'csv hdr')
rep("""rows.push(row('Limbah material ±'+adv.waste.avg+'%','','','','','',adv.waste.total));""",
    """rows.push(row(T('Limbah material ±|Material waste ±')+adv.waste.avg+'%','','','','','',adv.waste.total));""",1,'csv waste')
rep("""if(adv.workDays>0)rows.push(row('Tenaga kerja ('+adv.workDays+' hari × '+CFG.hoursPerDay+' jam × '+CFG.laborRate+' /jam)','','',adv.workDays+' hari','','',adv.labor));""",
    """if(adv.workDays>0)rows.push(row(T('Tenaga kerja (|Labor (')+adv.workDays+T(' hari × | d × ')+CFG.hoursPerDay+T(' jam × | h × ')+CFG.laborRate+T(' /jam)| /hr'),'','',adv.workDays+T(' hari| d'),'','',adv.labor));""",1,'csv labor')
rep("""rows.push(row('Kompleksitas: '+adv.cx.label+' (×'+adv.cx.score.toFixed(2)+')'));""",
    """rows.push(row(T('Kompleksitas: |Complexity: ')+adv.cx.label+' (×'+adv.cx.score.toFixed(2)+')'));""",1,'csv cx')
rep("""rows.push(row('Diskon volume ('+adv.vol.pct+'%)','','','','','',-adv.vol.amount));""",
    """rows.push(row(T('Diskon volume (|Volume discount (')+adv.vol.pct+'%)','','','','','',-adv.vol.amount));""",1,'csv vol')
rep("""rows.push(row('Kontingensi '+adv.cont.pct+'% — '+adv.cont.reason,'','','','','',adv.cont.amount));""",
    """rows.push(row(T('Kontingensi |Contingency ')+adv.cont.pct+'% — '+adv.cont.reason,'','','','','',adv.cont.amount));""",1,'csv cont')
rep("""rows.push(row('PPN '+adv.ppnPct+'%','','','','','',adv.ppn));""",
    """rows.push(row(T('PPN |VAT ')+adv.ppnPct+'%','','','','','',adv.ppn));""",1,'csv ppn')
rep("""rows.push(row('Margin bengkel '+t.marginPct+'%','','','','','',t.margin));""",
    """rows.push(row(T('Margin bengkel |Workshop margin ')+t.marginPct+'%','','','','','',t.margin));""",1,'csv margin')
rep("""rows.push(row('PPN '+t.ppnPct+'%','','','','','',t.ppn));""",
    """rows.push(row(T('PPN |VAT ')+t.ppnPct+'%','','','','','',t.ppn));""",1,'csv ppn2')

# --- WA payload ---
rep("let msg='Halo EcoPower ID, saya baru memakai kalkulator RAB online.'",
    "let msg=T('Halo EcoPower ID, saya baru memakai kalkulator RAB online.|Hi EcoPower ID, I just used your online RAB calculator.')",1,'wa greet')
rep(r"if(L)msg+='\n\nLink konfigurasi (bisa dibuka & diedit lagi): '+L;}",
    r"if(L)msg+='\n\n'+T('Link konfigurasi (bisa dibuka & diedit lagi): |Config link (open & edit it again here): ')+L;}",1,'wa link')
rep(r"msg+='\nMohon info harga final & jadwal produksinya. Terima kasih.';",
    r"msg+='\n'+T('Mohon info harga final & jadwal produksinya. Terima kasih.|Please send the final pricing & production schedule. Thank you.');",1,'wa close')
rep("S.packageCode?'Paket: '+nm(S.packageCode):''", "S.packageCode?T('Paket: |Package: ')+nm(S.packageCode):''",1,'wa pkg')
rep("'Tipe: '+jenis", "T('Tipe: |Type: ')+jenis",1,'wa tipe')
rep("akt.push('Estimasi grand total: '+fmt(tot)+' (berlaku 30 hari)');",
    "akt.push(T('Estimasi grand total: |Estimated grand total: ')+fmt(tot)+T(' (berlaku 30 hari)| (valid for 30 days)'));",1,'wa tot')

s=io.open(p,'w',encoding='utf-8').write(s)
print('PATCH B WROTE. FAILS:', fails if fails else 'none')
