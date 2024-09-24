import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

# Görev sınıfı tanımlaması
class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.date_added = datetime.now()  # Görev eklendiğinde tarih ve saat

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        return self.description

# Görev Yönetimi Uygulaması
class TaskManager:
    def __init__(self, file_name="tasks.txt"):
        self.tasks = []
        self.file_name = file_name
        self.load_tasks()

    def add_task(self, description):
        new_task = Task(description)
        self.tasks.append(new_task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()

    def save_tasks(self):
        with open(self.file_name, "w") as file:
            for task in self.tasks:
                status = "Tamamlandı" if task.completed else "Tamamlanmadı"
                date_added = task.date_added.strftime("%Y-%m-%d %H:%M")  # Tarih formatı
                file.write(f"{task.description},{status},{date_added}\n")

    def load_tasks(self):
     if os.path.exists(self.file_name):
        with open(self.file_name, "r") as file:
            for line in file:
                # Satırı virgüle göre ayırma ve yeterli eleman kontrolü
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue  # Yetersiz veri varsa atla

                description, status, date_added = parts
                task = Task(description)
                task.date_added = datetime.strptime(date_added, "%Y-%m-%d %H:%M")  # Tarih yükleme
                if status == "Tamamlandı":
                    task.mark_completed()
                self.tasks.append(task)


# GUI arayüzü oluşturma
class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Görev Yönetimi Uygulaması")

        # Pencere boyutunu ayarlama
        self.root.geometry("800x500")  # Genişlik x Yükseklik
        self.root.configure(bg='lightblue')  # Arka plan rengi

        # Giriş alanı
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=40)

        # Görev ekleme butonu
        self.add_button = tk.Button(root, text="Görev Ekle", command=self.add_task, bg='green', fg='white')
        self.add_button.pack(pady=10)

        # Görev listesi
        self.task_listbox = tk.Listbox(root, height=10, width=50)
        self.task_listbox.pack(pady=10)
        self.refresh_task_list()

        # Seçili görevi tamamla butonu
        self.complete_button = tk.Button(root, text="Görev Tamamlandı", command=self.complete_task, bg='orange', fg='white')
        self.complete_button.pack(pady=5)

        # Seçili görevi sil butonu
        self.delete_button = tk.Button(root, text="Görevi Sil", command=self.delete_task, bg='red', fg='white')
        self.delete_button.pack(pady=5)

        # Görevleri kaydet butonu
        self.save_button = tk.Button(root, text="Görevleri Kaydet", command=self.save_tasks, bg='blue', fg='white')
        self.save_button.pack(pady=5)

        # Pencereyi ortalamak için konum ayarlama
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()  # Güncellemeleri uygula
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')  # Pencereyi ortalama

    def add_task(self):
        task_desc = self.task_entry.get()
        if task_desc:
            self.manager.add_task(task_desc)
            self.task_entry.delete(0, tk.END)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Uyarı", "Görev açıklaması boş olamaz!")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.manager.delete_task(selected_task_index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir görev seçin!")

    def complete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.manager.complete_task(selected_task_index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Uyarı", "Lütfen tamamlamak için bir görev seçin!")

    def save_tasks(self):
        self.manager.save_tasks()
        messagebox.showinfo("Başarılı", "Görevler kaydedildi.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.manager.tasks):
            status = " [Tamamlandı]" if task.completed else ""
            date_added = task.date_added.strftime("%Y-%m-%d %H:%M")  # Tarih formatı
            self.task_listbox.insert(tk.END, f"{i+1}. {task}{status} (Eklendi: {date_added})")

# Ana program
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
