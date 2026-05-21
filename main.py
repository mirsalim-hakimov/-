import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# ---------- File paths ----------
TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"

# ---------- Default tasks by category ----------
DEFAULT_TASKS = {
    "Учёба": [
        "Прочитать статью по Python",
        "Решить 5 математических задач",
        "Выучить 10 новых английских слов",
        "Посмотреть лекцию по истории",
        "Написать конспект по теме"
    ],
    "Спорт": [
        "Сделать зарядку (15 мин)",
        "Пробежать 2 км",
        "Сделать 50 приседаний",
        "Пойти в спортзал",
        "Позаниматься йогой"
    ],
    "Работа": [
        "Ответить на рабочие письма",
        "Составить план на день",
        "Закончить отчёт",
        "Провести созвон с командой",
        "Организовать рабочий стол"
    ]
}


# ---------- Load/Save tasks ----------
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_TASKS.copy()


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


# ---------- Load/Save history ----------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


# ---------- GUI Application ----------
class TaskGeneratorApp:
    def init(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("750x600")
        self.root.resizable(True, True)

        self.tasks = load_tasks()
        self.history = load_history()
        self.current_filter = "Все"

        self.create_widgets()
        self.update_task_list()
        self.update_history_display()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # ---------- Task display area ----------
        display_frame = ttk.LabelFrame(main_frame, text="Случайная задача", padding=10)
        display_frame.pack(fill="x", pady=5)

        self.task_label = tk.Label(display_frame, text="Нажмите кнопку для генерации",
                                   font=("Arial", 14, "bold"), wraplength=600, height=3)
        self.task_label.pack(pady=10)

        self.generate_btn = ttk.Button(display_frame, text="🎲 Сгенерировать задачу",
                                       command=self.generate_task, width=30)
        self.generate_btn.pack(pady=5)

        # ---------- Filter area ----------
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация по типу", padding=10)
        filter_frame.pack(fill="x", pady=5)

        self.filter_var = tk.StringVar(value="Все")
        categories = ["Все"] + list(self.tasks.keys())

        for category in categories:
            ttk.Radiobutton(filter_frame, text=category, variable=self.filter_var,
                            value=category, command=self.apply_filter).pack(side="left", padx=10)

        # ---------- Add new task area ----------
        add_frame = ttk.LabelFrame(main_frame, text="Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", pady=5)

        ttk.Label(add_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
        self.category_combo = ttk.Combobox(add_frame, values=list(self.tasks.keys()), width=15)
        self.category_combo.set("Учёба")
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Задача:").grid(row=0, column=2, padx=5, pady=5)
        self.new_task_entry = ttk.Entry(add_frame, width=40)
        self.new_task_entry.grid(row=0, column=3, padx=5, pady=5)


ttk.Button(add_frame, text="➕ Добавить", command=self.add_task).grid(row=0, column=4, padx=5, pady=5)

# ---------- Task list (all tasks) ----------
list_frame = ttk.LabelFrame(main_frame, text="Все задачи", padding=10)
list_frame.pack(fill="both", expand=True, pady=5)

# Treeview for tasks
columns = ("Категория", "Задача")
self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=6)

self.task_tree.heading("Категория", text="Категория")
self.task_tree.heading("Задача", text="Задача")
self.task_tree.column("Категория", width=100)
self.task_tree.column("Задача", width=400)

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_tree.yview)
self.task_tree.configure(yscrollcommand=scrollbar.set)

self.task_tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Delete button
ttk.Button(list_frame, text="🗑 Удалить выбранную задачу",
           command=self.delete_task).pack(pady=5)

# ---------- History display ----------
history_frame = ttk.LabelFrame(main_frame, text="История сгенерированных задач", padding=10)
history_frame.pack(fill="both", expand=True, pady=5)

self.history_listbox = tk.Listbox(history_frame, height=6, font=("Arial", 10))
self.history_listbox.pack(side="left", fill="both", expand=True)

history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
self.history_listbox.configure(yscrollcommand=history_scrollbar.set)
history_scrollbar.pack(side="right", fill="y")

# History buttons
btn_frame = ttk.Frame(history_frame)
btn_frame.pack(side="bottom", fill="x", pady=5)

