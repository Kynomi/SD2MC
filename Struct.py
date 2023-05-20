import tkinter
from tkinter import ttk
import yaml
"""Это файл структуры проекта, здесь находятся классы вкладок и структур данных"""


class Styles(ttk.Style):
    """Класс стилей проекта"""
    def __init__(self, *args, **kwargs):
        super(Styles, self).__init__(*args, **kwargs)
        mystyle = super()
        # TScrollBar style
        mystyle.theme_create("MyAppStyle", parent="alt", settings={
            "TNotebook": {"configure": {"background": "#212224",
                                        "borderwidth": "0",
                                        "tabmargins": [0, 0, 0, 0]}},
            "TNotebook.Tab": {"configure": {"padding": ["26", "15"],
                                            "font": ('Roboto/Roboto_Bold.ttf', '20', 'bold'),
                                            "foreground": "#a9b2b7",
                                            "tabsmargin": [0, 0, 0, 0],
                                            "background": "#28292c",
                                            "borderwidth": "0",
                                            "focuscolor": "#212224"},
                              "map": {"background": [('active', '#2f3634'), ('selected', '#212224')],
                                      "foreground": [('active', "#a8b8a6"), ('selected', "#81878b")],
                                      "focuscolor": [('active', "#2f3634")]}}})
        # TButton
        mystyle.theme_settings("MyAppStyle", settings={
            "TButton": {"configure": {"background": "#33393f",
                                      "foreground": "#9ca9a2",
                                      "font": ('Roboto/Roboto_Bold.ttf', '20', 'bold'),
                                      "padding": ["26", "12"]},
                        "map": {"background": [('pressed', '#16232d')],
                                "foreground": [('pressed', '#82978c')]},
                        "layout": [('Button.border', {'sticky': 'nswe', 'border': '1', 'children':
                            [('Button.padding', {'sticky': 'nswe', 'children':
                                [('Button.label', {'sticky': 'nswe'})]})]})]}})
        # Tlabel
        mystyle.theme_settings("MyAppStyle", settings={
            "TLabel": {"configure": {"foreground": "#6f767c",
                                     "background": "#1f1f1f",
                                     "font": ('Roboto/Roboto_Bold.ttf', '18', 'bold')},
                       "layout": [('Label.label', {'sticky': 'nswe'})]}})
        # TFrame
        mystyle.theme_settings("MyAppStyle", settings={
            "TFrame": {"configure": {"background": "#1f1f1f"}}})
        # TEntry
        mystyle.theme_settings("MyAppStyle", settings={
            "TEntry": {"configure": {"background": "#3d3d40",
                                     "relief": tkinter.FLAT,
                                     "bordercolor": "#000000",
                                     "foreground": "#7e7e80"},
                       "layout": [('Entry.highlight', {'sticky': 'nswe', 'children':
                           [('Entry.border', {'border': '1', 'sticky': 'nswe', 'children':
                               [('Entry.padding', {'sticky': 'nswe', 'children':
                                   [('Entry.textarea', {'sticky': 'nswe'})]})]})]})]}})
        # TCombobox
        mystyle.theme_settings("MyAppStyle", settings={
            "Arrowless.Vertical.scrollbar": {"layout": [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children': [
                ('Vertical.Scrollbar.thumb', {'sticky': 'nswe'})]})],
                                             "configure": {"background": "#525252",
                                                           "relief": tkinter.FLAT,
                                                           "troughrelief": tkinter.FLAT,
                                                           "troughcolor": "#9f9f9f",
                                                           "troughborderwidth": "0"}}})
        mystyle.theme_settings("MyAppStyle", settings={
            "Arrowless.Horizontal.scrollbar": {"layout": [('Horizontal.Scrollbar.trough', {'sticky': 'nswe', 'children':
                [('Horizontal.Scrollbar.thumb', {'sticky': 'nswe'})]})],
                                               "configure": {"background": "#525252",
                                                             "relief": 'flat',
                                                             "troughrelief": 'flat',
                                                             "troughcolor": "#9f9f9f",
                                                             "troughborderwidth": "0"
                                                             }}})
        mystyle.theme_settings("MyAppStyle", settings={
            "TCombobox": {"configure": {"background": "#3d3d40",
                                        "foreground": "#9c9c9f",
                                        "arrowcolor": "#9c9c9f",
                                        "fieldbackground": "#3d3d40",
                                        "relief": "flat",
                                        "arrowsize": 15},
                          "layout": [('Entry.textarea', {'sticky': 'nswe', 'children':
                              [('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'})]})]},
            "TScrollbar": {"configure": {"background": "#525252",
                                         "foreground": "#0000ee",
                                         "troughcolor": "#9f9f9f",
                                         "relief": "flat",
                                         "arrowcolor": "#9f9f9f"},
                           "layout": [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children': [
                               ('Vertical.Scrollbar.thumb', {'sticky': 'nswe'})]})]}})
        # Header
        mystyle.theme_settings("MyAppStyle", settings={
            'Header.TFrame': {"configure": {"background": "#2a2c2e"}}})
        # TCheckButton
        mystyle.theme_settings("MyAppStyle", settings={
            'TCheckbutton': {"configure": {"font": ('Roboto/Roboto_Bold.ttf', '18', 'bold'),
                                           "focuscolor": "#1f1f1f",
                                           "background": "#1f1f1f",
                                           "foreground": "#7e7e80",
                                           "indicatorcolor": "#474748",
                                           "shadecolor": "#474748",
                                           'lightcolor': '#474748',
                                           "relief": tkinter.FLAT,
                                           "shiftrelief": tkinter.FLAT}}})
        mystyle.theme_use("MyAppStyle")


