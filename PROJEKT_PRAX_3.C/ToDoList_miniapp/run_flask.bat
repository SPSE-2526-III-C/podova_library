@echo off
echo ==========================================
echo  Spustanie Flask aplikacie (automaticky)
echo ==========================================
echo.
 
:: Presun do priecinka, kde sa nachadza tento subor
cd /d "%~dp0"
 
:: Skontroluj, ci existuje venv, ak nie, vytvor ho
if not exist ".venv" (
    echo Vytvaram virtualne prostredie...
    py -3 -m venv .venv
)
 
:: Aktivuj venv (KRITICKY FIX)
echo Aktivujem virtualne prostredie...
call ".venv\Scripts\activate.bat"
 
:: Aktualizuj pip
echo Aktualizujem pip...
python -m pip install --upgrade pip >nul
 
:: Instaluj balicky, len ak chybaju
echo Kontrolujem potrebne balicky...
pip show flask >nul 2>&1 || pip install flask
pip show flask-wtf >nul 2>&1 || pip install flask-wtf
pip show flask-sqlalchemy >nul 2>&1 || pip install flask-sqlalchemy
 
:: Spusti aplikaciu
echo.
echo ==========================================
echo Spustam Flask aplikaciu...
echo ==========================================
echo.
 
set FLASK_APP=main
set FLASK_DEBUG=1
 
python -m flask run
 
:: Po vypnuti servera deaktivuj venv
deactivate
 
echo.
echo ==========================================
echo Flask server bol ukonceny.
echo Stlac lubovolnu klavesu pre zatvorenie okna.
echo ==========================================
pause