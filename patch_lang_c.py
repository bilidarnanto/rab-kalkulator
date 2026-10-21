# Patch C: fix B misses + SOW + riwayat/perbandingan
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

# fix viab warn (teks asli berbeda)
rep("""h+='<div class="warn">Ada aspek berstatus PERIKSA. Naikkan beban/panel/baterai hingga semua OK — atau kirim link konfigurasi ini ke admin untuk penyesuaian desain.</div>';""",
    """h+='<div class="warn">'+T('Ada aspek berstatus PERIKSA. Naikkan beban/panel/baterai hingga semua OK — atau kirim link konfigurasi ini ke admin untuk penyesuaian desain.|Some aspects show CHECK. Increase the load/panels/battery until all OK — or send this config link to the admin for design help.')+'</div>';""",1,'viab warn')
# fix a-csv (2 lokasi)
rep("alert('Susun dulu paket / add-on / kebutuhan listrik.');return;}",
    "alert(T('Susun dulu paket / add-on / kebutuhan listrik.|Build a package / add-on / power needs first.'));return;}",2,'a-csv')
# fix wa greet
rep(r"let msg='Halo EcoPower ID, saya baru memakai kalkulator RAB online.\n'",
    r"let msg=T('Halo EcoPower ID, saya baru memakai kalkulator RAB online.|Hi EcoPower ID, I just used your online RAB calculator.')+'\n'",1,'wa greet')

# ---------- SOW ----------
rep("""const scope=[['Desain & persiapan','samakan kebutuhan, pengukuran, sketsa layout sederhana, dan daftar material — kami konfirmasi desain ke Anda sebelum mulai memotong bahan.']];""",
    """const scope=[[T('Desain & persiapan|Design & preparation'),T('samakan kebutuhan, pengukuran, sketsa layout sederhana, dan daftar material — kami konfirmasi desain ke Anda sebelum mulai memotong bahan.|we align on needs, take measurements, sketch a simple layout and draft the materials list — the design is confirmed with you before any cutting starts.')]];""",1,'sow1')
rep("""scope.push(['Struktur & bodi','pembongkaran seperlunya, penguatan rangka, pelapis dinding/lantai ('+join(pkg)+'), anti-bocor & peredam seperlunya.']);""",
    """scope.push([T('Struktur & bodi|Structure & body'),T('pembongkaran seperlunya, penguatan rangka, pelapis dinding/lantai (|as-needed disassembly, frame reinforcement, wall/floor lining (')+join(pkg)+T('), anti-bocor & peredam seperlunya.|), leak-proofing & damping as needed.')]);""",1,'sow2')
rep("""scope.push(['Interior & finishing','fabrikasi furniture, pelapisan/finishing ('+join(int)+') mengikuti gambar yang sudah disetujui.']);""",
    """scope.push([T('Interior & finishing|Interior & finish'),T('fabrikasi furniture, pelapisan/finishing (|fabricated furniture, lining & finishing (')+join(int)+T(') mengikuti gambar yang sudah disetujui.|) following the approved drawing.')]);""",1,'sow3')
rep("""scope.push(['Instalasi kelistrikan kendaraan','titik lampu/saklar, sekuring/MCB, grounding, dan pengujian beban sebelum serah terima.']);""",
    """scope.push([T('Instalasi kelistrikan kendaraan|Vehicle electrical installation'),T('titik lampu/saklar, sekuring/MCB, grounding, dan pengujian beban sebelum serah terima.|light and switch points, circuit breakers/MCB, grounding, and a load test before handover.')]);""",1,'sow4')
rep("""scope.push(['Pemasangan peralatan & aksesori',join(alat)+' — dipasang, disambung, dan diuji fungsinya satu per satu.']);""",
    """scope.push([T('Pemasangan peralatan & aksesori|Equipment & accessory installation'),join(alat)+T(' — dipasang, disambung, dan diuji fungsinya satu per satu.| — mounted, wired and tested one by one.')]);""",1,'sow5')
rep("""scope.push(['Instalasi PLTS / tenaga surya','panel terpasang & kabel rapi, baterai + inverter + MPPT menyala, pengujian pengisian/pemakaian, plus pendampingan cara pakai.']);""",
    """scope.push([T('Instalasi PLTS / tenaga surya|Solar PV installation'),T('panel terpasang & kabel rapi, baterai + inverter + MPPT menyala, pengujian pengisian/pemakaian, plus pendampingan cara pakai.|panels mounted & cabled neatly, battery + inverter + MPPT powered up, charge/load testing, plus usage guidance.')]);""",1,'sow6')
