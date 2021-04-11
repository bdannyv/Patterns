from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def is_enabled(self):
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def get_volume(self):
        pass

    @abstractmethod
    def volume_up(self):
        pass

    @abstractmethod
    def volume_down(self):
        pass

    @abstractmethod
    def get_channel(self):
        pass

    @abstractmethod
    def channel_back(self):
        pass

    @abstractmethod
    def channel_forward(self):
        pass


class TV(Device):
    def __init__(self):
        self._channel = 1
        self._volume = 0
        self._is_enabled = False

    @property
    def is_enabled(self):
        return self._is_enabled

    def turn_on(self):
        self._is_enabled = True

    def turn_off(self):
        self._is_enabled = False

    def get_volume(self):
        return self._volume

    def volume_up(self):
        self._volume += 10

    def volume_down(self):
        self._volume -= 10

    def get_channel(self):
        return self._channel

    def channel_back(self):
        self._channel = self._channel - 1 if self._channel > 0 else 99

    def channel_forward(self):
        self._channel = self._channel+1 if self._channel < 99 else 0

    def __str__(self):
        return (f'TV is turned on\nChannel:{self.get_channel()}\nVolume:{self.get_volume()}\n' if self.is_enabled else
                f'TV is turned off')


class Radio(Device):
    def __init__(self):
        self._wave = 95.5
        self._volume = 0
        self._is_enabled = False

    @property
    def is_enabled(self):
        return self._is_enabled

    def turn_on(self):
        self._is_enabled = True

    def turn_off(self):
        self._is_enabled = False

    def get_volume(self):
        return self._volume

    def volume_up(self):
        self._volume += 1

    def volume_down(self):
        self._volume -= 1

    def get_channel(self):
        return self._wave

    def channel_back(self):
        self._wave -= 0.01

    def channel_forward(self):
        self._wave += 0.01

    def __str__(self):
        return (f'Radio is turned on\nWave:{self.get_channel()}FM\nVolume:{self.get_volume()}\n' if self.is_enabled else
                f'Radio is turned off')


class AirCondition(Device):
    modes = ['comfort', 'fast', 'manual']

    def __init__(self):
        self._mode_num = 0
        self._volume = 0
        self._is_enabled = False

    @property
    def is_enabled(self):
        return self._is_enabled

    def turn_on(self):
        self._is_enabled = True

    def turn_off(self):
        self._is_enabled = False

    def get_volume(self):
        return self._volume

    def volume_up(self):
        self._volume += 10 if self._volume==10 else self._volume+1

    def volume_down(self):
        self._volume -= 0 if self._volume == 0 else self._volume-1

    def get_channel(self):
        print(f"MODE NUM {self._mode_num}")
        return self.modes[self._mode_num]

    def channel_back(self):
        self._mode_num = len(self.modes) - 1 if self._mode_num == 0 else self._mode_num - 1

    def channel_forward(self):
        self._mode_num = 0 if self._mode_num == len(self.modes)-1 else self._mode_num + 1

    def __str__(self):
        return (f'Air Condition is turned on\nMode:{self.get_channel()}\nVolume:{self.get_volume()}\n' if self.is_enabled else
                f'Air Condition is turned off')


class Remote:
    def __init__(self, device: Device):
        self.impl = device

    def power(self):
        if self.impl.is_enabled:
            self.impl.turn_off()
        else:
            self.impl.turn_on()
        print(self.impl)

    def channel_up_button(self):
        self.impl.channel_forward()
        print(self.impl)

    def channel_down_button(self):
        self.impl.channel_back()
        print(self.impl)

    def volume_up_button(self):
        self.impl.volume_up()
        print(self.impl)

    def volume_down_button(self):
        self.impl.volume_down()
        print(self.impl)


if __name__ == '__main__':
    tv = TV()
    print(tv)
    radio = Radio()
    print(radio)
    ac = AirCondition()
    print(ac)
    ac_remote = Remote(ac)
    ac_remote.power()
    ac_remote.channel_up_button()
    ac_remote.channel_up_button()
    ac_remote.channel_up_button()

    ac_remote.volume_up_button()
    ac_remote.power()
