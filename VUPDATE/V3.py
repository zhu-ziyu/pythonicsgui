import tkinter as tk
from tkinter import messagebox
import webbrowser
import random
import string

# ================= 原始 console 函数 =================
def password_validation(password):

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


# ================ 全局预设 & 状态 ===================
# 预设 10 个随机用户名
preset_usernames = [
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    for _ in range(10)
]
# 当前生成的验证码
code_actual = ""


# ================= 主窗口 & 样式 ====================
root = tk.Tk()
root.title("Password Validation GUI – SAM")
root.configure(bg="black")
root.resizable(False, False)

# 尝试 Jaro 字体，否则回退 Arial
FONT_NAME = "Jaro"
try:
    import tkinter.font as tkFont
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

# =============== Tkinter 变量 ======================
username_var     = tk.StringVar()
password_var     = tk.StringVar()
verify_var       = tk.StringVar()
email_var        = tk.StringVar()
verification_var = tk.StringVar()
is_human_var     = tk.IntVar(value=0)
agree_var        = tk.IntVar(value=0)
error_var        = tk.StringVar(value="")

min_length_var   = tk.IntVar(value=6)
complexity_var   = tk.StringVar(value="High")
theme_preset_var = tk.StringVar(value="Custom")


# ================ 功能函数 ========================
def change_theme(val):
    """
    通过滑块或 OptionMenu 切换背景亮度/预设主题。
    """
    presets = {
        "Dark":  (0,   "#ffffff"),
        "Light":(100, "#000000"),
        "Blue": (70,  "#000000"),
    }

    if val in presets:
        brightness, text_color = presets[val]
        comp = int(brightness * 255 / 100)
    else:
        try:
            brightness = int(float(val))
        except:
            brightness = int(val)
        brightness = max(0, min(100, brightness))
        comp = int(brightness * 255 / 100)
        inv = 255 - comp
        text_color = f"#{inv:02x}{inv:02x}{inv:02x}"

    bg_color = f"#{comp:02x}{comp:02x}{comp:02x}"
    root.configure(bg=bg_color)
    left_frame.configure(bg=bg_color)
    right_frame.configure(bg=bg_color)

    # 更新所有子控件背景/前景色
    for w in left_frame.winfo_children() + right_frame.winfo_children():
        if isinstance(w, tk.Label):
            fg = "red" if w is error_label else text_color
            w.configure(bg=bg_color, fg=fg)
        elif isinstance(w, (tk.Button, tk.Checkbutton, tk.Radiobutton, tk.OptionMenu, tk.Scale)):
            w.configure(bg=bg_color, fg=text_color)
        elif isinstance(w, tk.Entry):
            entry_bg = "#e6e6e6" if comp > 128 else "#2e2e2e"
            w.configure(bg=entry_bg, fg=text_color)
        elif isinstance(w, tk.Spinbox) or isinstance(w, tk.Listbox):
            w.configure(bg=bg_color, fg=text_color)


def check_all_conditions(*args):
    """
    实时检查“是否可以启用 DONE 按钮”：
      - Username/Password/Verify/Email/Code 均非空
      - 已勾选 “I am human” & “I agree”
      - 生成验证码后，输入的验证码与之匹配
    （此处不弹窗，不做格式或逻辑校验，只控制按钮可用状态）
    """
    global code_actual
    user       = username_var.get().strip()
    pwd        = password_var.get().strip()
    pwd2       = verify_var.get().strip()
    email      = email_var.get().strip()
    code_input = verification_var.get().strip()

    can_submit = all([
        user, pwd, pwd2, email, code_input,
        is_human_var.get() == 1,
        agree_var.get() == 1,
        code_actual and code_input.upper() == code_actual
    ])

    done_button.config(state="normal" if can_submit else "disabled")


def generate_code():
    """生成 3 位随机大写字母验证码并显示"""
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
        # 此处也可弹 info 提示
    else:
        error_var.set(f"ERROR: Reset email sent to {email}")
        messagebox.showinfo("Password Reset", f"Reset email sent to {email}")


