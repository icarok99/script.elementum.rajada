
# code
sed -i 's/script.jacktook.rajada/script.elementum.rajada/g' burst/update_providers.py
sed -i "s/p_dialog.create('Jacktook/p_dialog.create('Elementum/g" burst/burst.py

# resources
sed -i 's/script.jacktook.rajada/script.elementum.rajada/g' resources/settings.xml

sed -i 's/script.jacktook.rajada/script.elementum.rajada/g' resources/language/*.pot
sed -i 's/script.jacktook.rajada/script.elementum.rajada/g' resources/language/*/*.po
sed -i 's/Jacktook Rajada/Elementum Rajada/g' resources/language/*.pot
sed -i 's/Jacktook Rajada/Elementum Rajada/g' resources/language/*/*.po


