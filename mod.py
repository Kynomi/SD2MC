from functions import vpk_parse, ParseError
from re import findall, IGNORECASE, MULTILINE, search


def find_only_one(expression, text, error):
    try:
        return findall(expression, text, IGNORECASE+MULTILINE)[0]
    except IndexError:
        raise ParseError(f'{error}')


def parse_script(item_name, items_game_text):
    if search(item_name, items_game_text, flags=IGNORECASE):
        script_expression = r"({\s*\"name\"\s*?\"" + f"{item_name}" + r"\"[\s\S]*?)\s*?\"\d*?\"\s*?\t\t{\s*?^\t\t\t\"name\""
        return findall(script_expression, items_game_text, IGNORECASE + MULTILINE)[0]
    raise ParseError(f'Предмета {item_name} не существует')


class Item:
    """Класс предмета"""

    def __init__(self, default_item, custom_item, style):
        self.default_item = default_item
        self.custom_item = custom_item
        self.style = style

    def get_item(self):
        return self.default_item, self.custom_item, self.style

    def __str__(self):
        result = f'default_item: {self.default_item} '
        result += f'custom_item: {self.custom_item} '
        result += f'style: {self.style}'
        return result


class Mod:
    """Класс мода"""

    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.items = []

    def append_item(self, default_item, custom_item, style):
        """Функция добавления предмета в мод"""
        self.items.append(Item(default_item, custom_item, style))

    def get_items(self):
        """Функция возвращающая список предметов в моде"""
        items = []
        for item in self.items:
            items.append([item.default_item, item.custom_item, item.style])
        return items

    def delete_style(self, custom_item):
        for i in self.items:
            if i.get_item()[1] == custom_item:
                i.style = None

    def change_mod(self, **mod_info):
        """Функция отвечающая за изменение модификации"""
        custom_item = mod_info['custom_item']
        style = mod_info['style']
        new_custom_item = mod_info['new_custom_item']
        new_style = mod_info['new_style']
        style_index = None
        if style is not None:
            style_index = style.split('(')[0]
            style = style.split('(')[1].replace(')', '')
        elif style == 'None':
            style = None
        for item in self.items:
            if new_custom_item is not None:
                if item.custom_item == custom_item:
                    if style is not None:
                        if item.custom_item != style_index:
                            item.custom_item = new_custom_item
                            item.default_item = mod_info['new_default_item']
                        else:
                            item.custom_item = new_custom_item
                            item.default_item = mod_info['new_default_item']
                            item.style = new_style
                    else:
                        item.custom_item = new_custom_item
                        item.default_item = mod_info['new_default_item']
            if new_style is not None:
                if item.style == style and item.custom_item == style_index:
                    item.style = new_style

    def delete_item(self, item_name):
        for item in self.items:
            if item.get_item()[1] == item_name:
                self.items.remove(item)

    def __str__(self):
        s = ''
        for item in self.items:
            s += f'{str(item)}\n'
        return s


