from tkinter import Toplevel, Entry, Frame, Label, Button, messagebox
import random
import string


class SessionName(Toplevel):

    def __init__(self, app) -> None:
        super().__init__(app)
        
        '''
        Базовые настройки Toplevel окна.
        '''
        
        self.title('Имя сессии')

        self.geometry(f'700x300+{self.winfo_screenwidth()//2-350}+{self.winfo_screenheight()//2-320}')
        self.resizable(False, False)

        self.config(background = '#1e293b')

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
        hint_label = Label(frame_top, text = '*Укажите имя сессии', background = '#1e293b', foreground = '#d6e7ed', font = 'arial 25')
        hint_label.pack(expand = True)

        # поле ввода имени сессии.
        self.entry_session_name = Entry(self, font = 'arial 25', width = 30)
        self.entry_session_name.pack(expand = True)
        self.entry_session_name.focus()

        button_okay = Button(frame_bottom, text = 'Окей', background = '#2bd465', 
                             font = 'arial 14', width = 20, command = self.__on_press_okey)
        button_okay.place(x = 110, y = 60)

        button_cancel = Button(frame_bottom, text = 'Случайное имя', background = '#abd926', 
                               font = 'arial 14', width = 20, command = self.__random_name_session)
        button_cancel.place(x = 360, y = 60)

        self.bind('<Return>', self.__on_press_return)

    def __on_press_okey(self):
        self.__pass_info()
    
    def __on_press_return(self, event):
        self.__pass_info()

    # метод получения введенного имени.
    def __pass_info(self):

        info = self.entry_session_name.get()

        if info.replace(' ', '') == '':
            self.destroy()
            return
            
        self.master.start_session_with_session_name(info)
        self.destroy()

    # метод генерации рандомного имени.
    def __random_name_session(self): 

        info = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        self.master.start_session_with_session_name(info)
        self.destroy()