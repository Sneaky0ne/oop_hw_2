from abc import ABC, abstractmethod
from io import StringIO
from typing import List, Optional
import copy


class Printable(ABC):
    """Base abstract class for printable objects."""

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        """Base printing method for the tree structure display.
        Implement properly to display hierarchical structure."""
        # To be implemented

    @abstractmethod
    def clone(self):
        """Create a deep copy of this object."""
        pass


class BasicCollection(Printable):
    """Base class for collections of items."""

    def __init__(self):
        self.items = []

    def add(self, elem):
        # To be implemented
        pass

    def find(self, elem):
        # To be implemented
        pass

    def clone(self):
        pass


class Component(Printable):
    """Base class for computer components."""

    def __init__(self, numeric_val=0):
        self.numeric_val = numeric_val

    def clone(self):
        pass

    # To be implemented


class Address(Printable):
    """Class representing a network address."""

    def __init__(self, addr):
        self.address = addr

    def clone(self):
        pass

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        if not is_last:
            os.write(f"\n{prefix}+-{self.address}")
        else:
            os.write(f"\n{prefix}\-{self.address}")
    # To be implemented


class Computer(BasicCollection, Component):
    """Class representing a computer with addresses and components."""

    def __init__(self, name):
        self.name = name
        self.addresses = []
        self.components = []
        BasicCollection.__init__(self, )
        Component.__init__(self)

    def __str__(self):
        return self.name

    def add_address(self, addr: str):
        # To be implemented
        self.addresses.append(Address(addr))
        return self

    def add_component(self, comp: Component):
        # To be implemented
        self.components.append(comp)
        return self

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        if not is_last:
            os.write(f"\n+-Host: {self.name}")
            for index, addresses in enumerate(self.addresses):
                addresses.print_me(
                    os,
                    prefix="| ",
                    is_last=(index == len(self.components) + len(self.addresses) - 1),
                    no_slash=False,
                    is_root=False
                )
            for index, components in enumerate(self.components):
                components.print_me(
                    os,
                    prefix="| ",
                    is_last=(index == len(self.components) - 1),
                    no_slash=False,
                    is_root=False
                )
        else:
            os.write(f"\n\-Host: {self.name}")
            for index, addresses in enumerate(self.addresses):
                addresses.print_me(
                    os,
                    prefix="  ",
                    is_last=(index == len(self.addresses) + len(self.addresses) - 1),
                    no_slash=True,
                    is_root=False
                )
            for index, components in enumerate(self.components):
                components.print_me(
                    os,
                    prefix="  ",
                    is_last=(index == len(self.components) - 1),
                    no_slash=False,
                    is_root=False
                )

    # Другие методы...


class Network(Printable):
    """Class representing a network of computers."""

    def __init__(self, name):
        self.name = name
        self.computers = []

    def __str__(self):
        buf = StringIO()
        self.print_me(buf, is_root=True)
        return buf.getvalue()

    def add_computer(self, comp: Computer):
        self.computers.append(comp)
        # To be implemented
        return self

    def find_computer(self, name):
        # To be implemented
        for comp in self.computers:
            if comp.name == name:
                return comp
        return None

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        os.write(f"Network: {self.name}")
        for index, comp in enumerate(self.computers):
            comp.print_me(
                os,
                prefix="+",
                is_last=(index == len(self.computers) - 1),
                no_slash=False,
                is_root=False
            )

    def clone(self):
        import copy
        return copy.deepcopy(self)
    # Другие методы...


class Disk(Component):
    """Disk component class with partitions."""
    # Определение типов дисков
    SSD = 0
    MAGNETIC = 1

    def __init__(self, storage_type, size):
        # Initialize properly
        self.partitions = []
        self.storage_type = "SSD" if storage_type == self.SSD else "HDD"
        self.size = size
        super().__init__()

    def __str__(self):
        return self.storage_type

    def add_partition(self, size, name):
        # To be implemented
        self.partitions.append(f"{size} GiB, {name}")
        return self

    def print_partitions(self, os, prefix):
        for index, partition in enumerate(self.partitions):
            if index != len(self.partitions) - 1:
                os.write(f"\n{prefix}+-[{index}]: {partition}")
            else:
                os.write(f"\n{prefix}\-[{index}]: {partition}")

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        if not is_last:
            os.write(f"\n{prefix}+-{self.storage_type}, {self.size} GiB")
            self.print_partitions(os, prefix+"| ")
        else:
            os.write(f"\n{prefix}\-{self.storage_type}, {self.size} GiB")
            self.print_partitions(os, prefix+"  ")

class CPU(Component):
    """CPU component class."""

    def __init__(self, cores, mhz):
        # To be implemented
        self.cores = cores
        self.mhz = mhz
        super().__init__()

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        if not is_last:
            os.write(f"\n{prefix}+-CPU, {self.cores} cores @ {self.mhz}MHz")


