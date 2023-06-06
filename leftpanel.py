import re
from tkinter import END, DISABLED, NORMAL
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
class FileEditorWidget(ScrolledText):
    def __init__(self, master=None, file_path=None, open_func=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Double-Button-1>', self.on_double_click)

        self.config(state=DISABLED)
        self.open_func=open_func
        if file_path is not None:
            self.open_directory(file_path)
        self.tag_configure("no_select", selectbackground="white", selectforeground="black")

    def open_directory(self, file_path):
        self.config(state=NORMAL)
        self.file_path=file_path
        #print(f'Открытие папки: {file_path}')
        # Очистка текущего содержимого виджета
        self.delete(1.0, END)
        # Получение списка папок и файлов в указанной директории
        folder = Path(file_path)
        folders = [item.name for item in folder.iterdir() if item.is_dir()]
        files = [item.name for item in folder.iterdir() if item.is_file()]

        #print(f'Папка: {folder}')
        #print(f'Папки: {folders}')
        #print(f'Файлы: {files}')
        # Вывод основной папки
        self.insert(END, folder.name + '\n', "no_select")

        # Вывод папок и файлов
        for subfolder in folders:
            self.insert(END, '\t' +u"\U0001F4C1"+ subfolder + '\n', "no_select")

        for file in files:
            self.insert(END, '\t' +	u"\U0001F4C4"+ file + '\n', "no_select")

        self.config(state=DISABLED)

    def remove_emoji(self, text):
        return re.sub(r'[^\w\s#@/:%.,_-]', '', text)
    def on_double_click(self, event):
        #удаляем выделение(не работает)
        self.tag_remove("sel", "1.0", "end")
        # Получение координат клика мыши и определение, какой элемент был выбран
        x, y = event.x, event.y
        index = self.index(f'@{x},{y}')
        line = int(index.split('.')[0])
        element = self.get(f'{line}.0', f'{line}.end')
        element= self.remove_emoji(element)
        # Если элемент является файлом с расширением .py, вызываем функцию открытия файла
        if element.endswith('.pacl'):
            element=element.lstrip()
            #print(f'Открытие файла: {element}')
            path=self.file_path+'/'+element
            self.open_func(open_path=path)
