import ast
import tkinter as tk
from typing import List, Tuple


def extract_classes_info(file_path: str) -> List[Tuple[str, List[str], List[str]]]:
    """
    Функция для анализа кода и извлечения информации о классах, их наследовании, методах и переменных.
    :param file_path: путь к файлу с кодом Python
    :return: список кортежей вида (имя класса, список основных классов, список методов и переменных класса)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    class_info = []
    tree = ast.parse(code)
    for item in tree.body:
        if isinstance(item, ast.ClassDef):
            base_classes = [base.id for base in item.bases if isinstance(base, ast.Name)]
            class_methods_and_vars = [m.name for m in item.body if isinstance(m, (ast.FunctionDef, ast.Assign))]
            class_info.append((item.name, base_classes, class_methods_and_vars))

    return class_info


class RightPanel(tk.Frame):
    def __init__(self, master: tk.Tk, file_path: str):
        super().__init__(master)
        self.master = master
        self.file_path = file_path
        self.classes_info = extract_classes_info(self.file_path)
        self.create_widgets()

    def create_widgets(self):
        for i, (class_name, base_classes, methods_and_vars) in enumerate(self.classes_info):
            if base_classes:
                base_classes_str = f" ({', '.join(base_classes)})"
            else:
                base_classes_str = ""

            class_label = tk.Label(self, text=f"{class_name}{base_classes_str}")
            class_label.grid(row=i * 2, column=0, sticky=tk.W)

            for j, method_or_var in enumerate(methods_and_vars):
                method_or_var_label = tk.Label(self, text=f"\t{method_or_var}")
                method_or_var_label.grid(row=i * 2 + 1, column=j, sticky=tk.W)