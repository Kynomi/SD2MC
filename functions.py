from os import path, rename, remove, mkdir
import yaml
from shutil import move, rmtree, Error, make_archive
import winreg
from subprocess import call


def get_vpk_path():
    """Эта функция получает путь до ВПК файла"""
    with open('config.yaml', 'r') as config:
        vpk_path = yaml.safe_load(config)
        vpk_path = vpk_path['vpk_path']
    return vpk_path


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


def mod_info_check():
    """Функция проверяющая наличие файла информации о модах"""
    if not path.exists('mods_info.yaml'):
        mod_info = open("mod_info.yaml", "w")
        mod_info.close()
    else:
        mod_info = open("mod_info.yaml", "w")
        mod_info.write('')
        mod_info.close()


def config_check():
    """Функция проверяющая наличие конфигурационного файла и создающя его,
    Возвращает путь до ВПК"""
    if not path.exists('config.yaml'):
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        aKey = winreg.OpenKey(aReg, r"Software\\Valve\\Steam\\")
        steam_path = winreg.QueryValueEx(aKey, 'SteamPath')[0]
        with open('config.yaml', 'w') as config:
            steam_path = steam_path.replace("/", "\\")
            vpk_path = {
                'vpk_path': f"{steam_path}\\steamapps\\common\\dota 2 beta\\game\\dota\\pak01_dir.vpk"}
            yaml.dump(vpk_path, config)
            vpk_path = vpk_path['vpk_path']
    else:
        vpk_path = get_vpk_path()
    return vpk_path


def scripts_check(vpk_path):
    """Проверка наличия файлов скриптов"""
    if not path.exists('items_game.txt'):
        vpk_parse(export_file_path='scripts/items/items_game.txt',
                  output_path='', vpk_path=vpk_path)
    if not path.exists('items_russian.txt'):
        vpk_parse(export_file_path='resource/localization/items_russian.txt',
                  output_path='', vpk_path=vpk_path)


def check_files():
    """Функция проверяющая наличие необходимых файлов"""
    mod_info_check()
    vpk_path = config_check()
    scripts_check(vpk_path)


class ParseError(Exception):
    pass