ttk.Button(btn_frame, text="🗑 Очистить историю", command=self.clear_history).pack(side="left", padx=5)
ttk.Button(btn_frame, text="🔄 Обновить", command=self.update_history_display).pack(side="left", padx=5)


def generate_task(self):
    """Generate a random task based on current filter"""
    available_tasks = []

    if self.current_filter == "Все":
        # Collect tasks from all categories
        for category, task_list in self.tasks.items():
            for task in task_list:
                available_tasks.append((category, task))
    else:
        # Collect tasks from selected category only
        if self.current_filter in self.tasks:
            for task in self.tasks[self.current_filter]:
                available_tasks.append((self.current_filter, task))

    if not available_tasks:
        messagebox.showwarning("Нет задач", f"В категории '{self.current_filter}' нет задач!\nДобавьте новые задачи.")
        return

    # Select random task
    category, task = random.choice(available_tasks)

    # Display task
    self.task_label.config(text=f"{task}\n\n(Категория: {category})")

    # Save to history
    history_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "task": task
    }
    self.history.insert(0, history_entry)  # Add to beginning
    save_history(self.history)
    self.update_history_display()


def apply_filter(self):
    """Apply category filter"""
    self.current_filter = self.filter_var.get()
    self.update_task_list()


def update_task_list(self):
    """Update the task treeview based on current filter"""
    # Clear current items
    for item in self.task_tree.get_children():self.task_tree.delete(item)

# Add tasks based on filter
if self.current_filter == "Все":
    for category, task_list in self.tasks.items():
        for task in task_list:
            self.task_tree.insert("", "end", values=(category, task))
else:
    if self.current_filter in self.tasks:
        for task in self.tasks[self.current_filter]:
            self.task_tree.insert("", "end", values=(self.current_filter, task))


def add_task(self):
    """Add a new task"""
    new_task = self.new_task_entry.get().strip()
    category = self.category_combo.get()

    # Validation: not empty
    if not new_task:
        messagebox.showerror("Ошибка", "Задача не может быть пустой строкой!")
        return

    # Check if category exists
    if category not in self.tasks:
        messagebox.showerror("Ошибка", f"Категория '{category}' не существует!")
        return

    # Check for duplicate
    if new_task in self.tasks[category]:
        messagebox.showwarning("Предупреждение", "Такая задача уже существует в этой категории!")
        return

    # Add task
    self.tasks[category].append(new_task)
    save_tasks(self.tasks)

    # Clear entry
    self.new_task_entry.delete(0, tk.END)

    # Update display
    self.update_task_list()

    # Update category combo if needed (in case new category was added)
    self.category_combo['values'] = list(self.tasks.keys())

    messagebox.showinfo("Успех", f"Задача '{new_task}' добавлена в категорию '{category}'")


def delete_task(self):
    """Delete selected task"""
    selected = self.task_tree.selection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите задачу для удаления!")
        return

    # Get task details
    item = self.task_tree.item(selected[0])
    category = item['values'][0]
    task = item['values'][1]

    # Confirm deletion
    if messagebox.askyesno("Подтверждение", f"Удалить задачу:\n'{task}' из категории '{category}'?"):
        if category in self.tasks and task in self.tasks[category]:
            self.tasks[category].remove(task)
            save_tasks(self.tasks)

            # Remove empty category (optional)
            if not self.tasks[category]:
                del self.tasks[category]
                save_tasks(self.tasks)
                # Update filter options
                self.update_filter_buttons()

            self.update_task_list()
            self.category_combo['values'] = list(self.tasks.keys())
            messagebox.showinfo("Успех", "Задача удалена!")


def update_filter_buttons(self):
    """Update radio buttons when categories change"""
    # This is a bit complex to rebuild dynamically, so we'll just update the combo
    pass


def update_history_display(self):
    """Update history listbox"""
    self.history_listbox.delete(0, tk.END)

    for entry in self.history[:50]:  # Show last 50 entries
        self.history_listbox.insert(tk.END, f"{entry['date']} | {entry['category']} | {entry['task']}")


def clear_history(self):
    """Clear all history"""
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        self.history = []
        save_history(self.history)
        self.update_history_display()
        messagebox.showinfo("Успех", "История очищена!")


# ---------- Main execution ----------
if name == "main":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()