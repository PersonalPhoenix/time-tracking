from tkinter import Toplevel, Frame, Label, Entry


class ChangeName(Toplevel):
    
    def __init__(self) -> None:
        super().__init__()

        '''
        Базовые настройки Toplevel окна.
        '''

        self.title('Смена имени сессии')

        screen_width = self.winfo_screenwidth()
        screen_hight = self.winfo_screenheight()
        self.geometry(f'700x500+{screen_width//2-350}+{screen_hight//2-320}')
        self.resizable(False, False)

        '''
        Разметка Toplevel окна.
        '''

        current_name_session_frame = Frame(self, background = '#1e293b')
        current_name_session_frame.place(relx = 0, rely = 0, relheight = 0.5, relwidth = 1)

        change_name_session_frame = Frame(self, background = '#1e293b')
        change_name_session_frame.place(relx = 0, rely = 0.5, relheight = 0.5, relwidth = 1)

        '''
        Разметка Toplevel окна.
        '''

        current_name_session_label = Label()
        current_name_session_label.pack(expand = True)

        change_name_session_entry = Entry()
        change_name_session_entry.pack(expand = True)