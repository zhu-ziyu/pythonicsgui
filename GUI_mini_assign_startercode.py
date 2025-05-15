from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import random
import string

from torch.onnx import verification


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


#CREATE WIDGETS
root = Tk()
mainframe = Frame(root)

some_font = Font(family='Jaro', size=20)

title = Label(mainframe, text='GUI MINI ASSIGN', font=some_font)
#左边
text = Entry(mainframe, font=some_font)
password = Entry(mainframe, font=some_font)
veruufypassword = Entry(mainframe, font=some_font)
gamil=Entry(mainframe, font=some_font)
Verification=Entry(mainframe, font=some_font)
checkpwd=Button(mainframe)
done=Button(mainframe)
#右
passtitile=Label(mainframe, text='Password validation', font=some_font)
generate=Button(mainframe, text='Generate password', font=some_font, command=x)
onelabel=Label(mainframe)
twolabel=Label(mainframe)
threelabel=Label(mainframe)
checkhuman=Button(mainframe)
usernameentry=Entry(mainframe)
minleghe=Spinbox(mainframe)
pwdfuza=Checkbutton(mainframe)



#theme
theme=OptionMenu(mainframe)
huakuai=Scale(mainframe, from_=0, to=10)



text.grid(row=0, column=0)
password.grid(row=1, column=0)
veruufypassword.grid(row=2, column=0)
gamil.grid(row=3, column=0)
verification.grid(row=4, column=0)
checkpwd.grid(row=5, column=0)
done.grid(row=6, column=0)
passtitile.grid(row=7, column=0)
generate.grid(row=8, column=0)
onelabel.grid(row=9, column=0)
twolabel.grid(row=9, column=1)
threelabel.grid(row=10, column=1)
checkhuman.grid(row=11, column=1)
pwdfuza.grid(row=12, column=1)

#GRID WIDGETS
mainframe.grid(padx=50, pady=50)

title.grid(row=1, column=1)
root.mainloop()
