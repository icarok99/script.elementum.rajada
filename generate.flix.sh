cd ..
zip -r -u -9 -T script.flix.rajada-0.5.zip script.flix.rajada/ \
-x "script.flix.rajada/.git/*" \
-x "*.pyc" \
-x "script.flix.rajada/scripts/check_provider/*" \
-x "script.flix.rajada/addon.xml"

printf "@ script.flix.rajada/addon.flix.xml\n@=script.flix.rajada/addon.xml\n" | zipnote -w script.flix.rajada-0.5.zip
