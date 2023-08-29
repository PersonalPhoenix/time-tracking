from tkinter import ttk, Toplevel, N, NO, VERTICAL, END, Menu, IntVar
import sqlite3


def create_journal() -> Toplevel:

   '''
   Базовые настройки Toplevel окна.
   '''

   journal_window = Toplevel()
   journal_window.title('Журнал сессий')

   screen_width = journal_window.winfo_screenwidth()
   screen_hight = journal_window.winfo_screenheight()
   journal_window.geometry(f'1218x500+{screen_width//2-609}+{screen_hight//2-320}')

   journal_window.rowconfigure(index = 0, weight = 1)
   journal_window.columnconfigure(index = 0, weight = 1)

   '''
   Функционал меню-фильтра
   '''
   def update_columns():
      refresh_view()

   def refresh_view():
      return one_var, two_var, three_var, four_var, five_var, six_var, seven_var, eight_var, nine_var
         
   '''
   Меню-фильтр отображаемых колонок таблицы.
   '''
   
   menu = Menu(journal_window)
   journal_window.config(menu = menu)

   filter_menu = Menu(menu, tearoff = 0)

   one_var = IntVar(value = 1)
   two_var = IntVar(value = 1)
   three_var = IntVar(value = 1)
   four_var = IntVar(value = 1)
   five_var = IntVar(value = 1)
   six_var = IntVar(value = 1)
   seven_var = IntVar(value = 1)
   eight_var = IntVar(value = 1)
   nine_var = IntVar(value = 1)
   filter_menu.add_checkbutton(label = 'Номер сессии', variable = one_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Имя сессии', variable = two_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Начало сессии', variable = three_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Конец сессии', variable = four_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Время в работе', variable = five_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Пауза', variable = six_var, command = update_columns) 
   filter_menu.add_checkbutton(label = 'Начало паузы', variable = seven_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Конец паузы', variable = eight_var, command = update_columns)
   filter_menu.add_checkbutton(label = 'Время в паузе', variable = nine_var, command = update_columns)

   menu.add_cascade(label = 'Отображаемые колонки', menu = filter_menu)

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
   tree = ttk.Treeview(journal_window, columns = columns, show = 'headings')
   tree.grid(row = 0, column = 0, sticky = 'nsew')
 
   # определение заголовком колокнок таблицы.
   tree.heading('№', text = '№', anchor = N)
   tree.heading('Имя сессии', text = 'Имя', anchor = N)
   tree.heading('Start', text = 'Начал', anchor = N)
   tree.heading('End', text = 'Закончил', anchor = N)
   tree.heading('Time in work', text = 'Время в работе', anchor = N)
   tree.heading('Pause', text = 'Пауза', anchor = N)
   tree.heading('Start_Pause', text = 'Начало паузы', anchor = N)
   tree.heading('End_Pause', text = 'Конец паузы', anchor = N)
   tree.heading('Time pause', text = 'Время в паузе', anchor = N)
   
   # определяем параметры каждой из колонок таблицы.
   tree.column('#1', stretch = NO, width = 50, anchor = N)
   tree.column('#2', stretch = NO, width = 200, anchor = N)
   tree.column('#3', stretch = NO, width = 150, anchor = N)
   tree.column('#4', stretch = NO, width = 150, anchor = N)
   tree.column('#5', stretch = NO, width = 150, anchor = N)
   tree.column('#6', stretch = NO, width = 50, anchor = N)
   tree.column('#7', stretch = NO, width = 150, anchor = N)
   tree.column('#8', stretch = NO, width = 150, anchor = N)
   tree.column('#9', stretch = NO, width = 150, anchor = N)

   if not data:
      tree.insert('', END, values = 'Данных по Вашим сессиям пока что нет :)')

   else:
      for info in data:
         tree.insert('', END, values = info)

   # добавление виджета вертикальной прокрутки.
   scrollbar = ttk.Scrollbar(journal_window, orient = VERTICAL, command = tree.yview)
   tree.configure(yscroll = scrollbar.set)
   scrollbar.grid(row = 0, column = 1, sticky = 'ns')