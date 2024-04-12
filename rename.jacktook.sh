
# code
sed -i 's/script.elementum.rajada/script.jacktook.rajada/g' burst/update_providers.py
sed -i "s/p_dialog.create('Elementum/p_dialog.create('Jacktook/g" burst/burst.py

# resources
sed -i 's/script.elementum.rajada/script.jacktook.rajada/g' resources/settings.xml

sed -i 's/script.elementum.rajada/script.jacktook.rajada/g' resources/language/*.pot
sed -i 's/script.elementum.rajada/script.jacktook.rajada/g' resources/language/*/*.po
sed -i 's/Elementum Rajada/Jacktook Rajada/g' resources/language/*.pot
sed -i 's/Elementum Rajada/Jacktook Rajada/g' resources/language/*/*.po

