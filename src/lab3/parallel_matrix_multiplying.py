import sys

import numpy as np
from mpi4py import MPI

numberRows = int(sys.argv[1])
numberColumns = int(sys.argv[2])
TaskMaster = 0

assert numberRows == numberColumns

print("Инициализация переменных")
a = np.zeros(shape=(numberRows, numberColumns))
b = np.zeros(shape=(numberRows, numberColumns))
c = np.zeros(shape=(numberRows, numberColumns))


def populate_matrix(p):
    for i in range(0, numberRows):
        for j in range(0, numberColumns):
            p[i][j] = i + j


comm = MPI.COMM_WORLD
worldSize = comm.Get_size()
rank = comm.Get_rank()
processorName = MPI.Get_processor_name()

print("Процесс #%d запущен" % rank)
print("Запуск из процессора %s, ранг %d из процессоров %d" % (processorName, rank, worldSize))

# Рассчет среза на один процесс
if worldSize == 1:
    slice_ = numberRows
else:
    slice_ = numberRows // (worldSize - 1)

assert slice_ >= 1

populate_matrix(b)

comm.Barrier()

if rank == TaskMaster:
    print("Инициализация матриц A и B (%d,%d)" % (numberRows, numberColumns))
    print("Старт")
    populate_matrix(a)

    for i in range(1, worldSize):
        offset = (i - 1) * slice_  # 0, 10, 20
        print(offset)
        row = a[offset, :]
        comm.send(offset, dest=i, tag=i)
        comm.send(row, dest=i, tag=i)
        for j in range(0, slice_):
            comm.send(a[j + offset, :], dest=i, tag=j + offset)
    print("Отправлено всем процессам")

comm.Barrier()

if rank != TaskMaster:

    print("Данные получены с процесса #%d" % rank)
    offset = comm.recv(source=0, tag=rank)
    recv_data = comm.recv(source=0, tag=rank)
    for j in range(1, slice_):
        c = comm.recv(source=0, tag=j + offset)
        recv_data = np.vstack((recv_data, c))

    print("Начало вычислений с процесса #%d" % rank)

    # Цикл по строкам
    t_start = MPI.Wtime()
    for i in range(0, slice_):
        res = np.zeros(shape=numberColumns)
        if slice_ == 1:
            r = recv_data
        else:
            r = recv_data[i, :]
        ai = 0
        for j in range(0, numberColumns):
            q = b[:, j]
            for x in range(0, numberColumns):
                res[j] = res[j] + (r[x] * q[x])
            ai = ai + 1
        if i > 0:
            send = np.vstack((send, res))
        else:
            send = res
    t_diff = MPI.Wtime() - t_start

    print("Процесс #%d завершен в %5.4fs" % (rank, t_diff))
    # Отправка больших данных
    print("Отправка результатов в мастер %d байт" % send.nbytes)
    comm.Send([send, MPI.FLOAT], dest=0, tag=rank)  # 1, 12, 23

comm.Barrier()

if rank == TaskMaster:
    print("Проверка результов")
    res1 = np.zeros(shape=(slice_, numberColumns))
    comm.Recv([res1, MPI.FLOAT], source=1, tag=1)

    kl = np.vstack(res1)
    for i in range(2, worldSize):
        resx = np.zeros(shape=(slice_, numberColumns))
        comm.Recv([resx, MPI.FLOAT], source=i, tag=i)
        print("Получен ответ от процесса #%d" % i)
        kl = np.vstack((kl, resx))
    print("Конец")
    print("Результат умножения AxB.\n")
    print(kl)

comm.Barrier()