rep("""dur='±2–3 hari kerja instalasi';""", """dur=T('±2–3 hari kerja instalasi|±2–3 days of installation work');""",1,'sow dur1')
rep("""dur='±'+adv.workDays+' hari kerja di bengkel';""", """dur='±'+adv.workDays+T(' hari kerja di bengkel| days of workshop work');""",1,'sow dur2')
rep("""dur='disesuaikan pesanan';""", """dur=T('disesuaikan pesanan|tailored to the order');""",1,'sow dur3')
rep("""const kami=[
    'Dikerjakan sesuai lingkup & material dalam dokumen ini — pembongkaran/pekerjaan di luar itu minta ijin dan persetujuan biaya lebih dahulu (cukup via WhatsApp).',
    'Menyediakan pembaruan progres + foto pada tiap tahap besar kepada WhatsApp Anda.',
    'Garansi pengerjaan 90 hari untuk cacat instalasi; garansi produk mengikuti ketentuan vendor masing-masing.',
    'Serah terima bersih: fungsi diuji bersama Anda, area kerja dibersihkan, cara pemakaian dijelaskan.'];""",
"""const kami=[
    T('Dikerjakan sesuai lingkup & material dalam dokumen ini — pembongkaran/pekerjaan di luar itu minta ijin dan persetujuan biaya lebih dahulu (cukup via WhatsApp).|We build exactly to the scope & materials in this document — any work outside it needs your prior approval and cost agreement (WhatsApp is enough).'),
    T('Menyediakan pembaruan progres + foto pada tiap tahap besar kepada WhatsApp Anda.|We send progress updates + photos to your WhatsApp at every major stage.'),
    T('Garansi pengerjaan 90 hari untuk cacat instalasi; garansi produk mengikuti ketentuan vendor masing-masing.|90-day workmanship warranty for installation defects; product warranty follows each vendor\\'s own terms.'),
    T('Serah terima bersih: fungsi diuji bersama Anda, area kerja dibersihkan, cara pemakaian dijelaskan.|Clean handover: functions tested together, work area cleaned, usage explained.')];""",1,'sow kami')
rep("""const Anda=[
    'Menyampaikan kebutuhan dan perubahan desain sedini mungkin — terlebih sebelum material mulai dipotong.',
    'Menyediakan akses kendaraan/lokasi yang aman selama pengerjaan berlangsung.',
    'Melunasi termin pembayaran sesuai jadwal yang dikonfirmasi admin.',
    'Merawat pekerjaan sesuai panduan yang kami berikan agar garansi tetap berlaku.'];""",
"""const Anda=[
    T('Menyampaikan kebutuhan dan perubahan desain sedini mungkin — terlebih sebelum material mulai dipotong.|Share your needs and design changes early — especially before materials are cut.'),
    T('Menyediakan akses kendaraan/lokasi yang aman selama pengerjaan berlangsung.|Provide safe access to the vehicle/site while the work is in progress.'),
    T('Melunasi termin pembayaran sesuai jadwal yang dikonfirmasi admin.|Settle the payment installments on the schedule confirmed by the admin.'),
    T('Merawat pekerjaan sesuai panduan yang kami berikan agar garansi tetap berlaku.|Maintain the work as per our guidance to keep the warranty valid.')];""",1,'sow anda')
rep("""const luar=[
    'Kerusakan tersembunyi yang baru ketahuan saat pembongkaran (karat, rapuh, bocor lama): kami foto, laporkan, dan lanjut setelah Anda menyetujui biayanya.',
    'Perbaikan wajib/rutin kendaraan (mesin, kelistrikan pabrik mobil).',
    'Kerugian akibat pemakaian tidak sesuai panduan (mis. beban PLTS melebihi daya terpasang).'];""",
"""const luar=[
    T('Kerusakan tersembunyi yang baru ketahuan saat pembongkaran (karat, rapuh, bocor lama): kami foto, laporkan, dan lanjut setelah Anda menyetujui biayanya.|Hidden damage discovered during disassembly (rust, rot, old leaks): we photograph, report, and continue after you approve the cost.'),
    T('Perbaikan wajib/rutin kendaraan (mesin, kelistrikan pabrik mobil).|Mandatory/routine vehicle repairs (engine, factory wiring).'),
    T('Kerugian akibat pemakaian tidak sesuai panduan (mis. beban PLTS melebihi daya terpasang).|Damage from use contrary to our guidance (e.g. solar loads above the installed capacity).')];""",1,'sow luar')
rep("""let h='<div class="sow"><div class="grow"><div><h4>🛠️ Lingkup pekerjaan</h4><ul>'+""",
    """let h='<div class="sow"><div class="grow"><div><h4>'+T('🛠️ Lingkup pekerjaan|🛠️ Scope of work')+'</h4><ul>'+""",1,'sow h4a')
