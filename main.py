import re
from tkinter import messagebox
from re import findall, IGNORECASE
from os import system, path, rename, remove, mkdir
from shutil import move, rmtree, Error, make_archive
from Struct import *

try:
    from config import vpk_path
except ModuleNotFoundError:
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    aKey = winreg.OpenKey(aReg, r"Software\\Valve\\Steam\\")
    steam_path = winreg.QueryValueEx(aKey, 'SteamPath')[0]
    with open('config.py', 'w') as config:
        steam_path = steam_path.replace("/", "\\")
        config.write('vpk_path = ' + f'"{steam_path}\\steamapps\\common\\dota 2 beta\\game\\dota\\pak01_dir.vpk"')
        config.close()
    from config import vpk_path


def vpk_parse(export_file_path, output_path, output_name=None):
    if '\\' in export_file_path:
        export_file_path = export_file_path.replace('\\', '/')
    file_name = export_file_path.split('/')[-1]
    output_path = path.abspath(output_path)
    decompiler_path = path.abspath('Decompiler/Decompiler.exe')
    system(f'{decompiler_path} -i "{vpk_path}" -f "{export_file_path}" -o "{output_path}"')
    start_path = path.abspath(output_path + '\\' + export_file_path)
    try:
        move(start_path, output_path)
    except Error:
        remove(path.relpath(output_path) + '\\' + file_name)
        move(start_path, output_path)
    if output_name is not None:
        if not output_name.replace(' ', '') == '':
            rename(output_path + '\\' + file_name, output_path + '\\' + output_name)
    rmtree_name = output_path + '\\' + export_file_path.split('/')[0]
    if path.exists(rmtree_name):
        rmtree(rmtree_name)


