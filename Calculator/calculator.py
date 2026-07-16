import customtkinter as ctk
import math

# ---------------- Window ---------------- #

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("My Calculator")
window.geometry("420x700")

# ---------------- Display ---------------- #

display_frame = ctk.CTkFrame(
    window,
    corner_radius=20,
    fg_color="#FDE6EF"
)

display_frame.pack(
    fill="x",
    padx=20,
    pady=20
)

display = ctk.CTkLabel(
    display_frame,
    text="0",
    font=("Arial", 45, "bold"),
    text_color="black",
    anchor="e"
)

display.pack(
    fill="x",
    padx=20,
    pady=30
)

# ---------------- Logic ---------------- #

display_text = ""
scientific_visible = False

OPERATORS = ["+", "-", "x", "÷", "^"]


def format_number(num):
    """Format a float for display without losing precision or
    dropping into unwanted scientific notation for normal-sized numbers."""
    if num != num or num in (float("inf"), float("-inf")):
        raise ValueError

    # Whole numbers -> show as integers
    if num == int(num) and abs(num) < 1e15:
        return str(int(num))

    # Keep up to 10 decimal places, then trim trailing zeros
    formatted = f"{num:.10f}".rstrip("0").rstrip(".")
    return formatted if formatted else "0"


def get_last_segment(text):
    """Return the number/expression currently being typed (the part after the
    last top-level operator). Respects parentheses so it doesn't split
    inside an already-wrapped function call like sin(30+2)."""
    last_index = -1
    depth = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch in OPERATORS and depth == 0 and i != 0:  # ignore a leading '-'
            last_index = i
    return text[last_index + 1:]


def wrap_function(func_name=None, power=None, reciprocal=False):
    """Wrap the current number/segment in a function call (sin(...), sqrt(...),
    (...)**2, etc.) instead of computing immediately. The actual value is
    only calculated when '=' is pressed, matching real calculator behavior."""
    global display_text
    segment = get_last_segment(display_text)
    prefix = display_text[:len(display_text) - len(segment)]
    base = segment if segment else "0"

    if power is not None:
        wrapped = f"({base})**{power}"
    elif reciprocal:
        wrapped = f"(1/({base}))"
    else:
        wrapped = f"{func_name}({base})"

    display_text = prefix + wrapped



def press(value):
    global display_text, scientific_visible

    # ---------------- Backspace ---------------- #

    if value == "⇚":
        display_text = display_text[:-1]
        display.configure(text=display_text if display_text else "0")
        return

    # ---------------- Clear ---------------- #

    if value == "C":
        display_text = ""
        display.configure(text="0")
        return

    # ---------------- SCI Toggle ---------------- #

    if value == "Sci":
        scientific_visible = not scientific_visible

        if scientific_visible:
            scientific_frame.pack(
                before=button_frame,
                fill="x",
                padx=20,
                pady=10
            )
            window.geometry("420x930")
        else:
            scientific_frame.pack_forget()
            window.geometry("420x700")

        return

    # ---------------- Decimal point (prevent duplicates) ---------------- #

    if value == ".":
        segment = get_last_segment(display_text)
        if "." in segment:
            return  # already has a decimal point in this number
        if segment == "":
            display_text += "0."  # e.g. start of a fresh number -> "0."
        else:
            display_text += "."
        display.configure(text=display_text)
        return

    # ---------------- Operators (with negative-number support) ---------------- #

    if value in OPERATORS:

        # Allow "-" to start a number (unary minus) at the start of the
        # display, or right after another operator.
        if value == "-" and (display_text == "" or display_text[-1] in OPERATORS):
            if display_text != "" and display_text[-1] == "-":
                return  # don't stack multiple minus signs
            display_text += "-"
            display.configure(text=display_text)
            return

        if display_text == "":
            return

        if display_text[-1] in OPERATORS:
            display_text = display_text[:-1]

        display_text += value
        display.configure(text=display_text)
        return

    try:

        # ---------- Scientific Functions (deferred until "=") ---------- #
        # These insert a function call like sin(30) or (9)**2 into the
        # expression instead of computing right away, so the value only
        # appears once "=" is pressed, matching real calculator behavior.

        if value == "x²":
            wrap_function(power=2)

        elif value == "x³":
            wrap_function(power=3)

        elif value == "√":
            wrap_function("sqrt")

        elif value == "1/x":
            wrap_function(reciprocal=True)

        elif value == "sin":
            wrap_function("sin")

        elif value == "cos":
            wrap_function("cos")

        elif value == "tan":
            wrap_function("tan")

        elif value == "log":
            wrap_function("log")

        elif value == "ln":
            wrap_function("ln")

        elif value == "π":
            display_text += str(math.pi)

        elif value == "e":
            display_text += str(math.e)

        # ---------- Percentage ---------- #

        elif value == "%":
            if display_text:
                number = float(display_text)
                display_text = format_number(number / 100)

        # ---------- Equal ---------- #

        elif value == "=":

            expression = (
                display_text
                .replace("x", "*")
                .replace("÷", "/")
                .replace("^", "**")
            )

            # Functions inserted by the scientific buttons are resolved
            # here, in degrees for the trig functions.
            safe_functions = {
                "sin": lambda a: math.sin(math.radians(a)),
                "cos": lambda a: math.cos(math.radians(a)),
                "tan": lambda a: math.tan(math.radians(a)),
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
            }

            result = eval(
                expression,
                {"__builtins__": None},
                safe_functions
            )

            display_text = format_number(result)

        # ---------- Normal Buttons ---------- #

        else:
            display_text += value

        display.configure(
            text=display_text if display_text else "0"
        )

    except Exception:
        display_text = ""
        display.configure(text="Error")