class Memory(Component):
    """Memory component class."""

    def __init__(self, size):
        self.size = size
        super().__init__()
        # To be implemented
        pass

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        if not is_last:
            os.write(f"\n{prefix}+-Memory, {self.size} MiB")
        else:
            os.write(f"\n{prefix}\-Memory, {self.size} MiB")


# Пример использования (может быть неполным или содержать ошибки)
def main():
    # test()
    # return

    # Создание тестовой сети
    n = Network("MISIS network")

    # Добавляем первый сервер с одним CPU и памятью
    n.add_computer(
        Computer("server1.misis.ru")
        .add_address("192.168.1.1")
        .add_component(CPU(4, 2500))
        .add_component(Memory(16000))
    )

    # Добавляем второй сервер с CPU и HDD с разделами
    n.add_computer(
        Computer("server2.misis.ru")
        .add_address("10.0.0.1")
        .add_component(CPU(8, 3200))
        .add_component(
            Disk(Disk.MAGNETIC, 2000)
            .add_partition(500, "system")
            .add_partition(1500, "data")
        )
    )

    # Выводим сеть для проверки форматирования
    print("=== Созданная сеть ===")
    print(n)

    # Тест ожидаемого вывода
    expected_output = """Network: MISIS network
+-Host: server1.misis.ru
| +-192.168.1.1
| +-CPU, 4 cores @ 2500MHz
| \-Memory, 16000 MiB
\-Host: server2.misis.ru
  +-10.0.0.1
  +-CPU, 8 cores @ 3200MHz
  \-HDD, 2000 GiB
    +-[0]: 500 GiB, system
    \-[1]: 1500 GiB, data"""

    assert str(n) == expected_output, "Формат вывода не соответствует ожидаемому"
    print("✓ Тест формата вывода пройден")

    # Тестируем глубокое копирование
    print("\n=== Тестирование глубокого копирования ===")
    x = n.clone()

    # Тестируем поиск компьютера
    print("Поиск компьютера server2.misis.ru:")
    c = x.find_computer("server2.misis.ru")
    print(c)

    # Модифицируем найденный компьютер в копии
    print("\nДобавляем SSD к найденному компьютеру в копии:")
    c.add_component(
        Disk(Disk.SSD, 500)
        .add_partition(500, "fast_storage")
    )

    # Проверяем, что оригинал не изменился
    print("\n=== Модифицированная копия ===")
    print(x)
    print("\n=== Исходная сеть (должна остаться неизменной) ===")
    print(n)

    # Проверяем ассерты для тестирования системы
    print("\n=== Выполнение тестов ===")

    # Тест поиска
    assert x.find_computer("server1.misis.ru") is not None, "Компьютер не найден"
    print("✓ Тест поиска пройден")

    # Тест независимости копий
    original_server2 = n.find_computer("server2.misis.ru")
    modified_server2 = x.find_computer("server2.misis.ru")

    original_components = sum(1 for _ in original_server2.components)
    modified_components = sum(1 for _ in modified_server2.components)

    assert original_components == 2, f"Неверное количество компонентов в оригинале: {original_components}"
    assert modified_components == 3, f"Неверное количество компонентов в копии: {modified_components}"
    print("✓ Тест независимости копий пройден")

    # Проверка типов дисков
    disk_tests = [
        (Disk(Disk.SSD, 256), "SSD"),
        (Disk(Disk.MAGNETIC, 1000), "HDD")
    ]

    for disk, expected_type in disk_tests:
        assert expected_type in str(disk), f"Неверный тип диска в выводе: {str(disk)}"
    print("✓ Тест типов дисков пройден")

    print("\nВсе тесты пройдены!")

def test():
    n = Network("test.test")

    n.add_computer(Computer(name="server1.misis.ru")
                   .add_address("192.168.1.1")
                   .add_component(Disk(storage_type=1, size=2000)
                                  .add_partition(500, "System")
                                  .add_partition(500, "System"))
                   .add_component(Memory(16000))
                   )

    n.add_computer(Computer(name="server2.misis.ru")
                   .add_address("10.0.0.1")
                    .add_component(CPU(4, 25000))
                   .add_component(Disk(storage_type=1, size=2000)
                                  .add_partition(500, "System")
                                  .add_partition(1500, "data"))
                   )

    n.add_computer(Computer(name="server2.misis.ru")
                   .add_address("10.0.0.1")
                   .add_component(Disk(storage_type=1, size=2000)
                                  .add_partition(500, "System")
                                  .add_partition(1500, "data"))
                   )

    print(n)
    return


if __name__ == "__main__":
    main()
