from tkinter import Entry, Frame, Label, Button
import random
import string

from .toplevel_mixin import ToplevelMixin


class SessionName(ToplevelMixin):

    def __init__(self, width, height, 
                 width_alignment, height_alignment, title_window) -> None:
        super().__init__(width, height, width_alignment, 
                         height_alignment, title_window)

        '''
        Разметка Toplevel окна.
        '''

        # frame для label.
        frame_top = Frame(self, background = '#1e293b')
        frame_top.place(relx = 0, rely = 0, relheight = 0.5, relwidth = 1)

        frame_bottom = Frame(self, background = '#1e293b')
        frame_bottom.place(relx = 0, rely = 0.5, relheight = 0.5, relwidth = 1)

        '''
        Виджеты Toplevel окна.
        '''

        # подсказка над полем ввода.
        self.hint_label = Label(frame_top, text = '*Укажите имя сессии', background = '#1e293b', 
                                foreground = '#d6e7ed', font = 'arial 25')
        self.hint_label.pack(expand = True)

        # поле ввода имени сессии.
        self.entry_session_name = Entry(self, font = 'arial 25', width = 30)
        self.entry_session_name.pack(expand = True)
        self.entry_session_name.focus()

        # кнопка 'Okay'.
        self.button_okay = Button(frame_bottom, text = 'Окей', background = '#2bd465', 
                                  font = 'arial 14', width = 20, cursor = 'hand2',
                                  command = self.__on_press_okey)
        self.button_okay.place(x = 110, y = 60)

        # кнопка 'Случайное имя'.
        self.button_random_name = Button(frame_bottom, text = 'Случайное имя', background = '#abd926', 
                                         font = 'arial 14', width = 20, cursor = 'hand2',
                                         command = self.__random_name_session)
        self.button_random_name.place(x = 360, y = 60)  

        '''
        Бинды Toplevel окна.
        '''

        # бинд для передачи имени сесси по нажатию 'Enter'.
        self.bind('<Return>', self.__on_press_return)

        # бинд изменения цвета кнопки 'Okay' при наведении мыши.
        self.button_okay.bind('<Enter>', self.__on_enter_button_okay)
        # бинд изменения цвета кнопки 'Случайное имя' при отведении мыши.
        self.button_okay.bind('<Leave>', self.__on_leave_button_okay)

        # бинд изменения цвета кнопки 'Случайное имя' при наведении мыши.
        self.button_random_name.bind('<Enter>', self.__on_enter_button_random_name)
        # бинд изменения цвета кнопки 'Случайное имя' при отведении мыши.
        self.button_random_name.bind('<Leave>', self.__on_leave_button_random_name)

    '''
    Методы класса.
    '''

    # передача имени сесси при нажатии кнопки 'Okay'.
    def __on_press_okey(self) -> None:
        self.__pass_info()

    # передача имени сесси по нажатию 'Enter'.
    def __on_press_return(self, event) -> None:
        self.__pass_info()

    # метод получения введенного имени.
    def __pass_info(self) -> None:

        info: str = self.entry_session_name.get()

        if info.replace(' ', '') == '':
            self.destroy()
            return
            
        self.master._start_session_with_session_name(info)
        self.destroy()

    # метод генерации рандомного имени.
    def __random_name_session(self) -> None: 

        info: str = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        self.master._start_session_with_session_name(info)
        self.destroy()

    # изменение цвета кнопки 'Okay' при наведении мыши.
    def __on_enter_button_okay(self, event) -> None:
        self.button_okay.config(bg = '#166d34')

    # изменение цвета кнопки 'Okay' при отведении мыши.
    def __on_leave_button_okay(self, event) -> None:
        self.button_okay.config(bg = '#2bd465')

    # изменение цвета кнопки 'Случайное имя' при наведении мыши.
    def __on_enter_button_random_name(self, event) -> None:
        self.button_random_name.config(bg = '#77971a')

    # изменение цвета кнопки 'Случайное имя' при отведении мыши.
    def __on_leave_button_random_name(self, event) -> None:
        self.button_random_name.config(bg = '#abd926')