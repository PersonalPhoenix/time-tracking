from tkinter import ttk, Toplevel, N, NO, VERTICAL, END, Menu, IntVar
import sqlite3

from .crud_operations_in_journal import CreateCrudWindow


class CreateJournal(Toplevel):

    def __init__(self) -> None:
        super().__init__()

        '''
        Базовые настройки Toplevel окна.
        '''

        self.title('Журнал сессий')

        screen_width = self.winfo_screenwidth()
        screen_hight = self.winfo_screenheight()
        self.geometry(f'1218x500+{screen_width//2-609}+{screen_hight//2-320}')

        self.rowconfigure(index = 0, weight = 1)
        self.columnconfigure(index = 0, weight = 1)

        '''
        Выборка данных для заполнения журнала.
        '''
   
        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()
        cursor.execute('''SELECT * FROM sessions''')
        data = cursor.fetchall()
        connect.commit()
        cursor.close()
   
        '''
        Стиль таблицы Toplevel окна.
        '''

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background = '#1e293b', foreground = '#fdf4e3',
                       rowheight = 20, fieldbackground = '#1e293b',)
        style.map('Treeview', background = [('selected', '#0009ff')])

        '''
        Разметка Toplevel окна как таблицы.
        '''
   
        # определение колонок таблицы.
        columns = ('№', 'Имя сессии', 'Start', 'End', 'Time in work', 'Pause', 'Start_Pause', 'End_Pause', 'Time pause')
    
        # разметка Toplevel окна виджетом таблицы.
        self.tree = ttk.Treeview(self, columns = columns, show = 'headings')
        self.tree.grid(row = 0, column = 0, sticky = 'nsew')
 
        # определение заголовком колокнок таблицы.
        self.tree.heading('№', text = '№', anchor = N)
        self.tree.heading('Имя сессии', text = 'Имя', anchor = N)
        self.tree.heading('Start', text = 'Начал', anchor = N)
        self.tree.heading('End', text = 'Закончил', anchor = N)
        self.tree.heading('Time in work', text = 'Время в работе', anchor = N)
        self.tree.heading('Pause', text = 'Пауза', anchor = N)
        self.tree.heading('Start_Pause', text = 'Начало паузы', anchor = N)
        self.tree.heading('End_Pause', text = 'Конец паузы', anchor = N)
        self.tree.heading('Time pause', text = 'Время в паузе', anchor = N)
   
        # определяем параметры каждой из колонок таблицы.
        self.tree.column('#1', stretch = NO, width = 50, anchor = N)
        self.tree.column('#2', stretch = NO, width = 200, anchor = N)
        self.tree.column('#3', stretch = NO, width = 150, anchor = N)
        self.tree.column('#4', stretch = NO, width = 150, anchor = N)
        self.tree.column('#5', stretch = NO, width = 150, anchor = N)
        self.tree.column('#6', stretch = NO, width = 50, anchor = N)
        self.tree.column('#7', stretch = NO, width = 150, anchor = N)
        self.tree.column('#8', stretch = NO, width = 150, anchor = N)
        self.tree.column('#9', stretch = NO, width = 150, anchor = N)

        if not data:
           self.tree.insert('', END, values = 'Данных по Вашим сессиям пока что нет :)')

        else:
           for info in data:
              self.tree.insert('', END, values = info)

        # добавление виджета вертикальной прокрутки.
        scrollbar = ttk.Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.tree.configure(yscroll = scrollbar.set)
        scrollbar.grid(row = 0, column = 1, sticky = 'ns')

        # бинд 'Двойной клик ЛКМ' по записи журнала.
        self.tree.bind("<Double-Button-1>", self.__on_treeview_click)

        '''
        Меню журнала.
        '''

        menu = Menu(self)
        self.config(menu = menu)
        menu.add_command(label = 'Обновить журнал', command = self.__refresh_journal)

    '''
    Методы класса.
    '''

    # обработка двойного нажатия ЛКМ по записи журнала.
    def __on_treeview_click(self, event) -> None:

        try:
           item = self.tree.selection()[0]
           values = self.tree.item(item, "values")
           if values[7] == ':)':
             return
           note = CreateCrudWindow(values)
           self.wait_window(note)
           self.__refresh_journal()
           
        except IndexError: pass

    def __refresh_journal(self) -> None:
       self.destroy()
       self.__init__()