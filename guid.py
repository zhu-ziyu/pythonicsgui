from tkinter import *
import tkinter.font as tkFont
import random
import string


root = Tk()
root.title("Password Validation GUI – SAM")
root.resizable(False, False)

# 尝试 Jaro 字体，否则回退 Arial
FONT_NAME = "Jaro"
try:
    tkFont.Font(family=FONT_NAME, size=12)
except:
    FONT_NAME = "Arial"

title_font    = (FONT_NAME, 36, "bold")
label_font    = (FONT_NAME, 16)
entry_font    = (FONT_NAME, 16)
button_font   = (FONT_NAME, 16, "bold")
code_font     = (FONT_NAME, 32, "bold")
checkbox_font = (FONT_NAME, 14)
spinbox_font  = (FONT_NAME, 14)
radio_font    = (FONT_NAME, 14)
option_font   = (FONT_NAME, 14)
listbox_font  = (FONT_NAME, 14)



max_repeats_var   = IntVar(value=4)
min_length_var    = IntVar(value=0)
complexity_var    = StringVar(value="High")
theme_preset_var  = StringVar(value="Dark")
username_var      = StringVar()
password_var      = StringVar()
verify_var        = StringVar()
email_var         = StringVar()
verification_var  = StringVar()
is_human_var      = IntVar(value=0)
agree_var         = IntVar(value=0)
error_var         = StringVar(value="")

# 左右两部分
left_frame  = Frame(root)
right_frame = Frame(root)
left_frame.grid (row=0, column=0, sticky="nw")
right_frame.grid(row=0, column=1, sticky="ne")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)


title_label = Label(left_frame,
    text="Password validation\n--SAM",
    font=title_font
)
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10), sticky="w")

logo_label = Label(left_frame,
    text="[Logo]",
    font=label_font
)
logo_label.grid(row=1, column=0, columnspan=2, pady=10)

generate_btn = Button(left_frame,
    text="Generate code",
    font=button_font
)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

code_frame = Frame(left_frame)
code_frame.grid(row=3, column=0, columnspan=2, pady=10)

letter_label1 = Label(code_frame, text="", font=code_font)
letter_label1.grid(row=0, column=0, padx=5)
underscore_label1 = Label(code_frame, text="_", font=code_font)
underscore_label1.grid(row=1, column=0, padx=5)

letter_label2 = Label(code_frame, text="", font=code_font)
letter_label2.grid(row=0, column=1, padx=5)
underscore_label2 = Label(code_frame, text="_", font=code_font)
underscore_label2.grid(row=1, column=1, padx=5)

letter_label3 = Label(code_frame, text="", font=code_font)
letter_label3.grid(row=0, column=2, padx=5)
underscore_label3 = Label(code_frame, text="_", font=code_font)
underscore_label3.grid(row=1, column=2, padx=5)

human_cb = Checkbutton(left_frame,
    text="I am human",
    variable=is_human_var,
    font=checkbox_font
)
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")

agree_cb = Checkbutton(left_frame,
    text="I agree to the User Guidelines",
    variable=agree_var,
    font=checkbox_font
)
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

length_label = Label(left_frame,
    text="Password Length:",
    font=label_font
)
length_label.grid(row=5, column=0, padx=20, sticky="e")

length_spinbox = Spinbox(left_frame,
    from_=0, to=100, width=5,
    textvariable=min_length_var,
    font=spinbox_font,
    state="readonly"
)
length_spinbox.grid(row=5, column=1, sticky="w")

complexity_label = Label(left_frame,
    text="Complexity:",
    font=label_font
)
complexity_label.grid(row=6, column=0, padx=20, sticky="e")

rb_low = Radiobutton(left_frame,
    text="Low", value="Low",
    variable=complexity_var,
    font=radio_font
)
rb_low.grid(row=6, column=1, padx=2, sticky="w")

rb_medium = Radiobutton(left_frame,
    text="Medium", value="Medium",
    variable=complexity_var,
    font=radio_font
)
rb_medium.grid(row=6, column=2, padx=2, sticky="w")

rb_high = Radiobutton(left_frame,
    text="High", value="High",
    variable=complexity_var,
    font=radio_font
)
rb_high.grid(row=6, column=3, padx=2, sticky="w")

theme_label = Label(left_frame,
    text="Theme Preset:",
    font=label_font
)
theme_label.grid(row=7, column=0, padx=20, sticky="e")

opt = OptionMenu(left_frame, theme_preset_var, "Dark", "Light")
opt.configure(font=option_font)
opt.grid(row=7, column=1, columnspan=2, sticky="w")

max_repeats_label = Label(left_frame,
    text="Max repeats:",
    font=label_font
)
max_repeats_label.grid(row=8, column=0, padx=20, sticky="e")

scale = Scale(left_frame,
    from_=0, to=4, orient="horizontal",
    variable=max_repeats_var,
    font=option_font, length=200
)
scale.grid(row=8, column=1, columnspan=2, pady=10, sticky="w")

error_label = Label(left_frame,
    textvariable=error_var,
    font=label_font
)
error_label.grid(row=9, column=0, columnspan=3, padx=20, pady=(5,20), sticky="w")

preset_label = Label(right_frame,
    text="Choose preset username:",
    font=label_font
)
preset_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20,5), sticky="w")

listbox = Listbox(right_frame,
    height=6, font=listbox_font,
    exportselection=False
)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")


username_label = Label(right_frame,
    text="Username:",
    font=label_font
)
username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
username_entry = Entry(right_frame,
    textvariable=username_var,
    font=entry_font,
    width=30
)
username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

password_label = Label(right_frame,
    text="Password:",
    font=label_font
)
password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
password_entry = Entry(right_frame,
    textvariable=password_var,
    font=entry_font,
    width=30,
    show="*"
)
password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

verify_label = Label(right_frame,
    text="Verify pwd:",
    font=label_font
)
verify_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
verify_entry = Entry(right_frame,
    textvariable=verify_var,
    font=entry_font,
    width=30,
    show="*"
)
verify_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

gmail_label = Label(right_frame,
    text="Gmail:",
    font=label_font
)
gmail_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
gmail_entry = Entry(right_frame,
    textvariable=email_var,
    font=entry_font,
    width=30
)
gmail_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

verification_label = Label(right_frame,
    text="Verification:",
    font=label_font
)
verification_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
verification_entry = Entry(right_frame,
    textvariable=verification_var,
    font=entry_font,
    width=30
)
verification_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

validate_btn = Button(right_frame,
    text="Validate pwd",
    font=button_font
)
validate_btn.grid(row=7, column=0, padx=10, pady=(10,20), sticky="w")

done_button = Button(right_frame,
    text="DONE",
    font=button_font,
    state=DISABLED
)
done_button.grid(row=7, column=1, padx=10, pady=(10,20), sticky="e", ipadx=10)

root.mainloop()
