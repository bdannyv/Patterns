from abc import ABC, abstractmethod

class Builder(ABC):
    @abstractmethod
    def action1(self): # at least 1 action?
        pass

class Director:
    pass

class App:
    pass