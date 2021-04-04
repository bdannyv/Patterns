from abc import abstractmethod, ABC
from faker import Faker


class Component(ABC):
    @abstractmethod
    def do_my_work(self) -> None:
        pass


class Person(Component):  # Leaf
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def __str__(self):
        return f'{self.role}:{self.name}'

    def do_my_work(self) -> None:
        print(f'{self.role} {self.name} is doing his(her) work')


class Department(Component):  # Composite
    team = {}  # members of department {role: {name: John,

    # object: Person}
    def __init__(self, name):
        self.name = name

    def add(self, person: Person):
        """Add a team member"""
        newby = self.team.get(person.role)
        if newby is None:
            print(f'We have a new team member! {person.role} {person.name}')
            self.team[person.role] = {
                'name': person.name,
                'object': person
            }
        else:
            print(f"We are already have a {person.role}")

    def remove(self, person: Person):
        """Remove a team member"""
        fired = self.team.get(person.role)
        if fired in None:
            print(f"We have no {person.role} in our team.")
        else:
            print(f'{person.role} {person.name} is leaving us')
            del (self.team[person.role])

    def do_my_work(self) -> None:
        for members in self.team:
            self.team[members]['object'].do_my_work()


class Company(Component):
    units = {}

    def __init__(self, name):
        self.name = name

    def add(self, dep: Department):
        """Add a department"""
        newby = self.units.get(dep.name)
        if newby is None:
            if isinstance(dep, Person):
                print(f'New person in company! {dep.role} {dep.name}')
            else:
                print(f'New {dep.name} department assembled ')
            self.units[dep.name] = dep
        else:
            print(f"We are already have a {dep.name} team")

    def remove(self, dep: Department):
        """Remove a team member"""
        fired = self.units.get(dep.name)
        if fired in None:
            print(f"We have no {dep.name} team in our company.")
        else:
            print(f'{dep.name} team is leaving us')
            del (self.units[dep.name])

    def do_my_work(self) -> None:
        for deps in self.units:
            self.units[deps].do_my_work()


if __name__ == '__main__':
    faker = Faker()
    print("_" * 50)

    coogle = Company(name='Coogle')
    print(f'NEW PROJECT FOR {coogle.name.upper()} HAS STARTED')
    print("_" * 50)
    dev = Department("Development")
    marketing = Department('Marketing')
    security = Department('Security')
    management = Department('Management')
    lawyers = Department('Lawyers')

    for chief in ['CEO', 'CTO', 'CFO', 'Press Secretary']:
        coogle.add(Person(name=faker.name(),
                          role=chief))
    for dep in [dev, management, marketing, security, lawyers]:
        coogle.add(dep)

    print("_" * 50)

    for i in range(10):
        dev.add(Person(name=faker.name(),
                       role=f'developer {i}'))
    dev.add(Person(name=faker.name(),
                   role='senior developer'))

    print("_" * 50)

    for i in range(5):
        lawyers.add(Person(name=faker.name(),
                           role=f'lawyer {i}'))
    lawyers.add(Person(name=faker.name(),
                       role='senior lawyer'))

    print("_" * 50)

    for i in range(5):
        security.add(Person(name=faker.name(),
                            role=f'security engineer {i}'))
    security.add(Person(name=faker.name(),
                        role='senior security engineer'))

    print("_" * 50)

    for i in coogle.units:
        management.add(Person(name=faker.name(),
                              role=f'{i} manager'))

    print("_" * 50)
    for i in range(3):
        marketing.add(Person(name=faker.name(),
                             role=f'market manager {i}'))
    print("_" * 50)

    coogle.do_my_work()
