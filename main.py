import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import os

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Pro")
        self.root.geometry("500x550")
        self.data_file = "tasks.json"
        self.tasks = self.load_data()

        # UI элементы
        tk.Label(root, text="Название задачи:").pack(pady=5)
        self.entry_title = tk.Entry(root, width=40)
        self.entry_title.pack()

        tk.Label(root, text="Категория:").pack(pady=5)
        self.combo_cat = ttk.Combobox(root, values=["Работа", "Учеба", "Личное", "Спорт"])
        self.combo_cat.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=self.add_task, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_task, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удача дня", command=self.random_task_tip).pack(side=tk.LEFT, padx=5)

        tk.Label(root, text="Фильтр по категории:").pack()
        self.filter_cat = ttk.Combobox(root, values=["Все", "Работа", "Учеба", "Личное", "Спорт"])
        self.filter_cat.current(0)
        self.filter_cat.bind("<<ComboboxSelected>>", self.update_listbox)
        self.filter_cat.pack(pady=5)

        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(pady=10, padx=10)
        
        self.update_listbox()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def add_task(self):
        title = self.entry_title.get().strip()
        category = self.combo_cat.get()

        # Валидация
        if not title or not category:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        
        self.tasks.append({"title": title, "category": category})
        self.save_data()
        self.update_listbox()
        self.entry_title.delete(0, tk.END)

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            selected_text = self.listbox.get(index)
            # Ищем задачу в общем списке для удаления
            title = selected_text.split(" [")[0]
            self.tasks = [t for t in self.tasks if t['title'] != title]
            self.save_data()
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления")

    def update_listbox(self, event=None):
        self.listbox.delete(0, tk.END)
        filt = self.filter_cat.get()
        for task in self.tasks:
            if filt == "Все" or task['category'] == filt:
                self.listbox.insert(tk.END, f"{task['title']} [{task['category']}]")

    def random_task_tip(self):
        tips = ["Сделай это прямо сейчас!", "Разбей задачу на части", "Отдохни 5 минут", "Приоритеты важны"]
        messagebox.showinfo("Совет", random.choice(tips))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
