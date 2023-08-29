import time
from tkinter import Tk, Menu, Frame, Button, Label, messagebox
import sqlite3

from singleton import Singleton
from functional_menu.file import change_current_path, current_path, default_path, clear_database
from functional_menu.export import export_sql_to_excel, export_sql_to_csv, export_sql_to_word
from functional_menu.hint import guide_message, contact_message, copyright_message
from session_name import SessionName
from jourlnal import create_journal


class App(Singleton, Tk):

    '''
    Главное окно приложения.
    '''

    def __init__(self) -> Tk:
        super().__init__()

        '''
        Базовые настройки главного окна.
        '''

        # инициализация главного окна.
        self.title('Учет времени')

        # настройка Ш/В окна и положения на рабочем столе.
        screen_width = self.winfo_screenwidth()
        screen_hight = self.winfo_screenheight()
        self.geometry(f'750x552+{screen_width//2-screen_width//4}+{screen_hight//2-350}')
        self.resizable(False, False)

        '''
        Разметка главного окна
        '''

        # frame для отображения таймера прямого отсчета.
        frame_top = Frame(self, background = '#1e293b')
        frame_top.place(relx = 0, rely = 0, relheight = 0.3, relwidth = 1)

        # frame для кнопки 'Старт'.
        frame_mid_left = Frame(self, background = '#1e293b')
        frame_mid_left.place(relx = 0, rely = 0.3, relheight = 0.3, relwidth = 0.5)

        # frame для кнопки 'Пауза'.
        frame_mid_right = Frame(self, background = '#1e293b')
        frame_mid_right.place(relx = 0.5, rely = 0.3, relheight = 0.3, relwidth = 0.5)

        # frame для кнопки 'Обнулить сессию'.
        frame_bot_left = Frame(self, background = '#1e293b')
        frame_bot_left.place(relx = 0, rely = 0.6, relheight = 0.25, relwidth = 0.5)

        # frame для кнопки 'Просмотреть журнал'.
        frame_bot_right = Frame(self, background = '#1e293b')
        frame_bot_right.place(relx = 0.5, rely = 0.6, relheight = 0.25, relwidth = 0.5)

        # frame для текущей даты по МКС.
        frame_deep_left = Frame(self, background = '#1e293b')
        frame_deep_left.place(relx = 0, rely = 0.85, relheight = 0.15, relwidth = 0.5)

        # frame для текущего времени по МСК.
        frame_deep_right = Frame(self, background = '#1e293b')
        frame_deep_right.place(relx = 0.5, rely = 0.85, relheight = 0.15, relwidth = 0.5)
            
        '''
        Меню главного окна.
        '''

        # инициализация меню.
        main_menu = Menu(self)
        self.config(menu = main_menu)

        # пункт меню 'Файл'.
        file_menu = Menu(main_menu, tearoff = 0)
        file_menu.add_command(label = 'Изменить путь экспорта', activebackground = '#808080',command = change_current_path)
        file_menu.add_command(label = 'Сделать путь по умолчанию', activebackground = '#808080', command = default_path)
        file_menu.add_command(label = 'Текущий путь экспорта', activebackground = '#808080', command = current_path)
        file_menu.add_separator()
        file_menu.add_command(label = 'Очистить базу данных', activebackground = 'red', command = clear_database)

        # пункт меню 'Экспорт'.
        export_menu = Menu(main_menu, tearoff = 0)
        export_menu.add_command(label = 'Экспорт в Excel', activebackground = '#2bd465', command = export_sql_to_excel)
        export_menu.add_command(label = 'Экспорт в CSV', activebackground = '#bf6148', command = export_sql_to_csv)
        export_menu.add_command(label = 'Экспорт в Word', activebackground = '#0009ff', command = export_sql_to_word)

        # пункт меню 'Справка'.
        hint_menu = Menu(main_menu, tearoff = 0)
        hint_menu.add_command(label = 'Подсказка', activebackground = '#808080', command = guide_message)
        hint_menu.add_command(label = 'Контакты', activebackground = '#808080', command = contact_message)
        hint_menu.add_command(label = 'Copyright © 2023', activebackground = '#808080', command = copyright_message)

        # добавление пунктов меню 'Файл' и 'Экспорт' в главное меню.
        main_menu.add_cascade(label = 'Файл', menu = file_menu)
        main_menu.add_cascade(label = 'Экспорт', menu = export_menu)
        main_menu.add_cascade(label = 'Справка', menu = hint_menu)

        '''
        Функционал виджетов главного окна.
        '''
        
        # отображение времени начала сессии.
        def __start_time_session() -> None:
            
            if self.SESSION == True:
                messagebox.showerror('Внимание', 'Сессия уже началась :)')
                return
            
            self.__session_name()

            if self.SESSION_NAME == '':
                messagebox.showerror('Внимание', 'Вы не указали имя сессии\nСессия была отменена')
                return
            
            else:
                
                self.SESSION = True
                _ = time.strftime(f'%H:%M:%S')
                self.SESSION_START = f'{_[0:2]}ч {_[3:5]}м {_[6:8]}c'
                session_label['text'] = f'Сессия начата в: {_}'

                __session_start_time_in_seconds()
                __working_hours()

        # вычислиение времени начало сессии в секундах.
        def __session_start_time_in_seconds() -> int:
            
            self.START_TIME_IN_SECONDS = \
                        int(session_label['text'][17:19])*3600 + \
                        int(session_label['text'][20:22])*60 + \
                        int(session_label['text'][23:25])

        # таймер прямого отсчета времени в работе.
        def __working_hours() -> None:
            
            if self.SESSION == True:
                if self.PAUSE == False:
                    current_time = \
                            int((time.strftime('%H')[0:2]))*3600 + \
                            int((time.strftime('%M')[0:2]))*60 + \
                            int((time.strftime('%S')[0:2]))
                    in_work = current_time - (self.START_TIME_IN_SECONDS + sum(self.ALL_TIME_PAUSE))
                    hours =  in_work // 3600
                    minutes = (in_work - hours * 3600) // 60
                    seconds = (in_work - hours * 3600) - minutes * 60
                    time_session_label['text'] = f'Время в работе: {hours}ч:{minutes}м:{seconds}с'
                    self.TIME_IN_WORK = f'{hours}ч {minutes}м {seconds}с'
                    time_session_label.after(1000, __working_hours)
                else:
                    return
            else:
                return

        def __on_press_pause() -> None:
                
            if self.SESSION == False:
                messagebox.showerror('Внимание', 'Нельза оставить то, что еще не началось :)')

            else:
                self.PAUSE = True

                button_pause['text'] = 'Продолжить'
                button_pause['command'] = __on_press_continue

                self.END_PAUSE = 'Пауза не была остановлена'

                __set_pause()
                __in_pause()

        def __on_press_continue() -> None:

            self.PAUSE = False
            _ = time.strftime('%H:%M:%S')
            self.END_PAUSE = f'{_[0:2]}ч {_[3:5]}м {_[6:8]}с '

            button_pause['text'] = 'Пауза'
            button_pause['command'] = __on_press_pause
            pause_time_text_label['text'] = 'Пауза не установлена'
            text_time_in_pause_label['text'] = ''
            
            __working_hours()

        def __set_pause() -> None:
            self.HAVE_PAUSE = 'Да'
            _ = time.strftime('%H:%M:%S')
            self.START_PAUSE = f'{_[0:2]}ч {_[3:5]}м {_[6:8]}с'
            pause_time_text_label['text'] = f'Пауза установлена в: {_}'

        def __in_pause() -> None:

            if self.PAUSE == True:
                start_pause = \
                            int(pause_time_text_label['text'][21:23])*3600 +\
                            int(pause_time_text_label['text'][24:26])*60 +\
                            int(pause_time_text_label['text'][27:29])
                current_time = int(time.strftime('%H'))*3600 + int(time.strftime('%M'))*60 + int(time.strftime('%S'))
                time_in_pause = current_time - start_pause
                self.TIME_PAUSE = time_in_pause
                hours = time_in_pause // 3600
                minutes = (time_in_pause - hours * 3600) // 60
                seconds = (time_in_pause - hours * 3600) - minutes * 60
                text_time_in_pause_label['text'] = f'Время в паузе: {hours}ч:{minutes}м:{seconds}с'
                self.TIME_IN_PAUSE = f'{hours}ч {minutes}м {seconds}с'
                text_time_in_pause_label.after(1000, __in_pause)

            else:
                self.ALL_TIME_PAUSE.append(self.TIME_PAUSE)
        
        # заверешние сессии.
        def __on_press_end_session() -> None:

            if self.SESSION == True or self.PAUSE == True:
                if messagebox.askokcancel('Внмиание', 'Вы действительно хотите завершить сессию?'):
                    __save_info_in_db()
            else:
                messagebox.showerror('Внимание', 'Нельзя остановить то, что еще не началось :)')

        def __save_info_in_db() -> None:
            
            _ = time.strftime('%H:%M:%S')
            connect = sqlite3.connect('db.sqlite3')
            cursor = connect.cursor()
            cursor.execute('''INSERT INTO sessions(
                           name_session, start_session, end_session, 
                           time_in_work, pause, start_pause, end_pause, 
                           time_in_pause)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                           (self.SESSION_NAME, self.SESSION_START,
                            f'{_[0:2]}ч {_[3:5]}м {_[6:8]}с', self.TIME_IN_WORK,
                            self.HAVE_PAUSE, self.START_PAUSE, 
                            self.END_PAUSE, self.TIME_IN_PAUSE))
            connect.commit()
            cursor.close()
            messagebox.showinfo('Внимание', 'Информация о сессии была успешна сохранена')

            __reset_by_zero()

        def __reset_by_zero() -> None:
    
            self.PAUSE = False
            self.SESSION = False
            self.START_TIME_IN_SECONDS = 0
            self.TIME_PAUSE = 0
            self.ALL_TIME_PAUSE = []
            self.SESSION_NAME = ''
            self.SESSION_START= ''
            self.TIME_IN_WORK = ''
            self.HAVE_PAUSE = 'Нет'
            self.START_PAUSE = 'Нет'
            self.END_PAUSE = 'Нет'
            self.TIME_IN_PAUSE = 'Нет'
            self.CLOSE_TOPLEVEL = False

            session_label['text'] = 'Сессия не начата'
            time_session_label['text'] = 'Время в работе: 0ч:0м:0с'

            button_pause['text'] = 'Пауза'
            button_pause['command'] = __on_press_pause
            pause_time_text_label['text'] = 'Пауза не установлена'
            text_time_in_pause_label['text'] = ''

        # часы главного окна.
        def __clock() -> None:

            # текущее время МСК.
            current_time_label['text'] = time.strftime('%H:%M:%S')
            current_time_label.after(1000, __clock)

            # текущая дата МСК.
            current_data_label['text'] = time.strftime('%d:%m:%Y')
            current_data_label.after(86400000, __clock)
            
        '''
        Виджеты главного окна.
        '''

        # label имени сессии.
        session_label = Label(frame_top, background = '#1e293b', foreground = '#d6e7ed',
                              text = 'Сессия не начата', font = 'arial 32')
        session_label.pack(expand = True)

        # label для таймера прямого отсчета.
        time_session_label = Label(frame_top, background = '#1e293b', foreground = '#d6e7ed',
                                   text = 'Время в работе: 0ч:0м:0с', font = 'arial 32')
        time_session_label.pack(expand = True)

        # кнопка 'Начать сессию'.
        button_start = Button(frame_mid_left, text = 'Начать сессию', font = 'arial 14', 
                              width = 25, background = '#2bd465', cursor = 'hand2',
                              command = __start_time_session)
        button_start.pack(expand = True)

        # label информации о паузе.
        pause_time_text_label = Label(frame_mid_right, background = '#1e293b', foreground = '#d6e7ed',
                                      text = 'Пауза не установлена', font = 'arial 14')
        pause_time_text_label.place(relx = 0.01, rely = 0.09, relheight = 0.2, relwidth = 1)

        # label информации о длительности паузы.
        text_time_in_pause_label = Label(frame_mid_right, background = '#1e293b', foreground = '#d6e7ed',
                                   text = '', font = 'arial 14')
        text_time_in_pause_label.place(relx = 0.01, rely = 0.7, relheight = 0.2, relwidth = 1)

        # кнопка 'Пауза / Продолжить'.
        button_pause = Button(frame_mid_right, text = 'Пауза', font = 'arial 14', 
                              width = 25,background = '#abd926', cursor = 'hand2',
                              command = __on_press_pause)
        button_pause.pack(expand = True)
        
        # кнопка 'Завершить сессию'.
        button_end_session = Button(frame_bot_left, text = 'Завершить сессию',
                                    font = 'arial 14', width = 25,
                                    background = '#ff000a', cursor = 'hand2',
                                    command = __on_press_end_session)
        button_end_session.pack(expand = True)

        # кнопка 'Просмотреть журнал'.
        button_view_journal = Button(frame_bot_right, text = 'Просмотреть журнал',
                                    font = 'arial 14', width = 25,
                                    background = '#0009ff', cursor = 'hand2',
                                    command = create_journal)
        button_view_journal.pack(expand = True)

        # label текущего времени по МСК.
        current_time_label = Label(frame_deep_right, font = 'arial 14', background = '#1e293b', foreground = '#d6e7ed')
        current_time_label.pack(expand = True)

        # label текущей даты по МСК.
        current_data_label = Label(frame_deep_left, font = 'arial 14', background = '#1e293b', foreground = '#d6e7ed')
        current_data_label.pack(expand = True)

        # вызов часов после реализации label'ов для отображения даты/времени.
        __clock()

    '''
    Методы класса
    '''
    
    # указание имени сессии при начале работы.
    def __session_name(self) -> None:
        session_top_level = SessionName(self)
        self.wait_window(session_top_level)

    # получение указанного имени.
    def start_session_with_session_name(self, info) -> messagebox:
        self.SESSION_NAME = info
        messagebox.showinfo('Имя сессии', f'Имя сессии: {info}')