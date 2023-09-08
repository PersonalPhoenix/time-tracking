from tkinter import Label, Frame, Button, messagebox
import sqlite3

from .change_name import ChangeName
from .toplevel_mixin import ToplevelMixin


class CreateCrudWindow(ToplevelMixin):
    '''
    Класс для Toplevel окна, отображения детальной информации
    записи по двойному клику пользователя, с функционалом
    изменения имени сессии и удаления записи.
    '''

    def __init__(self, values, width,
                 height, width_alignment, height_alignment, title_window) -> None:
        super().__init__(width, height,
                         width_alignment, height_alignment, title_window)

        # кортеж данных выбранной записи.
        self.values = values
        
        '''
        Разметка Toplevel окна.
        '''

        # frame'ы для информации о записи журнала.
        left_frame = Frame(self, background = '#1e293b')
        left_frame.place(relx = 0, rely = 0, relheight = 0.7, relwidth = 0.5)

        right_frame = Frame(self, background = '#1e293b')
        right_frame.place(relx = 0.5, rely = 0, relheight = 0.7, relwidth = 0.5)

        # frame для кнопки 'Изменить имя сессии'.
        bottom_left_frame = Frame(self, background = '#1e293b')
        bottom_left_frame.place(relx = 0, rely = 0.7, relheight = 0.3, relwidth = 0.5)

        # frame для кнопки 'Удалить запись'.
        bottom_right_frame = Frame(self, background = '#1e293b')
        bottom_right_frame.place(relx = 0.5, rely = 0.7, relheight = 0.3, relwidth = 0.5)

        '''
        Виджеты Toplevel окна.
        '''

        # кнопка для изменения имени сессии.
        self.change_name_session_button = Button(bottom_left_frame, text = 'Изменить имя сессии', 
                                                 background = '#abd926', font = 'arial 14', width = 20,
                                                 cursor = 'hand2', command = self.__change_name_note)
        self.change_name_session_button.pack(expand = True)

        # кнопка для удаления записи.
        self.delete_note_button = Button(bottom_right_frame, text = 'Удалить запись', 
                                         background = '#ff000a', font = 'arial 14', width = 20, 
                                         cursor = 'hand2', command = self.__delete_note)
        self.delete_note_button.pack(expand = True)

        # номер сесии.
        self.id_label = Label(left_frame, text = f'№ {self.values[0]}',
                         background = '#1e293b', foreground = '#d6e7ed',
                         font = 'arial 14')
        self.id_label.pack(expand = True)

        # имя сессии.
        self.name_label = Label(right_frame, text = f'Имя сессии: {self.values[1]}',
                                background = '#1e293b', foreground = '#d6e7ed', 
                                font = 'arial 14')
        self.name_label.pack(expand = True)

        # начало сессии.
        self.start_session_label = Label(left_frame, text = f'Начало сессии: {self.values[2]}', 
                                         background = '#1e293b', foreground = '#d6e7ed', 
                                         font = 'arial 14')
        self.start_session_label.pack(expand = True)

        # конец сессии.
        self.end_session_label = Label(right_frame, text = f'Конец сессии: {self.values[3]}', 
                                       background = '#1e293b', foreground = '#d6e7ed', 
                                       font = 'arial 14')
        self.end_session_label.pack(expand = True)

        # начало паузы.
        self.start_pause_label = Label(left_frame, text = f'Начало паузы: {self.values[6]}', 
                                       background = '#1e293b', foreground = '#d6e7ed', 
                                       font = 'arial 14')
        self.start_pause_label.pack(expand = True)
    
        # конец паузы.  
        self.end_pause_label = Label(right_frame, text = f'Конец паузы: {self.values[7]}', 
                                     background = '#1e293b', foreground = '#d6e7ed', 
                                     font = 'arial 14')
        self.end_pause_label.pack(expand = True)

        # время в работе.
        self.time_in_work_label = Label(left_frame, text = f'Время в работе: {self.values[4]}', 
                                        background = '#1e293b', foreground = '#d6e7ed', 
                                        font = 'arial 14')
        self.time_in_work_label.pack(expand = True)

        # время паузы.
        self.time_in_pause_label = Label(right_frame, text = f'Время в паузе: {self.values[8]}', 
                                         background = '#1e293b', foreground = '#d6e7ed', 
                                         font = 'arial 14')
        self.time_in_pause_label.pack(expand = True)

        '''
        Бинды Toplevel окна.
        '''
        
        # бинд изменения цвета кнопки 'Изменить имя сессии' при наведении мыши.
        self.change_name_session_button.bind('<Enter>', self.__on_enter_change_name_session_button)
        # бинд изменения цвета кнопки 'Изменить имя сессии' при отведении мыши.
        self.change_name_session_button.bind('<Leave>', self.__on_leave_change_name_session_button)

        # бинд изменения цвета кнопки 'Удадить запись' при наведении мыши.
        self.delete_note_button.bind('<Enter>', self.__on_enter_delete_note_button)
        # бинд изменения цвета кнопки 'Удадить запись' при отведении мыши.
        self.delete_note_button.bind('<Leave>', self.__on_leave_delete_note_button)

    '''
    Методы класса.
    '''

    # изменение имени отдельной записи в журнале.
    def __change_name_note(self) -> None:
        change_name = ChangeName(700, 500, 350, 320, 'Смена имени сессии')
    
    
    # удаление отдельной записи в журнале.
    def __delete_note(self) -> None:

        if messagebox.askokcancel('Внимание', 'Вы действительно хотите удалить эту запись?'):
            try:
                connect = sqlite3.connect('db.sqlite3')
                cursor = connect.cursor()

                cursor.execute('''DELETE FROM sessions WHERE id = ?;''', (self.values[0]))
                cursor.execute('''UPDATE sqlite_sequence SET seq = seq - 1;''')
                cursor.execute('''UPDATE sessions SET id = id - 1 WHERE id > ?;''', (self.values[0]))
                connect.commit()
                cursor.close()

                messagebox.showinfo('Успех', 'Запись была успешно удалена')
                self.destroy()
                
            except:
                messagebox.showerror('Внимание', 'Возникла ошибка при подключении к базе данных')

        return
    
    
    # изменение цвета кнопки 'Изменить имя сессии' при наведении мыши.
    def __on_enter_change_name_session_button(self, event) -> None:
        self.change_name_session_button.config(bg = '#77971a')


    # изменение цвета кнопки 'Изменить имя сессии' при отведении мыши.
    def __on_leave_change_name_session_button(self, event) -> None:
        self.change_name_session_button.config(bg = '#abd926')


    # изменение цвета кнопки 'Удалить запись' при наведении мыши.
    def __on_enter_delete_note_button(self, event) -> None:
        self.delete_note_button.config(bg = '#800005')


    # изменение цвета кнопки 'Удалить запись' при отведении мыши.
    def __on_leave_delete_note_button(self, event) -> None:
        self.delete_note_button.config(bg = '#ff000a')
