import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class CozyTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy To-Do List")
        self.root.geometry("400x500")
        self.root.configure(bg="#E6F3FF")  # Soft blue background

        # Task list storage
        self.tasks = []

        # UI Elements
        self.title_label = tk.Label(root, text="My Cozy To-Do List", font=("Helvetica", 18, "bold"), bg="#E6F3FF", fg="#2E4057")
        self.title_label.pack(pady=10)

        self.task_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#FFFFFF", fg="#2E4057", relief="flat", bd=2)
        self.task_entry.pack(pady=10)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#A8DADC", fg="#2E4057", font=("Helvetica", 10), relief="flat", bd=2)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=50, height=15, font=("Helvetica", 12), bg="#FFFFFF", fg="#2E4057", selectmode=tk.SINGLE, relief="flat", bd=2)
        self.task_listbox.pack(pady=10)

        self.button_frame = tk.Frame(root, bg="#E6F3FF")
        self.button_frame.pack(pady=5)

        self.done_button = tk.Button(self.button_frame, text="Mark Done", command=self.mark_done, bg="#F4A261", fg="#2E4057", font=("Helvetica", 10), relief="flat", bd=2)
        self.done_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="#E76F51", fg="#FFFFFF", font=("Helvetica", 10), relief="flat", bd=2)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.save_button = tk.Button(self.button_frame, text="Save List", command=self.save_list, bg="#A8DADC", fg="#2E4057", font=("Helvetica", 10), relief="flat", bd=2)
        self.save_button.grid(row=0, column=2, padx=5)

        self.load_button = tk.Button(self.button_frame, text="Load List", command=self.load_list, bg="#A8DADC", fg="#2E4057", font=("Helvetica", 10), relief="flat", bd=2)
        self.load_button.grid(row=0, column=3, padx=5)

        # Load tasks on startup if file exists
        self.load_list_on_start()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"text": task, "done": False})
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def mark_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task.")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task.")

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = task["text"]
            if task["done"]:
                display_text = f"✓ {display_text}"
                self.task_listbox.insert(tk.END, display_text)
                self.task_listbox.itemconfig(tk.END, {'fg': '#A8DADC'})  # Soft green for done
            else:
                self.task_listbox.insert(tk.END, display_text)

    def save_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.tasks, f)
            messagebox.showinfo("Saved", "To-do list saved successfully!")

    def load_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                self.tasks = json.load(f)
            self.update_listbox()
            messagebox.showinfo("Loaded", "To-do list loaded successfully!")

    def load_list_on_start(self):
        if os.path.exists("todo_list.json"):
            with open("todo_list.json", 'r') as f:
                self.tasks = json.load(f)
            self.update_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = CozyTodoApp(root)
    root.mainloop()
