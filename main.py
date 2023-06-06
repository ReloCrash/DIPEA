import math
import os
import sys
import threading
from tkinter import *
from tkinter import ttk

from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
import subprocess

import chardet as chardet

from leftpanel import FileEditorWidget
from pacode_l import PaCodeL


class Application(Tk):
    def __init__(self):
        #super().__init__()
        global text_change, pacode_l
        sfg="black"
        sbg="#EEEEEE"
        sbbg="#93A6B1"
        sddg="#EEEEEE"
        self.window = Tk()
        #print(math.cos(4))
        self.window.title("A PYTHON IDE")
        # create and configure menu
        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)

        # create editor window for writing code haveltica
        # style = ttk.Style(window)
        # style.configure('TScrollbar', background="#222831")
        self.editor = ScrolledText(self.window, font=("helvetica 12"), pady=4, wrap=None)
        # editor.pack(fill=BOTH, expand=1)

        self.editor.focus()
        # Создание виджета для нумерации строк
        self.line_number_widget = Text(self.window, font=("helvetica 12"), width=4, pady=4, takefocus=0, fg=sfg, bg=sbbg)


        self.line_number_widget.config(state=DISABLED)

        self.file_path = ""

        self.create_Mainmenu()
        self.create_PKMmenu()
        self.view_menu.add_checkbutton(label="Status Bar", onvalue=True, offvalue=0, variable=self.show_status_bar, command=self.hide_statusbar)
        self.status_bars = ttk.Label(self.window, text=" \t\t\t characters: 0 words: 0")
        #status_bars.pack(side=BOTTOM)
        self.file_bars = ttk.Label(self.window, text="")

        self.window.bind("<Control-o>", self.open_file)
        self.window.bind("<Control-s>", self.save_file)
        self.window.bind("<Control-S>", self.save_as)
        self.window.bind("<F5>", self.run)
        self.editor.bind('<KeyRelease>', self.update_line_numbers)
        self.window.bind("<Control-q>", self.close)
        self.window.bind("<Button-3>", self.show_PKMmenu)
        self.editor.bind("<<Modified>>", self.change_word)
        text_change = False
        # create output window to display output of written code
        self.output_window = ScrolledText(self.window, height=10)
        self.left_panel = FileEditorWidget(self.window, font=("helvetica 12"), width=25, open_func=self.open_file)

        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(2, weight=3)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_columnconfigure(1, weight=0)

        self.line_number_widget.grid(row=0, column=1, sticky="ns")
        self.status_bars.grid(row=2, column=2, sticky="n")
        self.file_bars.grid(row=2, column=0, sticky="nw")
        self.editor.grid(row=0, column=2, sticky="nsew")
        self.output_window.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.left_panel.grid(row=0, column=0, sticky="ns")


        self.window.geometry("+200+200")
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.light()
        self.create_Swind()
        self.window.mainloop()
        #sys.stdout.reconfigure(encoding='utf-8')


    def open_file(self, event=None, open_path=None):
        global code, file_path
        # code = editor.get(1.0, END)
        if open_path is None:
            open_path = askopenfilename(filetypes=[("Pacole File", "*.pacl")])
        file_path = open_path
        print(file_path)
        with open(file_path, "r") as file:
            code = file.read()
            self.editor.delete(1.0, END)
            self.editor.insert(1.0, code)
        self.update_line_numbers()
        self.left_panel.open_directory(os.path.dirname(file_path))
        self.file_bars.config(text="\t"+os.path.basename(file_path))



    def save_file(self, event=None):
        global code, file_path

        if file_path == '':
            save_path = asksaveasfilename(defaultextension=".pacl", filetypes=[("Pacole File", "*.pacl")])
            file_path = save_path
        else:
            save_path = file_path
        with open(save_path, "w", encoding='utf-8') as file:
            code = self.editor.get(1.0, END)
            file.write(code)

    def save_as(self, event=None):
        global code, file_path
        save_path = asksaveasfilename(defaultextension=".pacl", filetypes=[("Pacole File", "*.pacl")])
        file_path = save_path
        with open(save_path, "w", encoding='utf-8') as file:
            code = self.editor.get(1.0, END)
            file.write(code)

    def create_file(self, event=None):
        global code, file_path
        #print("111")
        file_path = asksaveasfilename(defaultextension=".pacl",
                                      filetypes=[("Pacole Files", "*.pacl"), ("All Files", "*.*")])
        print(file_path)
        if file_path:
            with open(file_path, "w", encoding='utf-8') as file:
                file.write("")
            with open(file_path, "r", encoding='utf-8') as file:
                code = file.read()
                self.editor.delete(1.0, END)
                self.editor.insert(1.0, code)
        self.update_line_numbers()
        self.left_panel.open_directory(os.path.dirname(file_path))
        self.file_bars.config(text="\t"++os.path.basename(file_path))

    def list_files(self, event=None):
        project_path = os.getcwd()
        self.file_list_text.delete(1.0, ttk.END)
        for item in os.listdir(project_path):
            if os.path.isfile(os.path.join(project_path, item)):
                self.file_list_text.insert(ttk.END, f"{item}\n")

    def process_output(self, process):
        output_buffer = ""
        input_detected = False
        while True:
            output = process.stdout.read(1)
            #print(output)
            #output = output.encode("utf-16")

            #res = chardet.detect(output)
            #print(res["encoding"])
            print(output)
            if output:
                self.output_window.insert(END, output)
                if output == "\n":
                    if input_detected:
                        input_detected = False
                    else:
                        # output_window.insert(END, "")
                        input_detected = True
            else:
                break
        self.output_window.insert(END, "Процесс завершен")

    def run(self, event=None):
        self.save_file()
        global code, file_path, pacode_l
        '''
        code = editor.get(1.0, END)
        exec(code)
        '''
        '''cmd = f"python {file_path}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        output_window.delete(1.0, END)

        output_window.insert(1.0, output)

        output_window.insert(1.0, error)
        '''
        if not file_path:
            return

        self.output_window.delete(1.0, END)
        self.output_window.insert(END, f"{file_path}\n")
        #print(file_path)
        '''
        process = subprocess.Popen(
            ["python", file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
            text=True
        )
        '''
        pacodel = PaCodeL()
        process=pacodel.run(file_path)

        threading.Thread(target=self.process_output, args=(process,), daemon=True).start()
        self.output_window.bind("<Return>", lambda e: self.send_input(process))

    def send_input(self, process):
        self.input_data = self.output_window.get("insert linestart", "insert").strip()
        #self.input_data.encode(encoding="utf-8")
        #print(self.input_data)
        self.output_window.insert(END, "\n")

        process.stdin.write(f"{self.input_data}\n".encode("utf-8"))
        # output_window.insert(1.0, f"{input_data}\n")
        process.stdin.flush()

    def update_line_numbers(self, event=None):
        text_content = self.editor.get("1.0", END)
        line_count = text_content.count("\n")

        line_numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_number_widget.config(state=NORMAL)
        self.line_number_widget.delete("1.0", END)
        self.line_number_widget.insert("1.0", line_numbers)
        self.line_number_widget.config(state=DISABLED)
        return "break"

    # function to close IDE window
    def close(self, event=None):
        self.window.destroy()


    def cut_text(self, event=None):
        self.editor.event_generate(("<<Cut>>"))

    def copy_text(self, event=None):
        self.editor.event_generate(("<<Copy>>"))

    def paste_text(self, event=None):
        self.editor.event_generate(("<<Paste>>"))

    def show_PKMmenu(self, event):
        self.PKM_menu.post(event.x_root, event.y_root)
    # доавляем меню на пкм
    def create_PKMmenu(self, event=None):
        self.PKM_menu = Menu(self.window, tearoff=0)
        self.PKM_menu.add_command(label="Cut", command=self.cut_text)
        self.PKM_menu.add_command(label="Copy", command=self.copy_text)
        self.PKM_menu.add_command(label="Paste", command=self.paste_text)
    def create_Mainmenu(self, event=None):
        self.file_menu = Menu(self.menu, tearoff=0)
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.run_menu = Menu(self.menu, tearoff=0)
        self.view_menu = Menu(self.menu, tearoff=0)
        self.theme_menu = Menu(self.menu, tearoff=0)

        # add menu labels
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu.add_cascade(label="Run", menu=self.run_menu)
        self.menu.add_cascade(label="View", menu=self.view_menu)
        self.menu.add_cascade(label="Theme", menu=self.theme_menu)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Create", accelerator="Ctrl+N", command=self.create_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.close)
        # add commands in edit menu
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        self.run_menu.add_command(label="Run", accelerator="F5", command=self.run)

        self.show_status_bar = BooleanVar()
        self.show_status_bar.set(True)

        self.theme_menu.add_command(label="light", command=self.light)
        self.theme_menu.add_command(label="dark", command=self.dark)

    def hide_statusbar(self, event=None):
        global show_status_bar
        if show_status_bar:
            self.status_bars.pack_forget()
            show_status_bar = False
        else:
            self.status_bars.pack(side=BOTTOM)
            show_status_bar = True

    def change_word(self, event=None):
        global text_change
        if self.editor.edit_modified():
            text_change = True
            word = len(self.editor.get(1.0, "end-1c").split())
            chararcter = len(self.editor.get(1.0, "end-1c").replace(" ", ""))
            self.status_bars.config(text=f" \t\t\t\t\t\t characters: {chararcter} words: {word}")
        self.editor.edit_modified(False)

    def light(self, event=None):
        global sfg, sbg, sbbg, sddg
        sfg = "black"
        sbg = "#EEEEEE"
        sbbg = "#93A6B1"
        sddg = "#EEEEEE"
        self.editor.config(fg=sfg, bg=sbg)
        self.output_window.config(fg=sfg, bg=sbg)
        self.window.configure(bg=sbbg)
        self.file_menu.configure(fg=sfg, bg=sbg)
        self.edit_menu.configure(fg=sfg, bg=sbg)
        self.run_menu.configure(fg=sfg, bg=sbg)
        self.view_menu.configure(fg=sfg, bg=sbg)
        self.theme_menu.configure(fg=sfg, bg=sbg)
        self.PKM_menu.configure(fg=sfg, bg=sbbg)
        self.status_bars.config(foreground=sfg, background=sbbg)
        self.line_number_widget.configure(fg=sfg, bg=sbbg)
        self.left_panel.configure(fg=sfg, bg=sbg)
        self.left_panel.tag_configure("no_select", selectbackground=sbg, selectforeground=sfg)
        self.file_bars.config(foreground=sfg, background=sbbg)

    def dark(self, event=None):
        global sfg, sbg, sbbg, sddg
        sfg = "#EEEEEE"
        sbg = "#222831"
        sbbg = "#393E46"
        sddg = "#FD7013"
        self.editor.config(fg=sfg, bg=sbg)
        self.output_window.config(fg=sfg, bg=sbg)
        self.window.configure(bg=sbbg)
        self.menu.configure(fg=sfg, bg=sbg)
        self.file_menu.configure(fg=sfg, bg=sbg)
        self.edit_menu.configure(fg=sfg, bg=sbg)
        self.run_menu.configure(fg=sfg, bg=sbg)
        self.view_menu.configure(fg=sfg, bg=sbg)
        self.theme_menu.configure(fg=sfg, bg=sbg)
        self.PKM_menu.configure(fg=sfg, bg=sbbg)
        self.status_bars.config(foreground=sfg, background=sbbg)
        self.line_number_widget.configure(fg=sfg, bg=sbbg)
        self.left_panel.configure(fg=sfg, bg=sbg)
        self.left_panel.tag_configure("no_select", selectbackground=sbg, selectforeground=sfg)
        self.file_bars.config(foreground=sfg, background=sbbg)


    def create_Swind(self, event=None):
        swind = Tk()
        swind.attributes("-topmost", True)
        create_btn = ttk.Button(swind, text="Создать", command=lambda: [swind.destroy(), self.create_file()])
        create_btn.pack(padx=10, pady=10, side=LEFT)

        open_btn = ttk.Button(swind, text="Открыть", command=lambda: [swind.destroy(), self.open_file()])
        open_btn.pack(padx=10, pady=10, side=LEFT)

        swind.geometry("+400+400")
        swind.wm_attributes("-topmost", True)
        swind.overrideredirect(True)
        swind.configure(highlightthickness=5, highlightbackground="red")

    def close_window(self, event=None):
        global sfg, sbg, sbbg, sddg
        ewind = Tk()
        ewind.attributes("-topmost", True)
        ewind.overrideredirect(True)
        ewind.configure(highlightthickness=5, highlightbackground=sbbg)
        ewind.configure(bg=sddg)
        save_btn = ttk.Button(ewind, text="Сохранить", command=lambda: [self.save_file(), ewind.destroy(), self.window.destroy()])
        save_btn.pack(padx=10, pady=10, side=LEFT)
        # save_btn.configure(foreground=sfg, bg=sbg)
        save_as_btn = ttk.Button(ewind, text="Сохранить как",
                                 command=lambda: [self.save_as(), ewind.destroy(), self.window.destroy()])
        save_as_btn.pack(padx=10, pady=10, side=LEFT)
        # save_as_btn.configure(foreground=sfg, background=sbg)
        destroy_btn = ttk.Button(ewind, text="Закрыть", command=lambda: [ewind.destroy(), self.window.destroy()])
        destroy_btn.pack(padx=10, pady=10, side=LEFT)
        # destroy_btn.configure(foreground=sfg, background=sbg)
        # window.geometry("+200+200")
        ewind.geometry("+400+400")


if __name__ == "__main__":
    app = Application()
