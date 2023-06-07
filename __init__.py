from functions import check_files
from interface import main_app


if __name__ == '__main__':
    lang = check_files()
    lang_file = f'Resources\\Languages\\{lang}.yaml'
    main_app(lang_file)
