import logging
import threading
import time

# Конфигурация логирования
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


# Целевая функция недемонического потока
def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')


# Целевая функция демонического потока
def daemon():
    logging.debug('Starting')
    time.sleep(3)  # "спать" 3 секунды
    logging.debug('Exiting')


# запуск программы
if __name__ == '__main__':
    # Создание потоков
    daemon_thread = threading.Thread(name='daemon', target=daemon, daemon=True)
    non_daemon_thread = threading.Thread(name='non-daemon', target=non_daemon)

    # Запуск потоков
    daemon_thread.start()
    non_daemon_thread.start()
