import re,html,sys,os
def load(f):
    s=open(f,encoding='utf-8',errors='ignore').read()
    s=re.sub(r'<script[^>]*>.*?</script>','',s,flags=re.S)
    s=re.sub(r'<style[^>]*>.*?</style>','',s,flags=re.S)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s); s=re.sub(r'\s+',' ',s)
    return s
for f in sys.argv[1:]:
    if not os.path.exists(f) or os.path.getsize(f)<5000:
        print(f'== {f} SKIP(size {os.path.getsize(f) if os.path.exists(f) else 0})'); continue
    s=load(f); seen=set()
    for m in re.finditer(r'Rp[0-9][0-9., ]{2,20}',s):
        h=re.sub(r'\s+',' ',m.group(0)).strip()
        if not re.search(r'[0-9]{3}',h) or h in seen: continue
        seen.add(h)
        pre=s[max(0,m.start()-90):m.start()].strip()[-80:]
        post=s[m.end():m.end()+55].strip()
        print(f'{f} | {h} || ...{pre}> {post}')
