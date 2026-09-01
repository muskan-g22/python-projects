
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ================= DATABASE =================

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL
)
""")

conn.commit()


# ================= APP SETTINGS =================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ================= MAIN WINDOW =================

app = ctk.CTk()

app.title("Personal Expense Tracker")
app.geometry("1100x700")
app.minsize(950, 600)


# ================= FUNCTIONS =================

def add_expense():

    date = date_entry.get().strip()
    category = category_menu.get()
    description = description_entry.get().strip()
    amount = amount_entry.get().strip()

    if not date or not category or not amount:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in Date, Category and Amount."
        )
        return

    try:
        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )
        return

    cursor.execute("""
        INSERT INTO expenses
        (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    """, (date, category, description, amount))

    conn.commit()

    clear_fields()
    display_expenses()
    update_summary()


def delete_expense():

    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select an expense to delete."
        )
        return

    item = expense_table.item(selected[0])
    expense_id = item["values"][0]

    confirm = messagebox.askyesno(
        "Delete Expense",
        "Are you sure you want to delete this expense?"
    )

    if confirm:

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        conn.commit()

        display_expenses()
        update_summary()


def clear_fields():

    date_entry.delete(0, "end")
    date_entry.insert(
        0,
        datetime.now().strftime("%Y-%m-%d")
    )

    category_menu.set("Select Category")

    description_entry.delete(0, "end")
    amount_entry.delete(0, "end")


def display_expenses():

    for item in expense_table.get_children():
        expense_table.delete(item)

    cursor.execute("""
        SELECT id, date, category, description, amount
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    for expense in expenses:

        expense_table.insert(
            "",
            "end",
            values=(
                expense[0],
                expense[1],
                expense[2],
                expense[3],
                f"₹{expense[4]:,.2f}"
            )
        )


def update_summary():

    # Total
    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total = cursor.fetchone()[0] or 0

    total_value.configure(
        text=f"₹{total:,.2f}"
    )

    # This month
    current_month = datetime.now().strftime("%Y-%m")

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE date LIKE ?
    """, (current_month + "%",))

    monthly = cursor.fetchone()[0] or 0

    monthly_value.configure(
        text=f"₹{monthly:,.2f}"
    )

    # Number of transactions
    cursor.execute(
        "SELECT COUNT(*) FROM expenses"
    )

    count = cursor.fetchone()[0]

    transaction_value.configure(
        text=str(count)
    )


def search_expenses():

    search = search_entry.get().strip()

    for item in expense_table.get_children():
        expense_table.delete(item)

    cursor.execute("""
        SELECT id, date, category, description, amount
        FROM expenses
        WHERE category LIKE ?
           OR description LIKE ?
           OR date LIKE ?
        ORDER BY id DESC
    """, (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

    expenses = cursor.fetchall()

    for expense in expenses:

        expense_table.insert(
            "",
            "end",
            values=(
                expense[0],
                expense[1],
                expense[2],
                expense[3],
                f"₹{expense[4]:,.2f}"
            )
        )


def show_all():

    search_entry.delete(0, "end")

    display_expenses()


def close_app():

    conn.close()
    app.destroy()


# ================= HEADER =================

header = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header.pack(
    fill="x",
    padx=30,
    pady=(25, 10)
)


title = ctk.CTkLabel(
    header,
    text="💰 Personal Expense Tracker",
    font=ctk.CTkFont(
        size=30,
        weight="bold"
    )
)

title.pack(side="left")


subtitle = ctk.CTkLabel(
    header,
    text="Manage your money smarter",
    font=ctk.CTkFont(size=14),
    text_color="#9CA3AF"
)

subtitle.pack(
    side="left",
    padx=15,
    pady=(10, 0)
)


# ================= SUMMARY CARDS =================

summary_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

summary_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


# Total card
total_card = ctk.CTkFrame(
    summary_frame,
    corner_radius=15,
    fg_color="#1E293B"
)

total_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)

ctk.CTkLabel(
    total_card,
    text="TOTAL EXPENSES",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    ),
    text_color="#94A3B8"
).pack(
    anchor="w",
    padx=20,
    pady=(18, 5)
)

total_value = ctk.CTkLabel(
    total_card,
    text="₹0.00",
    font=ctk.CTkFont(
        size=24,
        weight="bold"
    )
)

total_value.pack(
    anchor="w",
    padx=20,
    pady=(0, 18)
)


# Monthly card
monthly_card = ctk.CTkFrame(
    summary_frame,
    corner_radius=15,
    fg_color="#172554"
)

monthly_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)

ctk.CTkLabel(
    monthly_card,
    text="THIS MONTH",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    ),
    text_color="#93C5FD"
).pack(
    anchor="w",
    padx=20,
    pady=(18, 5)
)

monthly_value = ctk.CTkLabel(
    monthly_card,
    text="₹0.00",
    font=ctk.CTkFont(
        size=24,
        weight="bold"
    )
)

monthly_value.pack(
    anchor="w",
    padx=20,
    pady=(0, 18)
)


# Transactions card
transaction_card = ctk.CTkFrame(
    summary_frame,
    corner_radius=15,
    fg_color="#1E293B"
)

transaction_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 0)
)

ctk.CTkLabel(
    transaction_card,
    text="TRANSACTIONS",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    ),
    text_color="#94A3B8"
).pack(
    anchor="w",
    padx=20,
    pady=(18, 5)
)

transaction_value = ctk.CTkLabel(
    transaction_card,
    text="0",
    font=ctk.CTkFont(
        size=24,
        weight="bold"
    )
)

transaction_value.pack(
    anchor="w",
    padx=20,
    pady=(0, 18)
)


# ================= ADD EXPENSE =================

form_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)

form_frame.pack(
    fill="x",
    padx=30,
    pady=15
)


ctk.CTkLabel(
    form_frame,
    text="Add New Expense",
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    )
).grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="w",
    padx=20,
    pady=(18, 12)
)


# Date
ctk.CTkLabel(
    form_frame,
    text="Date"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=20
)

date_entry = ctk.CTkEntry(
    form_frame,
    width=180,
    height=38
)

date_entry.grid(
    row=2,
    column=0,
    padx=20,
    pady=(5, 20)
)

date_entry.insert(
    0,
    datetime.now().strftime("%Y-%m-%d")
)


# Category
ctk.CTkLabel(
    form_frame,
    text="Category"
).grid(
    row=1,
    column=1,
    sticky="w",
    padx=10
)

category_menu = ctk.CTkComboBox(
    form_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Education",
        "Health",
        "Other"
    ],
    width=180,
    height=38
)

category_menu.grid(
    row=2,
    column=1,
    padx=10,
    pady=(5, 20)
)

category_menu.set("Select Category")


# Description
ctk.CTkLabel(
    form_frame,
    text="Description"
).grid(
    row=1,
    column=2,
    sticky="w",
    padx=10
)

description_entry = ctk.CTkEntry(
    form_frame,
    width=220,
    height=38,
    placeholder_text="e.g. Lunch, Bus fare..."
)

description_entry.grid(
    row=2,
    column=2,
    padx=10,
    pady=(5, 20)
)


# Amount
ctk.CTkLabel(
    form_frame,
    text="Amount"
).grid(
    row=1,
    column=3,
    sticky="w",
    padx=10
)

amount_entry = ctk.CTkEntry(
    form_frame,
    width=150,
    height=38,
    placeholder_text="₹ 0.00"
)

amount_entry.grid(
    row=2,
    column=3,
    padx=10,
    pady=(5, 20)
)


# Add button
add_button = ctk.CTkButton(
    form_frame,
    text="+ Add Expense",
    width=150,
    height=38,
    corner_radius=8,
    font=ctk.CTkFont(weight="bold"),
    command=add_expense
)

add_button.grid(
    row=2,
    column=4,
    padx=20,
    pady=(5, 20)
)


# ================= SEARCH =================

search_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

search_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 10)
)


search_entry = ctk.CTkEntry(
    search_frame,
    width=300,
    height=38,
    placeholder_text="🔍 Search expenses..."
)

search_entry.pack(side="left")


ctk.CTkButton(
    search_frame,
    text="Search",
    width=100,
    height=38,
    command=search_expenses
).pack(
    side="left",
    padx=8
)


ctk.CTkButton(
    search_frame,
    text="Show All",
    width=100,
    height=38,
    fg_color="#374151",
    hover_color="#4B5563",
    command=show_all
).pack(side="left")


# ================= TABLE =================

table_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 15)
)


columns = (
    "ID",
    "Date",
    "Category",
    "Description",
    "Amount"
)


style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#1F2937",
    foreground="white",
    rowheight=35,
    fieldbackground="#1F2937",
    borderwidth=0,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#111827",
    foreground="white",
    font=("Arial", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#2563EB")
    ]
)


expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)


for column in columns:

    expense_table.heading(
        column,
        text=column
    )


expense_table.column(
    "ID",
    width=60,
    anchor="center"
)

expense_table.column(
    "Date",
    width=130,
    anchor="center"
)

expense_table.column(
    "Category",
    width=150,
    anchor="center"
)

expense_table.column(
    "Description",
    width=350
)

expense_table.column(
    "Amount",
    width=150,
    anchor="center"
)


expense_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ================= BOTTOM BUTTONS =================

button_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

button_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 20)
)


ctk.CTkButton(
    button_frame,
    text="🗑 Delete Selected",
    width=160,
    height=38,
    fg_color="#DC2626",
    hover_color="#B91C1C",
    command=delete_expense
).pack(side="left")


ctk.CTkButton(
    button_frame,
    text="Clear Fields",
    width=130,
    height=38,
    fg_color="#374151",
    hover_color="#4B5563",
    command=clear_fields
).pack(
    side="left",
    padx=10
)


# ================= START =================

display_expenses()
update_summary()

app.protocol(
    "WM_DELETE_WINDOW",
    close_app
)

app.mainloop()