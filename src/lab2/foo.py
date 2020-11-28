import numpy as np
from mpi4py import MPI
from pprint import pprint

size = 10000  # размерность вектора
iter = 20  # количество итерации

comm = MPI.COMM_WORLD  # инициализация коммуникатора

pprint(f"Запуск #{comm.rank + 1} из {comm.size} параллельных MPI процессов")

vector_size = size // comm.size  # распределение длины вектора для каждого процесса
size = comm.size * vector_size
offset = comm.rank * vector_size  # сдвиг индекса для

vector = np.zeros(size)  # инициализация вектора
vector[0] = 1.0

# Инициализация матрицы
matrix = np.zeros((vector_size, size))
for i in range(vector_size):
    j = (offset + i - 1) % size
    matrix[i, j] = 1.0

comm.Barrier()  # Начало блокировки, пока все процессы коммуникатора не достигнут этой процедуры
t_start = MPI.Wtime()  # Начало замера времени

# Умножение матрицы на вектор iter раз
for t in range(iter):
    my_new_vec = np.inner(matrix, vector)
    comm.Allgather([my_new_vec, MPI.DOUBLE],  # Сборка данных со всех процессов
                   [vector, MPI.DOUBLE])

comm.Barrier()  # Конец блокировка, пока все процессы коммуникатора не достигнут этой процедуры
t_diff = MPI.Wtime() - t_start  # Конец замера времени

# Вывод результатов
pprint("%d итерации размером %d в %5.2fсек: %5.2f итерации в секунду" % (iter, size, t_diff, iter / t_diff))
pprint(100 * "=")
