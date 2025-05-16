from tkinter import *
from tkinter.ttk import *
import webbrowser
import random
import string


# ================= 密码验证函数 =================
def password_validation(password):
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    return has_lower, has_upper, has_digit, has_symbol


# ================ 全局预设 ===================
preset_usernames = [''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) for _ in range(10)]  # 修复的列表推导式
code_actual = ""

# ================= 主窗口 ====================
root = Tk()
root.title("Password Validation GUI – SAM")
root.configure(bg="black")
root.resizable(False, False)

# =============== 样式变量 ===================
FONT_NAME = "Arial"
title_font = (FONT_NAME, 36, "bold")
error_font = (FONT_NAME, 14, "bold")
code_font = (FONT_NAME, 32, "bold")

# =============== 控制变量 ===================
username_var = StringVar()
password_var = StringVar()
email_var = StringVar()
verification_var = StringVar()
is_human_var = IntVar(value=0)
agree_var = IntVar(value=0)
error_var = StringVar(value="")
min_length_var = IntVar(value=0)
complexity_var = StringVar(value="Low")
theme_var = StringVar(value="Dark")
repeat_limit_var = IntVar(value=0)


# =============== 核心功能 ===================
def update_password_length(*args):
    pwd = password_var.get()
    min_length_var.set(len(pwd))


def check_repeating_chars(password, limit):
    if len(password) < 2: return True
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count > limit:
                return False
        else:
            count = 1
    return True


def validate_password():
    pwd = password_var.get()
    error_msg = ""

    # 检查连续重复字符
    if not check_repeating_chars(pwd, repeat_limit_var.get()):
        error_msg = f"连续重复字符过多（最多允许{repeat_limit_var.get()}次）"

    # 复杂度检查
    complexity = complexity_var.get()
    has_lower, has_upper, has_digit, has_symbol = password_validation(pwd)

    if complexity == "Medium":
        if not ((has_lower or has_upper) and (has_digit or has_symbol)):
            error_msg = "中等强度：需要字母+（数字或符号）"
    elif complexity == "High":
        if not (has_digit and has_symbol and (has_lower or has_upper)):
            error_msg = "高强度：需要包含字母、数字和符号"

    error_var.set("错误：" + error_msg if error_msg else "")
    return not bool(error_msg)


def change_theme(theme):
    bg_color = "white" if theme == "Light" else "black"
    fg_color = "black" if theme == "Light" else "white"

    root.configure(bg=bg_color)
    for frame in [left_frame, right_frame]:
        frame.configure(bg=bg_color)
        for widget in frame.winfo_children():
            if isinstance(widget, (Label, Checkbutton, Radiobutton)):
                widget.configure(bg=bg_color, fg=fg_color)
            elif isinstance(widget, Entry):
                widget.configure(bg="white" if theme == "Light" else "#333", fg=fg_color)
            elif isinstance(widget, Button):
                widget.configure(bg="#e0e0e0" if theme == "Light" else "#333", fg=fg_color)

    code_bg = "white" if theme == "Light" else "black"
    code_frame.configure(bg=code_bg)
    for label in letter_labels + underscore_labels:
        label.configure(bg=code_bg, fg=fg_color)


def check_all_conditions(*args):
    pwd = password_var.get()
    can_submit = all([
        username_var.get().strip(),
        pwd,
        email_var.get().strip(),
        verification_var.get().strip().upper() == code_actual,
        is_human_var.get() == 1,
        agree_var.get() == 1,
        validate_password()
    ])
    done_button.config(state="normal" if can_submit else "disabled")


def generate_code():
    global code_actual
    code_actual = "".join(random.choices(string.ascii_uppercase, k=3))
    for i, ch in enumerate(code_actual):
        letter_labels[i].config(text=ch)
    verification_var.set("")
    check_all_conditions()


