#!/bin/sh
while IFS='|' read -r slug q; do
  [ -z "$slug" ] && continue
  f="$slug.html"
  if [ ! -s "$f" ] || grep -qi 'captcha' "$f" 2>/dev/null; then
    curl -k -sS -m 60 -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36' "https://search.brave.com/search?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")" -o "$f"
    sleep 18
  fi
done < q2.txt
ls -la *.html | head -0