# ---------------- Button Frame ---------------- #

button_frame = ctk.CTkFrame(
    window,
    fg_color="transparent"
)

button_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)
scientific_frame = ctk.CTkFrame(
    window,
    fg_color="transparent"
)

# Hide it initially
scientific_frame.pack_forget()

# Make rows and columns expand

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)

for i in range(4):
    scientific_frame.grid_columnconfigure(i, weight=1)

for i in range(3):
    scientific_frame.grid_rowconfigure(i, weight=1)

# ---------------- Buttons ---------------- #
scientific_buttons = [
    "sin", "cos", "tan", "√",
    "x²", "x³", "1/x", "^",
    "log", "ln", "π", "e"
]
buttons = [
    "Sci", "%", "C", "⇚",
    "7", "8", "9", "÷",
    "4", "5", "6", "x",
    "1", "2", "3", "-",
    ".", "0", "=", "+"
]
for index, value in enumerate(scientific_buttons):

    row = index // 4
    column = index % 4

    button = ctk.CTkButton(
        scientific_frame,
        text=value,
        command=lambda v=value: press(v),
        corner_radius=15,
        height=60,
        font=("Arial", 24, "bold"),
        fg_color="#7C4DFF",
        hover_color="#5E35B1"
    )

    button.grid(
        row=row,
        column=column,
        padx=5,
        pady=5,
        sticky="nsew"
    )

for index, value in enumerate(buttons):

    row = index // 4
    column = index % 4

    # Empty placeholder
    if value == "":
        continue

    # Button colors
    if value == "C":
        fg = "#F42648"
        txt = "black"

    elif value == "=":
        fg = "#0FD9EF"
        txt = "white"

    elif value in ["+", "-", "x", "÷", "%", "⇚"]:
        fg = "#FFFFFF"
        txt = "#F778A1"

    else:
        fg = "#F778A1"
        txt = "white"

    button = ctk.CTkButton(
        button_frame,
        text=value,
        command=lambda v=value: press(v),
        corner_radius=15,
        height=70,
        font=("Arial", 28, "bold"),
        fg_color=fg,
        hover_color="#0740E9",
        text_color=txt
    )

    button.grid(
        row=row,
        column=column,
        padx=6,
        pady=6,
        sticky="nsew"
    )


def keyboard(event):

    if event.keysym == "Return":
        press("=")

    elif event.keysym == "BackSpace":
        press("⇚")

    elif event.keysym == "Escape":
        press("C")

    elif event.char in "0123456789.+-*/()%":

        if event.char == "*":
            press("x")

        elif event.char == "/":
            press("÷")

        else:
            press(event.char)


window.bind("<Key>", keyboard)
window.mainloop()