import tkinter as tk
from tkinter import messagebox
import webbrowser
import random

# Initialize main window
root = tk.Tk()
root.title("Password Validation")
root.configure(bg="black")
root.resizable(False, False)

# Font configuration (use Jaro if available, else fallback)
FONT_NAME = "Jaro"
try:
    import tkinter.font as tkFont
    tkFont.Font(family=FONT_NAME, size=12)
except:
    FONT_NAME = "Arial"
    # If Jaro font is not installed, fallback to Arial (or default font)

# Define font styles for different UI elements
title_font = (FONT_NAME, 36, "bold")
label_font = (FONT_NAME, 16)
entry_font = (FONT_NAME, 16)
button_font = (FONT_NAME, 16, "bold")
error_font = (FONT_NAME, 14, "bold")
code_font = (FONT_NAME, 32, "bold")
checkbox_font = (FONT_NAME, 14)

# Variables for form inputs and states
username_var = tk.StringVar()
password_var = tk.StringVar()
verify_var = tk.StringVar()
email_var = tk.StringVar()
verification_var = tk.StringVar()  # user input for verification code
is_human_var = tk.IntVar(value=0)
agree_var = tk.IntVar(value=0)
error_var = tk.StringVar(value="")  # error message text

# Store the actual generated verification code
code_actual = ""

# Function to update theme (background and text colors) based on slider value
def change_theme(val):
    try:
        brightness = int(float(val))
    except:
        brightness = int(val)
    brightness = max(0, min(100, brightness))
    # Calculate grayscale color from black (0) to white (255)
    comp = int(brightness * 255 / 100)
    bg_color = f"#{comp:02x}{comp:02x}{comp:02x}"
    inv = 255 - comp
    text_color = f"#{inv:02x}{inv:02x}{inv:02x}"
    # Apply background and foreground colors to widgets
    root.configure(bg=bg_color)
    left_frame.configure(bg=bg_color)
    right_frame.configure(bg=bg_color)
    title_label.configure(bg=bg_color, fg=text_color)
    logo_label.configure(bg=bg_color)
    generate_btn.configure(bg=bg_color, fg=text_color)
    for lbl in letter_labels:
        lbl.configure(bg=bg_color, fg=text_color)
    for ul in underscore_labels:
        ul.configure(bg=bg_color, fg=text_color)
    human_cb.configure(bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color)
    agree_cb.configure(bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color)
    slider.configure(bg=bg_color)
    # Adjust slider trough and text colors for contrast
    if brightness < 50:
        slider.configure(troughcolor="gray", fg="white")
    else:
        slider.configure(troughcolor="lightgray", fg="black")
    # Update right frame widgets' colors
    for widget in right_frame.winfo_children():
        if isinstance(widget, tk.Label):
            if widget == error_label:
                widget.configure(bg=bg_color, fg="red")  # error text stays red
            else:
                widget.configure(bg=bg_color, fg=text_color)
        elif isinstance(widget, tk.Entry):
            # Use slightly off-white/black background for entries for visibility
            entry_bg = "#e6e6e6" if brightness > 50 else "#2e2e2e"
            widget.configure(bg=entry_bg, fg=text_color)
        elif isinstance(widget, tk.Button):
            # Update button text color (keep system default background for buttons)
            if str(widget.cget("text")).lower() == "done":
                # Only change DONE button text when active (enabled)
                if widget['state'] == 'normal':
                    widget.configure(fg=text_color)
            else:
                widget.configure(fg=text_color)

# Function to validate inputs and update error messages & DONE button state
def check_all_conditions(*args):
    global code_actual
    all_ok = True
    msg = ""
    user = username_var.get().strip()
    pwd = password_var.get().strip()
    pwd2 = verify_var.get().strip()
    email = email_var.get().strip()
    code_input = verification_var.get().strip()
    # Check for any empty fields
    if user == "" or pwd == "" or pwd2 == "" or email == "" or code_input == "":
        msg = "All fields must be filled in"
        all_ok = False
    else:
        # Check email format
        if "@" not in email or "." not in email:
            msg = "Email format is incorrect"
            all_ok = False
        # Check if passwords match
        elif pwd != pwd2:
            msg = "Passwords do not match"
            all_ok = False
        # Check username/password correctness (default credentials)
        elif user != "samzhu" or pwd != "ziyunb666":
            msg = "Wrong password"
            all_ok = False
        # Check verification code match (case-insensitive)
        elif code_actual and code_input.upper() != code_actual:
            msg = "Verification code incorrect"
            all_ok = False
    # Update error label text
    if msg:
        error_var.set("ERROR: " + msg)
    else:
        error_var.set("")
    # Update DONE button (enable only if all conditions OK and both checkboxes checked)
    if all_ok and is_human_var.get() == 1 and agree_var.get() == 1:
        done_button.config(state="normal")
    else:
        done_button.config(state="disabled")

# Generate a new verification code and display it on the GUI
def generate_code():
    global code_actual
    code_actual = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    # Display each letter in the code label slots
    for i, ch in enumerate(code_actual):
        letter_labels[i].config(text=ch)
    # Clear the verification Entry field for new input
    verification_var.set("")
    # Clear any prior "code incorrect" error message
    if error_var.get().startswith("ERROR: Verification code incorrect"):
        error_var.set("")
    # Re-validate to update DONE button state
    check_all_conditions()

