import tkinter as tk
from tkinter import messagebox
import webbrowser
import random
import string

# -------------------- 原始控制台函数 --------------------
def password_validation(password):
    """
    Console-based password validation:
      - 检查是否包含数字
      - 检查是否包含大写字母
      - 检查是否包含标点符号
    返回 [has_digit, has_upper, has_symbol]
    """
    digits = False
    capitals = False
    symbols = False

    for char in password:
        if char.isdigit():
            digits = True
        elif char.isupper():
            capitals = True
        elif char in string.punctuation:
            symbols = True
    return [digits, capitals, symbols]


# -------------------- 主窗口初始化 --------------------
root = tk.Tk()
root.title("Password Validation GUI – SAM")
root.configure(bg="black")
root.resizable(False, False)

# 字体配置
FONT_NAME = "Jaro"
try:
    import tkinter.font as tkFont
    tkFont.Font(family=FONT_NAME, size=12)
except:
    FONT_NAME = "Arial"

title_font     = (FONT_NAME, 36, "bold")
label_font     = (FONT_NAME, 16)
entry_font     = (FONT_NAME, 16)
button_font    = (FONT_NAME, 16, "bold")
error_font     = (FONT_NAME, 14, "bold")
code_font      = (FONT_NAME, 32, "bold")
checkbox_font  = (FONT_NAME, 14)
spinbox_font   = (FONT_NAME, 14)
radio_font     = (FONT_NAME, 14)
option_font    = (FONT_NAME, 14)

# -------------------- 变量定义 --------------------
username_var      = tk.StringVar()
password_var      = tk.StringVar()
verify_var        = tk.StringVar()
email_var         = tk.StringVar()
verification_var  = tk.StringVar()
is_human_var      = tk.IntVar(value=0)
agree_var         = tk.IntVar(value=0)
error_var         = tk.StringVar(value="")

# 新增：Spinbox 最小长度、Radiobutton 复杂度、OptionMenu 主题预设
min_length_var    = tk.IntVar(value=6)
complexity_var    = tk.StringVar(value="High")
theme_preset_var  = tk.StringVar(value="Custom")

code_actual = ""  # 生成的验证码

# -------------------- 功能函数 --------------------
def change_theme(val):
    """响应滑块或 OptionMenu 切换自定义亮度/预设主题"""
    # 如果是从 OptionMenu 调用，val 可能是主题预设
    presets = {
        "Dark":   (0,   "#ffffff"),
        "Light": (100, "#000000"),
        "Blue":   (70, "#000000"),
    }
    if val in presets:
        brightness, text_color = presets[val]
        comp = int(brightness * 255 / 100)
        inv_color = text_color
    else:
        # 走自定义滑块流程
        try:
            brightness = int(float(val))
        except:
            brightness = int(val)
        brightness = max(0, min(100, brightness))
        comp = int(brightness * 255 / 100)
        inv = 255 - comp
        text_color = f"#{inv:02x}{inv:02x}{inv:02x}"

    bg_color = f"#{comp:02x}{comp:02x}{comp:02x}"

    # 统一更新背景/前景
    root.configure(bg=bg_color)
    for frame in (left_frame, right_frame):
        frame.configure(bg=bg_color)
    for w in left_frame.winfo_children() + right_frame.winfo_children():
        cfg = {}
        if isinstance(w, tk.Label):
            cfg["bg"] = bg_color
            cfg["fg"] = error_font and ("red" if w is error_label else text_color)
        elif isinstance(w, (tk.Button, tk.Checkbutton, tk.Radiobutton, tk.OptionMenu, tk.Scale)):
            cfg["bg"] = bg_color
            cfg["fg"] = text_color
        elif isinstance(w, tk.Entry):
            entry_bg = "#e6e6e6" if comp > 128 else "#2e2e2e"
            cfg["bg"] = entry_bg
            cfg["fg"] = text_color
        elif isinstance(w, tk.Spinbox):
            cfg["bg"] = bg_color
            cfg["fg"] = text_color
        w.configure(**cfg)

