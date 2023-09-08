from tkinter import Frame, Label, Entry

from .toplevel_mixin import ToplevelMixin


class ChangeName(ToplevelMixin):
    '''
    Класс для Toplevel окна.
    Окно смены имени сессии у выбранной записи.
    '''

    def __init__(self, width, height, width_alignment, 
                 height_alignment, title_window) -> None:
        super().__init__(width, height, width_alignment, 
                         height_alignment, title_window)

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

        current_name_session_label = Label(self,)
        current_name_session_label.pack(expand = True)

        change_name_session_entry = Entry(self,)
        change_name_session_entry.pack(expand = True)
        