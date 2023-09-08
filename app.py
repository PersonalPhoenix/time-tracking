from main_window.main import App


class WorkApp(App):
    '''
    Настроечный класс окна приложения.
    '''

    # переменные управления состоянием сессии.
    # включена ли пауза.
    PAUSE: bool = False
    # начата ли сессия.
    SESSION: bool = False
    # время начала сессии в секундах.
    START_TIME_IN_SECONDS: int = 0
    # время в паузе в секудах.
    TIME_PAUSE: int = 0
    # суммарное время пауз.
    ALL_TIME_PAUSE: list = []

    # переменные для записи информации о сессии в БД.
    # имя сессии.
    SESSION_NAME: str = ''
    # время начала сессии.
    SESSION_START: str = ''
    # время в работе.
    TIME_IN_WORK: str = ''
    # наличие паузы.
    HAVE_PAUSE: str = 'Нет'
    # время начала паузы
    START_PAUSE: str = 'Нет'
    # время конца паузы.
    END_PAUSE: str = 'Нет'
    # время в паузе.
    TIME_IN_PAUSE: str = 'Нет'


if __name__ == '__main__':
    app = WorkApp()
    app._clock()
    app.mainloop()
    