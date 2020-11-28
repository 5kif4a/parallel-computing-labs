import random
import time
from threading import Thread


class MyThread(Thread):
    """
    Класс потока
    """

    def __init__(self, name):
        """Инициализация потока"""
        super().__init__()
        self.name = name

    def run(self):
        """
        Запуск потока
        :return: None
        """
        amount = random.randint(3, 15)  # Генерация рандомного количества времени задержки
        time.sleep(amount)  # говорим "спать" потоку некоторое случайное количество времени
        print(f"{self.name} запущен")  # вывод сообщения


def create_threads():
    """
    Создаем 5 потоков
    :return: None
    """
    for i in range(5):
        name = f"Поток #{i + 1}"
        my_thread = MyThread(name)
        my_thread.start()


if __name__ == "__main__":
    # запуск программы
    create_threads()
