from tkinter import Toplevel


class ToplevelMixin(Toplevel):
    '''
    Миксин с базовыми настройками Toplevel окна.
    '''
    
    def __init__(self, width, height, width_alignment, 
                 height_alignment, title_window) -> None:
        super().__init__()

        # заголовок окна.
        self.title_window = title_window
        # ширина окна (в px).
        self.width = width
        # высота окна (в px).
        self.height = height
        # выравнивание начального положения окна по ширине (в px).
        self.width_alignment = width_alignment
        # выравнивание начального положения окна по высоте (в px).
        self.height_alignment = height_alignment

        self.title(f'{self.title_window}')

        # определение ширины экрана пользователя (в px).
        screen_width = self.winfo_screenwidth()
        # определение высоты экрана пользователя (в px).
        screen_hight = self.winfo_screenheight()
        # задаем размеры и выравнивание.
        self.geometry(f'{self.width}x{self.height}+{screen_width//2-width_alignment}+{screen_hight//2-height_alignment}')
        # запрет на изменение размеров окна по ширине и высоте.
        self.resizable(False, False)
        