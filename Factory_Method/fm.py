from abc import ABC, abstractmethod


class Product(ABC):
    @abstractmethod
    def some_operation(self):
        pass

class Creator:
    @abstractmethod
    def factory_method(self) -> Product:
        pass

    def action(self):
        prod = self.factory_method()

        return prod.some_operation() + "Скважина в работе"


"""EXAMPLE"""
# Products creation
class ESPwell(Product): # Product1
    def some_operation(self):
        return 'Насос запущен.'

class GasLiftWell(Product): # Product2
    def some_operation(self):
        return 'Запущена подача газа.'

class FlowingWell(Product): # Product3
    def some_operation(self):
        return 'Скважина открыта.'

# Creators
class EspWellCreator(Creator):
    def factory_method(self) -> Product:
        return ESPwell()

class GasLiftWellCreator(Creator):
    def factory_method(self) -> Product:
        return GasLiftWell()

class FlowingWellCreator(Creator):
    def factory_method(self) -> Product:
        return FlowingWell()

if __name__ == '__main__':
    print("Создатель скважины с УЭЦН")

    esp_creator = EspWellCreator()
    print(esp_creator.action())

    print('\n\nСоздатель газлифтной скважины')

    gl_creator = GasLiftWellCreator()
    print(gl_creator.action())

    print('\n\nСоздатель фонтанной скважины')

    f_creator = FlowingWellCreator()
    print(f_creator.action())