def full_validation():
    """
    点击 DONE 时执行的完整校验逻辑。
    返回 (True, "") 如果全部通过，否则 (False, "错误消息")。
    包括：
      - 邮件格式
      - 密码一致
      - password_validation 类型检查
      - 最低长度 & 复杂度
      - 硬编码用户名/密码
      - 验证码匹配
    """
    user       = username_var.get().strip()
    pwd        = password_var.get().strip()
    pwd2       = verify_var.get().strip()
    email      = email_var.get().strip()
    code_input = verification_var.get().strip()

    if "@" not in email or "." not in email:
        return False, "Email format is incorrect"
    if pwd != pwd2:
        return False, "Passwords do not match"
    has_digit, has_upper, has_symbol = password_validation(pwd)
    if len(pwd) < min_length_var.get():
        return False, f"Password length must ≥ {min_length_var.get()}"
    comp = complexity_var.get()
    if comp == "Low" and not has_digit:
        return False, "Low complexity requires at least one digit"
    if comp == "Medium" and not (has_digit and has_upper):
        return False, "Medium complexity requires digit + uppercase"
    if comp == "High" and not (has_digit and has_upper and has_symbol):
        return False, "High complexity requires digit + uppercase + symbol"
    if user != "samzhu" or pwd != "ziyunb666":
        return False, "Wrong username or password"
    if code_input.upper() != code_actual:
        return False, "Verification code incorrect"
    return True, ""


def on_done():
    """
    DONE 点击后的处理：先调用 full_validation()，
    失败则弹 error messagebox 并显示到左下角，
    成功则弹 success messagebox。
    """
    ok, msg = full_validation()
    if not ok:
        error_var.set("ERROR: " + msg)
        messagebox.showerror("Validation Error", msg)
    else:
        error_var.set("")
        messagebox.showinfo("Success", "All inputs are valid. Form submission successful.")


def on_listbox_select(evt):
    """从 Listbox 选中用户名后，填入 Username"""
    sel = listbox.curselection()
    if sel:
        idx = sel[0]
        username_var.set(preset_usernames[idx])
        check_all_conditions()


# =================== 布局 ========================
left_frame  = tk.Frame(root, bg="black")
right_frame = tk.Frame(root, bg="black")
left_frame.grid (row=0, column=0, sticky="nsw")
right_frame.grid(row=0, column=1, sticky="nse")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# --- 左侧 ---
title_label = tk.Label(
    left_frame, text="Password validation\n--SAM",
    font=title_font, fg="white", bg="black"
)
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10), sticky="w")

# Logo
try:
    #logo_img   = tk.PhotoImage(file="logo_white.png")
    logo_label = tk.Label(left_frame, image=logo_img, bg="black")
except:
    logo_label = tk.Label(
        left_frame, text="[Logo]",
        font=label_font, fg="white", bg="black"
    )
logo_label.grid(row=1, column=0, columnspan=2, pady=10)

# 生成验证码按钮
generate_btn = tk.Button(
    left_frame, text="Generate code",
    font=button_font, command=generate_code
)
generate_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# 验证码显示区
code_frame = tk.Frame(left_frame, bg="black")
code_frame.grid(row=3, column=0, columnspan=2, pady=10)
letter_labels, underscore_labels = [], []
for i in range(3):
    l = tk.Label(code_frame, text="", font=code_font, fg="white", bg="black")
    l.grid(row=0, column=i, padx=5)
    letter_labels.append(l)
    u = tk.Label(code_frame, text="_", font=code_font, fg="white", bg="black")
    u.grid(row=1, column=i, padx=5)
    underscore_labels.append(u)

# 原有复选框
human_cb = tk.Checkbutton(
    left_frame, text="I am human",
    variable=is_human_var, command=on_human_toggle,
    font=checkbox_font, fg="white", bg="black", selectcolor="black"
)
agree_cb = tk.Checkbutton(
    left_frame, text="I agree to the User Guidelines",
    variable=agree_var, command=on_agree_toggle,
    font=checkbox_font, fg="white", bg="black", selectcolor="black"
)
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

