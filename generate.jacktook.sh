cd ..
zip -r -u -9 -T script.jacktook.rajada.zip script.jacktook.rajada/ \
-x "script.jacktook.rajada/.git/*" \
-x "*.pyc" \
-x "script.jacktook.rajada/scripts/check_provider/*" \
-x "script.jacktook.rajada/addon.xml"

printf "@ script.jacktook.rajada/addon.jacktook.xml\n@=script.jacktook.rajada/addon.xml\n" | zipnote -w script.jacktook.rajada.zip