rep("""'</ul><p class="mut">Jangka waktu estimasi: '+esc(dur)+' (belum termasuk lead-time barang, kira-kira 7–14 hari).</p></div>';""",
    """'</ul><p class="mut">'+T('Jangka waktu estimasi: |Estimated duration: ')+esc(dur)+T(' (belum termasuk lead-time barang, kira-kira 7–14 hari).| (excluding material lead time, roughly 7–14 days).')+'</p></div>';""",1,'sow dur p')
rep("""h+='<div><h4>🤝 Komitmen kami (bengkel)</h4><ul>'+kami.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'+
     '<h4>🙏 Hak & kewajiban Anda (konsumen)</h4><ul>'+Anda.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div></div>';""",
    """h+='<div><h4>'+T('🤝 Komitmen kami (bengkel)|🤝 Our commitments (workshop)')+'</h4><ul>'+kami.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'+
     '<h4>'+T('🙏 Hak & kewajiban Anda (konsumen)|🙏 Your rights & duties (customer)')+'</h4><ul>'+Anda.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div></div>';""",1,'sow h4b')
rep("""'<h4>⚠️ Di luar lingkup — selalu beritahu kami dahulu</h4>""", """'<h4>'+T('⚠️ Di luar lingkup — selalu beritahu kami dahulu|⚠️ Out of scope — always tell us first')+'</h4>""",1,'sow h4c')
rep("""'<p class="mut">Estimasi berlaku 30 hari: semua angka & lingkup mengacu pada dokumen ini. Jadwal, termin, dan garansi final dikonfirmasi admin EcoPower sebelum pengerjaan dimulai — konsultasinya gratis.</p></div>';""",
    """'<p class="mut">'+T('Estimasi berlaku 30 hari: semua angka & lingkup mengacu pada dokumen ini. Jadwal, termin, dan garansi final dikonfirmasi admin EcoPower sebelum pengerjaan dimulai — konsultasinya gratis.|Estimate valid for 30 days: all figures & scope follow this document. Final schedule, installments and warranty are confirmed by the EcoPower admin before work starts — the consultation is free.')+'</p></div>';""",1,'sow final')

# ---------- SOW headings wired ----------
rep("""h+='<h3>Lingkup pekerjaan & kesepakatan (SOW)</h3>'+""",
    """h+='<h3>'+T('Lingkup pekerjaan & kesepakatan (SOW)|Scope of work & agreement (SOW)')+'</h3>'+""",2,'sow heading')

# ---------- riwayat & perbandingan ----------
rep("(S.vehicleType==='plts'?'PLTS mandiri':t+(pk?' · '+pk:''))", "(S.vehicleType==='plts'?T('PLTS mandiri|Standalone solar'):t+(pk?' · '+pk:''))",1,'snap label')
rep("const cf=decodeCfg(e.cfg);if(!cf){toast('Snapshot rusak');return;}", "const cf=decodeCfg(e.cfg);if(!cf){toast(T('Snapshot rusak|Broken snapshot'));return;}",1,'hist broken')
rep("toast('Konfigurasi dimuat dari riwayat ✓');", "toast(T('Konfigurasi dimuat dari riwayat ✓|Configuration loaded from history ✓'));",1,'hist load t')
rep("histSave(histLoad().filter(x=>x.id!==id));bandSel.delete(id);renderRiwayat();toast('Entri dihapus');", "histSave(histLoad().filter(x=>x.id!==id));bandSel.delete(id);renderRiwayat();toast(T('Entri dihapus|Entry deleted'));",1,'hist del t')
rep("""const fb=()=>{if(window.prompt('Salin link snapshot:',link))done();};""",
    """const fb=()=>{if(window.prompt(T('Salin link snapshot:|Copy the snapshot link:'),link))done();};""",1,'hist prompt')
rep("const done=()=>toast('Link snapshot disalin ✓');", "const done=()=>toast(T('Link snapshot disalin ✓|Snapshot link copied ✓'));",1,'hist copied t')
rep("else{if(bandSel.size>=3){toast('Bandingkan maksimal 3 penawaran');return;}bandSel.add(id);}", "else{if(bandSel.size>=3){toast(T('Bandingkan maksimal 3 penawaran|Compare up to 3 quotes'));return;}bandSel.add(id);}",1,'hist max3')
rep("""let h='<h3>⚖️ Perbandingan penawaran</h3><table class="cmp"><thead><tr><th style="width:110px">Aspek</th>'+""",
    """let h='<h3>'+T('⚖️ Perbandingan penawaran|⚖️ Quote comparison')+'</h3><table class="cmp"><thead><tr><th style="width:110px">'+T('Aspek|Aspect')+'</th>'+""",1,'banding head')
