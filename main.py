import tkinter as tk
from tkinter import scrolledtext, font, filedialog, simpledialog, messagebox
import json
import sys

class DZLangInterpreter:
    def __init__(self):
        self.variables = {}
        self.arrays = {}
        self.dictionaries = {}
        self.classes = {}

    def execute(self, command):
        tokens = command.split()
        if not tokens:
            return

        cmd = tokens[0]

        try:
            if cmd == "let":
                self.handle_let(tokens[1:])
            elif cmd == "print":
                return self.handle_print(tokens[1])
            elif cmd == "input":
                return self.handle_input(tokens[1])
            elif cmd == "if":
                return self.handle_if(tokens[1:])
            elif cmd == "while":
                self.handle_while(tokens[1:])
            elif cmd == "def":
                self.handle_def(tokens[1:])
            elif cmd == "array":
                self.handle_array(tokens[1])
            elif cmd == "push":
                self.handle_push(tokens[1:])
            elif cmd == "pop":
                return self.handle_pop(tokens[1])
            elif cmd == "dict":
                self.handle_dict(tokens[1])
            elif cmd == "set":
                self.handle_set(tokens[1:])
            elif cmd == "get":
                return self.handle_get(tokens[1:])
            elif cmd == "class":
                self.handle_class(tokens[1])
            elif cmd == "method":
                self.handle_method(tokens[1:])
            elif cmd == "try":
                return self.handle_try(tokens[1:])
            elif cmd == "help":
                return self.handle_help(tokens[1])
            elif cmd == "exit":
                return "Exiting the program."
            elif cmd == "save":
                return self.handle_save(tokens[1])
            elif cmd == "load":
                return self.handle_load(tokens[1])
            elif cmd == "delete":
                self.handle_delete(tokens[1])
            elif cmd == "clear":
                self.handle_clear()
            else:
                return f"Unknown command: {cmd}"
        except Exception as e:
            return f"Error: {e}"

    def handle_let(self, tokens):
        if len(tokens) < 3 or tokens[1] != '=':
            raise ValueError("Invalid syntax for 'let' command.")
        var_name = tokens[0]
        expression = " ".join(tokens[2:])
        self.variables[var_name] = self.evaluate_expression(expression)

    def evaluate_expression(self, expression):
        for var in self.variables:
            expression = expression.replace(var, str(self.variables[var]))
        try:
            return eval(expression)
        except Exception as e:
            return f"Error evaluating expression: {e}"

    def handle_print(self, var_name):
        if isinstance(var_name, str):
            if var_name.isdigit():
                return var_name
            if var_name in self.arrays:
                return str(self.arrays[var_name])
            if var_name in self.dictionaries:
                return str(self.dictionaries[var_name])
            return str(self.variables.get(var_name, "Undefined variable"))
        return "Invalid input for print command."

    def handle_input(self, var_name):
        user_input = simpledialog.askstring("Input", f"Введите значение для {var_name}:")
        if user_input is not None:
            self.variables[var_name] = user_input
            return f"{var_name} = {user_input}"
        return "Input canceled."

    def handle_if(self, tokens):
        condition = tokens[0]
        if condition in self.variables and self.variables[condition] > 0:
            return " ".join(tokens[2:]).strip('"')

    def handle_while(self, tokens):
        condition = tokens[0]
        while self.variables.get(condition, 0) > 0:
            self.variables[condition] -= 1

    def handle_def(self, tokens):
        func_name = tokens[0]
        self.variables[func_name] = "Function defined"

    def handle_array(self, array_name):
        self.arrays[array_name] = []

    def handle_push(self, tokens):
        array_name = tokens[0]
        value = tokens[2]
        if array_name in self.arrays:
            self.arrays[array_name].append(int(value))

    def handle_pop(self, array_name):
        if array_name in self.arrays and self.arrays[array_name]:
            return self.arrays[array_name].pop()
        return "Array is empty or does not exist."

    def handle_dict(self, dict_name):
        self.dictionaries[dict_name] = {}

    def handle_set(self, tokens):
        dict_name = tokens[0]
        key = tokens[1]
        value = tokens[3]
        self.dictionaries[dict_name][key] = int(value)

    def handle_get(self, tokens):
        dict_name = tokens[0]
        key = tokens[1]
        return str(self.dictionaries.get(dict_name, {}).get(key, "Key not found"))

    def handle_class(self, class_name):
        self.classes[class_name] = {}

    def handle_method(self, tokens):
        class_name = tokens[0]
        method_name = tokens[1]
        if class_name in self.classes:
            self.classes[class_name][method_name] = "Method defined"
        else:
            raise ValueError(f"Class {class_name} not defined.")

    def handle_try(self, tokens):
        try:
            eval(" ".join(tokens))
        except ZeroDivisionError:
            return "Caught division by zero"
        except Exception as e:
            return f"Error: {e}"

    def handle_help(self, command):
        return f"Help for command: {command}"

    def handle_save(self, filename):
        with open(filename, 'w') as file:
            json.dump({
                'variables': self.variables,
                'arrays': self.arrays,
                'dictionaries': self.dictionaries,
                'classes': self.classes
            }, file)
        return f"State saved to {filename}"

    def handle_load(self, filename):
        try:
            with open(filename, 'r') as file:
                state = json.load(file)
                self.variables = state.get('variables', {})
                self.arrays = state.get('arrays', {})
                self.dictionaries = state.get('dictionaries', {})
                self.classes = state.get('classes', {})
            return f"State loaded from {filename}"
        except Exception as e:
            return f"Error loading state: {e}"

    def handle_delete(self, var_name):
        if var_name in self.variables:
            del self.variables[var_name]
            return f"Variable {var_name} deleted."
        elif var_name in self.arrays:
            del self.arrays[var_name]
            return f"Array {var_name} deleted."
        elif var_name in self.dictionaries:
            del self.dictionaries[var_name]
            return f"Dictionary {var_name} deleted."
        else:
            return f"{var_name} not found."

    def handle_clear(self):
        self.variables.clear()
        self.arrays.clear()
        self.dictionaries.clear()
        self.classes.clear()
        return "All variables, arrays, dictionaries, and classes cleared."

