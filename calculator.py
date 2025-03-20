import customtkinter as ctk
import re

# Initialize the main window
root = ctk.CTk()
root.geometry("350x600")  # Increased height to accommodate more history
root.title("Modern Calculator")
root.resizable(False, False)

# Set appearance and color theme
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

# Entry field for input
entry = ctk.CTkEntry(root, font=("Arial", 24), width=330, justify="right", corner_radius=10)
entry.pack(pady=(20, 10))

# Function to handle button clicks
def button_click(value):
    current = entry.get()
    entry.delete(0, "end")
    entry.insert("end", current + value)

# Function to clear entry field
def clear_entry():
    entry.delete(0, "end")

# Safe evaluation of arithmetic expressions
def safe_eval(expression):
    # Remove any characters that are not digits, operators, or parentheses
    expression = re.sub(r'[^0-9+\-*/(). ]', '', expression)
    try:
        # Evaluate the sanitized expression
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except:
        return "Error"

# Function to evaluate the expression
def evaluate_expression():
    expression = entry.get()
    result = safe_eval(expression)
    entry.delete(0, "end")
    entry.insert("end", str(result))
    if result != "Error":
        update_history(f"{expression} = {result}")

# Frame for buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

# Button layout
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

# Define colors for operator and clear buttons
operator_color = "#e67e22"  # Orange
equal_color = "#27ae60"     # Green
clear_color = "#e74c3c"     # Red

# Create buttons dynamically
for text, row, col in buttons:
    if text in {"+", "-", "*", "/"}:
        fg_color = operator_color
    elif text == "=":
        fg_color = equal_color
    else:
        fg_color = "#2c3e50"  # Default button color

    btn = ctk.CTkButton(
        button_frame, text=text, font=("Arial", 18), width=70, height=50,
        corner_radius=10, fg_color=fg_color, hover_color="#34495e",
        command=lambda t=text: button_click(t) if t != "=" else evaluate_expression()
    )
    btn.grid(row=row, column=col, padx=5, pady=5)

# Clear button
clear_btn = ctk.CTkButton(
    root, text="C", font=("Arial", 18), width=150, height=50,
    corner_radius=10, fg_color=clear_color, hover_color="#c0392b",
    command=clear_entry
)
clear_btn.pack(pady=(10, 20))

# History label
history_label = ctk.CTkLabel(root, text="History:", font=("Arial", 25))
history_label.pack()

# History listbox
history_listbox = ctk.CTkTextbox(root, height=300, width=300, state="disabled")
history_listbox.pack(pady=(0, 20))

# Function to update history
def update_history(entry):
    history_listbox.configure(state="normal")
    # Insert the new entry at the end
    history_listbox.insert("end", entry + "\n")
    # Get all current entries
    history = history_listbox.get("1.0", "end-1c").split("\n")
    # If there are more than 9 entries, delete the first one
    if len(history) > 9:
        history_listbox.delete("1.0", "2.0")
    history_listbox.configure(state="disabled")

root.mainloop()
