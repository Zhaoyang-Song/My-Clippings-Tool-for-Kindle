@echo off
echo RUNING MyClippingsTool.py
python MyClippingsTool.py
echo search.py run complete

echo RUNING search_main/search.py
cd search_main
python search.py
cd ..
echo search_main/search.py run complete

echo Open the generated local web page
start "" index.html

pause