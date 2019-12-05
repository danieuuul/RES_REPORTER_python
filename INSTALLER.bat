@echo off

cd px
start px.exe
px.exe --proxy=inet-rj.petrobras.com.br:804 --save
px --install 

set /p chave="DIGITE SUA CHAVE: "

SET origfile= px.ini
SET tempfile= temp.ini
SET insertbefore=10
FOR /F %%C IN ('FIND /C /V "" ^<%origfile%') DO SET totallines=%%C

<%origfile% (FOR /L %%i IN (1,1,%totallines%) DO (
  SETLOCAL EnableDelayedExpansion
  SET /P L=
  IF %%i==%insertbefore% ECHO username = %chave%
  ECHO(!L!
  ENDLOCAL
)
) >%tempfile%
COPY /Y %tempfile% %origfile% >NUL
DEL %tempfile%

taskkill /f /im px.exe
start px.exe

pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install --upgrade pip
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install PyQt5
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install sip
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install h5py
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install xarray
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install plotly
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install seaborn==0.9.0
pip --proxy http://127.0.0.1:3128 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install openpyxl

taskkill /f /im px.exe

