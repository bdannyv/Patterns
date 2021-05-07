from datetime import datetime


class Memento:
    def __init__(self, state: dict):
        self._state = {k:v for k,v in zip(state.keys(), state.values())}
        self._date = datetime.now()

    def get_state(self):
        return self._state

    def get_date(self):
        return self._date

    def __str__(self):
        return f'Memento {self._date}'

    def __repr__(self):
        return self.__str__()


class Originator:
    def __init__(self, **kwargs):
        for k in kwargs:
            self.__dict__[k] = kwargs[k]

    def change_something(self, attr: str, new_value):
        self.__dict__[attr] = new_value

    def save(self) -> Memento:
        return Memento(self.__dict__)

    def revert(self, mem: Memento) -> None:
        self.__dict__.update(mem.get_state())

class CareTaker:
    def __init__(self, origin: Originator):
        self.mems = []
        self.originator = origin

    def backup(self):
        self.mems.append(self.originator.save())

    def undo(self) -> None:
        if self.mems:
            last = self.mems.pop()
            self.originator.revert(last)
        else:
            return

    def history(self):
        return self.mems


if __name__ == "__main__":
    origin = Originator(string='str', integer=10, floating=5.0, tuple_=(10,5.0), list_=[1,2,3])
    print("first version -", origin.__dict__)
    ct = CareTaker(origin)
    ct.backup()
    origin.change_something('integer', 15)
    print('second version -', origin.__dict__)

    ct.undo()
    print('after undo -', origin.__dict__)
