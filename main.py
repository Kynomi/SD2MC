import re
from tkinter import messagebox
from re import findall, IGNORECASE, MULTILINE, sub
from os import system, path, rename, remove, mkdir
from shutil import move, rmtree, Error, make_archive
from Struct import Styles, Mods, AddMods, ConfigureMods, SettingsFrame
from Struct import tkinter, ttk
import winreg
import yaml


def get_vpk_path():
    """Эта функция получает путь до ВПК файла"""
    with open('config.yaml', 'r') as config:
        vpk_path = yaml.safe_load(config)
        vpk_path = vpk_path['vpk_path']
    return(vpk_path)


def vpk_parse(vpk_path, export_file_path, output_path, output_name=None):
    """Функция экспортирующая файл из ВПК"""
    if '\\' in export_file_path:
        export_file_path = export_file_path.replace('\\', '/')
    file_name = export_file_path.split('/')[-1]  # Получение названия файла
    output_path = path.abspath(output_path)  # Получение абсолютного выходного пути
    decompiler_path = path.abspath('Decompiler/Decompiler.exe')  # Путь до дикомпилера
    system(f'{decompiler_path} -i "{vpk_path}" -f "{export_file_path}" -o "{output_path}"')  # Вызов команды в командной строке для экспорта файла из ВПК
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
        config = open('config.yaml', 'w')
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        aKey = winreg.OpenKey(aReg, r"Software\\Valve\\Steam\\")
        steam_path = winreg.QueryValueEx(aKey, 'SteamPath')[0]
        with open('config.yaml', 'w') as config:
            steam_path = steam_path.replace("/", "\\")
            vpk_path = {
                'vpk_path' : f"{steam_path}\\steamapps\\common\\dota 2 beta\\game\\dota\\pak01_dir.vpk"}
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


