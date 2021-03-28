from abc import ABC, abstractmethod

class Well(ABC): # Product interface
    _counter = 0
    def __init__(self):
        self._counter += 1
        self._id = self._counter
        self.is_on = False

    def __str__(self):
        return f"{self.type1} {self.type2} well {self.id}"

    @property
    def id(self):
        return self._id

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def shut_in(self):
        pass

    @property
    @abstractmethod
    def type1(self):
        """wellbore type"""
        pass

    @property
    @abstractmethod
    def type2(self):
        """well purpose"""
        pass

class HorizontalWell(Well, ABC): # Product A
    def __init__(self):
        super().__init__()
        self._type = 'Horizontal'

    @property
    def type1(self):
        return self._type

class VerticalWell(Well, ABC): # Product B
    def __init__(self):
        super().__init__()
        self._type = 'Vertical'

    @property
    def type1(self):
        return self._type

class SlantedWell(Well, ABC): # Product C
    _counter = 0
    def __init__(self):
        super().__init__()
        self._type = 'Slanted'

    @property
    def type1(self):
        return self._type

class InjectionWell(Well, ABC): # Product 1

    def shut_in(self):
        self.is_on = False
        print(f"{self.__str__()}:injection has been stopped")

    def turn_on(self):
        self.is_on = True
        print(f"{self.__str__()}:injection has been started")

    @property
    def type2(self):
        return "Injecting"


class ProducingWell(Well, ABC):  # Product 2

    def shut_in(self):
        self.is_on = False
        print(f"{self.__str__()}:production has been stopped")

    def turn_on(self):
        self.is_on = True
        print (f"{self.__str__()}:production has been started")

    @property
    def type2(self):
        return "Producing"


class InjectionHorizontalWell(HorizontalWell, InjectionWell): # Product A1
    def __init__(self):
        super().__init__()


class ProducingHorizontalWell(HorizontalWell, ProducingWell): # Product A2
    def __init__(self):
        super().__init__()

class InjectionVerticalWell(VerticalWell, InjectionWell): # Product B1
    def __init__(self):
        super().__init__()


class ProducingVerticalWell(VerticalWell, ProducingWell): # Product B2
    def __init__(self):
        super().__init__()


class InjectionSlantedWell(SlantedWell, InjectionWell): # Product C1
    def __init__(self):
        super().__init__()

class ProducingSlantedWell(SlantedWell, ProducingWell): # Product C2
    def __init__(self):
        super().__init__()

    def __str__(self):
        return super().__str__()

class ServiceCompany(ABC): # Abstract Factory Interface

    @abstractmethod
    def build_horizontal_well(self) -> HorizontalWell:
        pass

    @abstractmethod
    def build_vertical_well(self) -> VerticalWell:
        pass

    @abstractmethod
    def build_slanted_well(self) -> SlantedWell:
        pass

class InjectionServiceCompany(ServiceCompany): # Product 1 Factory

    def build_horizontal_well(self) -> InjectionHorizontalWell:
        return InjectionHorizontalWell()

    def build_vertical_well(self) -> InjectionVerticalWell:
        return InjectionVerticalWell()

    def build_slanted_well(self) -> InjectionSlantedWell:
        return InjectionSlantedWell()

class ProducingServiceCompany(ServiceCompany): # Product 2 Factory

    def build_horizontal_well(self) -> ProducingHorizontalWell:
        return ProducingHorizontalWell()

    def build_vertical_well(self) -> ProducingVerticalWell:
        return ProducingVerticalWell()

    def build_slanted_well(self) -> ProducingSlantedWell:
        return ProducingSlantedWell()


if __name__ == "__main__":
    slb = ProducingServiceCompany()
    hb = InjectionServiceCompany()

    print('Some wells has been built:')
    sw1p = slb.build_slanted_well()
    print(f'-{sw1p}')
    sw2i = hb.build_slanted_well()
    print(f'-{sw2i}')

    hw1p = slb.build_horizontal_well()
    print(f'-{hw1p}')
    hw2i = hb.build_horizontal_well()
    print(f'-{hw2i}')

    vw1p = slb.build_vertical_well()
    print(f'-{vw1p}')
    vw2i = hb.build_vertical_well()
    print(f'-{vw2i}')
