from typing import instance


class Singleton(object):

    def __new__(cls) -> instance:
        
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)

        return cls.instance