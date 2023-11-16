IF NOT EXIST venv (python -m venv venv/
cd venv\scripts
call activate.bat
cd ../..
pip install PyYAML
pip install dearpygui
python __init__.py
) ELSE (
cd venv\scripts
call activate.bat
cd ../..
python __init__.py
)