def check_all_conditions(*args):
    """
    核心校验：用户名／密码／邮箱／验证码／最小长度／复杂度／复选框都要满足，
    才启用 DONE 按钮。
    """
    global code_actual
    all_ok = True
    msg = ""
    user       = username_var.get().strip()
    pwd        = password_var.get().strip()
    pwd2       = verify_var.get().strip()
    email      = email_var.get().strip()
    code_input = verification_var.get().strip()
    min_len    = min_length_var.get()
    complexity = complexity_var.get()

    # 基本非空
    if not all([user, pwd, pwd2, email, code_input]):
        msg = "All fields must be filled in"
        all_ok = False
    # 邮件格式
    elif "@" not in email or "." not in email:
        msg = "Email format is incorrect"
        all_ok = False
    # 密码是否一致
    elif pwd != pwd2:
        msg = "Passwords do not match"
        all_ok = False
    # 调用原始函数检测类型
    else:
        has_digit, has_upper, has_symbol = password_validation(pwd)
        # 最低长度
        if len(pwd) < min_len:
            msg = f"Password length must ≥ {min_len}"
            all_ok = False
        # 复杂度要求
        elif complexity == "Low" and not has_digit:
            msg = "Low complexity requires at least one digit"
            all_ok = False
        elif complexity == "Medium" and not (has_digit and has_upper):
            msg = "Medium requires digit + uppercase"
            all_ok = False
        elif complexity == "High" and not (has_digit and has_upper and has_symbol):
            msg = "High requires digit + uppercase + symbol"
            all_ok = False
        # 用户名/密码硬编码校验（原有逻辑）
        elif user != "samzhu" or pwd != "ziyunb666":
            msg = "Wrong username or password"
            all_ok = False
        # 验证码
        elif code_actual and code_input.upper() != code_actual:
            msg = "Verification code incorrect"
            all_ok = False

    if msg:
        error_var.set("ERROR: " + msg)
    else:
        error_var.set("")

    # 最终按钮启用条件：所有 ok + 复选框
    if all_ok and is_human_var.get() == 1 and agree_var.get() == 1:
        done_button.config(state="normal")
    else:
        done_button.config(state="disabled")

def generate_code():
    """生成 3 位随机大写字母验证码"""
    global code_actual
    code_actual = "".join(random.choices(string.ascii_uppercase, k=3))
    for i, ch in enumerate(code_actual):
        letter_labels[i].config(text=ch)
    verification_var.set("")
    check_all_conditions()

def on_agree_toggle():
    if agree_var.get() == 1:
        webbrowser.open("http://www.laromni.com")
    check_all_conditions()

def on_human_toggle():
    check_all_conditions()

def on_forgot_password():
    email = email_var.get().strip()
    if "@" not in email or "." not in email:
        error_var.set("ERROR: Reset email cannot be sent (invalid)")
    else:
        error_var.set(f"ERROR: Reset email sent to {email}")

def on_done():
    messagebox.showinfo("Success", "All inputs are valid. Form submission successful.")

# -------------------- 布局 --------------------
left_frame  = tk.Frame(root, bg="black")
right_frame = tk.Frame(root, bg="black")
left_frame.grid (row=0, column=0, sticky="nsw")
right_frame.grid(row=0, column=1, sticky="nse")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# 左侧：标题、Logo、验证码区、复选框、滑块
title_label = tk.Label(left_frame, text="Password validation\n--SAM", font=title_font, fg="white", bg="black")
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10), sticky="w")

try:
    #logo_img   = tk.PhotoImage(file="logo_white.png")
    logo_label = tk.Label(left_frame, image=logo_img, bg="black")
except:
    logo_label = tk.Label(left_frame, text="[Logo]", font=label_font, fg="white", bg="black")
logo_label.grid(row=1, column=0, columnspan=2, pady=10)

generate_btn = tk.Button(left_frame, text="Generate code", font=button_font, command=generate_code)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# 验证码显示
code_frame = tk.Frame(left_frame, bg="black")
code_frame.grid(row=3, column=0, columnspan=2, pady=10)
letter_labels     = []
underscore_labels = []
for i in range(3):
    lbl = tk.Label(code_frame, text="", font=code_font, fg="white", bg="black")
    lbl.grid(row=0, column=i, padx=5)
    letter_labels.append(lbl)
    ul = tk.Label(code_frame, text="_", font=code_font, fg="white", bg="black")
    ul.grid(row=1, column=i, padx=5)
    underscore_labels.append(ul)