class Mods:
    """Класс списка модов"""

    def __init__(self):
        self.mods = {}

    @staticmethod
    def find_default_item(custom_item, items_game_text, **kwargs):
        custom_item_script = parse_script(custom_item, items_game_text)
        if '"item_rarity"\t\t"arcana"' in custom_item_script:
            raise ParseError('Данная программа не умеет делать арканы')
        if "style" in kwargs.keys():
            styles = find_only_one(r'^\s*?\"styles\"[\s\S]*?^\t\t\t\t}', custom_item_script, 'У этого предмета нет стилей')
            if f'\t\t\t\t\t"{kwargs["style"]-1}"' not in styles:
                raise ParseError('Такого стиля не существует')
        default_item_script = None
        default_items = findall(r'\t\t{\n[^}]*?^\t\t\t"prefab"\t\t"default_item"[\s\S]*?^\t\t}', items_game_text,
                                   flags=MULTILINE+IGNORECASE)
        custom_item_slot = findall(r'"item_slot"\t\t("[\s\S]*?")', custom_item_script, flags=IGNORECASE)
        custom_item_used_by_heroes = findall(r'\t\t\t"used_by_heroes"\n\t\t\t{\n\t\t\t\t"([\s\S]*?)"',
                                             custom_item_script, flags=MULTILINE+IGNORECASE)[0]
        for default_item in default_items:
            if len(custom_item_slot) > 0:
                if custom_item_slot[0] in default_item and custom_item_used_by_heroes in default_item:
                    default_item_script = default_item
            else:
                if 'item_slot' not in default_item and custom_item_used_by_heroes in default_item:
                    default_item_script = default_item
        if 'model_player' not in default_item_script:
            raise ParseError(f'У {custom_item} нет стандартной модели')
        default_item_name = findall(r'"name"\t\t"([\s\S]*?)"', default_item_script, IGNORECASE)[0]
        return default_item_name

    def append_mod(self, **mod_info):
        """Добавляет мод в список модов"""
        mod_name = mod_info['mod_name']
        custom_item = mod_info['custom_item']
        style = mod_info['style']
        if 'default_item' not in mod_info.keys():
            with open('items_game.txt', 'r', encoding='utf-8') as items_game_file:
                items_game_text = items_game_file.read()
                if style is not None:
                    default_item = self.find_default_item(custom_item, items_game_text, style=int(style))
                else:
                    default_item = self.find_default_item(custom_item, items_game_text)
        else:
            default_item = mod_info['default_item']
        if mod_name in self.mods.keys():
            self.mods[mod_name].append_item(default_item, custom_item, style)
        else:
            self.mods[mod_name] = Mod(mod_name)
            self.mods[mod_name].append_item(default_item, custom_item, style)

    def get_mods(self):
        """Возвращает список модов для обновления данных"""
        mods = {}
        for mod_name, mod in self.mods.items():
            items = mod.get_items()
            mods[mod_name] = items
        return mods

    def get_mod_items(self, mod):
        return self.mods[mod].get_items()

    def change_mod(self, **mod_info):
        """Функция отвечающая за изменение модификации"""
        new_default_item = None
        mod_name = mod_info['mod_name']
        custom_item = mod_info['custom_item']
        style = mod_info['style']
        new_mod_name = mod_info['new_mod_name']
        new_custom_item = mod_info['new_custom_item']
        if new_custom_item:
            items_game_file = open('items_game.txt', 'r', encoding='utf-8')
            items_game_text = items_game_file.read()
            items_game_file.close()
            new_default_item = self.find_default_item(new_custom_item, items_game_text)
        else:
            new_custom_item = None
        new_style = mod_info['new_style']
        for key, mod in self.mods.items():
            if key == mod_name:
                mod.change_mod(custom_item=custom_item, new_custom_item=new_custom_item,
                               new_default_item=new_default_item, style=style, new_style=new_style)
                break
        if new_mod_name is not None:
            self.mods[new_mod_name] = self.mods.pop(mod_name)

    def delete_style(self, **mod_info):
        mod_name = mod_info['mod_name']
        custom_item = mod_info['custom_item']
        for k, v in self.mods.items():
            if k == mod_name:
                v.delete_style(custom_item=custom_item)

    def delete_mod(self, **mod_info):
        for mod_name, mod in self.mods.items():
            if mod_name == mod_info['mod_name']:
                mod.delete_item(mod_info['item_name'])

    def __str__(self):
        string = ''
        for k, v in self.mods.items():
            string += f'{k}:\n {str(v)} \n'
        return string


