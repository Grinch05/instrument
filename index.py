import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import io

class ShoeStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Автоматизация обувного магазина")
        self.root.geometry("800x600")
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.username_label = tk.Label(self.root, text="Имя пользователя")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Пароль")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Войти", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.authenticate(username, password):
            self.show_main_menu(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def authenticate(self, username, password):
        conn = sqlite3.connect('shoe_store.db')
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()
        if result:
            self.role = result[0]
            return True
        return False

    def show_main_menu(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()

        welcome_label = tk.Label(self.root, text=f"Добро пожаловать, {username}!")
        welcome_label.pack()

        if self.role == 'admin':
            add_shoe_button = tk.Button(self.root, text="Добавить обувь", command=self.add_shoe)
            add_shoe_button.pack()

            delete_shoe_button = tk.Button(self.root, text="Удалить обувь", command=self.delete_shoe)
            delete_shoe_button.pack()

        view_shoes_button = tk.Button(self.root, text="Просмотреть обувь", command=self.view_shoes)
        view_shoes_button.pack()

        logout_button = tk.Button(self.root, text="Выйти", command=self.show_login_screen)
        logout_button.pack()

    def add_shoe(self):
        self.show_add_shoe_form()

    def show_add_shoe_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        name_label = tk.Label(self.root, text="Название")
        name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        size_label = tk.Label(self.root, text="Размер")
        size_label.pack()
        self.size_entry = tk.Entry(self.root)
        self.size_entry.pack()

        price_label = tk.Label(self.root, text="Цена")
        price_label.pack()
        self.price_entry = tk.Entry(self.root)
        self.price_entry.pack()

        model_label = tk.Label(self.root, text="Модель")
        model_label.pack()
        self.model_entry = tk.Entry(self.root)
        self.model_entry.pack()

        country_label = tk.Label(self.root, text="Страна изготовитель")
        country_label.pack()
        self.country_entry = tk.Entry(self.root)
        self.country_entry.pack()

        image_label = tk.Label(self.root, text="Фотография")
        image_label.pack()
        self.image_path = tk.Entry(self.root)
        self.image_path.pack()

        browse_button = tk.Button(self.root, text="Обзор", command=self.browse_image)
        browse_button.pack()

        submit_button = tk.Button(self.root, text="Добавить обувь", command=self.submit_shoe)
        submit_button.pack()

        back_button = tk.Button(self.root, text="Назад", command=lambda: self.show_main_menu("admin"))
        back_button.pack()

    def browse_image(self):
        self.image_file_path = filedialog.askopenfilename()
        self.image_path.delete(0, tk.END)
        self.image_path.insert(0, self.image_file_path)

    def submit_shoe(self):
        name = self.name_entry.get()
        size = int(self.size_entry.get())
        price = float(self.price_entry.get())
        model = self.model_entry.get()
        country = self.country_entry.get()
        image_path = self.image_path.get()

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        conn = sqlite3.connect('shoe_store.db')
        c = conn.cursor()
        c.execute("INSERT INTO shoes (name, size, price, model, country, image) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, size, price, model, country, image_data))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Обувь успешно добавлена")
        self.show_main_menu("admin")

    def delete_shoe(self):
        self.show_delete_shoe_form()

    def show_delete_shoe_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        id_label = tk.Label(self.root, text="ID обуви")
        id_label.pack()
        self.id_entry = tk.Entry(self.root)
        self.id_entry.pack()

        delete_button = tk.Button(self.root, text="Удалить обувь", command=self.submit_delete_shoe)
        delete_button.pack()

        self.display_shoes()

        back_button = tk.Button(self.root, text="Назад", command=lambda: self.show_main_menu("admin"))
        back_button.pack()

    def submit_delete_shoe(self):
        shoe_id = int(self.id_entry.get())

        conn = sqlite3.connect('shoe_store.db')
        c = conn.cursor()
        c.execute("DELETE FROM shoes WHERE id=?", (shoe_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Обувь успешно удалена")
        self.delete_shoe()

    def display_shoes(self):
        conn = sqlite3.connect('shoe_store.db')
        c = conn.cursor()
        c.execute("SELECT * FROM shoes")
        shoes = c.fetchall()
        conn.close()

        for shoe in shoes:
            shoe_info = f"Название: {shoe[1]}, Размер: {shoe[2]}, Цена: {shoe[3]}, Модель: {shoe[4]}, Страна: {shoe[5]}"
            if self.role == 'admin':
                shoe_info = f"ID: {shoe[0]}, " + shoe_info
            shoe_label = tk.Label(self.root, text=shoe_info)
            shoe_label.pack()

            image_data = shoe[6]
            if image_data:
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(self.root, image=photo)
                image_label.image = photo
                image_label.pack()

    def view_shoes(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.display_shoes()

        back_button = tk.Button(self.root, text="Назад", command=lambda: self.show_main_menu("admin" if self.role == 'admin' else "user"))
        back_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoeStoreApp(root)
    root.mainloop()
