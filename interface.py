import dearpygui.dearpygui as dpg
from mod import Mods


def save_init():
    dpg.save_init_file("dpg.ini")


def reload(mods):
    """Перезагрузка всех combobox"""
    mod_names = list(mods.mods.keys())
    dpg.configure_item('itm_combobox', items=mod_names)
    dpg.configure_item('mod_name_combo', items=mod_names)


def reload_mod_name(sender, app_data, mods):
    items = mods.get_mod_items(app_data)
    default_items = []
    custom_items = []
    styles = []
    for i in items:
        default_items.append(i[0])
        custom_items.append(i[1])
        styles.append(f'{i[1]}({i[2]})'.replace('None', 'Отсутствует'))
    dpg.configure_item('default_itm_combo', items=default_items)
    dpg.configure_item('custom_itm_combo', items=custom_items)
    dpg.configure_item('styles_itm_combo', items=styles)


def mods_information():
    pass


def show_window(sender, app_data, user_data):
    dpg.configure_item(user_data, show=True)


def add_mods(sender, app_data, mods):
    """Добавление предмета в модификацию"""
    default_item = dpg.get_value('default_itm_input')
    custom_item = dpg.get_value('custom_itm_input')
    style = dpg.get_value('style_itm_input')
    if not (dpg.get_value('style_itm_checkbox') and style.strip() != ''):
        style = None
    mod_name = dpg.get_value('mod_name_input')
    dpg.set_value('default_itm_input', '')
    dpg.set_value('custom_itm_input', '')
    dpg.set_value('style_itm_input', '')
    dpg.set_value('mod_name_input', mod_name)
    dpg.set_value('style_itm_checkbox', False)
    mods.append_mod(default_item=default_item, custom_item=custom_item, style=style, mod_name=mod_name)
    reload(mods)


def main_app():
    mods = Mods()
    dpg.create_context()
    dpg.configure_app(init_file='dpg.ini')

    with dpg.font_registry():
        big_start = 0x00C0
        small_start = 0x00E0
        replace_start_big = 0x0410
        replace_start_small = 0x0430
        with dpg.font('Roboto/Roboto-Bold.ttf', 15, default_font=True) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            for i in range(0, 32):
                dpg.add_char_remap(big_start + i, replace_start_big + i)
                dpg.add_char_remap(small_start + i, replace_start_small + i)

    dpg.bind_font(default_font)

    with dpg.viewport_menu_bar():
        with dpg.menu(label='Файл'):
            dpg.add_menu_item(label='Сохранить конфигурацию модов')
            dpg.add_menu_item(label='Загрузить конфигурацию модов')
            dpg.add_menu_item(label='Настройки')
        with dpg.menu(label='Вкладки'):
            dpg.add_menu_item(label='Добавить модификации', callback=show_window, user_data='mods_window')
            dpg.add_menu_item(label='Конфигурация Модификаций', callback=show_window, user_data='config_mods_window')
            dpg.add_menu_item(label='Сохранить конфигурацию вкладок', callback=save_init)

    with dpg.window(label='Добавить модификации', width=600, height=400, show=False, tag='mods_window', no_resize=True):
        dpg.add_input_text(label='Название стандартного предмета', width=150, tag='default_itm_input')
        dpg.add_input_text(label='Название скина', width=150, tag='custom_itm_input')
        with dpg.group(horizontal=True):
            dpg.add_input_text(label='Стиль', width=150, tag='style_itm_input')
            dpg.add_checkbox(tag='style_itm_checkbox')
        dpg.add_input_text(label='Название модификации', width=150, tag='mod_name_input')
        dpg.add_button(label='Добавить модификацию', user_data=mods, callback=add_mods)
        with dpg.child_window(label='Информация о модификациях'):
            dpg.add_combo(items=[], tag='itm_combobox', callback=mods_information)
            dpg.add_text()

    with dpg.window(label='Изменить конфигурацию модификаций', width=600, height=400, show=False, tag='config_mods_window', pos=[600, 0]):
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='mod_name_combo', width=200, callback=reload_mod_name, user_data=mods)
            dpg.add_input_text(label='Название модификации', width=200)
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='default_itm_combo', width=200)
            dpg.add_input_text(width=200, label='Стандартный предмет')
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='custom_itm_combo', width=200)
            dpg.add_input_text(width=200, label='Скин')
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='styles_itm_combo', width=200)
            dpg.add_input_text(width=200, label='Стиль')
            dpg.add_button(label='Удалить стиль')
        with dpg.group(horizontal=True):
            dpg.add_button(label='Изменить конфигурацию модов')
    dpg.create_viewport(title='Custom Title', width=1280, height=720)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
