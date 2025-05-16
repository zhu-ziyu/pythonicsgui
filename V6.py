from tkinter import *
import random
import string

# 辅助函数用于密码验证
def has_letter(pwd):
    return any(c.isalpha() for c in pwd)

def has_upper(pwd):
    return any(c.isupper() for c in pwd)

def has_lower(pwd):
    return any(c.islower() for c in pwd)

def has_digit(pwd):
    return any(c.isdigit() for c in pwd)

def has_symbol(pwd):
    return any(c in string.punctuation for c in pwd)

def has_long_run(pwd, max_len):
    if len(pwd) == 0:
        return False
    count = 1
    for i in range(1, len(pwd)):
        if pwd[i] == pwd[i-1]:
            count += 1
            if count > max_len:
                return True
        else:
            count = 1
    return False

def get_max_allowed_run():
    return max_repeats_var.get() + 1

# 全局变量
preset_usernames = [''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) for _ in range(10)]
code_actual = ""

# Tkinter 变量
username_var = StringVar()
password_var = StringVar()
verify_var = StringVar()
email_var = StringVar()
verification_var = StringVar()
is_human_var = IntVar(value=0)
agree_var = IntVar(value=0)
error_var = StringVar(value="")
min_length_var = IntVar(value=6)
complexity_var = StringVar(value="High")
theme_preset_var = StringVar(value="Dark")
max_repeats_var = IntVar(value=2)
password_length_var = StringVar(value="Length: 0")

# 函数
def change_theme(val):
    if val == "Dark":
        bg_color = "black"
        text_color = "white"
        entry_bg = "#2e2e2e"
    elif val == "Light":
        bg_color = "white"
        text_color = "black"
        entry_bg = "#e6e6e6"
    else:
        return
    root.configure(bg=bg_color)
    left_frame.configure(bg=bg_color)
    right_frame.configure(bg=bg_color)
    code_frame.configure(bg=bg_color)  # 确保验证码框架背景更新
    for w in left_frame.winfo_children() + right_frame.winfo_children():
        if isinstance(w, Label):
            fg = "red" if w is error_label else text_color
            w.configure(bg=bg_color, fg=fg)
        elif isinstance(w, (Button, Checkbutton, Radiobutton, OptionMenu)):
            w.configure(bg=bg_color, fg=text_color)
        elif isinstance(w, Entry):
            w.configure(bg=entry_bg, fg=text_color)
        elif isinstance(w, (Spinbox, Listbox)):
            w.configure(bg=bg_color, fg=text_color)
        elif isinstance(w, Scale):
            w.configure(bg=bg_color, fg=text_color, troughcolor=bg_color)

def check_all_conditions(*args):
    global code_actual
    error_msg = ""
    user = username_var.get().strip()
    pwd = password_var.get().strip()
    pwd2 = verify_var.get().strip()
    email = email_var.get().strip()
    code_input = verification_var.get().strip()
    if not user:
        error_msg = "需要输入用户名"
    elif not pwd:
        error_msg = "需要输入密码"
    elif not pwd2:
        error_msg = "需要输入确认密码"
    elif not email:
        error_msg = "需要输入邮箱"
    elif not code_input:
        error_msg = "需要输入验证码"
    elif is_human_var.get() != 1:
        error_msg = "必须勾选‘我是人类’"
    elif agree_var.get() != 1:
        error_msg = "必须同意用户指南"
    elif code_actual and code_input.upper() != code_actual:
        error_msg = "验证码不正确"
    else:
        if pwd != pwd2:
            error_msg = "两次输入的密码不匹配"
        elif len(pwd) < min_length_var.get():
            error_msg = f"密码长度必须至少为 {min_length_var.get()} 个字符"
        elif complexity_var.get() == "Medium" and not (has_letter(pwd) and (has_digit(pwd) or has_symbol(pwd))):
            error_msg = "中等复杂性要求至少包含一个字母和一个数字或符号"
        elif complexity_var.get() == "High" and not (has_upper(pwd) and has_lower(pwd) and has_digit(pwd) and has_symbol(pwd)):
            error_msg = "高复杂性要求包含大写字母、小写字母、数字和符号"
        elif has_long_run(pwd, get_max_allowed_run()):
            max_run = get_max_allowed_run()
            error_msg = f"密码包含超过 {max_run} 个连续相同字符"
    if error_msg:
        error_var.set("错误: " + error_msg)
        done_button.config(state="disabled")
    else:
        error_var.set("")
        done_button.config(state="normal")

