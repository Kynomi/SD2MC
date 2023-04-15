IF NOT EXIST venv (python3 -m venv venv/
cd venv\scripts
call activate.bat
cd ../..
pip3 install PyYAML
python main.py
) ELSE (
cd venv\scripts
call activate.bat
cd ../..
python main.py
)