class Item:
    """Класс предмета"""
    def __init__(self, default_item, custom_item, style):
        self.default_item = default_item
        self.custom_item = custom_item
        self.style = style

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
    
    def change_mod(self, **mod_info):
        """Функция отвечающая за изменение модификации"""
        default_item = mod_info['default_item']
        custom_item = mod_info['custom_item']
        style = mod_info['style']
        new_default_item = mod_info['new_default_item']
        new_custom_item = mod_info['new_custom_item']
        new_style = mod_info['new_style']
        if style is not None:
            style_index = style.split('(')[0]
            style = style.split('(')[1].replace(')', '')
        if style == 'None':
            style = None
        for item in self.items:
            if new_default_item is not None:
                if item.default_item == default_item:
                    item.default_item = new_default_item
            if new_custom_item is not None:
                if item.custom_item == custom_item:
                    if style is not None:
                        if item.custom_item != style_index:
                            item.custom_item = new_custom_item
                        else:
                            item.custom_item = new_custom_item
                            item.style = new_style
                    else:
                        item.custom_item = new_custom_item
            if new_style is not None:
                if item.style == style and item.custom_item == style_index:
                    item.style = new_style


class Mods:
    """Класс списка модов"""
    def __init__(self):
        self.mods = {}

    def append_mod(self, **mod_info):
        """Добавляет мод в список модов"""
        mod_name = mod_info['mod_name']
        default_item = mod_info['default_item']
        custom_item = mod_info['custom_item']
        style = mod_info['style']
        if mod_name in self.mods.keys():
            self.mods[mod_name].append_item(default_item, custom_item, style)
        else:
            self.mods[mod_name] = Mod(mod_name)
            self.mods[mod_name].append_item(default_item, custom_item, style)

    def reload(self):
        """Возвращает список модов для обновления данных"""
        mods = {}
        for mod_name, mod in self.mods.items():
            items = mod.get_items()
            mods[mod_name] = items
        return mods

    def change_mod(self, **mod_info):
        """Функция отвечающая за изменение модификации"""
        mod_name = mod_info['mod_name']
        default_item = mod_info['default_item']
        custom_item = mod_info['custom_item']
        style = mod_info['style']
        new_mod_name = mod_info['new_mod_name']
        new_default_item = mod_info['new_default_item']
        new_custom_item = mod_info['new_custom_item']
        new_style = mod_info['new_style']
        for key, mod in self.mods.items():
            if key == mod_name:
                mod.change_mod(default_item=default_item, custom_item=custom_item,
                               style=style, new_default_item=new_default_item,
                               new_custom_item=new_custom_item, new_style=new_style)
                break
        if new_mod_name is not None:
            self.mods[new_mod_name] = self.mods.pop(mod_name)


