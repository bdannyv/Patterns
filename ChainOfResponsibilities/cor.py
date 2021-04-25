from abc import ABC, abstractmethod

""" Example of chain of responsibilities describing the way that almost every student has passed when he tried to get
 his diploma after successful completion of his university"""


class Student:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.has_debts = True
        self.has_lib_books = True
        self.has_cash = False
        self.military_dep_mark = False

    @staticmethod
    def request(req: str):
        return req


class MyHandler(ABC):
    """Handler interface"""

    @abstractmethod
    def handle(self, request: str, visitor: Student):
        """method for request handling"""
        pass

    @property
    @abstractmethod
    def next_handler(self):
        pass

    @next_handler.setter
    def next_handler(self, handler):
        pass


class UniversityDepartment(MyHandler):
    _next_handler = None

    @property
    def next_handler(self) -> MyHandler:
        return self._next_handler

    @next_handler.setter
    def next_handler(self, handler: MyHandler):
        self._next_handler = handler

    @abstractmethod
    def handle(self, request: str, visitor: Student):
        if self.next_handler:
            self.next_handler.handle(request, visitor)


class AccountingDepartment(UniversityDepartment):
    def handle(self, request: str, visitor: Student):
        if visitor.has_debts:
            print(f'Student: Hello! I would like to {request}\nAccountant: Ok! Lets check your debts to university...\n'
                  f'Oh! You have to pay a 12 rub for your room in university dormitory. There is the form for cashier.'
                  'Come back after you have paid all your debts\n')
            self.next_handler = Cashier()
            super().handle(request='pay my debt', visitor=visitor)
        else:
            print(f'Accountant: Ok! There is your stamp\n')
            self.next_handler = Library()
            super().handle(request='get a stamp from you', visitor=visitor)


class Cashier(UniversityDepartment):
    def handle(self, request: str, visitor: Student):
        if visitor.has_cash:
            print('Cashier: Your receipt')
            visitor.has_debts = False
            self.next_handler = AccountingDepartment()
            super().handle(request, visitor)
        else:
            print(f'Student: Hello! I would like to {request}\nCashier: Ok! Your 12 rubbles please\n'
                  f'Student: I would like to pay with my credit card\nCashier: but we have no terminal...\n(20 min later)\n'
                  f'Student: There are 12 rubbles...cash')
            visitor.has_cash = True
            self.handle(request, visitor)


class Library(UniversityDepartment):
    def handle(self, request: str, visitor: Student):
        if visitor.has_lib_books:
            print(f'Librarian: You have not returned some books! I going to put a stamp on your form only after books '
                  f'returning!')
            visitor.has_lib_books = False
            self.next_handler = self
            super().handle(request, visitor)
        else:
            print('Student: Hello! There are book that I have taken')
            self.next_handler = MilitaryDepartment()
            super().handle(request, visitor)


class MilitaryDepartment(UniversityDepartment):
    def handle(self, request: str, visitor: Student):
        print("Military Man:There is your stamp and there is your call to military office! Get out of here!")
        visitor.military_dep_mark = True
        self.next_handler = ThatGuyWhoGivesDiploma()
        super().handle(request=request, visitor=visitor)


class ThatGuyWhoGivesDiploma(UniversityDepartment):
    def handle(self, request: str, visitor: Student):
        if visitor.has_lib_books or visitor.has_debts or not visitor.military_dep_mark:
            print('that diploma guy: I can not give you your diploma')
        else:
            print("that diploma guy:Congrats!")


if __name__ == '__main__':
    John = Student(name='Иван')
    hell = AccountingDepartment()
    guy = ThatGuyWhoGivesDiploma()
    guy.handle(request=None, visitor=John)
    hell.handle(request='get my diploma', visitor=John)
