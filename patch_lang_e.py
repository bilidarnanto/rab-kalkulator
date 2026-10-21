# Patch E: nama katalog EN (nameEn dari API referensi) + nama alat EN
import io
p='build.py'
s=io.open(p,encoding='utf-8').read()
fails=[]
def rep(old,new,cnt=1,tag=''):
    global s
    n=s.count(old)
    if n<cnt or (cnt==1 and n!=1): fails.append(tag+'(found %d)'%n); return
    s=s.replace(old,new,cnt)

# 1) DATA components: sertakan nameEn
rep(('"code": c["code"], "name": c["nameId"], "category": c["category"],',
     '"code": c["code"], "name": c["nameId"], "nameEn": c.get("nameEn") or "", "category": c["category"],'),None,None,'x') if False else None

old='''        {
            "code": c["code"], "name": c["nameId"], "category": c["category"],
            "unit": c["unit"], "price": c["price"], "specs": c.get("specs") or {},'''
new='''        {
            "code": c["code"], "name": c["nameId"], "nameEn": c.get("nameEn") or "", "category": c["category"],
            "unit": c["unit"], "price": c["price"], "specs": c.get("specs") or {},'''
rep(old,new,1,'DATA nameEn')

# 2) appliances: kamus EN + nameEn di DATA
ap=io.open(p,encoding='utf-8').read()
rep('''    "appliances": [{"code": a, "name": n, "watts": w, "hours": h} for (a, n, w, h) in APPLIANCES],''',
'''    "appliances": [{"code": a, "name": n, "nameEn": AP_EN.get(a, n), "watts": w, "hours": h} for (a, n, w, h) in APPLIANCES],''',1,'DATA apl')
rep('''DATA = {''',
'''AP_EN = {
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

DATA = {''',1,'AP_EN dict')

# 3) JS mapper tn() — setelah blok bahasa
rep("function T(p){const i=p.indexOf('|');return LANG==='en'&&i>=0?p.slice(i+1):p.slice(0,i<0?p.length:i);}",
"""function T(p){const i=p.indexOf('|');return LANG==='en'&&i>=0?p.slice(i+1):p.slice(0,i<0?p.length:i);}
/* ---- nama katalog EN (nameId → nameEn dari API referensi) ---- */
const _EN={};(DATA.components||[]).forEach(c=>{if(c.nameEn)_EN[c.name]=c.nameEn;});
(DATA.appliances||[]).forEach(a=>{if(a.nameEn)_EN[a.name]=a.nameEn;});
function tn(x){if(LANG!=='en')return typeof x==='object'?(x.name||''):x;
  if(typeof x==='object')return x.nameEn||x.name||'';
  return _EN[x]||x;}""",1,'tn mapper')

# 4) titik render
rep("'+esc(c.name)+' — '+fmt(c.price)+'", "'+esc(tn(c))+' — '+fmt(c.price)+'",1,'opt select')
rep("""'<div><b>'+esc(c.name)+'</b><div class="mut">'+fmt(c.price)+' / '+esc(c.unit)""",
    """'<div><b>'+esc(tn(c))+'</b><div class="mut">'+fmt(c.price)+' / '+esc(c.unit)""",1,'addon card')
rep("""'<span class="nm">'+esc(a.name)+'</span>""", """'<span class="nm">'+esc(tn(a))+'</span>""",1,'apl name')
rep("h+='<tr><td>'+esc(L.name)+'<div class=\"mut\">'+esc(L.code)", "h+='<tr><td>'+esc(tn(L.name))+'<div class=\"mut\">'+esc(L.code)",1,'rab line')
rep("(!q||c.name.toLowerCase().includes(q)||c.code.toLowerCase().includes(q))",
    "(!q||c.name.toLowerCase().includes(q)||(c.nameEn||'').toLowerCase().includes(q)||c.code.toLowerCase().includes(q))",1,'cat filter')
rep("'</td><td>'+esc(c.name)+'</td><td class=\"mut\">'+esc(c.category)", "'</td><td>'+esc(tn(c))+'</td><td class=\"mut\">'+esc(c.category)",1,'cat name cell')
rep("'<tr><td>'+esc(L.name)+'<div class=\"mut\">'+esc(L.spec||L.code)", "'<tr><td>'+esc(tn(L.name))+'<div class=\"mut\">'+esc(L.spec||L.code)",1,'plts line')
rep("rows.push(row(L.name,L.code,", "rows.push(row(tn(L.name),L.code,",1,'csv line')
rep(".map(L=>L.name);", ".map(L=>tn(L.name));",1,'sow join')
rep("const pk=S.packageCode&&A_MAP[S.packageCode]?A_MAP[S.packageCode].name:'';",
    "const pk=S.packageCode&&A_MAP[S.packageCode]?tn(A_MAP[S.packageCode])::'';",1,'snap pk') if False else None
rep("const pk=S.packageCode&&A_MAP[S.packageCode]?A_MAP[S.packageCode].name:'';",
    "const pk=S.packageCode&&A_MAP[S.packageCode]?tn(A_MAP[S.packageCode]):'';",1,'snap pk')
rep("?esc(A_MAP[e.pkg].name):(e.veh==='plts'", "?esc(tn(A_MAP[e.pkg])):(e.veh==='plts'",1,'banding pkg')
rep("const nm=c=>A_MAP[c]?A_MAP[c].name:c;", "const nm=c=>A_MAP[c]?tn(A_MAP[c]):c;",1,'nm wa')

# gimana: baris 'row(tn(L.name)' sudah; sekarang tulis
s=io.open(p,'w',encoding='utf-8').write(s)
print('PATCH E WROTE. FAILS:', fails if fails else 'none')
