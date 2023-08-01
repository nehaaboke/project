import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

def add_task():
    task_description = task_entry.get()
    deadline_date = deadline_entry.get()

    if not task_description:
        messagebox.showwarning("Empty Task", "Please enter a task description.")
        return

    if not deadline_date:
        messagebox.showwarning("Empty Deadline", "Please enter a deadline for the task.")
        return

    tasks.append({"description": task_description, "deadline": deadline_date, "completed": False})
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    save_tasks_to_file()
    display_tasks()

def delete_task():
    selected_index = task_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No Task Selected", "Please select a task to delete.")
        return

    index = selected_index[0]
    del tasks[index]
    save_tasks_to_file()
    display_tasks()

def update_task():
    selected_index = task_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No Task Selected", "Please select a task to update.")
        return

    index = selected_index[0]
    new_description = task_entry.get()
    new_deadline = deadline_entry.get()

    if not new_description:
        messagebox.showwarning("Empty Task", "Please enter a task description.")
        return

    if not new_deadline:
        messagebox.showwarning("Empty Deadline", "Please enter a deadline for the task.")
        return

    tasks[index]["description"] = new_description
    tasks[index]["deadline"] = new_deadline
    save_tasks_to_file()
    display_tasks()

def complete_task():
    selected_index = task_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No Task Selected", "Please select a task to mark as completed.")
        return

    index = selected_index[0]
    tasks[index]["completed"] = True
    tasks[index]["completed_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_tasks_to_file()
    display_tasks()
    messagebox.showinfo("Task Completed", "Task marked as completed. Check the prompt for details.")
    completion_time = tasks[index]["completed_time"]
    completion_description = tasks[index]["description"]
    messagebox.showinfo("Task Completed", f"The task '{completion_description}' was completed at {completion_time}")

def save_tasks_to_file():
    with open("tasks.csv", "w", newline='') as file:
        writer = csv.writer(file)
        for task in tasks:
            writer.writerow([task['description'], task['deadline'], task['completed'], task.get('completed_time', '')])

def load_tasks_from_file():
    try:
        with open("tasks.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                description, deadline, completed, completed_time = row
                tasks.append({"description": description, "deadline": deadline, "completed": bool(completed),
                              "completed_time": completed_time if completed else None})
    except FileNotFoundError:
        pass

def display_tasks():
    global task_listbox
    task_listbox.delete(0, tk.END)
    for task in tasks:
        completion_status = "Completed" if task["completed"] else "Pending"
        task_listbox.insert(tk.END, f"{task['description']} - {task['deadline']} ({completion_status})")

def main():
    global task_entry
    global deadline_entry
    global tasks
    global task_listbox

    tasks = []
    load_tasks_from_file()

    root = tk.Tk()
    root.title("Todo List App")

    # Labels and Entry Fields
    task_label = tk.Label(root, text="Task:")
    task_label.grid(row=0, column=0, padx=5, pady=5)
    task_entry = tk.Entry(root)
    task_entry.grid(row=0, column=1, padx=5, pady=5)

    deadline_label = tk.Label(root, text="Deadline:")
    deadline_label.grid(row=1, column=0, padx=5, pady=5)
    deadline_entry = tk.Entry(root)
    deadline_entry.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    add_button = tk.Button(root, text="Add Task", command=add_task)
    add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    update_button = tk.Button(root, text="Update Task", command=update_task)
    update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    delete_button = tk.Button(root, text="Delete Task", command=delete_task)
    delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    complete_button = tk.Button(root, text="Complete Task", command=complete_task)
    complete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Task Listbox
    task_listbox = tk.Listbox(root, width=50)
    task_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    display_tasks()

    root.mainloop()

if __name__ == "__main__":
    main()