rep("""    ['Grand total',e=>'<b>'+fmt(e.tot)+'</b>'],
    ['Tipe',e=>esc({campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck',plts:'PLTS mandiri'}[e.veh]||e.veh)],
    ['Paket',e=>e.pkg&&A_MAP[e.pkg]?esc(A_MAP[e.pkg].name):(e.veh==='plts'?'—':'tanpa paket')],
    ['Add-on',e=>e.addons?'+'+e.addons:'—'],
    ['PLTS',e=>e.wp?e.wp+' Wp · '+e.kwh+' kWh':'—'],
    ['Inverter / MPPT',e=>e.wp?e.inv+' W / '+e.scc+' A':'—'],
    ['Tenaga kerja',e=>e.wd?e.wd+' hari kerja':'—'],
    ['Kompleksitas',e=>e.cx?'×'+Number(e.cx).toFixed(2):'—'],
    ['Berat komponen',e=>e.kg?'±'+e.kg+' kg':'—'],
  ];""",
"""    [T('Grand total|Grand total'),e=>'<b>'+fmt(e.tot)+'</b>'],
    [T('Tipe|Type'),e=>esc({campervan:'Campervan',motorhome:'Motorhome',foodtruck:'Food Truck',plts:T('PLTS mandiri|Standalone solar')}[e.veh]||e.veh)],
    [T('Paket|Package'),e=>e.pkg&&A_MAP[e.pkg]?esc(A_MAP[e.pkg].name):(e.veh==='plts'?'—':T('tanpa paket|no package'))],
    ['Add-on',e=>e.addons?'+'+e.addons:'—'],
    ['PLTS',e=>e.wp?e.wp+' Wp · '+e.kwh+' kWh':'—'],
    ['Inverter / MPPT',e=>e.wp?e.inv+' W / '+e.scc+' A':'—'],
    [T('Tenaga kerja|Labor'),e=>e.wd?e.wd+T(' hari kerja| working days'):'—'],
    [T('Kompleksitas|Complexity'),e=>e.cx?'×'+Number(e.cx).toFixed(2):'—'],
    [T('Berat komponen|Weight'),e=>e.kg?'±'+e.kg+' kg':'—'],
  ];""",1,'banding rows')
rep("""'<div class="mut mini">'+(e.wp?e.wp+' Wp · '+e.kwh+' kWh · ':'')+(e.wd?e.wd+' hari kerja · ':'')+'berat ±'+e.kg+' kg</div></div>'+""",
    """'<div class="mut mini">'+(e.wp?e.wp+' Wp · '+e.kwh+' kWh · ':'')+(e.wd?e.wd+T(' hari kerja · | working days · '):'')+T('berat ±|weight ±')+e.kg+' kg</div></div>'+""",1,'hist mini')
rep('>📂 Muat</button>', "'>+T('📂 Muat|📂 Load')+'</button>'",1,'hist muat')
rep("(bandSel.has(e.id)?'✅ Dipilih':'⚖️ Bandingkan')", "(bandSel.has(e.id)?T('✅ Dipilih|✅ Selected'):T('⚖️ Bandingkan|⚖️ Compare'))",1,'hist sel btn')
rep(r"""onclick="if(confirm(\'Hapus entri ini?\'))hapusRiwayat(""", r"""onclick="if(confirm(\''+T('Hapus entri ini?|Delete this entry?')+'\'))hapusRiwayat(""",1,'hist confirm')
rep("""if(!a.length){box.innerHTML='<h2>🗂️ Riwayat penawaran</h2><div class="mut">Belum ada. Tekan tombol “💾 Simpan ke Riwayat” pada hasil RAB — konfigurasi & angkanya bisa dibuka ulang atau dibandingkan kapan pun (maks. 30 entri).</div>';return;}""",
    """if(!a.length){box.innerHTML='<h2>'+T('🗂️ Riwayat penawaran|🗂️ Quote history')+'</h2><div class="mut">'+T('Belum ada. Tekan tombol “💾 Simpan ke Riwayat” pada hasil RAB — konfigurasi & angkanya bisa dibuka ulang atau dibandingkan kapan pun (maks. 30 entri).|Empty so far. Press “Save to History” on the RAB result — the configuration & figures can be reopened or compared any time (max. 30 entries).')+'</div>';return;}""",1,'hist empty')
rep("""let h='<h2>🗂️ Riwayat penawaran</h2>';""", """let h='<h2>'+T('🗂️ Riwayat penawaran|🗂️ Quote history')+'</h2>';""",1,'hist title2')
rep("""if(sel.length>=2)h+=bandingHtml(sel)+'<p class="mut mini">Angka hijau = grand total termurah di antara pilihan.</p>';""",
    """if(sel.length>=2)h+=bandingHtml(sel)+'<p class="mut mini">'+T('Angka hijau = grand total termurah di antara pilihan.|Green = the lowest grand total among the selected quotes.')+'</p>';""",1,'hist guide')

s=io.open(p,'w',encoding='utf-8').write(s)
print('PATCH C WROTE. FAILS:', fails if fails else 'none')
