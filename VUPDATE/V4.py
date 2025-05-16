from tkinter import *
from tkinter import messagebox
import webbrowser
import random
import string
import tkinter.font as tkFont

# ================= 主窗口 & 样式 ====================
root = Tk()
root.title("Password Validation GUI – SAM")
root.configure(bg="black")
root.resizable(False, False)

# 尝试 Jaro 字体，否则回退 Arial
FONT_NAME = "Jaro"
try:
    tkFont.Font(family=FONT_NAME, size=12)
except:
    FONT_NAME = "Arial"

# 字体样式
title_font    = (FONT_NAME, 36, "bold")
label_font    = (FONT_NAME, 16)
entry_font    = (FONT_NAME, 16)
button_font   = (FONT_NAME, 16, "bold")
error_font    = (FONT_NAME, 14, "bold")
code_font     = (FONT_NAME, 32, "bold")
checkbox_font = (FONT_NAME, 14)
spinbox_font  = (FONT_NAME, 14)
radio_font    = (FONT_NAME, 14)
option_font   = (FONT_NAME, 14)
listbox_font  = (FONT_NAME, 14)

# ================ 全局预设 & 状态 ===================
preset_usernames = [
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    for _ in range(10)
]
code_actual       = ""                # 还保留验证码功能

# 这些变量必须在 root = Tk() 之后创建
max_repeats_var   = IntVar(value=4)   # 滑块：最大允许连续重复字符
min_length_var    = IntVar(value=0)   # 动态显示当前密码长度
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

# ================= 原始 console 函数 =================
def password_validation(password):
    """
    检查密码中是否包含：数字、字母、标点符号
    返回 [has_digit, has_letter, has_symbol]
    """
    digits = False
    letters = False
    symbols = False

    for ch in password:
        if ch.isdigit():
            digits = True
        elif ch.isalpha():
            letters = True
        elif ch in string.punctuation:
            symbols = True
    return [digits, letters, symbols]


# ================ 功能函数 ========================
def change_theme(val):
    """
    仅保留 Dark/Light 主题：
    Dark：黑底白字；Light：白底黑字（Generate code 背景也设为白）
    """
    if val == "Light":
        bg, fg = "white", "black"
    else:
        bg, fg = "black", "white"

    root.configure(bg=bg)
    left_frame.configure(bg=bg)
    right_frame.configure(bg=bg)
    for w in left_frame.winfo_children() + right_frame.winfo_children():
        if isinstance(w, Label):
            fg_color = "red" if w is error_label else fg
            w.configure(bg=bg, fg=fg_color)
        elif isinstance(w, (Button, Checkbutton, Radiobutton, OptionMenu, Scale)):
            w.configure(bg=bg, fg=fg)
        elif isinstance(w, Entry):
            entry_bg = "#e6e6e6" if bg == "white" else "#2e2e2e"
            w.configure(bg=entry_bg, fg=fg)
        elif isinstance(w, (Spinbox, Listbox)):
            w.configure(bg=bg, fg=fg)
    generate_btn.configure(bg=bg, fg=fg)


def check_all_conditions(*args):
    """
    根据密码、复杂度、最小长度（动态）、最大重复限制，决定 DONE 按钮是否可用
    """
    pwd = password_var.get()
    has_digit, has_letter, has_symbol = password_validation(pwd)
    comp = complexity_var.get()
    # 检查重复字符
    mr = max_repeats_var.get()
    repeats_ok = True
    count = 1
    prev = ""
    for c in pwd:
        if c == prev:
            count += 1
            if count > mr:
                repeats_ok = False
                break
        else:
            count = 1
            prev = c
    length_ok = len(pwd) >= min_length_var.get()

    # 复杂度判定
    if comp == "Low":
        comp_ok = True
    elif comp == "Medium":
        comp_ok = has_letter and (has_digit or has_symbol)
    else:  # High
        comp_ok = has_letter and has_digit and has_symbol

    valid = repeats_ok and length_ok and comp_ok
    done_button.config(state=NORMAL if valid else DISABLED)


def generate_code():
    """保留原有验证码功能"""
    global code_actual
    code_actual = "".join(random.choices(string.ascii_uppercase, k=3))
    for i, ch in enumerate(code_actual):
        letter_labels[i].config(text=ch)
    verification_var.set("")
    check_all_conditions()


def on_agree_toggle(*args):
    if agree_var.get() == 1:
        webbrowser.open("http://www.laromni.com")
    check_all_conditions()


def on_human_toggle(*args):
    check_all_conditions()


def on_validate_password():
    """
    点击“Validate pwd”后，调用 check_all_conditions，
    并在左下角 error_label 显示不通过原因
    """
    check_all_conditions()
    if done_button["state"] == NORMAL:
        error_var.set("")  # 全部通过
    else:
        pwd = password_var.get()
        has_digit, has_letter, has_symbol = password_validation(pwd)
        comp = complexity_var.get()
        # 找出不通过的具体原因
        if len(pwd) < min_length_var.get():
            msg = f"Password length must ≥ {min_length_var.get()}"
        else:
            mr = max_repeats_var.get()
            cnt = 1
            prev = ""
            too_many = False
            for c in pwd:
                if c == prev:
                    cnt += 1
                    if cnt > mr:
                        too_many = True
                        break
                else:
                    cnt = 1
                    prev = c
            if too_many:
                msg = f"Max {mr} consecutive repeats allowed"
            elif comp == "Medium" and not (has_letter and (has_digit or has_symbol)):
                msg = "Medium requires letter + (digit or symbol)"
            elif comp == "High" and not (has_letter and has_digit and has_symbol):
                msg = "High requires letter + digit + symbol"
            else:
                msg = "Invalid password"
        error_var.set("ERROR: " + msg)