class CreateMod:
    def __init__(self, default_item_name, custom_item_name, mod_name, script_name):
        self.script_name = script_name
        self.default_item_name = default_item_name  # Название стандартной вещи
        self.custom_item_name = custom_item_name  # Название вещи на которую заменяем
        self.custom_item_path = ''  # Путь до вещи на которую заменяем
        self.default_item_path = ''  # Путь до стандартной вещи
        self.particles = {}  # Партиклы
        self.mod_name = mod_name
        self.item_script_create()  # Создание скрипта
        output_name = self.default_item_path.split('/')[-1]  # Конечное имя vmdl файла
        # Преобразование пути до стандартной вещи в конечный путь для впк парсера
        self.default_item_path = self.default_item_path.split('/')
        self.default_item_path = '/'.join(self.default_item_path[:-1])
        output_path = mod_name + "\\" + self.default_item_path
        # Парс вещи для мода
        vpk_parse(export_file_path=self.custom_item_path, output_path=output_path, output_name=output_name)
        # Парс партиклов для мода
        for original_particle, new_particle in self.particles.items():
            new_particle = new_particle + '_c'
            output_particle_path = original_particle.split('/')
            output_particle_path = '\\'.join(output_particle_path[:-1])
            output_particle_path = mod_name + "\\" + output_particle_path
            output_particle_name = original_particle.split('/')[-1] + '_c'
            vpk_parse(export_file_path=new_particle, output_path=output_particle_path, output_name=output_particle_name)

    def item_script_create(self):
        # Регулярное выражение для поиска скрипта по названию предмета
        # ({[\s\t\n] * ?\"name\"\s*\"Shadow Fiend's Head\"[\s\S]*})[\s\t\n]*\"\d*?\"
        # \"нужное поле\"\s*\"([\s\S]*?)\" поиск любого аттрибута в скрипте
        items_game = open('items_game.txt', 'r', encoding='utf-8')  # Файл items_game
        # Файл end_script
        end_script_file = open(f'{self.mod_name}\\mor_scripts\\{self.script_name}.txt', 'w+', encoding='utf-8')
        items_game_text = items_game.read()  # Текст файла items_game
        items_game.close()  # Закрывание файла
        # Регулярные выражения для поиска необходимых аттрибутов
        script_expression = r"({[\s\t\n]*?\"name\"\s*?\"" + f"{self.default_item_name}" + r"\"[\s\S]*?})[\s\t\n]*?\"\d*?\""
        model_path_expression = rf'\"model_player\"\s*\"([\s\S]*?)\"'
        custom_item_description_tag_expression = rf'\"item_description\"\s*\"([\s\S]*?)\"'
        # Поиск скрипта стандартного предмета
        default_item_script = findall(script_expression, items_game_text, IGNORECASE)[0]
        # Поиск пути до файла стандартной модели
        default_model_player_path = findall(model_path_expression, default_item_script, IGNORECASE)[0]
        # Обновление регулярного выражения
        script_expression = r"({[\s\t\n]*?\"name\"\s*?\"" + f"{self.custom_item_name}" + r"\"[\s\S]*?})[\s\t\n]*?\"\d*?\""
        # Поиск скрипта предмета, на который заменяем
        custom_item_script = findall(script_expression, items_game_text, IGNORECASE)[0]
        del script_expression
        # Поиск пути до модели, на которую будем заменять
        custom_item_model_player_path = findall(model_path_expression, custom_item_script, IGNORECASE)[0]
        del model_path_expression
        # Поиск тега для поиска названия кастомного предмета
        custom_item_description_tag = findall(custom_item_description_tag_expression, custom_item_script, IGNORECASE)[0]
        custom_item_description_tag = custom_item_description_tag.replace('#', '')
        del custom_item_description_tag_expression
        items_russian = open('items_russian.txt', 'r', encoding='utf-8')  # Файл items_russian
        items_russian_text = items_russian.read()  # Текст файла items_russian
        items_russian.close()  # Закрытие файла items_russian
        # Поиск описания вещи
        # "DOTA_Bundle_Assemblage_of_Announcers_Pack"        "Комплект «Собрание комментаторов»"
        custom_item_description_expression = rf"\"{custom_item_description_tag}\"\s*?\"([\s\S]*?)\""
        custom_item_description = findall(custom_item_description_expression, items_russian_text, IGNORECASE)[0]
        # Замены строк в скрипте
        custom_item_script = custom_item_script.replace('wearable', 'default_item')
        custom_item_script = custom_item_script.replace(self.custom_item_name, self.default_item_name)
        custom_item_script = custom_item_script.replace(custom_item_model_player_path, default_model_player_path)
        custom_item_script = custom_item_script.replace('#' + custom_item_description_tag, custom_item_description)
        # Поиск партиклов
        particles = re.findall(
            r'\"type\"\s*\"particle\"\s*?\"asset\"\s*?(\"[\s\S]*?\")\s*\"modifier\"\s*?(\"[\s\S]*?\")',
            custom_item_script)
        for i in particles:
            key = i[0].strip('"')
            particle = i[1].strip('"')
            self.particles[key] = particle
        end_script_file.write(custom_item_script)
        end_script_file.close()
        self.default_item_path = default_model_player_path + '_c'
        self.custom_item_path = custom_item_model_player_path + '_c'


