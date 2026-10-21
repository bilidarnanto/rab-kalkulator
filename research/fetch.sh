#!/bin/sh
while IFS='|' read -r slug q; do
  [ -z "$slug" ] && continue
  f="$slug.html"
  if [ ! -s "$f" ] || [ $(stat -c%s "$f") -lt 20000 ]; then
    curl -k -sS -m 60 --retry 1 -A 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0' "https://search.brave.com/search?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")" -o "$f"
    sleep 3
  fi
  echo "$slug $(stat -c%s $f 2>/dev/null)"
done < queries.txt
