import tkinter
from tkinter import ttk
# Это простой файл струтуры, для структурирования данных в болнн удобном виде


class Styles(ttk.Style):
    def __init__(self, *args, **kwargs):
        super(Styles, self).__init__(*args, **kwargs)
        mystyle = super()
        #TScrollBar style
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
        mystyle.theme_use("MyAppStyle")
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


class ModItems:
    def __init__(self):
        self.mod_names = []
        self.custom_items = []
        self.default_items = []

    def add_items(self, mod_name, custom_items, default_items):
        if mod_name not in self.mod_names:
            self.mod_names.append([mod_name])
            self.custom_items.append([custom_items])
            self.default_items.append([default_items])
        else:
            index = self.mod_names.index(mod_name)
            self.custom_items[index].append(custom_items)
            self.default_items[index].append(default_items)

    def get_mod(self, index):
        if type(index) == int:
            index = index
        elif type(index) == str:
            index = self.mod_names.index(index)
        else:
            return None
        return self.custom_items[index], self.default_items[index]

    def get_mod_name(self, index):
        return self.mod_names[index]

    def change_custom_item(self, old, new, mod_name):
        index = self.mod_names.index(mod_name)
        for i in self.custom_items[index]:
            if i == old:
                index_old = self.custom_items[index].index(i)
                self.custom_items[index][index_old] = new
                break

    def change_default_item(self, old, new, mod_name):
        index = self.mod_names.index(mod_name)
        for i in self.default_items[index]:
            if i == old:
                index_old = self.default_items[index].index(i)
                self.default_items[index][index_old] = new
                break

    def change_mod_name(self, old, new):
        for i in range(0, len(self.mod_names)):
            if self.mod_names[i] == old:
                self.mod_names[i] = new
                break

    def mods_count(self):
        return len(self.mod_names)


class ScrollTextBox(ttk.Frame):
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
    def __init__(self, *args, **kwargs):
        super(AddMods, self).__init__(*args, **kwargs)
        self.combobox_values = []
        self.text_strings = []
        #style
        style = Styles()
        style.theme_use("MyAppStyle")
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
        self.mod_info_choose_mod = ttk.Combobox(self, font=('Roboto/Roboto_Bold.ttf', '20', 'bold'), state='readonly')
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.font', ('Roboto/Roboto_Bold.ttf', '20', 'bold'))
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.background', "#3d3d40")
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.foreground', "#9c9c9f")
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.selectBackground', "#33393f")
        self.mod_info_choose_mod.option_add('*TCombobox*Listbox.selectForeground', "white")
        self.mod_info_choose_mod.bind("<<ComboboxSelected>>", self.combobox_current_value)
        self.place()

    def place(self):
        # Placing
        # mod_info_sizes
        self.mod_info.update()
        mod_info_height = 7
        self.mod_info.txt.configure(height=mod_info_height)
        sizes = self.mod_info.get_sizes()
        mod_info_size_x = sizes[0][0]+sizes[2][0]
        mod_info_size_y = sizes[0][1]+sizes[1][1]
        margin = (mod_info_size_y - 3*self.mod_name_field.winfo_reqheight()) // 2
        mod_info_x = self.winfo_reqwidth() - mod_info_size_x
        max_text_width = max(max(self.standart_item_label.winfo_reqwidth(), self.custom_item_label.winfo_reqwidth()), self.mod_name_label.winfo_reqwidth())
        custom_item_y = max(self.standart_item_label.winfo_reqheight(), self.standart_item_field.winfo_reqheight()) + margin
        mod_name_y = custom_item_y + margin + max(self.custom_item_label.winfo_reqheight(), self.custom_item_field.winfo_reqheight())
        confirm_button_y = mod_name_y + margin + max(self.mod_name_label.winfo_reqheight(), self.mod_name_field.winfo_reqheight())
        labels_x = 15
        fields_x = max_text_width+15+labels_x
        add_mods_confirmation_button_size_x = fields_x - labels_x + self.mod_name_field.winfo_reqwidth()
        mod_info_choose_mod_x = (mod_info_x - self.mod_info_choose_mod.winfo_reqwidth()) // 2 + mod_info_x
        self.add_mods_confirmation_button.place(x=labels_x, y=confirm_button_y, width=add_mods_confirmation_button_size_x)
        self.configure(height=confirm_button_y+self.add_mods_confirmation_button.winfo_reqheight())
        self.standart_item_label.place(x=labels_x, y=0)
        self.custom_item_label.place(x=labels_x, y=custom_item_y)
        self.mod_name_label.place(x=labels_x, y=mod_name_y)
        self.standart_item_field.place(x=fields_x, y=0)
        self.custom_item_field.place(x=fields_x, y=custom_item_y)
        self.mod_name_field.place(x=fields_x, y=mod_name_y)
        self.mod_info.place(x=mod_info_x, y=0)
        self.mod_info_choose_mod.place(x=mod_info_choose_mod_x, y=confirm_button_y)

    def add_mod_info(self, new_mod_name,  new_default_item, new_custom_item):
        strings = f'{new_default_item} : {new_custom_item}'
        index = None
        if not new_mod_name in self.combobox_values:
            self.combobox_values.append(new_mod_name)
            self.text_strings.append([strings])
            index = self.combobox_values.index(new_mod_name)
        else:
            index = self.combobox_values.index(new_mod_name)
            if strings not in self.text_strings[index]:
                self.text_strings[index].append(strings)
        self.mod_info_choose_mod.configure(values=self.combobox_values)
        self.mod_info_choose_mod.current(index)
        self.combobox_current_value()

    def combobox_current_value(self, event=None):
        selection = self.mod_info_choose_mod.get()
        string = '\n'.join(self.text_strings[self.combobox_values.index(selection)])
        self.mod_info.txt.configure(state='normal')
        self.mod_info.txt.delete('0.0', tkinter.END)
        self.mod_info.txt.insert('end', string)
