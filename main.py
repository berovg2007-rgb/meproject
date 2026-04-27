import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("600x600")
        self.data_file = "movies.json"
        self.movies = self.load_data()

        # Поля ввода
        tk.Label(root, text="Название:").pack()
        self.entry_title = tk.Entry(root, width=40)
        self.entry_title.pack()

        tk.Label(root, text="Жанр:").pack()
        self.combo_genre = ttk.Combobox(root, values=["Боевик", "Комедия", "Драма", "Ужасы", "Фантастика"])
        self.combo_genre.pack()

        tk.Label(root, text="Год выпуска:").pack()
        self.entry_year = tk.Entry(root, width=20)
        self.entry_year.pack()

        tk.Label(root, text="Рейтинг (0-10):").pack()
        self.entry_rating = tk.Entry(root, width=20)
        self.entry_rating.pack()

        tk.Button(root, text="Добавить фильм", command=self.add_movie, bg="blue", fg="white").pack(pady=10)

        # Фильтры
        filter_frame = tk.LabelFrame(root, text="Фильтрация")
        filter_frame.pack(pady=5, fill="x", padx=10)
        
        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.f_genre = ttk.Combobox(filter_frame, values=["Все", "Боевик", "Комедия", "Драма", "Ужасы", "Фантастика"])
        self.f_genre.current(0)
        self.f_genre.grid(row=0, column=1)

        tk.Label(filter_frame, text="Год:").grid(row=0, column=2)
        self.f_year = tk.Entry(filter_frame, width=10)
        self.f_year.grid(row=0, column=3)
        
        tk.Button(filter_frame, text="Применить", command=self.update_table).grid(row=0, column=4, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Title", "Genre", "Year", "Rating"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.update_table()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.combo_genre.get()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        # Валидация (Пункт 5 задания)
        if not (title and genre and year and rating):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        
        try:
            r = float(rating)
            if not (0 <= r <= 10): raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
            return

        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.save_data()
        self.update_table()
        messagebox.showinfo("Успех", "Фильм добавлен!")

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        filt_g = self.f_genre.get()
        filt_y = self.f_year.get().strip()

        for m in self.movies:
            if (filt_g == "Все" or m['genre'] == filt_g) and (not filt_y or m['year'] == filt_y):
                self.tree.insert("", tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