# Handler for the "I agree to the User Guidelines" checkbox
def on_agree_toggle():
    if agree_var.get() == 1:
        webbrowser.open("http://www.laromni.com")
    check_all_conditions()

# Handler for the "I am human" checkbox
def on_human_toggle():
    check_all_conditions()

# Handler for "forget the password" button
def on_forgot_password():
    email = email_var.get().strip()
    if email == "" or "@" not in email or "." not in email:
        error_var.set("ERROR: Reset email cannot be sent (email is empty or invalid)")
    else:
        error_var.set(f"ERROR: Reset email sent to {email}")

# Handler for "DONE" button (when activated)
def on_done():
    messagebox.showinfo("Success", "All inputs are valid. Form submission successful.")

# Create frames for left and right sections of the layout
left_frame = tk.Frame(root, bg="black")
right_frame = tk.Frame(root, bg="black")
left_frame.grid(row=0, column=0, sticky="nsw")
right_frame.grid(row=0, column=1, sticky="nse")

# Configure grid weights for overall layout (optional, for responsiveness)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

# Left frame widgets
title_label = tk.Label(left_frame, text="Password validation\n--SAM", font=title_font, fg="white", bg="black")
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

# Logo image (displayed above the "Generate code" button)
try:
    logo_img = tk.PhotoImage(file="../logo_white.png")
    logo_label = tk.Label(left_frame, image=logo_img, bg="black")
    logo_label.grid(row=1, column=0, columnspan=2, pady=10)
except Exception as e:
    logo_label = tk.Label(left_frame, text="[Logo]", font=label_font, fg="white", bg="black")
    logo_label.grid(row=1, column=0, columnspan=2, pady=10)

generate_btn = tk.Button(left_frame, text="Generate verification code", font=button_font, command=generate_code)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# Verification code display area (letters and underscores)
code_frame = tk.Frame(left_frame, bg="black")
code_frame.grid(row=3, column=0, columnspan=2, pady=10)
letter_labels = []
underscore_labels = []
for i in range(3):
    lbl = tk.Label(code_frame, text="", font=code_font, fg="white", bg="black")
    lbl.grid(row=0, column=i, padx=5)
    letter_labels.append(lbl)
    ul = tk.Label(code_frame, text="_", font=code_font, fg="white", bg="black")
    ul.grid(row=1, column=i, padx=5)
    underscore_labels.append(ul)

# Checkbutton widgets
human_cb = tk.Checkbutton(left_frame, text="I am human", font=checkbox_font,
                          variable=is_human_var, command=on_human_toggle,
                          fg="white", bg="black", selectcolor="black",
                          activebackground="black", activeforeground="white")
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")

agree_cb = tk.Checkbutton(left_frame, text="I agree to the User Guidelines", font=checkbox_font,
                          variable=agree_var, command=on_agree_toggle,
                          fg="white", bg="black", selectcolor="black",
                          activebackground="black", activeforeground="white")
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

slider = tk.Scale(left_frame, from_=0, to=100, orient="horizontal", command=change_theme, length=300,
                  fg="white", bg="black", highlightbackground="black")
slider.grid(row=5, column=0, columnspan=2, padx=20, pady=10)


error_label = tk.Label(left_frame, textvariable=error_var, font=error_font, fg="red", bg="black")
error_label.grid(row=6, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="w")

user_label = tk.Label(right_frame, text="Username:", font=label_font, fg="white", bg="black")
user_entry = tk.Entry(right_frame, textvariable=username_var, font=entry_font, width=30)
pass_label = tk.Label(right_frame, text="Password:", font=label_font, fg="white", bg="black")
pass_entry = tk.Entry(right_frame, textvariable=password_var, font=entry_font, width=30, show="*")
verify_label = tk.Label(right_frame, text="Verify Password:", font=label_font, fg="white", bg="black")
verify_entry = tk.Entry(right_frame, textvariable=verify_var, font=entry_font, width=30, show="*")
email_label = tk.Label(right_frame, text="Gmail:", font=label_font, fg="white", bg="black")
email_entry = tk.Entry(right_frame, textvariable=email_var, font=entry_font, width=30)
code_label = tk.Label(right_frame, text="Verification:", font=label_font, fg="white", bg="black")
code_entry = tk.Entry(right_frame, textvariable=verification_var, font=entry_font, width=30)


user_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
user_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
pass_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
pass_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
verify_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
verify_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
email_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
code_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
code_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")


forgot_btn = tk.Button(right_frame, text="forget the password", font=button_font, command=on_forgot_password)
forgot_btn.grid(row=5, column=0, padx=10, pady=(10, 20), sticky="w")
done_button = tk.Button(right_frame, text="DONE", font=button_font, state="disabled", command=on_done)
done_button.grid(row=5, column=1, padx=10, pady=(10, 20), sticky="e", ipadx=10)

username_var.trace_add("write", check_all_conditions)
password_var.trace_add("write", check_all_conditions)
verify_var.trace_add("write", check_all_conditions)
email_var.trace_add("write", check_all_conditions)
verification_var.trace_add("write", check_all_conditions)

root.mainloop()
