import customtkinter as ctk
import random
import os

# ------------------ APP SETUP ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("650x550")
app.title("Quiz Master")

# ------------------ DATA ------------------
questions = [
    {"question": "2 + 2 = ?", "options": ["2","3","4","5"], "answer": "4"},
    {"question": "Capital of India?", "options": ["Delhi","Mumbai","Kolkata","Chennai"], "answer": "Delhi"},
    {"question": "5 * 6 = ?", "options": ["30","20","25","15"], "answer": "30"},
    {"question": "Python is?", "options": ["Snake","Language","Game","Car"], "answer": "Language"},
    {"question": "What is the capital of India?","options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],"answer": "New Delhi"},
    {"question":"Sun rises from?","options":["West","East","North","South"],"answer":"East"},
    {"question":"What is the capital of India?","options":["Mumbai","New Delhi","Kolkata","Chennai"],"answer":"New Delhi"},
    {"question":"Which planet is known as the Red Planet?","options":["Earth","Venus","Mars","Jupiter"],"answer":"Mars"},
    {"question":"How many days are there in a week?","options":["5","6","7","8"],"answer":"7"},
    {"question":"Which animal is known as the King of the Jungle?","options":["Tiger","Elephant","Lion","Leopard"],"answer":"Lion"},
    {"question":"What is the national bird of India?","options":["Parrot","Peacock","Sparrow","Crow"],"answer":"Peacock"},
    {"question":"Which is the largest ocean on Earth?","options":["Indian Ocean","Atlantic Ocean","Arctic Ocean","Pacific Ocean"],"answer":"Pacific Ocean"},
    {"question":"How many colors are there in a rainbow?","options":["5","6","7","8"],"answer":"7"},
    {"question":"Which gas do plants absorb from the atmosphere?","options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"answer":"Carbon Dioxide"},
    {"question":"Which is the largest mammal in the world?","options":["Elephant","Blue Whale","Giraffe","Hippopotamus"],"answer":"Blue Whale"}
]

random.shuffle(questions)  # 🔥 RANDOM QUESTIONS

current_question = 0
score = 0
high_score = 0

# ------------------ HIGH SCORE ------------------
def load_high_score():
    global high_score
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    else:
        high_score = 0

def save_high_score():
    global high_score, score
    if score > high_score:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

# ------------------ SCREENS ------------------
def clear_screen():
    for widget in app.winfo_children():
        widget.destroy()

# ------------------ MENU ------------------
def show_menu():
    clear_screen()

    title = ctk.CTkLabel(app, text="🎮 Quiz Master", font=("Arial", 30, "bold"))
    title.pack(pady=40)

    start_btn = ctk.CTkButton(app, text="Start Game", width=200, command=start_game)
    start_btn.pack(pady=10)

    exit_btn = ctk.CTkButton(app, text="Exit", width=200, command=app.destroy)
    exit_btn.pack(pady=10)

    high_label = ctk.CTkLabel(app, text=f"🏆 High Score: {high_score}", font=("Arial", 16))
    high_label.pack(pady=20)

# ------------------ GAME ------------------
def start_game():
    global current_question, score
    current_question = 0
    score = 0
    random.shuffle(questions)

    show_game_screen()
    show_question()

def show_game_screen():
    clear_screen()

    global question_label, result_label, progress_label
    global option_buttons

    progress_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
    progress_label.pack(pady=5)

    question_label = ctk.CTkLabel(app, text="", font=("Arial", 20), wraplength=500)
    question_label.pack(pady=20)

    option_buttons = []
    for i in range(4):
        btn = ctk.CTkButton(app, width=300)
        btn.pack(pady=5)
        option_buttons.append(btn)

    result_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
    result_label.pack(pady=10)

# ------------------ QUESTION ------------------
def show_question():
    if current_question >= len(questions):
        show_result()
        return

    q = questions[current_question]

    progress_label.configure(text=f"Question {current_question+1}/{len(questions)}")
    question_label.configure(text=q["question"])
    result_label.configure(text="")

    for i, btn in enumerate(option_buttons):
        btn.configure(
            text=q["options"][i],
            fg_color="transparent",
            command=lambda opt=q["options"][i], b=btn: check_answer(opt, b)
        )

# ------------------ CHECK ------------------
def check_answer(selected_option, button):
    global current_question, score

    correct = questions[current_question]["answer"]

    for btn in option_buttons:
        btn.configure(state="disabled")

    if selected_option == correct:
        score += 1
        button.configure(fg_color="green")
        result_label.configure(text="Correct ✅", text_color="green")
    else:
        button.configure(fg_color="red")
        result_label.configure(text=f"Wrong ❌ ({correct})", text_color="red")

    current_question += 1
    app.after(1000, next_question)

def next_question():
    for btn in option_buttons:
        btn.configure(state="normal")
    show_question()

# ------------------ RESULT ------------------
def show_result():
    clear_screen()
    save_high_score()

    result = ctk.CTkLabel(app,
        text=f"🎉 Final Score: {score}/{len(questions)}",
        font=("Arial", 26, "bold"))
    result.pack(pady=40)

    back_btn = ctk.CTkButton(app, text="Back to Menu", command=show_menu)
    back_btn.pack(pady=10)

# ------------------ START ------------------
load_high_score()
show_menu()

app.mainloop()