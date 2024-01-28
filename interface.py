import dearpygui.dearpygui as dpg
from mod import Mods, CreateMod
from yaml import dump, load, Loader
from datetime import datetime
from functions import ParseError, create_mod_directories
from shutil import rmtree, make_archive
from os import path
import ctypes

myappid = 'kynomi.SD2MC' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def change_language(sender, app_data, user_data):
    with open('config.yaml', 'r') as config:
        data = load(config, Loader=Loader)
        data['language'] = app_data
    with open('config.yaml', 'w') as config:
        dump(data, config)
    result = message_box(user_data, 0)


def message_box(message, style):
    return ctypes.windll.user32.MessageBoxW(0, message, '', style)


def change_vpk_path(sender, app_data):
    print(app_data)
    with open('config.yaml', 'r') as config:
        data = load(config, Loader=Loader)
    with open('config.yaml', 'w', encoding='utf-8') as config_file:
        path = app_data['file_path_name'] + '\\game\\dota\\pak01_dir.vpk'
        data['vpk_path'] = path
        dump(data, config_file)
        dpg.configure_item('vpk_path', default_value=path)


def save_init():
    dpg.save_init_file("dpg.ini")


def reload(mods):
    """Перезагрузка всех combobox"""
    mod_names = list(mods.mods.keys())
    dpg.configure_item('itm_combobox', items=mod_names)
    dpg.configure_item('mod_name_combo', items=mod_names)


def reload_mod_name(sender, app_data, mods):
    """Функция отвечающая за обновление combobox'ов во вкладке изменение конфигурации модов.
    При выборе названия мода обновляются предметы и стили"""
    items = mods.get_mod_items(app_data)
    custom_items = []
    styles = []
    for i in items:
        custom_items.append(i[1])
        styles.append(f'{i[1]}({i[2]})'.replace('None', 'Отсутствует'))
    dpg.configure_item('custom_itm_combo', items=custom_items)
    dpg.configure_item('styles_itm_combo', items=styles)


def mods_information(sender, app_data, user_data):
    dpg.delete_item('mod_info_table')
    with dpg.table(tag='mod_info_table', parent='mod_info_child_window'):
        dpg.add_table_column(label='Стандартный предмет')
        dpg.add_table_column(label='Скин')
        dpg.add_table_column(label='Стиль')
        for item in user_data.get_mod_items(app_data):
            with dpg.table_row():
                style = item[2]
                if style is None:
                    style = 'Отсутствует'
                dpg.add_text(f'{item[0]}')
                dpg.add_text(f'{item[1]}')
                dpg.add_text(f'{style}')


def show_window(sender, app_data, user_data):
    dpg.configure_item(user_data, show=True)


def add_mods(sender, app_data, mods):
    """Добавление предмета в модификацию"""
    mod_name = dpg.get_value('mod_name_input')
    if not mod_name.strip() == '':
        custom_item = dpg.get_value('custom_itm_input')
        style = dpg.get_value('style_itm_input')
        if not (dpg.get_value('style_itm_checkbox') and style.strip() != ''):
            style = None
        dpg.set_value('custom_itm_input', '')
        dpg.set_value('style_itm_input', '')
        dpg.set_value('mod_name_input', mod_name)
        dpg.set_value('style_itm_checkbox', False)
        try:
            mods.append_mod(custom_item=custom_item, style=style, mod_name=mod_name)
            reload(mods)
        except ParseError as e:
            message_box(str(e), 0)
    else:
        message_box('Введите название модификации', 0)


def clear_change_mod_inputs(new_mod_name, mods):
    dpg.set_value('chg_mod_name', value='')
    dpg.set_value('chg_custom_itm', value='')
    dpg.set_value('chg_style_itm', value='')
    dpg.configure_item(item='mod_name_combo', default_value=new_mod_name)
    dpg.configure_item(item='custom_itm_combo', default_value='')
    dpg.configure_item(item='styles_itm_combo', default_value='')
    reload_mod_name(sender='', app_data=new_mod_name, mods=mods)


