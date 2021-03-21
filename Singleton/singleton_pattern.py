class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMetaClass):
    def __str__(self):
        return f"Singleton {id(self)}"

if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()

    print(s1)
    print(s2)