class MainApp(tkinter.Tk):
    def __init__(self):
        super(MainApp, self).__init__()
        # style
        style = Styles()
        style.theme_use('MyAppStyle')
        self.active_tab = ''
        self.change_mod_structure_frame = ConfigureMods(self, width=1280)  # Фрейм вкладки изменить конфигурацию мода
        self.add_mods_frame = AddMods(self, width=1280)  # Фрейм вкладки добавить моды
        self.settings_frame = SettingsFrame(self, width=1280)  # Фрейм вкладки настройки
        self.settings_frame.confirm_button['command'] = self.confirm_settings
        self.header_frame = ttk.Frame(self, style='Header.TFrame', width=1280, height=72)
        self.title('Dota2 Simple Mod Creater')
        if not path.exists('items_game.txt'):
            vpk_parse(export_file_path='scripts/items/items_game.txt', output_path='')
        if not path.exists('items_russian.txt'):
            vpk_parse(export_file_path='resource/localization/items_russian.txt', output_path='')
        self.mod_items = ModItems()
        self.configure(background='#1f1f1f')

    def create_mods(self):
        mod_count = self.mod_items.mods_count()
        for i in range(0, mod_count):
            mod_name = self.mod_items.get_mod_name(i)
            custom_items, default_items = self.mod_items.get_mod(i)
            try:
                mkdir(mod_name)
                mkdir(mod_name + '\\mor_scripts')
            except FileExistsError:
                rmtree(mod_name)
                mkdir(mod_name)
                mkdir(mod_name + '\\mor_scripts')
            for j in range(0, len(default_items)):
                print(f"now creating: {mod_name}, item: {custom_items[j]}")
                CreateMod(default_item_name=default_items[j], custom_item_name=custom_items[j],
                          mod_name=mod_name, script_name=f'script {j + 1}')
            make_archive(mod_name, 'zip', mod_name)
            rmtree(mod_name)
        messagebox.showinfo('Мод статус', 'Модификации были успешно созданы')

    def main_window(self):
        # Фреймы для вкладок
        self.add_mods_frame.add_mods_confirmation_button.configure(command=self.add_mods)
        # Main_window placing
        self.header()
        self.add_mods_frame.grid(row=1, column=0)
        self.active_tab = 'Добавить моды'
        # Tkinter mainloop
        self.change_mod_structure_frame.change_button['command'] = self.change_values
        tkinter.mainloop()

    def add_mods(self):
        default_item = str(self.add_mods_frame.standart_item_field.get())
        custom_item = str(self.add_mods_frame.custom_item_field.get())
        mod_name = str(self.add_mods_frame.mod_name_field.get())
        self.mod_items.add_items(mod_name=mod_name, custom_items=custom_item, default_items=default_item)
        self.add_mods_frame.add_mod_info(new_mod_name=mod_name, new_custom_item=custom_item,
                                         new_default_item=default_item)
        self.change_mod_structure_frame.add_mod_info(mod_name=mod_name, custom_item=custom_item,
                                                     default_item=default_item)
        self.add_mods_frame.clear_entry()

    def header(self):
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
        dict = {"Добавить моды": self.add_mods_frame,
                "Изменить конфигурацию модов": self.change_mod_structure_frame,
                "Настройки": self.settings_frame}
        dict[self.active_tab].grid_forget()
        dict[text].grid(row=1, column=0)
        self.active_tab = text

    def change_values(self):
        new_mod_name_array, new_custom_item_array, new_default_item_array, mod_name = self.change_mod_structure_frame.change_mod()
        if new_mod_name_array is not None:
            old_mod_name, new_mod_name = new_mod_name_array[1], new_mod_name_array[0]
            self.mod_items.change_mod_name(old=old_mod_name, new=new_mod_name)
        if new_custom_item_array is not None:
            old_custom_item, new_custom_item = new_custom_item_array[1], new_custom_item_array[0]
            self.mod_items.change_custom_item(old=old_custom_item, new=new_custom_item, mod_name=mod_name)
        if new_default_item_array is not None:
            old_default_item, new_default_item = new_default_item_array[1], new_default_item_array[0]
            self.mod_items.change_custom_item(old=old_default_item, new=new_default_item, mod_name=mod_name)
        self.add_mods_frame.change_mod_info(new_mod_name_array=new_mod_name_array,
                                            new_custom_item_array=new_custom_item_array,
                                            new_default_item_array=new_default_item_array)

    def confirm_settings(self):
        global vpk_path
        vpk_path = self.settings_frame.confirm_settings()


if __name__ == '__main__':
    vpk_parse(export_file_path='scripts\\items\\items_game.txt', output_path='')
    vpk_parse(export_file_path='resource/localization/items_russian.txt', output_path='')
    myapp = MainApp()
    myapp.geometry("1280x720")
    myapp.resizable(False, False)
    myapp.main_window()