def generate_code():
    global code_actual
    code_actual = "".join(random.choices(string.ascii_uppercase, k=3))
    for i, ch in enumerate(code_actual):
        letter_labels[i].config(text=ch)
    verification_var.set("")
    check_all_conditions()

def on_agree_toggle():
    check_all_conditions()

def on_human_toggle():
    check_all_conditions()

def full_validation():
    error_msg = ""
    user = username_var.get().strip()
    pwd = password_var.get().strip()
    pwd2 = verify_var.get().strip()
    email = email_var.get().strip()
    code_input = verification_var.get().strip()
    if not user:
        error_msg = "需要输入用户名"
    elif not pwd:
        error_msg = "需要输入密码"
    elif not pwd2:
        error_msg = "需要输入确认密码"
    elif not email:
        error_msg = "需要输入邮箱"
    elif not code_input:
        error_msg = "需要输入验证码"
    elif is_human_var.get() != 1:
        error_msg = "必须勾选‘我是人类’"
    elif agree_var.get() != 1:
        error_msg = "必须同意用户指南"
    elif code_actual and code_input.upper() != code_actual:
        error_msg = "验证码不正确"
    else:
        if pwd != pwd2:
            error_msg = "两次输入的密码不匹配"
        elif len(pwd) < min_length_var.get():
            error_msg = f"密码长度必须至少为 {min_length_var.get()} 个字符"
        elif complexity_var.get() == "Medium" and not (has_letter(pwd) and (has_digit(pwd) or has_symbol(pwd))):
            error_msg = "中等复杂性要求至少包含一个字母和一个数字或符号"

            error_msg = "高复杂性要求包含大写字母、小写字母、数字和符号"
        elif has_long_run(pwd, get_max_allowed_run()):
            max_run = get_max_allowed_run()
            error_msg = f"密码包含超过 {max_run} 个连续相同字符"
    if error_msg:
        return False, error_msg
    else:
        return True, ""

def on_done():
    ok, msg = full_validation()
    if ok:
        error_var.set("成功: 所有输入均有效")
    else:
        error_var.set("错误: " + msg)

def on_listbox_select(evt):
    sel = listbox.curselection()
    if sel:
        idx = sel[0]
        username_var.set(preset_usernames[idx])
        check_all_conditions()

# 主窗口
root = Tk()
root.title("密码验证 GUI – SAM")
root.configure(bg="black")
root.resizable(False, False)

# 字体
title_font = ("Jaro", 36, "bold")
label_font = ("Jaro", 16)
entry_font = ("Jaro", 16)
button_font = ("Jaro", 16, "bold")
error_font = ("Jaro", 14, "bold")
code_font = ("Jaro", 32, "bold")
checkbox_font = ("Jaro", 14)
spinbox_font = ("Jaro", 14)
radio_font = ("Jaro", 14)
option_font = ("Jaro", 14)
listbox_font = ("Jaro", 14)

# 框架
left_frame = Frame(root, bg="black")
right_frame = Frame(root, bg="black")
left_frame.grid(row=0, column=0, sticky="nsw")
right_frame.grid(row=0, column=1, sticky="nse")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# 左侧框架控件
title_label = Label(left_frame, text="密码验证\n--SAM", font=title_font, fg="white", bg="black")
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10), sticky="w")

logo_label = Label(left_frame, text="[Logo]", font=label_font, fg="white", bg="black")
logo_label.grid(row=1, column=0, columnspan=2, pady=10)

generate_btn = Button(left_frame, text="生成验证码", font=button_font, command=generate_code)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

