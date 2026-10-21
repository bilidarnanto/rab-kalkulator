import re,html,glob,os,sys
def text(f):
    s=open(f,encoding='utf-8',errors='ignore').read()
    s=re.sub(r'<script[^>]*>.*?</script>','',s,flags=re.S)
    s=re.sub(r'<style[^>]*>.*?</style>','',s,flags=re.S)
    # keep line-ish breaks between result entries
    s=re.sub(r'</(a|div|h[1-6]|li|td|tr)>','\n',s)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t]+',' ',s)
    return s
for f in sorted(glob.glob('*.html')):
    if os.path.getsize(f)>150000:
        t=text(f).replace('\n',' ~ ')
        m=re.findall(r'Rp[\s._0-9,/// ]{2,18}(?=\s|$|—|-)',t)
        m=[re.sub(r'\s+','',x) for x in m]
        m=[x for x in m if re.search(r'[0-9]{3,}',x)]
        # dedupe preserving order
        seen=set(); out=[]
        for x in m:
            if x not in seen: seen.add(x); out.append(x)
        print('##',f,'->',', '.join(out[:45]))
