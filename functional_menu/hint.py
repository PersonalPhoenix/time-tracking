from tkinter import messagebox


def guide_message() -> messagebox:
    messagebox.showinfo(
'Подсказка', 
'Данное приложение предназначено для учета личного времени.\n\n\
При вводе имени сесии можно использовать Enter вместо предложенных кнопок.\n\n\
Часовой пояс в приложении UTC+3 (МСК)')

def contact_message() -> messagebox:
    messagebox.showinfo(
'Контакты', 
'Вы можете связаться с автором.\n\n\
email: applmacter@gmail.com\n\n\
github: https://github.com/PersonalPhoenix')

def copyright_message() -> messagebox:
    messagebox.showinfo('Copyright', 'Copyright © 2023 by PersonalPhoenix')