def change_mod_info(sender, app_data, user_data):
    old_mod_name = dpg.get_value('mod_name_combo')
    if not old_mod_name.strip() == '':
        old_custom_item = dpg.get_value('custom_itm_combo')
        old_style = dpg.get_value('styles_itm_combo')
        if old_style.strip() == '':
            old_style = None
        new_mod_name = dpg.get_value('chg_mod_name')
        new_custom_item = dpg.get_value('chg_custom_itm')
        new_style = dpg.get_value('chg_style_itm')
        if new_mod_name.strip() == '':
            new_mod_name = None
        if new_custom_item.strip() == '' or new_custom_item == old_custom_item:
            new_custom_item = None
        if new_style.strip() == '':
            new_style = None
        try:
            user_data.change_mod(mod_name=old_mod_name, custom_item=old_custom_item, style=old_style,
                                 new_mod_name=new_mod_name, new_custom_item=new_custom_item,
                                 new_style=new_style)
        except ParseError as e:
            message_box(str(e), 0)
        reload(user_data)
        if dpg.get_value('itm_combobox') == old_mod_name:
            if not new_mod_name:
                mods_information(None, old_mod_name, user_data)
            else:
                mods_information(None, new_mod_name, user_data)

        if new_mod_name is None:
            new_mod_name = old_mod_name
        clear_change_mod_inputs(new_mod_name=new_mod_name, mods=user_data)


def delete_style(sender, app_data, user_data):
    custom_item = dpg.get_value('styles_itm_combo').split('(')[0]
    mod_name = dpg.get_value('mod_name_combo')
    user_data.delete_style(custom_item=custom_item, mod_name=mod_name)


def delete_mod(sender, app_data, user_data):
    mod_name = dpg.get_value('mod_name_combo')
    item_name = dpg.get_value('custom_itm_combo')
    if item_name.strip() != '' and mod_name.strip() != '':
        user_data.delete_mod(mod_name=mod_name, item_name=item_name)
    clear_change_mod_inputs(mod_name, user_data)
    if mod_name == dpg.get_value('itm_combobox'):
        mods_information(None, mod_name, user_data)


def save_mods_configuration(sender, app_data, user_data):
    data = user_data.get_mods()
    filename = f'{datetime.now():%d.%m.%y-%H_%M}.mds'
    print(filename)
    with open(filename, 'w') as mod_save:
        dump(data, mod_save)


def load_mod_configuration(sender, app_data, user_data):
    with open(app_data['file_path_name'], 'r') as mod_save_file:
        mods_info = load(mod_save_file, Loader=Loader)
        for mod_name, items in mods_info.items():
            for item in items:
                default_item = item[0]
                custom_item = item[1]
                style = item[2]
                user_data.append_mod(mod_name=mod_name, default_item=default_item, custom_item=custom_item, style=style)
    reload(user_data)


def create_mods(sender, app_data, user_data):
    mods_data = user_data.get_mods()
    with open('config.yaml', 'r') as config_file:
        vpk_path = load(config_file, Loader=Loader)['vpk_path']
    for mod_name, items in mods_data.items():
        create_mod_directories(mod_name)
        script_number = 1
        for item in items:
            default_item = item[0]
            custom_item = item[1]
            style = item[2]
            try:
                CreateMod(default_item, custom_item, mod_name, script_number, vpk_path, style)
                script_number += 1
            except ParseError:
                print(f'{mod_name} create failed')
        make_archive(mod_name, 'zip', mod_name)
        if path.isdir(mod_name):
            rmtree(mod_name)
    message_box('Модификации успешно созданы', 0)


