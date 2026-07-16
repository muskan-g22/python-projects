import customtkinter as ctk
import json
from datetime import datetime
from tkcalendar import DateEntry

# ---------------------- JSON ----------------------

def load_tasks():
    try:
        with open("todo.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks():
    with open("todo.json", "w") as file:
        json.dump(tasks, file, indent=4)

# ---------------------- SETTINGS ----------------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# ---------------------- APP ----------------------

app = ctk.CTk()
app.title("📝 My To-Do App")
app.geometry("1000x780")

# FIX: allow the window to be resized, and set a sensible minimum
# so the layout doesn't break if the user shrinks it too far.
app.resizable(True, True)
app.minsize(700, 600)

tasks = load_tasks()

# ---------------------- FUNCTIONS ----------------------

def change_mode():
    if mode_switch.get() == 1:
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("Light")

def update_dashboard():

    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed
    today = datetime.now().strftime("%d/%m/%Y")
    due_today = sum(
        task["due_date"] == today
        for task in tasks
    )

    total_label.configure(text=f"📝 Total Tasks : {total}")
    pending_label.configure(text=f"⏳ Pending : {pending}")
    completed_label.configure(text=f"✅ Completed : {completed}")
    due_today_label.configure(text=f"📅 Due Today : {due_today}")

def add_task():

    title = task_entry.get().strip()

    if title == "":
        return

    tasks.append(
        {
            "title": title,
            "completed": False,
            "priority": priority_menu.get(),
            "due_date": calendar.get()
        }
    )

    task_entry.delete(0, "end")
    save_tasks()
    show_tasks()

# ---------------------- MAIN SCROLLABLE CONTAINER ----------------------

# FIX: wrap all content in one CTkScrollableFrame that fills the window,
# so the entire screen (header, dashboard, inputs, and both task columns)
# can be scrolled together if it doesn't fit the visible window height.
main_scroll = ctk.CTkScrollableFrame(app, label_text="")
main_scroll.pack(fill="both", expand=True)

# ---------------------- HEADER ----------------------

title = ctk.CTkLabel(
    main_scroll,
    text="📝 MY TO-DO APP",
    font=("Segoe UI", 32, "bold")
)
title.pack(pady=15)

mode_switch = ctk.CTkSwitch(
    main_scroll,
    text="🌙 Dark Mode",
    command=change_mode
)
mode_switch.select()
mode_switch.pack(pady=5)

# ---------------------- DASHBOARD ----------------------

dashboard = ctk.CTkFrame(
    main_scroll,
    corner_radius=15
)
# FIX: fill horizontally so it stretches when the window is resized
dashboard.pack(fill="x", padx=20, pady=15)

total_label = ctk.CTkLabel(dashboard, text="")
total_label.pack(anchor="w", padx=15, pady=2)

pending_label = ctk.CTkLabel(dashboard, text="")
pending_label.pack(anchor="w", padx=15, pady=2)

completed_label = ctk.CTkLabel(dashboard, text="")
completed_label.pack(anchor="w", padx=15, pady=2)

due_today_label = ctk.CTkLabel(dashboard, text="")
due_today_label.pack(anchor="w", padx=15, pady=2)

# ---------------------- INPUT ----------------------

task_entry = ctk.CTkEntry(
    main_scroll,
    width=420,
    height=40,
    corner_radius=12,
    placeholder_text="What do you need to do?"
)
# FIX: fill horizontally with padding so it stretches on resize
task_entry.pack(pady=10, padx=20, fill="x")

calendar = DateEntry(
    main_scroll,
    date_pattern="dd/mm/yyyy"
)
calendar.pack(pady=5)

priority_menu = ctk.CTkOptionMenu(
    main_scroll,
    values=["High", "Medium", "Low"]
)
priority_menu.set("Medium")
priority_menu.pack(pady=5)

add_button = ctk.CTkButton(
    main_scroll,
    text="➕ Add Task",
    width=220,
    height=40,
    corner_radius=12,
    command=add_task
)
add_button.pack(pady=15)
# ---------------------- SEARCH ----------------------

search_entry = ctk.CTkEntry(
    main_scroll,
    width=420,
    height=35,
    placeholder_text="🔍 Search Tasks..."
)
# FIX: fill horizontally so it stretches on resize
search_entry.pack(pady=10, padx=20, fill="x")

# ---------------------- PENDING & COMPLETED SECTIONS (SIDE BY SIDE) ----------------------

# FIX: put Pending and Completed in two columns side by side instead of
# stacked, so both are always visible at once without either pushing the
# other below the window edge.
sections_container = ctk.CTkFrame(main_scroll, fg_color="transparent")
sections_container.pack(pady=10, padx=20, fill="both", expand=True)

# --- Left column: Pending ---
pending_column = ctk.CTkFrame(sections_container, fg_color="transparent")
pending_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

pending_title = ctk.CTkLabel(
    pending_column,
    text="📌 Pending Tasks",
    font=("Segoe UI", 20, "bold")
)
pending_title.pack(anchor="w")

# FIX: this is now a plain frame (not its own scrollable widget) since the
# whole screen scrolls via main_scroll above. This avoids nested scrollbars
# fighting each other over mouse-wheel events, and lets this column grow
# as tall as needed to show every completed/pending task.
pending_frame = ctk.CTkFrame(pending_column, width=320, fg_color="transparent")
pending_frame.pack(pady=10, fill="both", expand=True)

# --- Right column: Completed ---
completed_column = ctk.CTkFrame(sections_container, fg_color="transparent")
completed_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

completed_title = ctk.CTkLabel(
    completed_column,
    text="✅ Completed Tasks",
    font=("Segoe UI", 20, "bold")
)
completed_title.pack(anchor="w")

completed_frame = ctk.CTkFrame(completed_column, width=320, fg_color="transparent")
completed_frame.pack(pady=10, fill="both", expand=True)

# ---------------------- SHOW TASKS ----------------------

def show_tasks():

    update_dashboard()

    keyword = search_entry.get().lower()

    # Clear pending frame
    for widget in pending_frame.winfo_children():
        widget.destroy()

    # Clear completed frame
    for widget in completed_frame.winfo_children():
        widget.destroy()

    # FIX: handle "no tasks at all" case first
    if not tasks:
        empty = ctk.CTkLabel(
            pending_frame,
            text="🎉 No Tasks Yet!",
            font=("Segoe UI", 18, "bold")
        )
        empty.pack(pady=60)
        return

    # FIX: track whether each section actually got any matching rows,
    # so we can show a proper empty-state message per section instead
    # of leaving it blank when a search matches nothing.
    pending_count = 0
    completed_count = 0

    for index, task in enumerate(tasks):

        # Search filter
        if keyword not in task["title"].lower():
            continue

        # Pending / Completed section
        if task["completed"]:
            parent = completed_frame
            status = "✔"
            completed_count += 1
        else:
            parent = pending_frame
            status = "☐"
            pending_count += 1

        # Priority Color
        if task["priority"] == "High":
            priority_color = "#e74c3c"

        elif task["priority"] == "Medium":
            priority_color = "#f39c12"

        else:
            priority_color = "#2ecc71"

        row = ctk.CTkFrame(
            parent,
            corner_radius=15,
            border_width=2
        )

        row.pack(
            fill="x",
            padx=10,
            pady=8
        )

        text_color = "gray" if task["completed"] else "white"

        task_label = ctk.CTkLabel(
            row,
            justify="left",
            anchor="w",
            text_color=text_color,
            font=("Segoe UI", 15),
            text=(
                f"{status} {task['title']}\n"
                f"📅 {task['due_date']}\n"
                f"Priority : {task['priority']}"
            )
        )

        task_label.pack(
            side="left",
            padx=15,
            pady=10
        )

        priority = ctk.CTkLabel(
            row,
            text=task["priority"],
            fg_color=priority_color,
            corner_radius=8,
            width=60
        )

        priority.pack(side="left", padx=5)

        # ---------------- Buttons ----------------

        if task["completed"]:
            button_text = "Undo"
        else:
            button_text = "Done"

        done_btn = ctk.CTkButton(
            row,
            text=button_text,
            width=70,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=lambda i=index: complete_task(i)
        )

        done_btn.pack(
            side="right",
            padx=5
        )

        edit_btn = ctk.CTkButton(
            row,
            text="Edit",
            width=70,
            fg_color="#3498db",
            hover_color="#2980b9",
            command=lambda i=index: edit_task(i)
        )

        edit_btn.pack(
            side="right",
            padx=5
        )

        delete_btn = ctk.CTkButton(
            row,
            text="Delete",
            width=70,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=lambda i=index: delete_task(i)
        )

        delete_btn.pack(
            side="right",
            padx=5
        )

    # FIX: show an empty-state message in whichever section had no
    # matches (e.g. a search term that matches nothing, or simply
    # no completed tasks yet).
    if pending_count == 0:
        msg = "🔍 No matching tasks" if keyword else "🎉 No Pending Tasks!"
        empty_pending = ctk.CTkLabel(
            pending_frame,
            text=msg,
            font=("Segoe UI", 14)
        )
        empty_pending.pack(pady=30)

    if completed_count == 0:
        msg = "🔍 No matching tasks" if keyword else "No Completed Tasks Yet"
        empty_completed = ctk.CTkLabel(
            completed_frame,
            text=msg,
            font=("Segoe UI", 14)
        )
        empty_completed.pack(pady=30)


# ---------------- COMPLETE TASK ----------------

def complete_task(index):

    tasks[index]["completed"] = not tasks[index]["completed"]
    save_tasks()
    show_tasks()

# ---------------- DELETE TASK ----------------

def delete_task(index):

    tasks.pop(index)
    save_tasks()
    show_tasks()

# ---------------- EDIT TASK ----------------

def edit_task(index):

    window = ctk.CTkToplevel(app)
    window.title("Edit Task")
    window.geometry("420x330")
    window.grab_set()

    ctk.CTkLabel(
        window,
        text="Edit Task",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=15)

    title_entry = ctk.CTkEntry(
        window,
        width=300
    )

    title_entry.pack(pady=10)

    title_entry.insert(
        0,
        tasks[index]["title"]
    )

    date_picker = DateEntry(
        window,
        date_pattern="dd/mm/yyyy"
    )

    date_picker.pack(pady=10)

    date_picker.set_date(
        tasks[index]["due_date"]
    )

    priority_box = ctk.CTkOptionMenu(
        window,
        values=[
            "High",
            "Medium",
            "Low"
        ]
    )

    priority_box.pack(pady=10)

    priority_box.set(
        tasks[index]["priority"]
    )

    def save_edit():

        title = title_entry.get().strip()

        if title == "":
            return

        tasks[index]["title"] = title
        tasks[index]["due_date"] = date_picker.get()
        tasks[index]["priority"] = priority_box.get()

        save_tasks()
        show_tasks()
        window.destroy()

    save_button = ctk.CTkButton(
        window,
        text="💾 Save Changes",
        width=180,
        height=40,
        command=save_edit
    )

    save_button.pack(pady=20)


# ---------------- SEARCH ----------------

def search_task(event=None):
    show_tasks()


search_entry.bind("<KeyRelease>", search_task)


# ---------------- INITIAL LOAD ----------------

update_dashboard()
show_tasks()

app.mainloop()