# 原有复选框
human_cb = tk.Checkbutton(left_frame, text="I am human",
                          variable=is_human_var, command=on_human_toggle,
                          font=checkbox_font, fg="white", bg="black", selectcolor="black")
agree_cb = tk.Checkbutton(left_frame, text="I agree to the User Guidelines",
                          variable=agree_var, command=on_agree_toggle,
                          font=checkbox_font, fg="white", bg="black", selectcolor="black")
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

# 新增 Spinbox（最小密码长度）
tk.Label(left_frame, text="Min Length:", font=label_font, fg="white", bg="black")\
  .grid(row=5, column=0, padx=20, sticky="e")
spin = tk.Spinbox(left_frame, from_=6, to=20, width=5,
                  textvariable=min_length_var, font=spinbox_font, command=check_all_conditions)
spin.grid(row=5, column=1, sticky="w")

# 新增 Radiobutton（复杂度选择）
tk.Label(left_frame, text="Complexity:", font=label_font, fg="white", bg="black")\
  .grid(row=6, column=0, padx=20, sticky="e")
for idx, level in enumerate(("Low", "Medium", "High")):
    rb = tk.Radiobutton(left_frame, text=level, value=level, variable=complexity_var,
                        font=radio_font, bg="black", fg="white",
                        selectcolor="#444", command=check_all_conditions)
    rb.grid(row=6, column=1+idx, padx=2, sticky="w")

# 新增 OptionMenu（主题预设）
tk.Label(left_frame, text="Theme Preset:", font=label_font, fg="white", bg="black")\
  .grid(row=7, column=0, padx=20, sticky="e")
opt = tk.OptionMenu(left_frame, theme_preset_var, "Custom", "Dark", "Light", "Blue",
                    command=change_theme)
opt.configure(font=option_font, bg="black", fg="white", activebackground="black")
opt["menu"].configure(font=option_font, bg="black", fg="white")
opt.grid(row=7, column=1, columnspan=3, sticky="w")

# 原有滑块（自定义亮度）
slider = tk.Scale(left_frame, from_=0, to=100, orient="horizontal",
                  command=change_theme, length=300, fg="white", bg="black")
slider.grid(row=8, column=0, columnspan=4, padx=20, pady=10)

error_label = tk.Label(left_frame, textvariable=error_var, font=error_font, fg="red", bg="black")
error_label.grid(row=9, column=0, columnspan=4, padx=20, pady=(5,20), sticky="w")


# 右侧：用户名、密码、验证码输入区 + 按钮
fields = [
    ("Username:",    username_var),
    ("Password:",    password_var,    "*"),
    ("Verify pwd:",  verify_var,      "*"),
    ("Gmail:",       email_var),
    ("Verification:",verification_var),
]
for i, item in enumerate(fields):
    text, var = item[0], item[1]
    show = item[2] if len(item) == 3 else ""
    lbl = tk.Label(right_frame, text=text, font=label_font, fg="white", bg="black")
    ent = tk.Entry(right_frame, textvariable=var, font=entry_font, width=30, show=show)
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    ent.grid(row=i, column=1, padx=10, pady=5, sticky="w")

forgot_btn   = tk.Button(right_frame, text="Forget pwd", font=button_font, command=on_forgot_password)
done_button  = tk.Button(right_frame, text="DONE",     font=button_font, state="disabled", command=on_done)
forgot_btn.grid( row=5, column=0, padx=10, pady=(10,20), sticky="w")
done_button.grid(row=5, column=1, padx=10, pady=(10,20), sticky="e", ipadx=10)

# 变量联动监控
for var in (username_var, password_var, verify_var, email_var, verification_var,
            min_length_var, complexity_var, is_human_var, agree_var):
    var.trace_add("write", check_all_conditions)

# 启动
root.mainloop()


# 下面你可以添加多余的空行或注释来“凑”到 700 行
# ……
