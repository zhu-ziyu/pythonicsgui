from tkinter import *
import tkinter.font as tkFont
import random
import string
import webbrowser
from tkinter import messagebox

root = Tk()
root.title("Password Validation GUI – SAM")
root.resizable(False, False)

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


preset_usernames = [
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    for _ in range(10)
]

max_repeats_var   = IntVar(value=4)
min_length_var    = IntVar(value=0)
complexity_var    = StringVar(value="Low")
theme_preset_var  = StringVar(value="Dark")
username_var      = StringVar()
password_var      = StringVar()
verify_var        = StringVar()
email_var         = StringVar()
verification_var  = StringVar()
is_human_var      = IntVar(value=0)
agree_var         = IntVar(value=0)
error_var         = StringVar(value="")
success_var = StringVar(value="")


code_actual = ""   # 当前验证码

def full_error_message():
    if not username_var.get().strip():
        return "Username cannot be empty"
    email = email_var.get().strip()
    if not email:
        return "Email cannot be empty"
    if "@" not in email or "." not in email:
        return "Email format is incorrect"
    pwd = password_var.get()
    if not pwd:
        return "Password cannot be empty"
    if not verify_var.get():
        return "Please verify password"
    if pwd != verify_var.get():
        return "Passwords do not match"
    # 密码强度 & 重复
    msg = strength_error_message()
    if msg:
        return msg
    # 复选框
    if is_human_var.get() != 1:
        return "Please confirm you are human"
    if agree_var.get() != 1:
        return "You must agree to the User Guidelines"
    # 验证码
    if not code_actual:
        return "Please generate a verification code"
    code_input = verification_var.get().strip()
    if not code_input:
        return "Verification code cannot be empty"
    if code_input.upper() != code_actual:
        return "Verification code incorrect"
    return ""


def password_validation(pwd: str):
    """返回 (has_digit, has_letter, has_symbol)"""
    has_digit  = any(c.isdigit() for c in pwd)
    has_letter = any(c.isalpha() for c in pwd)
    has_symbol = any(c in string.punctuation for c in pwd)
    return has_digit, has_letter, has_symbol


def repeats_ok(pwd: str, limit: int):
    cnt = 1
    prev = ""
    for c in pwd:
        if c == prev:
            cnt += 1
            if cnt > limit:
                return False
        else:
            cnt = 1
            prev = c
    return True


def strength_error_message():

    pwd = password_var.get()
    has_digit, has_letter, has_symbol = password_validation(pwd)
    comp = complexity_var.get()
    mr   = max_repeats_var.get()

    if comp == "":                         return "Choose a complexity level"
    if len(pwd) == 0:                      return "Password cannot be empty"
    if len(pwd) < min_length_var.get():    return f"Password length must ≥ {min_length_var.get()}"
    if not repeats_ok(pwd, mr):            return f"Max {mr} consecutive repeats allowed"

    if comp == "Low":
        return ""                          # 无额外要求
    if comp == "Medium":
        if not (has_letter and (has_digit or has_symbol)):
            return "Medium needs letter + (digit or symbol)"
    if comp == "High":
        if not (has_letter and has_digit and has_symbol):
            return "High needs letter + digit + symbol"

    return ""


def refresh_done_state():
    ok = (full_error_message() == "")
    done_button.config(state=NORMAL if ok else DISABLED)


def on_generate_code():
    global code_actual
    code_actual = ''.join(random.choices(string.ascii_uppercase, k=3))
    letter_label1.config(text=code_actual[0])
    letter_label2.config(text=code_actual[1])
    letter_label3.config(text=code_actual[2])
    verification_var.set("")
    refresh_done_state()

def on_validate_pwd():
    msg = full_error_message()
    if msg == "":
        error_var.set("")
        success_var.set("ALL PASS")
    else:
        error_var.set("ERROR: " + msg)
        success_var.set("")
    refresh_done_state()



def on_submit():
    messagebox.showinfo("注册成功", "你已经成功注册")

def on_username_select(event):
    sel = listbox.curselection()
    if sel:
        username_var.set(listbox.get(sel[0]))
    refresh_done_state()

def on_password_change():
    min_length_var.set(len(password_var.get()))
    refresh_done_state()

