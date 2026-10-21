#!/bin/sh
while IFS='|' read -r slug q; do
  [ -z "$slug" ] && continue
  f="$slug.html"
  if [ ! -s "$f" ] || grep -qix 'captcha' "$f" 2>/dev/null; then
    curl -k -sS -m 70 -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36' "https://search.brave.com/search?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")" -o "$f" || true
    sleep 50
  fi
done < q3.txt
echo ALL_DONE