# Spinbox: 最小密码长度
tk.Label(left_frame, text="Min Length:", font=label_font, fg="white", bg="black")\
  .grid(row=5, column=0, padx=20, sticky="e")
tk.Spinbox(
    left_frame, from_=6, to=20, width=5,
    textvariable=min_length_var, font=spinbox_font,
    command=check_all_conditions
).grid(row=5, column=1, sticky="w")

# Radiobutton: 复杂度
tk.Label(left_frame, text="Complexity:", font=label_font, fg="white", bg="black")\
  .grid(row=6, column=0, padx=20, sticky="e")
for idx, lvl in enumerate(("Low","Medium","High")):
    rb = tk.Radiobutton(
        left_frame, text=lvl, value=lvl,
        variable=complexity_var, command=check_all_conditions,
        font=radio_font, fg="white", bg="black", selectcolor="#444"
    )
    rb.grid(row=6, column=1+idx, padx=2, sticky="w")

# OptionMenu: 主题预设
tk.Label(left_frame, text="Theme Preset:", font=label_font, fg="white", bg="black")\
  .grid(row=7, column=0, padx=20, sticky="e")
opt = tk.OptionMenu(
    left_frame, theme_preset_var,
    "Custom","Dark","Light","Blue",
    command=change_theme
)
opt.configure(font=option_font, bg="black", fg="white")
opt["menu"].configure(font=option_font, bg="black", fg="white")
opt.grid(row=7, column=1, columnspan=3, sticky="w")

# 自定义亮度滑块
slider = tk.Scale(
    left_frame, from_=0, to=100, orient="horizontal",
    command=change_theme, length=300,
    fg="white", bg="black"
)
slider.grid(row=8, column=0, columnspan=4, padx=20, pady=10)

# 左下角错误标签
error_label = tk.Label(
    left_frame, textvariable=error_var,
    font=error_font, fg="red", bg="black"
)
error_label.grid(row=9, column=0, columnspan=4, padx=20, pady=(5,20), sticky="w")


# --- 右侧 ---
# Listbox: 预设用户名
tk.Label(
    right_frame, text="Choose preset username:",
    font=label_font, fg="white", bg="black"
).grid(row=0, column=0, columnspan=2, padx=10, pady=(20,5), sticky="w")

listbox = tk.Listbox(
    right_frame, height=6, font=listbox_font, exportselection=False
)
for name in preset_usernames:
    listbox.insert("end", name)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
listbox.bind("<<ListboxSelect>>", on_listbox_select)

# 原有输入区
fields = [
    ("Username:",    username_var),
    ("Password:",    password_var,    "*"),
    ("Verify pwd:",  verify_var,      "*"),
    ("Gmail:",       email_var),
    ("Verification:",verification_var),
]
for i, item in enumerate(fields, start=2):
    text, var = item[0], item[1]
    show = item[2] if len(item)==3 else ""
    lbl = tk.Label(
        right_frame, text=text,
        font=label_font, fg="white", bg="black"
    )
    ent = tk.Entry(
        right_frame, textvariable=var,
        font=entry_font, width=30, show=show
    )
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    ent.grid(row=i, column=1, padx=10, pady=5, sticky="w")

# “忘记密码” & DONE 按钮
forgot_btn  = tk.Button(
    right_frame, text="Forget pwd",
    font=button_font, command=on_forgot_password
)
done_button = tk.Button(
    right_frame, text="DONE",
    font=button_font, state="disabled",
    command=on_done
)
forgot_btn.grid( row=8, column=0, padx=10, pady=(10,20), sticky="w")
done_button.grid(row=8, column=1, padx=10, pady=(10,20),
                 sticky="e", ipadx=10)

for var in (
    username_var, password_var, verify_var,
    email_var, verification_var,
    is_human_var, agree_var
):
    var.trace_add("write", check_all_conditions)

root.mainloop()

