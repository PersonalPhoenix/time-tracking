from os import getcwd
from json import load, dump
from sqlite3 import connect
from tkinter import filedialog, messagebox


def change_current_path() -> None:
    '''
    'Файл' -> 'Изменить путь экспорта'.
    '''

    dir_name: str = filedialog.askdirectory()
    
    if dir_name.replace(' ', '') == '':

        try: 
            with open ('settings.json', 'w', encoding = 'utf-8') as file:
                dump({'dir_name': f'{getcwd()}'}, file)
        except:
            messagebox.showerror('Внимание', 'Что-то случилось с settings.json\nПуть экспорта: текущая директория')

        messagebox.showinfo('Внимание', f'Путь не был указан.\n\nИспользуется путь по умолчанию:\n{getcwd()}')
        return
    
    try:
        with open('settings.json', 'w', encoding = 'utf-8') as file:
            dump({'dir_name': f'{dir_name}'}, file)
            messagebox.showinfo('Текущий путь экспорта', f'Теперь файлы экспортируются в: {dir_name}')
    except:
        messagebox.showerror('Внимание', 'Что-то случилось с settings.json\nПуть не был изменен')


def current_path() -> None:
    '''
    'Файл' -> 'Текущий путь экспорта'.
    '''

    try:
        with open ('settings.json', 'r', encoding = 'utf-8') as file:
            dir_name: str = load(file)['dir_name']
    except:
        messagebox.showerror('Внимание', 'Что-то случилось с settings.json\nПуть экспорта: текущая директория')

    messagebox.showinfo('Текущий путь для экспорта', f'{dir_name}')


def default_path() -> None:
    '''
    'Файл' -> 'Сделать путь по умолчанию'.
    '''

    try: 
        with open ('settings.json', 'w', encoding = 'utf-8') as file:
            dump({'dir_name': f'{getcwd()}'}, file)
    except:
        messagebox.showerror('Внимание', 'Что-то случилось с settings.json\nПуть экспорта: текущая директория')
    
    messagebox.showinfo('Текущий путь для экспорта', f'Путь экспорта по умолчанию:\n{getcwd()}')


def clear_database() -> None:
    '''
    'Файл' -> 'Очистить базу данных'.
    '''

    if messagebox.askokcancel('Внимание', 'Вы действительно хотите очистить базу данных?'):
        
        try:
            connect = connect('db.sqlite3')
            cursor = connect.cursor()
            cursor.execute('''DELETE FROM sessions;''')
            cursor.execute('''DELETE FROM sqlite_sequence WHERE name = 'sessions';''')
            connect.commit()
            cursor.close()
            messagebox.showinfo('Внимание', 'База данных была успешно очищена')

        except: messagebox.showerror('Ошибка', 'Возникла проблема при подключении к базе данных')
