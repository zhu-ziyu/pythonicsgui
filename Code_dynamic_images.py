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

# 字体样式
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

# 预设用户名
preset_usernames = [
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    for _ in range(10)
]

# 变量
max_repeats_var   = IntVar(value=4)
min_length_var    = IntVar(value=0)
complexity_var    = StringVar(value="")
theme_preset_var  = StringVar(value="Dark")
username_var      = StringVar()
password_var      = StringVar()
verify_var        = StringVar()
email_var         = StringVar()
verification_var  = StringVar()
is_human_var      = IntVar(value=0)
agree_var         = IntVar(value=0)
error_var         = StringVar(value="")

def on_generate_code():
    pass

def on_validate_pwd():
    pass

def on_submit():
    pass

def on_username_select(event):
    pass

def on_password_change(*args):
    pass

# 左右两部分
left_frame  = Frame(root)
right_frame = Frame(root)
left_frame.grid (row=0, column=0, sticky="nw")
right_frame.grid(row=0, column=1, sticky="ne")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# --- 左侧：标题 ---
title_label = Label(left_frame,
    text="Password validation\n--SAM",
    font=title_font
)
title_label.grid(row=0, column=0, columnspan=2,
                 padx=20, pady=(20,10))

# --- 左侧：加载并缩放 Logo 图片 ---
# 不使用 Pillow，使用内置 PhotoImage.subsample
logo_img = PhotoImage(file="logo_black.png")
orig_w = logo_img.width()
orig_h = logo_img.height()

# 计算缩放比（整数）
x_ratio = orig_w // 100
y_ratio = orig_h // 100
if x_ratio < 1:
    x_ratio = 1
if y_ratio < 1:
    y_ratio = 1

logo_img = logo_img.subsample(x_ratio, y_ratio)

# 在 Label 中显示图片，并保持引用防止被回收
logo_label = Label(left_frame, image=logo_img)
logo_label.image = logo_img
logo_label.grid(row=1, column=0, columnspan=2, pady=10)


# ——— 在 logo_label.grid(...) 之后加入 ———

# 难度到图片文件的映射
image_map = {
    "Low":    "imgg.png",  # 绿
    "Medium": "imgo.png",  # 橙
    "High":   "imgr.png",  # 红
}

def on_complexity_change(*args):
    sel = complexity_var.get()                     # 读取当前选中的 “Low/Medium/High”
    img_file = image_map.get(sel, "logo_black.png")      # 如果 sel 不在 map 中，回退 logo.png
    new_img = PhotoImage(file=img_file)
    # 缩放到大约 100×100px
    w, h = new_img.width(), new_img.height()
    x_ratio = max(1, w // 100)
    y_ratio = max(1, h // 100)
    new_img = new_img.subsample(x_ratio, y_ratio)
    # 更新到 label
    logo_label.configure(image=new_img)
    logo_label.image = new_img  # 保留引用，防止被 GC



# --- 左侧：其他控件 ---
generate_btn = Button(left_frame,
    text="Generate code",
    font=button_font,
    command=on_generate_code
)
generate_btn.grid(row=2, column=0, columnspan=2,
                  padx=20, pady=10)

code_frame = Frame(left_frame)
code_frame.grid(row=3, column=0, columnspan=2, pady=10)

# 验证码三个字符的 Label
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
    text="I am human", variable=is_human_var,
    font=checkbox_font
)
human_cb.grid(row=4, column=0, padx=20, pady=5, sticky="w")

agree_cb = Checkbutton(left_frame,
    text="I agree to the User Guidelines",
    variable=agree_var, font=checkbox_font
)
agree_cb.grid(row=4, column=1, padx=20, pady=5, sticky="w")

length_label = Label(left_frame,
    text="Password Length:", font=label_font
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
    text="Complexity:", font=label_font
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
    text="Theme Preset:", font=label_font
)
theme_label.grid(row=7, column=0, padx=20, sticky="e")

opt = OptionMenu(left_frame, theme_preset_var, "Dark", "Light")
opt.configure(font=option_font)
opt.grid(row=7, column=1, columnspan=2, sticky="w")

max_repeats_label = Label(left_frame,
    text="Max repeats:", font=label_font
)
max_repeats_label.grid(row=8, column=0, padx=20, sticky="e")

scale = Scale(left_frame,
    from_=0, to=4, orient="horizontal",
    variable=max_repeats_var,
    font=option_font, length=200
)
scale.grid(row=8, column=1, columnspan=2,
           pady=10, sticky="w")

error_label = Label(left_frame,
    textvariable=error_var, font=label_font
)
error_label.grid(row=9, column=0, columnspan=3,
                 padx=20, pady=(5,20), sticky="w")

# --- 右侧 控件 ---
preset_label = Label(right_frame,
    text="Choose preset username:", font=label_font
)
preset_label.grid(row=0, column=0, columnspan=2,
                  padx=10, pady=(20,5), sticky="w")

listbox = Listbox(right_frame,
    height=6, font=listbox_font, exportselection=False
)
listbox.grid(row=1, column=0, columnspan=2,
             padx=10, pady=5, sticky="w")

username_label = Label(right_frame,
    text="Username:", font=label_font
)
username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
username_entry = Entry(right_frame,
    textvariable=username_var,
    font=entry_font, width=30
)
username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

password_label = Label(right_frame,
    text="Password:", font=label_font
)
password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
password_entry = Entry(right_frame,
    textvariable=password_var,
    font=entry_font, width=30, show="*"
)
password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

verify_label = Label(right_frame,
    text="Verify pwd:", font=label_font
)
verify_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
verify_entry = Entry(right_frame,
    textvariable=verify_var,
    font=entry_font, width=30, show="*"
)
verify_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

gmail_label = Label(right_frame,
    text="Gmail:", font=label_font
)
gmail_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
gmail_entry = Entry(right_frame,
    textvariable=email_var,
    font=entry_font, width=30
)
gmail_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

verification_label = Label(right_frame,
    text="Verification:", font=label_font
)
verification_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
verification_entry = Entry(right_frame,
    textvariable=verification_var,
    font=entry_font, width=30
)
verification_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

validate_btn = Button(right_frame,
    text="Validate pwd", font=button_font,
    command=on_validate_pwd
)
validate_btn.grid(row=7, column=0, padx=10, pady=(10,20), sticky="w")

done_button = Button(right_frame,
    text="DONE", font=button_font,
    state=DISABLED, command=on_submit
)
done_button.grid(row=7, column=1, padx=10,
                 pady=(10,20), sticky="e", ipadx=10)

# 绑定事件
listbox.bind("<<ListboxSelect>>", on_username_select)
password_var.trace_add("write", on_password_change)

root.mainloop()
