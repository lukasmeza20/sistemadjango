python -m pip install --upgrade pip
pip install --upgrade virtualenv
python -m venv "C:\BuenosAires\AppWebBA_venv"
call cd /D "C:\BuenosAires"
call AppWebBA_venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install django
pip install pillow
pip install djangorestframework
pip install transbank-sdk
pip install django-extensions
pip install mssql-django