class DZLangApp:
    def __init__(self, root):
        self.interpreter = DZLangInterpreter()
        self.root = root
        self.root.title("DZLang Interpreter v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")

        # Настройка шрифтов
        self.default_font = font.Font(family="Courier New", size=12)
        self.button_font = font.Font(family="Courier New", size=12, weight="bold")

        # Настройка текстовой области для ввода кода
        self.text_area = scrolledtext.ScrolledText(root, width=80, height=20, font=self.default_font, bg="#3E3E3E", fg="#FFFFFF", wrap=tk.WORD, insertbackground='white', bd=0, highlightthickness=0)
        self.text_area.pack(pady=10, padx=10)

        # Настройка текстовой области для вывода
        self.output_area = scrolledtext.ScrolledText(root, width=80, height=10, font=self.default_font, bg="#3E3E3E", fg="#FFFFFF", wrap=tk.WORD, insertbackground='white', bd=0, highlightthickness=0)
        self.output_area.pack(pady=10, padx=10)

        # Кнопка "Run"
        run_button = tk.Button(root, text="Run", command=self.run_code, bg="#4CAF50", fg="white", font=self.button_font, relief=tk.FLAT, bd=0)
        run_button.pack(pady=5)

        # Кнопка "Open"
        open_button = tk.Button(root, text="Open", command=self.open_file, bg="#007BFF", fg="white", font=self.button_font, relief=tk.FLAT, bd=0)
        open_button.pack(pady=5)

        # Кнопка "Save"
        save_button = tk.Button(root, text="Save", command=self.save_file, bg="#FFC107", fg="white", font=self.button_font, relief=tk.FLAT, bd=0)
        save_button.pack(pady=5)

        # Кнопка "Load State"
        load_button = tk.Button(root, text="Load State", command=self.load_state, bg="#FF5722", fg="white", font=self.button_font, relief=tk.FLAT, bd=0)
        load_button.pack(pady=5)

        # Добавление метки для информации
        self.info_label = tk.Label(root, text="Введите команды DZLang и нажмите 'Run'", font=self.default_font, bg="#2E2E2E", fg="#FFFFFF")
        self.info_label.pack(pady=5)

        # Привязка горячих клавиш
        self.text_area.bind("<Control-c>", self.copy_text)
        self.text_area.bind("<Control-v>", self.paste_text)
        self.text_area.bind("<Control-x>", self.cut_text)
        self.text_area.bind("<Control-s>", lambda event: self.save_file())

        self.output_area.bind("<Control-c>", self.copy_output)

    def run_code(self):
        code = self.text_area.get("1.0", tk.END).strip().splitlines()
        output = []
        for line in code:
            result = self.interpreter.execute(line)
            if result is not None:
                output.append(result)

        self.output_area.config(state=tk.NORMAL)  # Разрешаем редактирование
        self.output_area.delete("1.0", tk.END)  # Очистка области вывода
        self.output_area.insert(tk.END, "\n".join(output))  # Вывод результатов
        self.output_area.config(state=tk.DISABLED)  # Запрещаем редактирование

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".dzlang", filetypes=[("DZLang files", "*.dzlang"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_area.delete("1.0", tk.END)  # Очистка текстовой области
                self.text_area.insert(tk.END, code)  # Вставка кода из файла

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".dzlang", filetypes=[("DZLang files", "*.dzlang"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get("1.0", tk.END)  # Получение кода из текстовой области
                file.write(code)  # Сохранение кода в файл

    def load_state(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            result = self.interpreter.handle_load(file_path)
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, result + "\n")
            self.output_area.config(state=tk.DISABLED)

    def copy_text(self, event=None):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self, event=None):
        self.text_area.event_generate("<<Paste>>")

    def cut_text(self, event=None):
        self.text_area.event_generate("<<Cut>>")

    def copy_output(self, event=None):
        self.output_area.event_generate("<<Copy>>")

def main():
    if len(sys.argv) > 1:
        interpreter = DZLangInterpreter()
        for command in sys.argv[1:]:
            result = interpreter.execute(command)
            if result is not None:
                print(result)
    else:
        root = tk.Tk()
        app = DZLangApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()
