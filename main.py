from re import findall, IGNORECASE
import shutil

from config import vpk_path as vp
from os import system, path, rename, remove
from shutil import move, rmtree, Error


def vpk_parse(export_file_path, output_path, output_name=None):
    file_name = export_file_path.split('/')[-1]
    print(output_path, "1 ый нужный")
    output_path = path.abspath(output_path)
    decompiler_path = path.abspath('Decompiler/Decompiler.exe')
    system(f'{decompiler_path} -i "{vp}" -f "{export_file_path}" -o "{output_path}"')
    start_path = path.abspath(output_path+'\\'+export_file_path)
    try:
        move(start_path, output_path)
        print(start_path, output_path, '2ой')
    except shutil.Error:
        remove(output_path+'\\'+file_name)
        move(start_path, output_path)
    if output_name is not None:
        if not output_name.replace(' ', '') == '':
            rename(output_path+'\\'+file_name, output_path+'\\'+output_name)
    rmtree_name = output_path + '\\' + export_file_path.split('/')[0]
    if path.exists(rmtree_name):
        rmtree(rmtree_name)


class CreateMod:
    def __init__(self, default_item_name, custom_item_name, mod_name):
        self.default_item_name = default_item_name # Название стандартной вещи
        self.custom_item_name = custom_item_name # Название вещи на которую заменяем
        self.custom_item_path = ''
        self.default_item_path = ''
        self.item_script_create()
        output_name = self.default_item_path.split('/')[-1]
        self.default_item_path = self.default_item_path.split('/')
        self.default_item_path = '/'.join(self.default_item_path[0:len(self.default_item_path)-1])
        output_path = mod_name + "\\" + self.default_item_path
        vpk_parse(export_file_path=self.custom_item_path, output_path=output_path, output_name=output_name)

    def item_script_create(self):
        # Регулярное выражение для поиска скрипта по названию предмета
        # ({[\s\t\n] * ?\"name\"\s*\"Shadow Fiend's Head\"[\s\S]*})[\s\t\n]*\"\d*?\"
        # \"нужное поле\"\s*\"([\s\S]*?)\" поиск любого аттрибута в скрипте
        items_game = open('items_game.txt', 'r', encoding='utf-8') # Файл items_game
        end_script_file = open('script 1', 'w+', encoding='utf-8') # Файл end_script
        items_game_text = items_game.read() # Текст файла items_game
        items_game.close() # Закрывание файла
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
        items_russian = open('items_russian.txt', 'r', encoding='utf-8') # Файл items_russian
        items_russian_text = items_russian.read() # Текст файла items_russian
        items_russian.close() # Закрытие файла items_russian
        # Поиск описания вещи
        # "DOTA_Bundle_Assemblage_of_Announcers_Pack"        "Комплект «Собрание комментаторов»"
        custom_item_description_expression = rf"\"{custom_item_description_tag}\"\s*?\"([\s\S]*?)\""
        custom_item_description = findall(custom_item_description_expression, items_russian_text, IGNORECASE)[0]
        # Замены строк в скрипте
        custom_item_script = custom_item_script.replace('wearable', 'default_item')
        custom_item_script = custom_item_script.replace(self.custom_item_name, self.default_item_name)
        custom_item_script = custom_item_script.replace(custom_item_model_player_path, default_model_player_path)
        custom_item_script = custom_item_script.replace('#'+custom_item_description_tag, custom_item_description)
        end_script_file.write(custom_item_script)
        end_script_file.close()
        self.default_item_path = default_model_player_path + '_c'
        self.custom_item_path = custom_item_model_player_path + '_c'


if __name__ == '__main__':
    vpk_parse(export_file_path='scripts/items/items_game.txt', output_path='')
    vpk_parse(export_file_path='resource/localization/items_russian.txt', output_path='')
    CreateMod(default_item_name="Shadow Fiend's Arms", custom_item_name="Arms of Desolation", mod_name='Shadow_fiend_sex')
