import tkinter as tk
from tkinter import ttk

subjects = []
selected_index = None
FILE_NAME = "subjects.txt"

# ---------- SAVE ----------
def save_subjects():
    with open(FILE_NAME, "w") as file:
        for sub in subjects:
            file.write(f"{sub['name']},{sub['deadline']},{sub['difficulty']},{sub['hours']},{sub['priority']}\n")

# ---------- LOAD ----------
def load_subjects():
    try:
        with open(FILE_NAME, "r") as file:
            subjects.clear()
            for line in file:
                name, deadline, difficulty, hours, priority = line.strip().split(",")

                subjects.append({
                    "name": name,
                    "deadline": int(deadline),
                    "difficulty": int(difficulty),
                    "hours": float(hours),
                    "priority": int(priority)
                })
    except FileNotFoundError:
        pass

# ---------- ADD ----------
def add_subject():
    name = name_entry.get()
    deadline = deadline_entry.get()
    difficulty = difficulty_entry.get()
    hours = hours_entry.get()

    if not name or not deadline or not difficulty or not hours:
        status_label.config(text="⚠ Fill all fields", fg="red")
        return

    try:
        deadline = int(deadline)
        difficulty = int(difficulty)
        hours = float(hours)
    except ValueError:
        status_label.config(text="⚠ Invalid input", fg="red")
        return

    priority = (difficulty * 2) + (10 - deadline)

    subjects.append({
        "name": name,
        "deadline": deadline,
        "difficulty": difficulty,
        "hours": hours,
        "priority": priority
    })

    save_subjects()

    status_label.config(text="✅ Subject Added", fg="green")

    name_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    difficulty_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)

# ---------- GENERATE ----------
def generate_plan():
    for row in table.get_children():
        table.delete(row)

    if not subjects:
        status_label.config(text="⚠ No subjects added", fg="red")
        return

    sorted_subjects = sorted(subjects, key=lambda x: x["priority"], reverse=True)

    total = len(sorted_subjects)
    morning = sorted_subjects[:total // 2]
    evening = sorted_subjects[total // 2:]

    # Morning
    start = 6.0
    if morning:
        time_per = 2 / len(morning)
        for sub in morning:
            end = start + time_per
            table.insert("", "end", values=(format_time(start), sub["name"], f"{round(time_per,2)} hr"))
            start = end
            table.insert("", "end", values=(format_time(start), "Break", "0.5 hr"))
            start += 0.5

    # Evening
    start = 18.0
    if evening:
        time_per = 5 / len(evening)
        for sub in evening:
            end = start + time_per
            table.insert("", "end", values=(format_time(start), sub["name"], f"{round(time_per,2)} hr"))
            start = end
            table.insert("", "end", values=(format_time(start), "Break", "0.5 hr"))
            start += 0.5

# ---------- SUGGEST ----------
def suggest():
    if not subjects:
        return
    best = max(subjects, key=lambda x: x["priority"])
    status_label.config(text=f"🔥 Study Now: {best['name']}", fg="blue")

# ---------- DELETE ----------
def delete_subject():
    selected = table.selection()

    if not selected:
        status_label.config(text="⚠ Select a subject", fg="red")
        return

    item = table.item(selected[0])
    name = item["values"][1]

    for sub in subjects:
        if sub["name"] == name:
            subjects.remove(sub)
            break

    save_subjects()
    table.delete(selected[0])
    status_label.config(text=f"❌ Deleted: {name}", fg="red")

# ---------- EDIT ----------
def edit_subject():
    global selected_index

    selected = table.selection()

    if not selected:
        status_label.config(text="⚠ Select a subject", fg="red")
        return

    item = table.item(selected[0])
    name = item["values"][1]

    for i, sub in enumerate(subjects):
        if sub["name"] == name:
            selected_index = i

            name_entry.delete(0, tk.END)
            name_entry.insert(0, sub["name"])

            deadline_entry.delete(0, tk.END)
            deadline_entry.insert(0, sub["deadline"])

            difficulty_entry.delete(0, tk.END)
            difficulty_entry.insert(0, sub["difficulty"])

            hours_entry.delete(0, tk.END)
            hours_entry.insert(0, sub["hours"])

            status_label.config(text="✏ Editing...", fg="blue")
            break

# ---------- UPDATE ----------
def update_subject():
    global selected_index

    if selected_index is None:
        status_label.config(text="⚠ Select subject first", fg="red")
        return

    name = name_entry.get()
    deadline = int(deadline_entry.get())
    difficulty = int(difficulty_entry.get())
    hours = float(hours_entry.get())

    priority = (difficulty * 2) + (10 - deadline)

    subjects[selected_index] = {
        "name": name,
        "deadline": deadline,
        "difficulty": difficulty,
        "hours": hours,
        "priority": priority
    }

    save_subjects()
    selected_index = None

    status_label.config(text="✅ Updated", fg="green")

# ---------- TIME ----------
def format_time(t):
    h = int(t)
    m = int((t - h) * 60)
    return f"{h}:{m:02d}"

# ---------- UI ----------
root = tk.Tk()
root.title("AI Study Planner")
root.geometry("700x550")
root.configure(bg="white")

tk.Label(root, text="AI Study Planner",
         font=("Segoe UI", 22, "bold"),
         bg="white").pack(pady=15)

input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(padx=20, pady=10, fill="x")

def entry(parent):
    return tk.Entry(parent, font=("Segoe UI", 10))

labels = ["Subject", "Deadline", "Difficulty", "Hours"]
entries = []

for i, text in enumerate(labels):
    tk.Label(input_frame, text=text, font=("Segoe UI", 11, "bold"),
             bg="#f5f5f5").grid(row=0, column=i, padx=5)
    e = entry(input_frame)
    e.grid(row=1, column=i, padx=5, pady=5)
    entries.append(e)

name_entry, deadline_entry, difficulty_entry, hours_entry = entries

def btn(text, cmd, col):
    tk.Button(btn_frame, text=text, command=cmd,
              bg="#4c6ef5", fg="white",
              font=("Segoe UI", 10, "bold")).grid(row=0, column=col, padx=5)

btn_frame = tk.Frame(root, bg="white")
btn_frame.pack()

btn("Add", add_subject, 0)
btn("Generate", generate_plan, 1)
btn("Suggest", suggest, 2)
btn("Delete", delete_subject, 3)
btn("Edit", edit_subject, 4)
btn("Update", update_subject, 5)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

columns = ("Time", "Subject", "Duration")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

table.pack(expand=True, fill="both", padx=20, pady=20)

status_label = tk.Label(root, text="", bg="white",
                        font=("Segoe UI", 12, "bold"))
status_label.pack()

# LOAD DATA
load_subjects()

root.mainloop()