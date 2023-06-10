import math
import os
import re
import subprocess

class PaCodeL:
    # Здесь будет словарь замены ключевых слов на их Python аналоги
    # Пример: "unknown_keyword": "python_keyword"
    unknown_lang_to_python = {

        "и": "and",
        "проверка": "assert",
        "как": "as",
        "несинх": "async",
        "ждать": "await",
        "сц": "break",
        "класс": "class",
        "пц": "continue",
        "алг": "def",
        "удал": "del",
        "инес": "elif",
        "иначе": "else",
        "исключение": "except",
        "Ложь": "False",
        "ЛОЖЬ": "False",
        "завершая": "finally",
        "нц для": "for in",
        "среди": "from",
        "общ": "global",
        "если": "if",
        "импорт": "import",
        "из": "in",
        "явл": "is",
        "лямбда": "lambda",
        "пусто": "None",
        "немест": "nonlocal",
        "не": "not",
        "или": "or",
        "пропуск": "pass",
        "созиск": "raise",
        "возврат": "return",
        "Истина": "True",
        "ИСТИНА": "True",
        "попытка": "try",
        "нц пока": "while",
        "кб": "with",
        "отпр": "yield",
        "цел": "int",
        "вещ": "float",
        "ком": "complex",
        "лог": "bool",
        "стр": "str",
        "нач": 'if __name__ == "__main__":',
        "нс": "\\n",
        "вывод": "print",
        "диап": "range",
        "ввод": "input",
        "выбор": "match",
        "при": "case",
        "длина": "len",
        "номер": "index",
        "символ": "__getitem__",
        "юкод": "ord",
        "юсим": "chr"
    }

    def __init__(self):
        self.user_data_folder = os.path.join(os.getenv("LOCALAPPDATA"), "Dipea")
        os.makedirs(self.user_data_folder, exist_ok=True)  # Создание папки, если она не существует

    def run(self, file_path: str):
        #print("0")
        #, encoding="utf-8"
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        #print("1")
        code = self.replace_keywords(code)

        if self.has_math_functions(code):
            code = "from math import *\n" + code

        output_file_path = os.path.join(self.user_data_folder, os.path.splitext(os.path.basename(file_path))[0] + ".py")
        #, encoding="utf-8"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(code)
        print(output_file_path)
        process = subprocess.Popen(
            ["python", output_file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
            text=True,
            encoding = "utf-8"
        )
        #subprocess.run(["python", output_file_path])
        return process
    def replace_keywords(self, code: str) -> str:

        code = code.replace("'",'"')
        # TODO fix it in a proper way
        string_map: list[str] = code.split('"')
        size = math.floor(len(string_map) / 2)
        # store all strings in map and replace it with corresponding number
        for i in range(0, size):
            code = code.replace(string_map[1 + 2 * i], "þ" + i.__str__())

        # replace language keywords to python keywords
        for unknown_keyword, python_keyword in self.unknown_lang_to_python.items():
            code = re.sub(unknown_keyword, python_keyword, code)

        # replace keywords back
        for i in range(0, size):
            code = code.replace("þ" + i.__str__(), string_map[1 + 2 * i])
        return code

    def has_math_functions(self, code: str) -> bool:
        math_functions = ["acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh", "ceil", "copysign", "cos", "cosh", "degrees", "e", "erf", "erfc", "exp", "expm1", "fabs", "factorial", "floor", "fmod", "frexp", "fsum", "gamma", "gcd", "hypot", "inf", "isclose", "isfinite", "isinf", "isnan", "ldexp", "lgamma", "log", "log1p", "log10", "log2", "modf", "nan", "pi", "pow", "radians", "remainder", "sin", "sinh", "sqrt", "tan", "tanh", "tau", "trunc"]
        return any(func in code for func in math_functions)
'''
if __name__ == "__main__":
    pacode_l = PaCodeL()
    pacode_l.run("path/to/your.pacl")  # Вставьте путь к вашему .pacl файлу
'''