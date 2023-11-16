import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk

class Task:
    def __init__(self, title, description, priority='Low', due_date=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self.due_date = due_date
        self.completed = False

    def complete_task(self):
        self.completed = True

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'created_at': str(self.created_at),
            'due_date': str(self.due_date) if self.due_date else None,
            'completed': self.completed
        }

    def __str__(self):
        return f"{self.title} - Priority: {self.priority} - Due Date: {self.due_date} - Created at: {self.created_at} - Completed: {self.completed}"

class TodoListApp:
    def __init__(self, root):
        self.root = ThemedTk(theme="arc")  # Using ttkthemes for modern styles
        self.root.title("Todo List App")

        self.todo_list = TodoList()
        self.todo_list.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        # Task Entry Frame
        task_frame = ttk.Frame(self.root)
        task_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(task_frame, text="Task Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(task_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(task_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.desc_entry = ttk.Entry(task_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(task_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W)
        self.priority_entry = ttk.Combobox(task_frame, values=['Low', 'Normal', 'High'], state='readonly')
        self.priority_entry.set('Low')
        self.priority_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(task_frame, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W)
        self.due_date_entry = ttk.Entry(task_frame, width=30)
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=5)

        add_button = ttk.Button(task_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Task List Frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        columns = ("Task", "Priority", "Due Date", "Created at", "Completed")
        self.task_treeview = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.task_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_bar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_treeview.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_treeview.config(yscrollcommand=scroll_bar.set)

        for col in columns:
            self.task_treeview.heading(col, text=col)
            self.task_treeview.column(col, width=100, anchor="center")

        # Buttons
        complete_button = ttk.Button(self.root, text="Complete Task", command=self.complete_task)
        complete_button.pack(pady=10)

        delete_button = ttk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_button.pack(pady=5)

        sort_label = ttk.Label(self.root, text="Sort by:")
        sort_label.pack()

        self.sort_option = tk.StringVar()
        self.sort_option.set('Priority')
        sort_combobox = ttk.Combobox(self.root, values=['Priority', 'Due Date', 'Creation Date'], textvariable=self.sort_option, state='readonly')
        sort_combobox.pack()

        sort_button = ttk.Button(self.root, text="Sort Tasks", command=self.sort_tasks)
        sort_button.pack(pady=5)

        save_button = ttk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        save_button.pack(pady=5)

        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app)
        exit_button.pack(pady=5)

        # Initialize task treeview
        self.update_task_treeview()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        priority = self.priority_entry.get()
        due_date_str = self.due_date_entry.get()

        if title and description:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
            new_task = Task(title, description, priority, due_date)
            self.todo_list.add_task(new_task)
            self.update_task_treeview()

            # Clear entry fields
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.priority_entry.set('Low')
            self.due_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Title and Description are required.")

    def update_task_treeview(self):
        self.clear_task_treeview()
        for task in self.todo_list.tasks:
            task_data = (f"{task.title}", f"{task.priority}", f"{task.due_date}", f"{task.created_at}", f"{task.completed}")
            self.task_treeview.insert("", tk.END, values=task_data)

    def clear_task_treeview(self):
        for item in self.task_treeview.get_children():
            self.task_treeview.delete(item)

    def complete_task(self):
        selected_item = self.task_treeview.selection()
        if selected_item:
            item_id = self.task_treeview.index(selected_item)
            self.todo_list.complete_task(item_id)
            self.update_task_treeview()
        else:
            messagebox.showwarning("Warning", "Select a task to mark as completed.")

    def delete_task(self):
        selected_item = self.task_treeview.selection()
        if selected_item:
            item_id = self.task_treeview.index(selected_item)
            self.todo_list.delete_task(item_id)
            self.update_task_treeview()
        else:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def sort_tasks(self):
        sort_option = self.sort_option.get()
        self.todo_list.sort_tasks(sort_option)
        self.update_task_treeview()

    def save_tasks(self):
        self.todo_list.save_tasks()
        messagebox.showinfo("Information", "Tasks saved successfully.")

    def exit_app(self):
        self.todo_list.save_tasks()
        self.root.destroy()

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def complete_task(self, task_id):
        if 0 <= task_id < len(self.tasks):
            task = self.tasks[task_id]
            task.complete_task()

    def delete_task(self, task_id):
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]

    def sort_tasks(self, sort_option):
        if sort_option == 'Priority':
            self.tasks.sort(key=lambda x: x.priority)
        elif sort_option == 'Due Date':
            self.tasks.sort(key=lambda x: x.due_date)
        elif sort_option == 'Creation Date':
            self.tasks.sort(key=lambda x: x.created_at)

    def save_tasks(self, file_name='tasks.json'):
        tasks_data = [task.to_dict() for task in self.tasks]
        with open(file_name, 'w') as file:
            json.dump(tasks_data, file)

    def load_tasks(self, file_name='tasks.json'):
        try:
            with open(file_name, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**task_data) for task_data in tasks_data]
        except FileNotFoundError:
            pass  # No tasks file found.

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()