image_map = {
    "Low":    "imgg.png",
    "Medium": "imgo.png",
    "High":   "imgr.png",
}
def on_complexity_change():
    sel = complexity_var.get()
    img_file = image_map.get(sel, "logo_black.png")
    try:
        new_img = PhotoImage(file=img_file)
        w, h = new_img.width(), new_img.height()
        x_ratio = max(1, w // 100)
        y_ratio = max(1, h // 100)
        new_img = new_img.subsample(x_ratio, y_ratio)
        logo_label.configure(image=new_img)
        logo_label.image = new_img
    except Exception:
        pass  # 图片缺失时静默

    refresh_done_state()
#已经失效
#def on_max_repeats_change():
#    pwd = password_var.get()
#    if pwd:
#        msg = strength_error_message()
#        if msg.startswith("Max ") and "repeats" in msg:
#            error_var.set("ERROR: " + msg)
#        else:
#            error_var.set("")
#    refresh_done_state()


def on_misc_change():
    refresh_done_state()

def change_theme(choice):
    if choice == "Dark":
        bg, fg = "black", "white"
        logo_label.config(image=logo_white_img)
        logo_label.image = logo_white_img
    else:
        bg, fg = "white", "black"
        logo_label.config(image=logo_black_img)
        logo_label.image = logo_black_img

    root.config(bg=bg)
    left_frame.config(bg=bg)
    right_frame.config(bg=bg)

    for w in left_frame.winfo_children() + right_frame.winfo_children():
        # 错误永远红，成功永远绿
        if w is error_label:
            w.config(bg=bg, fg="red")
        elif w is success_label:
            w.config(bg=bg, fg="green")
        elif isinstance(w, Spinbox):
            w.config(bg=bg, fg="black")
        else:
            try:
                w.config(bg=bg, fg=fg)
            except:
                pass


left_frame  = Frame(root)
right_frame = Frame(root)
left_frame.grid (row=0, column=0, sticky="nw")
right_frame.grid(row=0, column=1, sticky="ne")

# --- 左：标题 & Logo ---
title_label = Label(left_frame, text="Password validation\n--SAM", font=title_font)
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10))