class ScrollTextBox(ttk.Frame):
    """Класс содержит в себе виджет для отображения информации"""
    def __init__(self, *args, **kwargs):
        super(ScrollTextBox, self).__init__(*args, **kwargs)
        self.yscroll = ttk.Scrollbar(self, orient=tkinter.VERTICAL)
        self.xscroll = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL)
        self.txt = tkinter.Text(self, wrap=tkinter.NONE)
        self.txt.configure(xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set, state='disabled')
        self.yscroll.configure(command=self.txt.yview)
        self.xscroll.configure(command=self.txt.xview)
        self.txt.grid(row=0, column=0, sticky='nsew')
        self.xscroll.grid(row=1, column=0, columnspan=1, sticky='nsew')
        self.yscroll.grid(row=0, column=1, rowspan=1, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def get_sizes(self):
        txt_sizes = (self.txt.winfo_reqwidth(), self.txt.winfo_reqheight())
        scroll_x_sizes = (self.xscroll.winfo_reqwidth(), self.xscroll.winfo_reqheight())
        scroll_y_sizes = (self.yscroll.winfo_reqwidth(), self.yscroll.winfo_reqheight())
        return txt_sizes, scroll_x_sizes, scroll_y_sizes


class AddMods(ttk.Frame):
    """Вкладка добавления модов"""
    def __init__(self, *args, **kwargs):
        super(AddMods, self).__init__(*args, **kwargs)
        self.combobox_values = []
        self.strings = []
        # Lables
        self.standart_item_label = ttk.Label(self, text='Стандартная Вещь')
        self.custom_item_label = ttk.Label(self, text='Название вещи скина')
        self.mod_name_label = ttk.Label(self, text='Название модификации')
        # Entry
        self.standart_item_field = ttk.Entry(self, width=20, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.custom_item_field = ttk.Entry(self, width=20, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.mod_name_field = ttk.Entry(self, width=20, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        # Button
        self.add_mods_confirmation_button = ttk.Button(self, text="Добавить модификацию в список")
        # Mod_info
        self.mod_info = ScrollTextBox(self)
        self.mod_info.xscroll.configure(style='Arrowless.Horizontal.scrollbar')
        self.mod_info.yscroll.configure(style='Arrowless.Vertical.scrollbar')
        self.mod_info.txt.configure(width=50, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'),
                                    foreground="#969698", background="#3d3d40")
        #  Combobox
        self.mod_info_choose_mod = ttk.Combobox(self, font=('Roboto/Roboto_Bold.ttf', '20', 'bold'), state='readonly')
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.font', ('Roboto/Roboto_Bold.ttf', '20', 'bold'))
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.background', "#3d3d40")
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.foreground', "#9c9c9f")
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.selectBackground', "#33393f")
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.selectForeground', "white")
        self.mod_info_choose_mod.bind("<<ComboboxSelected>>", self.reload_text)
        #  Style
        self.style_checkbox_variable = tkinter.BooleanVar()
        self.style_checkbox = ttk.Checkbutton(self, text='Стиль', variable=self.style_checkbox_variable)
        self.style_field = ttk.Entry(self, width=20, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.placing()

    def placing(self):
        """Функция располагающая элементы внутри вкладки"""
        # Placing
        # mod_info_sizes
        self.mod_info.update()
        mod_info_height = 7
        self.mod_info.txt.configure(height=mod_info_height)
        sizes = self.mod_info.get_sizes()
        mod_info_size_x = sizes[0][0] + sizes[2][0]
        mod_info_size_y = sizes[0][1] + sizes[1][1]
        margin = (mod_info_size_y - 3 * self.mod_name_field.winfo_reqheight()) // 2
        mod_info_x = self.winfo_reqwidth() - mod_info_size_x
        max_text_width = max(max(self.standart_item_label.winfo_reqwidth(), self.custom_item_label.winfo_reqwidth()),
                             self.mod_name_label.winfo_reqwidth())
        custom_item_y = max(self.standart_item_label.winfo_reqheight(),
                            self.standart_item_field.winfo_reqheight()) + margin
        mod_name_y = custom_item_y + margin + max(self.custom_item_label.winfo_reqheight(),
                                                  self.custom_item_field.winfo_reqheight())
        style_y = mod_name_y + margin + max(self.style_field.winfo_reqheight(),
                                            self.style_checkbox.winfo_reqheight())
        confirm_button_y = style_y + margin + max(self.mod_name_label.winfo_reqheight(),
                                                  self.mod_name_field.winfo_reqheight())
        labels_x = 15
        fields_x = max_text_width + 15 + labels_x
        add_mods_confirmation_button_size_x = fields_x - labels_x + self.mod_name_field.winfo_reqwidth()
        mod_info_choose_mod_x = (mod_info_x - self.mod_info_choose_mod.winfo_reqwidth()) // 2 + mod_info_x
        self.add_mods_confirmation_button.place(x=labels_x, y=confirm_button_y,
                                                width=add_mods_confirmation_button_size_x)
        self.configure(height=confirm_button_y + self.add_mods_confirmation_button.winfo_reqheight())
        self.standart_item_label.place(x=labels_x, y=0)
        self.custom_item_label.place(x=labels_x, y=custom_item_y)
        self.mod_name_label.place(x=labels_x, y=mod_name_y)
        self.standart_item_field.place(x=fields_x, y=0)
        self.custom_item_field.place(x=fields_x, y=custom_item_y)
        self.mod_name_field.place(x=fields_x, y=mod_name_y)
        self.style_field.place(x=fields_x, y=style_y)
        self.style_checkbox.place(x=labels_x, y=style_y)
        self.mod_info.place(x=mod_info_x, y=0)
        self.mod_info_choose_mod.place(x=mod_info_choose_mod_x, y=confirm_button_y)

    def get_entry(self):
        """Функция возвращающая содержимое поле ввода"""
        default_item = self.standart_item_field.get().strip()
        custom_item = self.custom_item_field.get().strip()
        mod_name = self.mod_name_field.get().strip()
        if self.style_checkbox_variable.get() == tkinter.TRUE:
            style = self.style_field.get()
            if style.strip() == '':
                style = None
        else:
            style = None

        return default_item, custom_item, mod_name, style

    def clear_entry(self):
        """Функция очищающая поля ввода"""
        self.mod_name_field.delete(0, tkinter.END)
        self.custom_item_field.delete(0, tkinter.END)
        self.standart_item_field.delete(0, tkinter.END)
        self.style_field.delete(0, tkinter.END)
        self.mod_name_field.insert(0, self.mod_info_choose_mod.get())

    def reload_text(self, event=None):
        """Функция обновляющая текст окна информации"""
        selection = self.mod_info_choose_mod.get()
        string = self.strings[self.combobox_values.index(selection)]
        self.mod_info.txt.configure(state='normal')
        self.mod_info.txt.delete('0.0', tkinter.END)
        self.mod_info.txt.insert('end', string)
        self.mod_info.txt.configure(state='disabled')

    def reload(self, new_mod_name=None):
        """Функция обновляющая информацию о модах в окне информации"""
        self.combobox_values = []
        self.strings = []
        with open('mod_info.yaml', 'r') as mod_info:
            mods = yaml.safe_load(mod_info)
            for mod_name, items in mods.items():
                self.combobox_values.append(mod_name)
                string = ''
                for item in items:
                    default_item = item[0]
                    custom_item = item[1]
                    style = item[2]
                    string += f'{default_item}:{custom_item}'
                    if style is not None:
                        string += f'({style})\n'
                    else:
                        string += '\n'
                self.strings.append(string)
        self.mod_info_choose_mod.configure(values=self.combobox_values)
        if new_mod_name is not None:
            self.mod_info_choose_mod.current(self.combobox_values.index(new_mod_name))
        self.reload_text()
        self.clear_entry()


class ConfigureMods(ttk.Frame):
    """Класс вкладки конфигурации модов"""
    def __init__(self, *args, **kwargs):
        super(ConfigureMods, self).__init__(*args, **kwargs)
        self.mod_name_combobox_value = []
        self.default_item_combobox_value = []
        self.custom_item_combobox_value = []
        self.style_combobox_value = []
        self.mod_name_label = ttk.Label(self, text="Модификация")
        self.mod_name_combobox = ttk.Combobox(self, width=32, font=('Roboto/Roboto_Bold.ttf', '20', 'bold'), state='readonly')
        self.mod_name_field = ttk.Entry(self, width=19, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.default_item_label = ttk.Label(self, text="Стандартная вещи")
        self.default_item_combobox = ttk.Combobox(self, width=32, font=('Roboto/Roboto_Bold.ttf', '20', 'bold'), state='readonly')
        self.default_item_field = ttk.Entry(self, width=19, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.custom_item_label = ttk.Label(self, text="Скин")
        self.custom_item_combobox = ttk.Combobox(self, width=32, font=('Roboto/Roboto_Bold.ttf', '20', 'bold'), state='readonly')
        self.custom_item_field = ttk.Entry(self, width=19, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.style_field = ttk.Entry(self, width=19, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.style_label = ttk.Label(self, text="Стиль")
        self.style_combobox = ttk.Combobox(self,  width=32, font=('Roboto/Roboto_Bold.ttf', '20', 'bold'), state='readonly')
        self.change_button = ttk.Button(self, text='Изменить конфигурацию мода')
        self.mod_name_combobox.bind('<<ComboboxSelected>>', self.combobox_reload)
        self.placing()

    def placing(self):
        """Функция располагающая элементы внутри вкладки"""
        # Placing objects in frame
        self.mod_name_label.grid(row=0, column=0, sticky='W', padx=15)
        self.mod_name_combobox.grid(row=0, column=1)
        self.mod_name_field.grid(row=0, column=2)
        self.default_item_label.grid(row=1, column=0, sticky='W', padx=15)
        self.default_item_combobox.grid(row=1, column=1)
        self.default_item_field.grid(row=1, column=2)
        self.custom_item_label.grid(row=2, column=0, sticky='W', padx=15)
        self.custom_item_combobox.grid(row=2, column=1)
        self.custom_item_field.grid(row=2, column=2)
        self.style_label.grid(row=3, column=0, sticky='W', padx=15)
        self.style_combobox.grid(row=3, column=1)
        self.style_field.grid(row=3, column=2)
        self.change_button.grid(row=4, column=0, columnspan=3)
        self.grid_rowconfigure(0, weight=1, pad=35)
        self.grid_rowconfigure(1, weight=1, pad=35)
        self.grid_rowconfigure(2, weight=1, pad=35)
        self.grid_rowconfigure(3, weight=1, pad=35)
        self.grid_rowconfigure(4, weight=1, pad=35)
        self.grid_columnconfigure(0, weight=1, pad=25)
        self.grid_columnconfigure(1, weight=1, pad=25)
        self.grid_columnconfigure(2, weight=1)

    def clear_entry(self):
        """Функция очищающая поля ввода"""
        self.mod_name_field.delete(0, tkinter.END)
        self.custom_item_field.delete(0, tkinter.END)
        self.default_item_field.delete(0, tkinter.END)
        self.style_field.delete(0, tkinter.END)

    def reload(self):
        self.mod_name_combobox_value = []
        self.style_combobox_value = []
        self.custom_item_combobox_value = []
        self.default_item_combobox_value = []
        self.default_item_combobox['value'] = []
        self.custom_item_combobox['value'] = []
        self.mod_name_combobox['value'] = []
        self.style_combobox['value'] = []
        self.default_item_combobox.set('')
        self.custom_item_combobox.set('')
        self.mod_name_combobox.set('')
        self.style_combobox.set('')
        with open('mod_info.yaml', 'r') as mod_info:
            mods = yaml.safe_load(mod_info)
            for mod_name, mod in mods.items():
                self.mod_name_combobox_value.append(mod_name)
                mod_default_items = []
                mod_custom_items = []
                mod_styles = []
                for items in mod:
                    mod_default_items.append(items[0])
                    mod_custom_items.append(items[1])
                    mod_styles.append(f'{items[1]}({items[2]})')
                self.default_item_combobox_value.append(mod_default_items)
                self.custom_item_combobox_value.append(mod_custom_items)
                self.style_combobox_value.append(mod_styles)
        self.mod_name_combobox.configure(values=self.mod_name_combobox_value)

    def combobox_reload(self, event=None):
        index = self.mod_name_combobox_value.index(self.mod_name_combobox.get())
        self.default_item_combobox.configure(values=self.default_item_combobox_value[index])
        self.custom_item_combobox.configure(values=self.custom_item_combobox_value[index])
        self.style_combobox.configure(values=self.style_combobox_value[index])

    def get_entry(self):
        new_mod_name = self.mod_name_field.get()
        new_default_item = self.default_item_field.get()
        new_custom_item = self.custom_item_field.get()
        new_style = self.style_field.get()
        if new_mod_name.strip() == '':
            new_mod_name = None
        if new_default_item.strip() == '':
            new_default_item = None
        if new_custom_item.strip() == '':
            new_custom_item = None
        if new_style.strip() == '':
            new_style = None
        mod_name = self.mod_name_combobox.get()
        default_item = self.default_item_combobox.get()
        custom_item = self.custom_item_combobox.get()
        style = self.style_combobox.get()
        if style.strip() == '':
            style = None
        self.clear_entry()
        return [mod_name, default_item, custom_item, style, new_mod_name, new_default_item, new_custom_item, new_style]


class SettingsFrame(ttk.Frame):
    """Класс вкладки настроек"""
    def __init__(self, *args, **kwargs):
        super(SettingsFrame, self).__init__(*args, **kwargs)
        with open('config.yaml', 'r') as config:
            vpk_path = yaml.safe_load(config)['vpk_path']
        self.name_label = ttk.Label(self, text='Введите путь до доты')
        self.vpk_path_field = ttk.Entry(self, width=20, font=('Roboto/Roboto_Bold.ttf', '18', 'bold'))
        self.confirm_button = ttk.Button(self, text="Применить настройки")
        self.vpk_path_label = ttk.Label(self, text=vpk_path)
        self.placing()

    def placing(self):
        self.name_label.grid(row=0, column=0, sticky=tkinter.W, pady=50)
        self.vpk_path_field.grid(row=0, column=1, padx=50, pady=50)
        self.vpk_path_label.grid(row=1, column=0, pady=50, columnspan=2)
        self.confirm_button.grid(row=2, column=0, columnspan=3)

    def reload(self):
        with open('config.yaml', 'r') as config:
            vpk_path = yaml.safe_load(config)['vpk_path']
        self.vpk_path_label['text'] = vpk_path