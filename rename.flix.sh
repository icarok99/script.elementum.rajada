
# code
sed -i 's/script.elementum.rajada/script.flix.rajada/g' burst/update_providers.py
sed -i "s/p_dialog.create('Elementum/p_dialog.create('Flix/g" burst/burst.py

# resources
sed -i 's/script.elementum.rajada/script.flix.rajada/g' resources/settings.xml

sed -i 's/script.elementum.rajada/script.flix.rajada/g' resources/language/*.pot
sed -i 's/script.elementum.rajada/script.flix.rajada/g' resources/language/*/*.po
sed -i 's/Elementum Rajada/Flix Rajada/g' resources/language/*.pot
sed -i 's/Elementum Rajada/Flix Rajada/g' resources/language/*/*.po

