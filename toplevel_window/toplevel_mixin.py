from tkinter import Toplevel


class ToplevelMixin(Toplevel):

    def __init__(self, width, height, width_alignment, 
                 height_alignment, title_window) -> None:
        super().__init__()

        self.title_window = title_window
        self.width = width
        self.height = height
        self.width_alignment = width_alignment
        self.height_alignment = height_alignment

        self.title(f'{self.title_window}')

        screen_width = self.winfo_screenwidth()
        screen_hight = self.winfo_screenheight()
        self.geometry(f'{self.width}x{self.height}+{screen_width//2-width_alignment}+{screen_hight//2-height_alignment}')
        self.resizable(False, False)