class CreateMod:
    """Класс создания мода"""
    def __init__(self, default_item_name, custom_item_name, mod_name, script_number, vpk_path, style):
        self.style = int(style) - 1
        self.script_name = f'script {script_number}'
        self.vpk_path = vpk_path
        self.default_item_name = default_item_name  # Название стандартной вещи
        self.custom_item_name = custom_item_name  # Название вещи на которую заменяем
        self.custom_item_path = ''  # Путь до вещи на которую заменяем
        self.default_item_path = ''  # Путь до стандартной вещи
        self.particles = {}  # Партиклы
        self.mod_name = mod_name
        if self.item_script_create() is not False:# Создание скрипта
            output_name = self.default_item_path.split('/')[-1]  # Конечное имя vmdl файла
            # Преобразование пути до стандартной вещи в конечный путь для впк парсера
            self.default_item_path = self.default_item_path.split('/')
            self.default_item_path = '/'.join(self.default_item_path[:-1])
            output_path = mod_name + "\\" + self.default_item_path
            # Парс вещи для мода
            vpk_parse(export_file_path=self.custom_item_path, output_path=output_path, output_name=output_name, vpk_path=self.vpk_path)
            # Парс партиклов для мода
            for original_particle, new_particle in self.particles.items():
                new_particle = new_particle + '_c'
                output_particle_path = original_particle.split('/')
                output_particle_path = '\\'.join(output_particle_path[:-1])
                output_particle_path = mod_name + "\\" + output_particle_path
                output_particle_name = original_particle.split('/')[-1] + '_c'
                vpk_parse(export_file_path=new_particle, output_path=output_particle_path, output_name=output_particle_name, vpk_path=self.vpk_path)
            self.script_name = script_number + 1
        else:
            remove(f'{self.mod_name}\\mor_scripts\\{self.script_name}.txt')
            print(f'{self.custom_item_name} не был создан')
            script_name = script_number

    def item_script_create(self):
        """Функция генерирующая скрипты для мода"""
        # Регулярное выражение для поиска скрипта по названию предмета
        # ({[\s\t\n] * ?\"name\"\s*\"Shadow Fiend's Head\"[\s\S]*})[\s\t\n]*\"\d*?\"
        # \"нужное поле\"\s*\"([\s\S]*?)\" поиск любого аттрибута в скрипте
        with open('items_game.txt', 'r', encoding='utf-8') as items_game: # Файл items_game
            # Файл end_script
            with open(f'{self.mod_name}\\mor_scripts\\{self.script_name}.txt', 'w+', encoding='utf-8') as end_script_file:
                items_game_text = items_game.read()  # Текст файла items_game
                items_game.close()  # Закрывание файла
                # Регулярные выражения для поиска необходимых аттрибутов
                script_expression = r"({[\s\t\n]*?\"name\"\s*?\"" + f"{self.default_item_name}" + r"\"[\s\S]*?})[\s\t\n]*?\"\d*?\""
                model_path_expression = rf'\"model_player\"\s*\"([\s\S]*?)\"'
                custom_item_description_tag_expression = rf'\"item_description\"\s*\"([\s\S]*?)\"'
                item_name_expression = r'\"item_name\"\s*\"([\s\S]*?)\"'
                # Поиск скрипта стандартного предмета
                default_item_script = findall(script_expression, items_game_text, IGNORECASE)[0]
                # Поиск пути до файла стандартной модели
                try:
                    default_model_player_path = findall(model_path_expression, default_item_script, IGNORECASE)[0]
                    print('default')
                except IndexError:
                    return False
                # Обновление регулярного выражения
                script_expression = r"({\s*\"name\"\s*?\"" + f"{self.custom_item_name}" + r"\"[\s\S]*?)\s*?\"\d*?\"\s*?\t\t{\s*?^\t\t\t\"name\""
                # Поиск скрипта предмета, на который заменяем
                try:
                    custom_item_script = findall(script_expression, items_game_text, IGNORECASE+MULTILINE)[0]
                except IndexError:
                    return False
                if self.style is not None:
                    custom_item_script = self.styles_script(custom_item_script, self.style)
                del script_expression
                # Поиск пути до модели, на которую будем заменять
                custom_item_model_player_path = findall(model_path_expression, custom_item_script, IGNORECASE)[0]
                del model_path_expression
                # Замены строк в скрипте
                custom_item_script = custom_item_script.replace('wearable', 'default_item')
                custom_item_script = custom_item_script.replace(self.custom_item_name, self.default_item_name)
                custom_item_script = custom_item_script.replace(custom_item_model_player_path, default_model_player_path)
                # Поиск тега для поиска названия кастомного предмета
                with open('items_russian.txt', 'r', encoding='utf-8') as items_russian:  # Файл items_russian
                    items_russian_text = items_russian.read()  # Текст файла items_russian
                    # Изменение названия предмета
                    item_name_tag = findall(item_name_expression, custom_item_script)[0]
                    item_name_tag = item_name_tag.replace('#', '')
                    custom_item_item_name_exp = rf"\"{item_name_tag}\"\s*?\"([\s\S]*?)\""
                    custom_item_item_name = findall(custom_item_item_name_exp, items_russian_text, IGNORECASE)[0]
                    print(custom_item_item_name, item_name_tag)
                    custom_item_script = custom_item_script.replace('#' + item_name_tag, custom_item_item_name)
                    # Изменения описания вещи
                    custom_item_description_tag = findall(custom_item_description_tag_expression, custom_item_script, IGNORECASE)[0]
                    custom_item_description_tag = custom_item_description_tag.replace('#', '')
                    # Поиск описания вещи
                    # "DOTA_Bundle_Assemblage_of_Announcers_Pack"        "Комплект «Собрание комментаторов»"
                    custom_item_description_expression = rf"\"{custom_item_description_tag}\"\s*?\"([\s\S]*?)\""
                    try:
                        custom_item_description = findall(custom_item_description_expression, items_russian_text, IGNORECASE)[0]
                        del custom_item_description_tag_expression
                        custom_item_script = custom_item_script.replace('#' + custom_item_description_tag, custom_item_description)
                    except IndexError:
                        print(f'У {self.custom_item_name} нет описания')
                # Поиск партиклов
                particles = re.findall(r'\"type\"\s*\"particle\"\s*?\"asset\"\s*?(\"[\s\S]*?\")\s*\"modifier\"\s*?(\"[\s\S]*?\")', custom_item_script)
                for i in particles:
                    key = i[0].strip('"')
                    particle = i[1].strip('"')
                    self.particles[key] = particle
                end_script_file.write(custom_item_script)
                end_script_file.close()
                self.default_item_path = default_model_player_path + '_c'
                self.custom_item_path = custom_item_model_player_path + '_c'

    @staticmethod
    def styles_script(text, style):
        styles = findall(r'^\s*?\"styles\"[\s\S]*?}\s*?}', text, MULTILINE)[0]
        styles_count = len(findall(r'\"\d*\"\s*{', styles))
        new_model_exp = r'\"' + f'{style}' + '\"[\s\S]*?\"model_player\"\s*?\"([\s\S]*?)\"\s*?[\s\S]*?}'
        new_model = findall(new_model_exp, styles)[0]
        old_model = findall(r'\"model_player\"\s*?\"([\s\S]*?)\"', text)[0]
        text = text.replace(styles, '')
        text = text.replace(old_model, new_model)
        for i in range(0, styles_count):
            if i != style:
                expression = r'\"asset[\s\S]*?\"[\s\S]*?\"style\"\s*?\"' + f'{i}' + r'\"[\s\S]*?}'
                asset_modifiers_delete = findall(expression, text)
                for i in asset_modifiers_delete:
                    text = text.replace(i, '')
        print(text)
        print(styles)
        if "alternate_icons" in text:
            icon_replace = findall(r'\"alternate_icons\"\s*?{\n[\s\S]*?}\s*?}', text)[0]
            text = text.replace(icon_replace, '')
        delete_style = findall(r'^\s*?\"style\"\s*?\"[\s\S]*?\"', text, MULTILINE)
        for i in delete_style:
            text = text.replace(i, '')
        text = text.split('\n')
        text = [i for i in text if i.strip() != '']
        text = '\n'.join(text)
        return text


