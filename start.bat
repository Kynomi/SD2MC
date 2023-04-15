IF NOT EXIST venv (python -m venv venv/
cd venv\scripts
call activate.bat
cd ../..
pip install PyYAML
python main.py
) ELSE (
cd venv\scripts
call activate.bat
cd ../..
python main.py
)