# ================= 界面布局 ====================
left_frame = Frame(root, bg="black")
right_frame = Frame(root, bg="black")
left_frame.grid(row=0, column=0, sticky="nsw")
right_frame.grid(row=0, column=1, sticky="nse")

# 左侧组件
Label(left_frame, text="密码验证系统\n——SAM", font=title_font, fg="white", bg="black").grid(row=0, column=0,
                                                                                            columnspan=2, padx=20,
                                                                                            pady=(20, 10))

Button(left_frame, text="生成验证码", command=generate_code).grid(row=2, column=0, columnspan=2, pady=10)

code_frame = Frame(left_frame, bg="black")
code_frame.grid(row=3, column=0, columnspan=2)
letter_labels = []
for i in range(3):
    lbl = Label(code_frame, text="", font=code_font, width=2, anchor="center")
    lbl.grid(row=0, column=i, padx=5)
    letter_labels.append(lbl)
    Label(code_frame, text="￣", font=code_font, bg="black").grid(row=1, column=i)

Checkbutton(left_frame, text="我是人类", variable=is_human_var, command=check_all_conditions).grid(row=4, column=0,
                                                                                                   sticky=W)
Checkbutton(left_frame, text="同意用户协议", variable=agree_var,
            command=lambda: [webbrowser.open("http://www.laromni.com"), check_all_conditions()]).grid(row=4, column=1,
                                                                                                      sticky=W)

Label(left_frame, text="重复限制:", bg="black", fg="white").grid(row=5, column=0, sticky=E)
Scale(left_frame, from_=0, to=4, variable=repeat_limit_var, orient=HORIZONTAL).grid(row=5, column=1, sticky=EW)

Label(left_frame, text="密码强度:", bg="black", fg="white").grid(row=6, column=0, sticky=E)
Radiobutton(left_frame, text="低", variable=complexity_var, value="Low").grid(row=6, column=1, sticky=W)
Radiobutton(left_frame, text="中", variable=complexity_var, value="Medium").grid(row=6, column=2, sticky=W)
Radiobutton(left_frame, text="高", variable=complexity_var, value="High").grid(row=6, column=3, sticky=W)

Label(left_frame, text="当前长度:", bg="black", fg="white").grid(row=7, column=0, sticky=E)
Label(left_frame, textvariable=min_length_var, bg="black", fg="white").grid(row=7, column=1, sticky=W)

Label(left_frame, text="主题:", bg="black", fg="white").grid(row=8, column=0, sticky=E)
OptionMenu(left_frame, theme_var, "Dark", "Light", command=change_theme).grid(row=8, column=1, sticky=W)

Label(left_frame, textvariable=error_var, font=error_font, fg="red", bg="black").grid(row=9, column=0, columnspan=4,
                                                                                      pady=10)

# 右侧组件
listbox = Listbox(right_frame, height=6)
for name in preset_usernames:
    listbox.insert(END, name)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
listbox.bind("<<ListboxSelect>>", lambda e: username_var.set(listbox.get(listbox.curselection())))

fields = [
    ("用户名:", username_var),
    ("密码:", password_var, "*"),
    ("邮箱:", email_var),
    ("验证码:", verification_var),
]
for row, (text, var, *show) in enumerate(fields, start=2):
    Label(right_frame, text=text).grid(row=row, column=0, padx=10, pady=5, sticky=E)
    Entry(right_frame, textvariable=var, show=show[0] if show else "").grid(row=row, column=1, padx=10, pady=5)

Button(right_frame, text="验证密码", command=validate_password).grid(row=6, column=0, pady=10)
done_button = Button(right_frame, text="完成", state=DISABLED, command=lambda: error_var.set("验证成功！"))
done_button.grid(row=6, column=1, pady=10)

# ================ 事件绑定 ====================
password_var.trace_add("write", lambda *_: [update_password_length(), check_all_conditions()])
for var in [username_var, password_var, email_var, verification_var, is_human_var, agree_var]:
    var.trace_add("write", check_all_conditions)

root.mainloop()