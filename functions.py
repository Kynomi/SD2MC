from os import path, rename, remove, mkdir
import yaml
from shutil import move, rmtree, Error
import winreg
from subprocess import call


def get_properties(*args):
    """Эта функция получает настройки из конфиг файла"""
    with open('config.yaml', 'r') as config:
        data = yaml.safe_load(config)
        properties = []
        for property in args:
            properties.append(data[property])
    return properties


def vpk_parse(vpk_path, export_file_path, output_path, output_name=None):
    """Функция экспортирующая файл из ВПК"""
    if '\\' in export_file_path:
        export_file_path = export_file_path.replace('\\', '/')
    file_name = export_file_path.split('/')[-1]  # Получение названия файла
    output_path = path.abspath(output_path)
    decompiler_path = path.abspath('Decompiler/Decompiler.exe')  # Путь до дикомпилера
    call(f'"{decompiler_path}" -i "{vpk_path}" -f "{export_file_path}" -o "{output_path}"')  # Вызов команды в командной строке для экспорта файла из ВПК
    start_path = path.abspath(output_path + '\\' + export_file_path)  # Стартовый путь нужен для перемещения файла из исходного положения в выходное
    #  Пермещение файла
    try:
        move(start_path, output_path)
    except Error:
        remove(path.relpath(output_path) + '\\' + file_name)
        move(start_path, output_path)
    #  Переименование файла
    if output_name is not None:
        if not output_name.replace(' ', '') == '':
            try:
                rename(output_path + '\\' + file_name, output_path + '\\' + output_name)
            except FileExistsError:
                remove(output_path + '\\' + output_name)
                rename(output_path + '\\' + file_name, output_path + '\\' + output_name)
    # удаление мусора после экспорта
    rmtree_name = output_path + '\\' + export_file_path.split('/')[0]
    if path.exists(rmtree_name):
        rmtree(rmtree_name)


def config_check():
    """Функция проверяющая наличие конфигурационного файла и создающя его,
    Возвращает путь до ВПК"""
    if not path.exists('config.yaml'):
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        aKey = winreg.OpenKey(aReg, r"Software\\Valve\\Steam\\")
        steam_path = winreg.QueryValueEx(aKey, 'SteamPath')[0]
        with open('config.yaml', 'w') as config:
            steam_path = steam_path.replace("/", "\\")
            data = {
                'vpk_path': f"{steam_path}\\steamapps\\common\\dota 2 beta\\game\\dota\\pak01_dir.vpk",
                'language': 'en'}
            yaml.dump(data, config)
            properties = data.values()
    else:
        properties = get_properties('vpk_path', 'language')
    return properties


def scripts_check(vpk_path):
    """Проверка наличия файлов скриптов"""
    try:
        vpk_parse(export_file_path='scripts/items/items_game.txt',
                      output_path='', vpk_path=vpk_path)
        vpk_parse(export_file_path='resource/localization/items_russian.txt',
                      output_path='', vpk_path=vpk_path)
    except FileNotFoundError:
        pass


def check_files():
    """Функция проверяющая наличие необходимых файлов"""
    vpk_path, lang = config_check()
    scripts_check(vpk_path)
    return lang


def create_mod_directories(mod_name):
    if path.isdir(mod_name):
        rmtree(mod_name)
    mkdir(mod_name)
    mkdir(mod_name+'\\'+'mor_scripts')


class ParseError(Exception):
    pass