def on_done():
    """DONE 点击后，仅在左下角显示成功信息"""
    error_var.set("All checks passed!")


def on_listbox_select(evt):
    sel = listbox.curselection()
    if sel:
        username_var.set(preset_usernames[sel[0]])
        check_all_conditions()


def update_password_length(*args):
    """密码输入变化时，更新左侧的“密码长度”Spinbox"""
    pwd = password_var.get()
    min_length_var.set(len(pwd))
    check_all_conditions()

# ================ 绑定 Trace ========================
password_var.trace_add("write", update_password_length)
complexity_var.trace_add("write", check_all_conditions)
max_repeats_var.trace_add("write", check_all_conditions)
agree_var.trace_add("write", on_agree_toggle)
is_human_var.trace_add("write", on_human_toggle)

# =================== 布局 ========================
left_frame  = Frame(root, bg="black")
right_frame = Frame(root, bg="black")
left_frame.grid (row=0, column=0, sticky="nsw")
right_frame.grid(row=0, column=1, sticky="nse")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# --- 左侧 ---
title_label = Label(
    left_frame, text="Password validation\n--SAM",
    font=title_font, fg="white", bg="black"
)
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10), sticky="w")

logo_label = Label(
    left_frame, text="[Logo]",
    font=label_font, fg="white", bg="black"
)
logo_label.grid(row=1, column=0, columnspan=2, pady=10)

generate_btn = Button(
    left_frame, text="Generate code",
    font=button_font, command=generate_code
)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

code_frame = Frame(left_frame, bg="black")
code_frame.grid(row=3, column=0, columnspan=2, pady=10)
letter_labels = []
for i in range(3):
    l = Label(code_frame, text="", font=code_font, fg="white", bg="black")
    l.grid(row=0, column=i, padx=5)
    letter_labels.append(l)

human_cb = Checkbutton(
    left_frame, text="I am human",
    variable=is_human_var, font=checkbox_font,
    fg="white", bg="black", selectcolor="black"
)
agree_cb = Checkbutton(
    left_frame, text="I agree to the User Guidelines",
    variable=agree_var, font=checkbox_font,
    fg="white", bg="black", selectcolor="black"
)
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

Label(left_frame, text="Password Length:", font=label_font, fg="white", bg="black")\
    .grid(row=5, column=0, padx=20, sticky="e")
Spinbox(
    left_frame, from_=0, to=100, width=5,
    textvariable=min_length_var,
    font=spinbox_font, state="readonly"
).grid(row=5, column=1, sticky="w")

Label(left_frame, text="Complexity:", font=label_font, fg="white", bg="black")\
    .grid(row=6, column=0, padx=20, sticky="e")
for idx, lvl in enumerate(("Low", "Medium", "High")):
    rb = Radiobutton(
        left_frame, text=lvl, value=lvl,
        variable=complexity_var,
        font=radio_font, fg="white", bg="black", selectcolor="#444"
    )
    rb.grid(row=6, column=1+idx, padx=2, sticky="w")

Label(left_frame, text="Theme Preset:", font=label_font, fg="white", bg="black")\
    .grid(row=7, column=0, padx=20, sticky="e")
opt = OptionMenu(
    left_frame, theme_preset_var,
    "Dark", "Light",
    command=change_theme
)
opt.configure(font=option_font, bg="black", fg="white")
opt["menu"].configure(font=option_font, bg="black", fg="white")
opt.grid(row=7, column=1, columnspan=2, sticky="w")

Label(left_frame, text="Max repeats:", font=label_font, fg="white", bg="black")\
    .grid(row=8, column=0, padx=20, sticky="e")
Scale(
    left_frame, from_=0, to=4, orient="horizontal",
    variable=max_repeats_var, font=option_font,
    bg="black", fg="white", length=200
).grid(row=8, column=1, columnspan=2, pady=10, sticky="w")

error_label = Label(
    left_frame, textvariable=error_var,
    font=error_font, fg="red", bg="black"
)
error_label.grid(row=9, column=0, columnspan=3, padx=20, pady=(5,20), sticky="w")

# --- 右侧 ---
Label(
    right_frame, text="Choose preset username:",
    font=label_font, fg="white", bg="black"
).grid(row=0, column=0, columnspan=2, padx=10, pady=(20,5), sticky="w")
listbox = Listbox(
    right_frame, height=6, font=listbox_font, exportselection=False
)
for name in preset_usernames:
    listbox.insert("end", name)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
listbox.bind("<<ListboxSelect>>", on_listbox_select)

fields = [
    ("Username:",    username_var),
    ("Password:",    password_var,    "*"),
    ("Verify pwd:",  verify_var,      "*"),
    ("Gmail:",       email_var),
    ("Verification:",verification_var),
]
for i, item in enumerate(fields, start=2):
    text, var = item[0], item[1]
    show = item[2] if len(item) == 3 else ""
    lbl = Label(right_frame, text=text, font=label_font, fg="white", bg="black")
    ent = Entry(right_frame, textvariable=var, font=entry_font, width=30, show=show)
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    ent.grid(row=i, column=1, padx=10, pady=5, sticky="w")

validate_btn = Button(
    right_frame, text="Validate pwd",
    font=button_font, command=on_validate_password
)
done_button = Button(
    right_frame, text="DONE",
    font=button_font, state=DISABLED,
    command=on_done
)
validate_btn.grid(row=8, column=0, padx=10, pady=(10,20), sticky="w")
done_button.grid(row=8, column=1, padx=10, pady=(10,20), sticky="e", ipadx=10)

root.mainloop()
