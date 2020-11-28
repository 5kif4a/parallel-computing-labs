import os
import time
import urllib.request
from threading import Thread


class DownloadThread(Thread):
    """
    Класс потока, который скачивает файлы
    """

    def __init__(self, url, name):
        """
        Инициализация класса
        :param url: URL файла для скачивания
        :param name: имя файла
        """
        super().__init__()
        self.name = name
        self.url = url

    def run(self):
        """
        Запуск потока
        :return: None
        """
        start = time.thread_time()

        handle = urllib.request.urlopen(self.url)
        fname = os.path.basename(self.url)

        with open(fname, "wb") as f_handler:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                f_handler.write(chunk)

        end = time.thread_time()
        total = end - start
        print(f"{self.name} закончил загрузку {self.url}! Время загрузки файла: {total} сек")


def main(urls):
    # Создание потоков для скачивания файлов
    for item, url in enumerate(urls):
        name = "Поток %s" % (item + 1)
        thread = DownloadThread(url, name)
        thread.start()


if __name__ == "__main__":
    # список URL файлов для скачивания
    urls = [
        "https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png",
        "https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_1MB.png",
        "https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_2100kB.png",
        "http://speedtest.ftp.otenet.gr/files/test1Mb.db",
        "http://speedtest.ftp.otenet.gr/files/test100k.db"
    ]
    main(urls)