code_frame = Frame(left_frame, bg="black")
code_frame.grid(row=3, column=0, columnspan=2, pady=10)
letter_labels = []
for i in range(3):
    l = Label(code_frame, text="", font=code_font, fg="white", bg="black")
    l.grid(row=0, column=i, padx=5)
    letter_labels.append(l)

human_cb = Checkbutton(left_frame, text="我是人类", variable=is_human_var, command=on_human_toggle, font=checkbox_font, fg="white", bg="black", selectcolor="black")
agree_cb = Checkbutton(left_frame, text="我同意用户指南", variable=agree_var, command=on_agree_toggle, font=checkbox_font, fg="white", bg="black", selectcolor="black")
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

Label(left_frame, text="最小长度:", font=label_font).grid(row=5, column=0, padx=20, sticky="e")
Spinbox(left_frame, from_=6, to=20, width=5, textvariable=min_length_var, font=spinbox_font).grid(row=5, column=1, sticky="w")

Label(left_frame, text="复杂性:", font=label_font).grid(row=6, column=0, padx=20, sticky="e")
for idx, lvl in enumerate(("低", "中", "高")):
    rb = Radiobutton(left_frame, text=lvl, value=["Low", "Medium", "High"][idx], variable=complexity_var, font=radio_font, fg="white", bg="black", selectcolor="#444")
    rb.grid(row=6, column=1+idx, padx=2, sticky="w")

Label(left_frame, text="主题预设:", font=label_font).grid(row=7, column=0, padx=20, sticky="e")
opt = OptionMenu(left_frame, theme_preset_var, "Dark", "Light", command=change_theme)
opt.configure(font=option_font)
opt["menu"].configure(font=option_font)
opt.grid(row=7, column=1, sticky="w")

Label(left_frame, text="最大连续相同字符:", font=label_font).grid(row=8, column=0, sticky="e")
slider = Scale(left_frame, from_=0, to=4, orient="horizontal", variable=max_repeats_var, length=200)
slider.grid(row=8, column=1, sticky="w")

error_label = Label(left_frame, textvariable=error_var, font=error_font, fg="red", bg="black")
error_label.grid(row=9, column=0, columnspan=2, padx=20, pady=(5,20), sticky="w")

# 右侧框架控件
Label(right_frame, text="选择预设用户名:", font=label_font).grid(row=0, column=0, columnspan=2, padx=10, pady=(20,5), sticky="w")

listbox = Listbox(right_frame, height=6, font=listbox_font, exportselection=False)
for name in preset_usernames:
    listbox.insert("end", name)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
listbox.bind("<<ListboxSelect>>", on_listbox_select)

fields = [
    ("用户名:", username_var),
    ("密码:", password_var),
    ("确认密码:", verify_var),
    ("邮箱:", email_var),
    ("验证码:", verification_var),
]
for i, item in enumerate(fields, start=2):
    text, var = item[0], item[1]
    lbl = Label(right_frame, text=text, font=label_font)
    ent = Entry(right_frame, textvariable=var, font=entry_font, width=30)
    if text in ("密码:", "确认密码:"):
        ent.config(show="*")
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    ent.grid(row=i, column=1, padx=10, pady=5, sticky="w")

Label(right_frame, textvariable=password_length_var).grid(row=3, column=2, sticky="w")

done_button = Button(right_frame, text="完成", font=button_font, state="disabled", command=on_done)
done_button.grid(row=8, column=1, padx=10, pady=(10,20), sticky="e", ipadx=10)

# 跟踪变量变化
for var in (username_var, password_var, verify_var, email_var, verification_var, is_human_var, agree_var):
    var.trace_add("write", check_all_conditions)
min_length_var.trace_add("write", check_all_conditions)
complexity_var.trace_add("write", check_all_conditions)
max_repeats_var.trace_add("write", check_all_conditions)
password_var.trace_add("write", lambda *args: password_length_var.set(f"长度: {len(password_var.get())}"))

root.mainloop()