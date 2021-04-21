from abc import ABC, abstractmethod
from random import randint
from faker import Faker

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def request(self):
        return self.name, str(self.password)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class ObjectInterface(ABC):
    @abstractmethod
    def response(self, *args, **kwargs):
        pass

class PromocodeGenerator(ObjectInterface):
    def response(self):
        return "".join([str(randint(0,9)) if i%2==0 else chr(randint(65,85)) for i in range(20)])

class AccessProxyObject(ObjectInterface):

    def __init__(self, db: dict):
        self.sub = PromocodeGenerator()
        self.db = db

    def check_access(self, user:User):
        credentials = user.request()
        if credentials[0] in self.db and self.db[credentials[0]]==credentials[1]:
            return True
        return False

    def response(self, user: User):
        if self.check_access(user):
            print(f"Your promocode - {self.sub.response()}")
        else:
            print('Wrong credentials!')

if __name__ == '__main__':
    f = Faker()
    db = {f'{f.first_name()}': ''.join([str(randint(0,9)) for _ in range(10)]) for _ in range(5)}

    unauth1 = User(name='Will', password='0123456789')
    unauth2 = User(name='John', password='0123456710')

    authorized = [User(name=name, password=db[name]) for name in db]
    wrong_pass = [User(name=name, password=123) for name in db]

    biglion = AccessProxyObject(db=db)

    for us in [unauth1,unauth2,*authorized, *wrong_pass]:
        biglion.response(us)