logo_black_img = PhotoImage(file="logo_black.png")
logo_black_img = logo_black_img.subsample(
    max(1, logo_black_img.width()  // 100),
    max(1, logo_black_img.height() // 100)
)
logo_white_img = PhotoImage(file="logo_white.png")
logo_white_img = logo_white_img.subsample(
    max(1, logo_white_img.width()  // 100),
    max(1, logo_white_img.height() // 100)
)

logo_label = Label(left_frame, image=logo_black_img)
logo_label.image = logo_black_img
logo_label.grid(row=1, column=0, columnspan=2, pady=10)

#验证码
generate_btn = Button(left_frame, text="Generate code",
                      font=button_font, command=on_generate_code)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

code_frame = Frame(left_frame)
code_frame.grid(row=3, column=0, columnspan=2, pady=10)
letter_label1 = Label(code_frame, text="", font=code_font)
letter_label2 = Label(code_frame, text="", font=code_font)
letter_label3 = Label(code_frame, text="", font=code_font)
underscore_label1 = Label(code_frame, text="_", font=code_font)
underscore_label2 = Label(code_frame, text="_", font=code_font)
underscore_label3 = Label(code_frame, text="_", font=code_font)
letter_label1.grid    (row=0, column=0, padx=5)
letter_label2.grid    (row=0, column=1, padx=5)
letter_label3.grid    (row=0, column=2, padx=5)
underscore_label1.grid(row=1, column=0, padx=5)
underscore_label2.grid(row=1, column=1, padx=5)
underscore_label3.grid(row=1, column=2, padx=5)

#复选框
human_cb = Checkbutton(left_frame, text="I am human",
                       variable=is_human_var, font=checkbox_font,
                       command=refresh_done_state)
agree_cb = Checkbutton(left_frame,
    text="I agree to the User Guidelines",
    variable=agree_var,
    font=checkbox_font,
    command=lambda: webbrowser.open("http://www.laromni.com")
)

human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

Label(left_frame, text="Password Length:", font=label_font)\
    .grid(row=5, column=0, padx=20, sticky="e")
Spinbox(left_frame, from_=0, to=100, width=5, textvariable=min_length_var,
        font=spinbox_font, state="readonly")\
    .grid(row=5, column=1, sticky="w")

Label(left_frame, text="Complexity:", font=label_font)\
    .grid(row=6, column=0, padx=20, sticky="e")
rb_low    = Radiobutton(left_frame, text="Low",    value="Low",
                        variable=complexity_var, font=radio_font,
                        command=on_complexity_change)
rb_medium = Radiobutton(left_frame, text="Medium", value="Medium",
                        variable=complexity_var, font=radio_font,
                        command=on_complexity_change)
rb_high   = Radiobutton(left_frame, text="High",   value="High",
                        variable=complexity_var, font=radio_font,
                        command=on_complexity_change)
rb_low.grid   (row=6, column=1, padx=2, sticky="w")
rb_medium.grid(row=6, column=2, padx=2, sticky="w")
rb_high.grid  (row=6, column=3, padx=2, sticky="w")

#Theme Preset
Label(left_frame, text="Theme Preset:", font=label_font) \
    .grid(row=7, column=0, padx=20, sticky="e")
theme_preset_var.set("Light")   # 默认 Light
opt = OptionMenu(
    left_frame,
    theme_preset_var,
    "Light", "Dark",
    command=change_theme
)
opt.config(font=option_font)
opt.grid(row=7, column=1, columnspan=2, sticky="w")


#Max repeats已经弃用功能
#Label(left_frame, text="Max repeats:", font=label_font)\
#   .grid(row=8, column=0, padx=20, sticky="e")
#Scale(left_frame, from_=0, to=4, orient="horizontal", variable=max_repeats_var,
#      font=option_font, length=200,
#      command=lambda e: on_max_repeats_change())\
#    .grid(row=8, column=1, columnspan=2, pady=10, sticky="w")

# --- 错误消息 ---
error_label = Label(left_frame, textvariable=error_var, font=label_font, fg="red")
error_label.grid(row=9, column=0, columnspan=3, padx=20, pady=(5,20), sticky="w")

# ================= 右侧 =================
Label(right_frame, text="Choose random username:", font=label_font)\
    .grid(row=0, column=0, columnspan=2, padx=10, pady=(20,5), sticky="w")

listbox = Listbox(right_frame, height=6, font=listbox_font, exportselection=False)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
for name in preset_usernames:
    listbox.insert(END, name)

# 输入框
Label(right_frame, text="Username:", font=label_font)\
    .grid(row=2, column=0, padx=10, pady=5, sticky="e")
Entry(right_frame, textvariable=username_var, font=entry_font, width=30)\
    .grid(row=2, column=1, padx=10, pady=5, sticky="w")

Label(right_frame, text="Password:", font=label_font)\
    .grid(row=3, column=0, padx=10, pady=5, sticky="e")
Entry(right_frame, textvariable=password_var, font=entry_font, width=30, show="*")\
    .grid(row=3, column=1, padx=10, pady=5, sticky="w")

Label(right_frame, text="Verify pwd:", font=label_font)\
    .grid(row=4, column=0, padx=10, pady=5, sticky="e")
Entry(right_frame, textvariable=verify_var, font=entry_font, width=30, show="*")\
    .grid(row=4, column=1, padx=10, pady=5, sticky="w")

Label(right_frame, text="Gmail:", font=label_font)\
    .grid(row=5, column=0, padx=10, pady=5, sticky="e")
Entry(right_frame, textvariable=email_var, font=entry_font, width=30)\
    .grid(row=5, column=1, padx=10, pady=5, sticky="w")

Label(right_frame, text="Verification:", font=label_font)\
    .grid(row=6, column=0, padx=10, pady=5, sticky="e")
Entry(right_frame, textvariable=verification_var, font=entry_font, width=30)\
    .grid(row=6, column=1, padx=10, pady=5, sticky="w")

validate_btn = Button(right_frame, text="Validate pwd",
                      font=button_font, command=on_validate_pwd)
validate_btn.grid(row=7, column=0, padx=10, pady=(10,20), sticky="w")

done_button = Button(right_frame, text="DONE",
                     font=button_font, state=DISABLED, command=on_submit)
done_button.grid(row=7, column=1, padx=10, pady=(10,20), sticky="e", ipadx=10)

success_label = Label(
    right_frame,
    textvariable=success_var,
    font=label_font,
    fg="green"
)
success_label.grid(row=8, column=1, sticky="e", padx=10, pady=(0,10))


footer_label = Label(
    right_frame,
    text="ICS3U1\nMADE BY SAM",
    font=label_font
)
footer_label.grid(row=9, column=1, sticky="e", padx=10, pady=(0,10))



listbox.bind("<<ListboxSelect>>", on_username_select)
password_var.trace_add("write", lambda name, index, mode: on_password_change())
verify_var.trace_add("write",  lambda name, index, mode: on_misc_change)
verification_var.trace_add("write", lambda name, index, mode: on_misc_change)
is_human_var.trace_add("write",lambda name, index, mode: on_misc_change)
agree_var.trace_add("write",lambda name, index, mode: on_misc_change)
complexity_var.trace_add("write", lambda name, index, mode: on_complexity_change())
change_theme(theme_preset_var.get())


root.mainloop()
