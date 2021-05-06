from abc import ABC, abstractmethod


class Mediator(ABC):

    @abstractmethod
    def notify(self, component, event, destination):
        pass


class Aircraft(ABC):
    def __init__(self, mediator: Mediator):
        self._mediator = mediator
        self.has_priority = False

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator):
        self._mediator = mediator

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def number(self):
        pass

    def request(self, destination):
        print(f'{self}: requests for landing')
        self.mediator.notify(self, 'request for landing', destination)

    def land(self, destination):
        print(f'{self}: starts landing')
        self.mediator.notify(self, 'landing', destination)

    def emergency(self, destination):
        print(f'{self}: asks for emergency landing')
        self.mediator.notify(self, 'emergency landing', destination)

    def __str__(self):
        return f"{self.type} {self.number}"

    def __repr__(self):
        return self.__str__()


class Plane(Aircraft):
    _number = 0

    def __init__(self, mediator: Mediator):
        super().__init__(mediator)
        Plane._number += 1
        self.num = self._number

    @property
    def number(self):
        return self.num

    @property
    def type(self):
        return 'plane'


class Helicopter(Aircraft):
    _number = 0

    def __init__(self, mediator: Mediator):
        super().__init__(mediator)
        Helicopter._number += 1
        self.num = self._number

    @property
    def number(self):
        return self.num

    @property
    def type(self):
        return 'helicopter'


class PrivateJet(Plane):
    def __init__(self, mediator: Mediator):
        super().__init__(mediator)
        self.has_priority = True


class Platform(ABC):
    def __init__(self):
        self.queue = []

    @abstractmethod
    def check_type(self, aircraft: Aircraft):
        pass

    def priority_landing(self, aircraft: Aircraft):
        self.queue.insert(0, aircraft)

    def __repr__(self):
        return self.__str__()


class Runway(Platform):
    def __init__(self):
        super().__init__()

    def check_type(self, aircraft: Aircraft):
        if aircraft.type == 'plane':
            return True
        else:
            return False

    def __str__(self):
        return f"Runway"


class Helipad(Platform):
    def __init__(self, ):
        super().__init__()

    def check_type(self, aircraft: Aircraft):
        if aircraft.type == 'helicopter':
            return True
        else:
            return False

    def __str__(self):
        return f"Helipad"


class AirTrafficController(Mediator):
    def __init__(self, helipad: Helipad, runway: Runway):
        self.helipad = helipad
        self.runway = runway
        self.num_of_components = 0

    def notify(self, component: Helicopter, event: str, destination: Platform):
        if component in destination.queue and event == 'request':
            print('You are already requested for landing. Wait fot your turn please')
        elif destination.check_type(component):
            if event == 'request for landing':
                if component.has_priority:
                    destination.priority_landing(component)
                else:
                    if destination.queue:
                        print(f'Controller: Wait for permission')
                    else:
                        print(f'Controller: Platform is empty. Landing is permitted')
                    destination.queue.append(component)
            elif event == 'landing':
                if destination.queue[0] == component:
                    landed = destination.queue.pop(0)
                    print(f'Controller: {landed} has been landed')
                else:
                    print(
                        f'Controller: Landing for {component} is prohibited. Request for priority landing or wait for your turn')
            elif event == 'emergency landing':
                print(f'Controller: Attention! Emergency landing')
                if component in destination.queue:
                    destination.queue.pop(destination.queue.index(component))
                destination.priority_landing(component)
        else:
            print(f'Controller: {component.type} cannot land here')


if __name__ == '__main__':
    helipad = Helipad()
    runway = Runway()

    print(helipad, runway)

    trafic_c = AirTrafficController(helipad, runway)

    hel1 = Helicopter(mediator=trafic_c)
    hel2 = Helicopter(mediator=trafic_c)
    hel3 = Helicopter(mediator=trafic_c)

    pl1 = Plane(mediator=trafic_c)
    pl2 = Plane(mediator=trafic_c)
    pl3 = Plane(mediator=trafic_c)

    hel1.request(destination=helipad)
    hel2.request(destination=helipad)
    hel1.land(destination=helipad)
    hel3.request(destination=helipad)
    hel3.land(destination=helipad)
    hel3.emergency(destination=helipad)
    hel3.land(destination=helipad)
    print(helipad.queue)

    pl1.request(destination=helipad)
    pl1.request(destination=runway)
    pl2.request(destination=runway)
    pl3.request(destination=runway)
    print(runway.queue)

    pl2.land(destination=runway)
    pl1.land(destination=runway)
    pl2.land(destination=runway)
    pl3.land(destination=runway)