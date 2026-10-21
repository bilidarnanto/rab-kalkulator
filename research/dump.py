import re,html,sys
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8',errors='ignore').read()
    s=re.sub(r'<script[^>]*>.*?</script>','',s,flags=re.S); s=re.sub(r'<style[^>]*>.*?</style>','',s,flags=re.S)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s); s=re.sub(r'\s+',' ',s)
    print('#'*8,f,len(s))
    print(s[:6500])
    print()