def main_app(lang_file):
    mods = Mods()
    dpg.create_context()
    with open(lang_file, 'r', encoding='utf-8') as language_config:
        names = load(language_config, Loader=Loader)
        for k, v in names.items():
            names[k] = v[0].upper() + v[1:]
    dpg.add_file_dialog(directory_selector=True, tag='directory_selector', show=False,
                        default_path='C:/', width=600, height=300, callback=change_vpk_path)

    with dpg.file_dialog(directory_selector=False, tag='mod_selector', show=False, width=600, height=300, callback=load_mod_configuration, user_data=mods):
        dpg.add_file_extension('.mds', custom_text='mod save')

    with dpg.font_registry():
        big_start = 0x00C0
        small_start = 0x00E0
        replace_start_big = 0x0410
        replace_start_small = 0x0430
        with dpg.font('Resources/fonts/Roboto-Bold.ttf', 15, default_font=True) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            for i in range(0, 32):
                dpg.add_char_remap(big_start + i, replace_start_big + i)
                dpg.add_char_remap(small_start + i, replace_start_small + i)

    dpg.bind_font(default_font)

    with dpg.viewport_menu_bar():
        with dpg.menu(label=names['#menu_files']):
            dpg.add_menu_item(label=names['#create_mod'], callback=create_mods, user_data=mods)
            dpg.add_menu_item(label=names['#save_mod_config'], callback=save_mods_configuration, user_data=mods)
            dpg.add_menu_item(label=names['#load_mod_config'], callback=lambda: dpg.show_item('mod_selector'))
            dpg.add_menu_item(label=names['#settings'], callback=show_window, user_data='settings_window')
        with dpg.menu(label=names['#menu_tabs']):
            dpg.add_menu_item(label=names['#add_mods_tab'], callback=show_window, user_data='mods_window')
            dpg.add_menu_item(label=names['#mods_config_tab'], callback=show_window, user_data='config_mods_window')
            dpg.add_menu_item(label=names['#save_tabs_config'], callback=save_init)

    with dpg.window(label=names['#add_mods_tab'], width=600, height=400, tag='mods_window', no_resize=False):
        dpg.add_input_text(label=names['#skin_itm_name'], width=180, tag='custom_itm_input')
        with dpg.group(horizontal=True):
            dpg.add_input_text(label=names['#style'], width=180, tag='style_itm_input')
            dpg.add_checkbox(tag='style_itm_checkbox')
        dpg.add_input_text(label=names['#mod_name'], width=180, tag='mod_name_input')
        dpg.add_button(label=names['#add_mods_btn'], user_data=mods, callback=add_mods, width=180)
        with dpg.child_window(label='Информация о модификациях', tag='mod_info_child_window'):
            dpg.add_combo(items=[], tag='itm_combobox', callback=mods_information, user_data=mods)
            with dpg.table(tag='mod_info_table'):
                dpg.add_table_column(label=names['#standart_itm_name'])
                dpg.add_table_column(label=names['#skin_itm_name'])
                dpg.add_table_column(label=names['#style'])

    with dpg.window(label=names['#mods_config_tab'], width=600, height=200, tag='config_mods_window', pos=[600, 0]):
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='mod_name_combo', width=200, callback=reload_mod_name, user_data=mods)
            dpg.add_input_text(label=names['#mod_name'], width=200, tag='chg_mod_name')
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='custom_itm_combo', width=200)
            dpg.add_input_text(width=200, label=names['#skin_itm_name'], tag='chg_custom_itm')
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='styles_itm_combo', width=200)
            dpg.add_input_text(width=200, label=names['#style'], tag='chg_style_itm')
            dpg.add_button(label=names['#delete_style_btn'], callback=delete_style, user_data=mods)
        with dpg.group(horizontal=True):
            dpg.add_button(label=names['#change_mod_config_btn'], callback=change_mod_info, user_data=mods)
            dpg.add_button(label=names['#delete_item_from_mod_btn'], callback=delete_mod, user_data=mods)

    with dpg.window(label=names['#settings'], tag='settings_window', show=False, width=600, height=200):
        with open('config.yaml', 'r', encoding='utf-8') as config_file:
            vpk_path = load(config_file, Loader=Loader)['vpk_path']
        dpg.add_text(default_value=vpk_path, tag='vpk_path')
        dpg.add_button(label=names['#change_path_btn'], callback=lambda: dpg.show_item('directory_selector'))
        with dpg.group(horizontal=True):
            dpg.add_text(default_value=names['#select_lang'])
            dpg.add_combo(items=['en', 'ru'], callback=change_language, user_data=names['#change_lang_notif'])
    del names
    dpg.create_viewport(title='SD2MC', width=1280, height=720)
    dpg.configure_app(init_file='dpg.ini')
    dpg.set_viewport_small_icon('Resources/images/icon.ico')
    dpg.set_viewport_large_icon('Resources/images/icon.ico')
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
