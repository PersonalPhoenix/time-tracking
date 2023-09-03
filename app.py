from main_window.main import App


class WorkApp(App):

    # переменные управления состоянием сессии.
    PAUSE: bool = False
    SESSION: bool = False
    START_TIME_IN_SECONDS: int = 0
    TIME_PAUSE: int = 0
    ALL_TIME_PAUSE: list = []

    # переменные для записи информации о сессии в БД.
    SESSION_NAME: str = ''
    SESSION_START: str = ''
    TIME_IN_WORK: str = ''
    HAVE_PAUSE: str = 'Нет'
    START_PAUSE: str = 'Нет'
    END_PAUSE: str = 'Нет'
    TIME_IN_PAUSE: str = 'Нет'

if __name__ == '__main__':
    app = WorkApp()
    app._clock()
    app.mainloop()