class MainApp(tkinter.Tk):
    """Основной класс программы"""
    def __init__(self):
        super(MainApp, self).__init__()
        # style
        self.mods = Mods()
        style = Styles()
        style.theme_use('MyAppStyle')
        self.active_tab = ''
        self.change_mod_structure_frame = ConfigureMods(self, width=1280)  # Фрейм вкладки изменить конфигурацию мода
        self.add_mods_frame = AddMods(self, width=1280)  # Фрейм вкладки добавить моды
        self.settings_frame = SettingsFrame(self, width=1280)  # Фрейм вкладки настройки
        self.settings_frame.confirm_button['command'] = self.confirm_settings
        self.header_frame = ttk.Frame(self, style='Header.TFrame', width=1280, height=72)
        self.title('Dota2 Simple Mod Creater')
        self.configure(background='#1f1f1f')

    def main_window(self):
        """Функция основного окна"""
        # Фреймы для вкладок
        self.add_mods_frame.add_mods_confirmation_button.configure(command=self.add_mods)
        self.change_mod_structure_frame.change_button.configure(command=self.change_values)
        # Main_window placing
        self.header()
        self.add_mods_frame.grid(row=1, column=0)
        self.active_tab = 'Добавить моды'
        # Tkinter mainloop
        self.change_mod_structure_frame.change_button['command'] = self.change_values
        tkinter.mainloop()

    def header(self):
        """Функция создающая виджет header"""
        # Лямбда функции нужны для генерации кнопок с одной и той же командой, но разными аргументами.
        create_mods_button = ttk.Button(self.header_frame, text="Создать моды", command=self.create_mods)
        create_mods_button.pack(side='right', padx=2)
        add_mods_tab = ttk.Button(self.header_frame, command=lambda: self.change_tab('Добавить моды'))
        add_mods_tab['text'] = "Добавить моды"
        add_mods_tab.pack(side='left', padx=2)
        change_mods_tab = ttk.Button(self.header_frame, command=lambda: self.change_tab('Изменить конфигурацию модов'))
        change_mods_tab['text'] = "Изменить конфигурацию модов"
        change_mods_tab.pack(side='left', padx=2)
        settings_tab = ttk.Button(self.header_frame, command=lambda: self.change_tab('Настройки'))
        settings_tab['text'] = 'Настройки'
        settings_tab.pack(side='left', padx=2)
        self.header_frame.pack_propagate(False)
        self.header_frame.grid(row=0, column=0, pady=(0, 50))

    def change_tab(self, text):
        """функция изменяющая вкладку на выбранную пользователем"""
        dict = {"Добавить моды": self.add_mods_frame,
                "Изменить конфигурацию модов": self.change_mod_structure_frame,
                "Настройки": self.settings_frame}
        dict[self.active_tab].grid_forget()
        dict[text].grid(row=1, column=0, sticky='NSWE')
        self.active_tab = text

    def add_mods(self):
        """Функция добавляющая моды в список"""
        default_item, custom_item, mod_name, style = self.add_mods_frame.get_entry()
        self.mods.append_mod(custom_item=custom_item, default_item=default_item, mod_name=mod_name, style=style)
        mods = self.mods.reload()
        with open('mod_info.yaml', 'w') as mod_info:
            yaml.dump(mods, mod_info)
        self.add_mods_frame.reload(mod_name)
        self.change_mod_structure_frame.reload()

    def change_values(self):
        new_mod_info = self.change_mod_structure_frame.get_entry()
        self.mods.change_mod(mod_name=new_mod_info[0], default_item=new_mod_info[1], custom_item=new_mod_info[2],
                             style=new_mod_info[3], new_mod_name=new_mod_info[4], new_default_item=new_mod_info[5],
                             new_custom_item=new_mod_info[6], new_style=new_mod_info[7])
        mods = self.mods.reload()
        with open('mod_info.yaml', 'w') as mod_info:
            yaml.dump(mods, mod_info)
        if new_mod_info[4] is not None:
            self.add_mods_frame.reload(new_mod_name=new_mod_info[4])
        else:
            self.add_mods_frame.reload()
        self.change_mod_structure_frame.reload()

    def confirm_settings(self):
        new_vpk_path = self.settings_frame.vpk_path_field.get()
        if '/' in new_vpk_path:
            new_vpk_path.replace('/', '\\')
        new_vpk_path += 'steamapps\\common\\dota 2 beta\\game\\dota\\pak01_dir.vpk'
        with open('config.yaml', 'w', encoding='utf-8') as config:
            yaml.dump({'vpk_path': new_vpk_path}, config)

    def create_mods(self):
        """Функция создания модов из списка"""
        vpk_path = get_vpk_path()
        mod_count = len(self.mods.mods)
        for mod_name, mod in self.mods.mods.items():
            next_script = 1
            for item in mod.items:
                default_item = item.default_item
                custom_item = item.custom_item
                style = item.style
                try:
                    mkdir(mod_name)
                    mkdir(mod_name + '\\mor_scripts')
                except FileExistsError:
                    rmtree(mod_name)
                    mkdir(mod_name)
                    mkdir(mod_name + '\\mor_scripts')
                print(f"now creating: {mod_name}, item: {custom_item}")
                mod = CreateMod(default_item_name=default_item, custom_item_name=custom_item,
                          mod_name=mod_name, script_number=next_script, vpk_path=vpk_path, style=style)
                next_script = mod.script_name
            make_archive(mod_name, 'zip', mod_name)
            rmtree(mod_name)
        messagebox.showinfo('Мод статус', 'Модификации были успешно созданы')


if __name__ == '__main__':
    check_files()
    myapp = MainApp()
    myapp.geometry("1280x720")
    myapp.resizable(False, False)
    myapp.main_window()