class CreateMod:
    """Класс создания мода"""
    def __init__(self, default_item_name, custom_item_name, mod_name, script_number, vpk_path, style=None):
        if style is not None:
            self.style = int(style) - 1
        else:
            self.style = style
        self.script_name = f'script {script_number}'
        self.vpk_path = vpk_path
        self.default_item_name = default_item_name  # Название стандартной вещи
        self.custom_item_name = custom_item_name  # Название вещи на которую заменяем
        self.custom_item_path = ''  # Путь до вещи на которую заменяем
        self.default_item_path = ''  # Путь до стандартной вещи
        self.particles = {}  # Партиклы
        self.mod_name = mod_name
        self.item_script_create()
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

    def item_script_create(self):
        """Функция генерирующая скрипты для мода"""
        with open('items_game.txt', 'r', encoding='utf-8') as items_game:  # Файл items_game
            # Файл end_script
            with open(f'{self.mod_name}\\mor_scripts\\{self.script_name}.txt', 'w+', encoding='utf-8') as end_script_file:
                items_game_text = items_game.read()  # Текст файла items_game
                items_game.close()  # Закрывание файла
                # Регулярные выражения для поиска необходимых аттрибутов
                model_path_expression = rf'\"model_player\"\s*\"([\s\S]*?)\"'
                custom_item_description_tag_expression = rf'\"item_description\"\s*\"([\s\S]*?)\"'
                item_name_expression = r'\"item_name\"\s*\"([\s\S]*?)\"'
                item_rarity_expression = r'\"prefab\"\s*\"([\s\S]*?)\"'
                item_slot_expression = r'\"item_slot\"\s*\"([\s\S]*?)\"'
                default_item_script = parse_script(self.default_item_name, items_game_text)
                default_model_player_path = find_only_one(expression=model_path_expression, text=default_item_script,
                                                          error='У {self.default_item_name} нет ссылки на модель')
                # Обновление регулярного выражения
                # Поиск скрипта предмета, на который заменяем
                custom_item_script = parse_script(self.custom_item_name, items_game_text)
                if self.style is not None:
                    custom_item_script = self.styles_script(custom_item_script, self.style)
                # Поиск пути до модели, на которую будем заменять
                custom_item_model_player_path = findall(model_path_expression, custom_item_script, IGNORECASE)[0]
                default_item_prefab = findall(item_rarity_expression, default_item_script, IGNORECASE + MULTILINE)[0]
                # Замены строк в скрипте
                # Поиск тега для поиска названия кастомного предмета
                with open('items_russian.txt', 'r', encoding='utf-8') as items_russian:  # Файл items_russian
                    try:
                        item_slot_default = findall(item_slot_expression, default_item_script, flags=IGNORECASE)[0]
                        item_slot_custom = findall(item_slot_expression, custom_item_script, flags=IGNORECASE)[0]
                        custom_item_script = custom_item_script.replace(item_slot_custom, item_slot_default)
                    except IndexError:
                        pass
                    items_russian_text = items_russian.read()  # Текст файла items_russian
                    # Изменение названия предмета
                    item_name_tag = findall(item_name_expression, custom_item_script)[0]
                    item_name_tag = item_name_tag.replace('#', '')
                    custom_item_item_name_exp = rf"\"{item_name_tag}\"\s*?\"([\s\S]*?)\""
                    custom_item_item_name = findall(custom_item_item_name_exp, items_russian_text, IGNORECASE)[0]
                    custom_item_script = custom_item_script.replace('#' + item_name_tag, custom_item_item_name)
                    custom_item_script = custom_item_script.replace('wearable', default_item_prefab)
                    custom_item_script = custom_item_script.replace(self.custom_item_name, self.default_item_name, 1)
                    custom_item_script = custom_item_script.replace(custom_item_model_player_path, default_model_player_path)
                    print(custom_item_item_name, item_name_tag)
                    try:
                        # Поиск описания вещи
                        custom_item_description_tag = findall(custom_item_description_tag_expression, custom_item_script, IGNORECASE)[0]
                        custom_item_description_tag = custom_item_description_tag.replace('#', '')
                        custom_item_description_expression = rf"\"{custom_item_description_tag}\"\s*?\"([\s\S]*?)\""
                        custom_item_description = findall(custom_item_description_expression, items_russian_text, IGNORECASE)[0]
                        del custom_item_description_tag_expression
                        custom_item_script = custom_item_script.replace('#' + custom_item_description_tag, custom_item_description)
                    except IndexError:
                        print(f'У {self.custom_item_name} нет описания')
                # Поиск партиклов
                particles = findall(r'\"type\"\s*\"particle\"\s*?\"asset\"\s*?(\"[\s\S]*?\")\s*\"modifier\"\s*?(\"[\s\S]*?\")', custom_item_script)
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
        styles = findall(r'^\s*?\"styles\"[\s\S]*?^\t\t\t\t}', text, MULTILINE)[0]
        styles_count = len(findall(r'\"\d*\"\s*{', styles))
        new_model_exp = r'\"' + f'{style}' + r'\"[\s\S]*?\"model_player\"\s*?\"([\s\S]*?)\"\s*?[\s\S]*?}'
        try:
            new_model = findall(new_model_exp, styles)[0]
            old_model = findall(r'\"model_player\"\s*?\"([\s\S]*?)\"', text)[0]
            text = text.replace(styles, '')
            text = text.replace(old_model, new_model)
        except IndexError:
            text = text.replace(styles, '')
        for i in range(0, styles_count):
            if i != style:
                expression = r'\"asset[^}]*?\"[^}]*?\"style\"\s*?\"' + f'{i}' + r'\"[^}]*?}'
                asset_modifiers_delete = findall(expression, text)
                for delete in asset_modifiers_delete:
                    text = text.replace(delete, '')
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