import os
import time
import urllib.request
from queue import Queue
from threading import Thread


class Downloader(Thread):
    """
    Класс потока, который скачивает файлы
    """
    def __init__(self, queue):
        """
        Инициализация класс
        :param queue: Очередь
        """
        super().__init__()
        self.queue = queue

    @staticmethod
    def download_file(url):
        """
        Метод скачивания файла
        :param url: URL файла
        :return: None
        """

        start = time.thread_time()

        handle = urllib.request.urlopen(url)
        fname = os.path.basename(url)

        with open(fname, "wb") as f:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                f.write(chunk)

        end = time.thread_time()
        total = end - start

        print(f"{fname} закончил загрузку {url}! Время загрузки файла: {total} сек")

    def run(self):
        """
        Запуск потока
        :return: None
        """

        # пока очередь не пуста
        while True:
            # получаем URL файла
            url = self.queue.get()

            # скачиваем файл
            self.download_file(url)

            # завершаем задачу очереди
            self.queue.task_done()


if __name__ == "__main__":
    queue = Queue()  # Инициализация очереди

    # список URL файлов для скачивания
    urls = [
        "https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png",
        "https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_1MB.png",
        "https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_2100kB.png",
        "http://speedtest.ftp.otenet.gr/files/test1Mb.db",
        "http://speedtest.ftp.otenet.gr/files/test100k.db"
    ]

    # Создание потоков
    for i in range(5):
        t = Downloader(queue)
        t.setDaemon(True)
        t.start()

    # добавление ссылок на скачивание файлов в Очередь
    for url in urls:
        queue.put(url)

    # запуск очереди
    queue.join()
