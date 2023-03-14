import tkinter
from re import findall, IGNORECASE
from config import vpk_path as vp
from os import system, path, rename, remove, mkdir
from shutil import move, rmtree, Error, make_archive
from Struct import *


def vpk_parse(export_file_path, output_path, output_name=None):
    file_name = export_file_path.split('/')[-1]
    print(output_path, "1 ый нужный")
    output_path = path.abspath(output_path)
    decompiler_path = path.abspath('Decompiler/Decompiler.exe')
    system(f'{decompiler_path} -i "{vp}" -f "{export_file_path}" -o "{output_path}"')
    start_path = path.abspath(output_path + '\\' + export_file_path)
    try:
        move(start_path, output_path)
        print(start_path, output_path, '2ой')
    except Error:
        remove(output_path + '\\' + file_name)
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
        self.mod_name = mod_name
        self.item_script_create()  # Создание скрипта
        output_name = self.default_item_path.split('/')[-1]  # Конечное имя vmdl файла
        # Преобзразование пути до стандартной вещи в конечный путь для впк парсера
        self.default_item_path = self.default_item_path.split('/')
        self.default_item_path = '/'.join(self.default_item_path[0:len(self.default_item_path) - 1])
        output_path = mod_name + "\\" + self.default_item_path
        # Парс вещи для мода
        vpk_parse(export_file_path=self.custom_item_path, output_path=output_path, output_name=output_name)

    def item_script_create(self):
        # Регулярное выражение для поиска скрипта по названию предмета
        # ({[\s\t\n] * ?\"name\"\s*\"Shadow Fiend's Head\"[\s\S]*})[\s\t\n]*\"\d*?\"
        # \"нужное поле\"\s*\"([\s\S]*?)\" поиск любого аттрибута в скрипте
        items_game = open('items_game.txt', 'r', encoding='utf-8')  # Файл items_game
        # Файл end_script
        end_script_file = open(f'{self.mod_name}\\mor_scripts\\{self.script_name}', 'w+', encoding='utf-8')
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
        end_script_file.write(custom_item_script)
        end_script_file.close()
        self.default_item_path = default_model_player_path + '_c'
        self.custom_item_path = custom_item_model_player_path + '_c'


class MainApp(tkinter.Tk):
    def __init__(self):
        super(MainApp, self).__init__()
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
                CreateMod(default_item_name=default_items[j], custom_item_name=custom_items[j],
                          mod_name=mod_name, script_name=f'script {j + 1}')
            make_archive(mod_name, 'zip', mod_name)
            print('OK')
            rmtree(mod_name)

    def main_window(self):
        # Фреймы для вкладок
        self.add_mods_frame = AddMods(self, width=1280) # Фрейм вкладки добавить моды
        self.add_mods_frame.add_mods_confirmation_button.configure(command=self.add_mods)
        change_mod_structure_frame = ttk.Frame(self)  # Фрейм вкладки изменить конфигурацию мода
        settings_frame = ttk.Frame(self)  # Фрейм вкладки настройки
        header_frame = ttk.Frame(self, width=1280, height=70)  # Фрейм header
        # Создание стиля
        # header
        header_tab = ttk.Notebook(header_frame)
        header_button_compile_mods = ttk.Button(header_frame, text="Создать моды", command=self.create_mods)
        header_tab.add(self.add_mods_frame)
        header_tab.add(change_mod_structure_frame)
        header_tab.add(settings_frame)
        header_tab.tab(0, text='Добавить мод')
        header_tab.tab(1, text='Изменить состав мода')
        header_tab.tab(2, text='Настройки')
        header_frame.grid(row=0, column=0, pady=(0, 50))
        header_frame.pack_propagate(False)
        header_tab.pack(side='left')
        header_button_compile_mods.pack(side='right')
        #Main_window placing
        self.add_mods_frame.grid(row=1, column=0)
        self.add_mods_frame.pack_propagate(False)
        #Tkinter mainloop
        tkinter.mainloop()

    def add_mods(self):
        default_item = self.add_mods_frame.standart_item_field.get()
        custom_item = self.add_mods_frame.custom_item_field.get()
        mod_name = self.add_mods_frame.mod_name_field.get()
        self.mod_items.add_items(mod_name=mod_name, custom_items=custom_item, default_items=default_item)
        self.add_mods_frame.add_mod_info(new_mod_name=mod_name, new_custom_item=custom_item, new_default_item=default_item)




if __name__ == '__main__':
    myapp = MainApp()
    # custom_items = ['Arms of Desolation', 'Horns of Eternal Harvest', 'Pauldrons of Eternal Harvest']
    # default_items = ["Shadow Fiend's Arms", "Shadow Fiend's Head", "Shadow Fiend's Shoulders"]
    # myapp.mod_items.add_items(mod_name='Shadow_fiend_sex', default_items=default_items, custom_items=custom_items)
    # myapp.create_mods()
    myapp.geometry("1280x720")
    myapp.resizable(0, 0)
    myapp.main_window()
