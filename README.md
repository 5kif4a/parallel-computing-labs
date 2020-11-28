## Лабораторные работы по дисциплине "Параллельные и высокопроизводительные вычисления"
### Реализация на Python
#### Используемые библиотеки:
- [numpy](https://numpy.org/)
- [mpi4py](https://mpi4py.readthedocs.io/en/stable/)
#### Установка MPI на Win10
[Ссылка на скачивание](https://www.microsoft.com/en-us/download/details.aspx?id=57467)
#### Установка проекта и среды для запуска скриптов
```
git clone 
cd 
py -m venv venv
pip install -r requirements.txt
```
#### Лабораторная работа №1 - Параллелизм в Python
[Исходный код](src/lab1)
#### Лабораторная работа №2 - Параллельные методы умножения матрицы на вектор
[Исходный код](src/lab2/foo.py)  
Пример запуска скрипта  
```
mpiexec -n 4 py foo.py
```
#### Лабораторная работа №3 - Параллельные методы матричного умножения
[Исходный код](src/lab3/parallel_matrix_multiplying.py)  
Пример запуска скрипта  
```
mpiexec -n 4 py parallel_matrix_multiplying.py <кол-во строк матрицы> <кол-во столбцов матрицы>
```
#### Лабораторная работа №4 - Параллельные методы решения систем линейных уравнений
[Исходный код](src/lab4)  
**Параллельный алгоритм Гаусса для решения СЛАУ**   
Пример запуска скрипта
```
# сгенерировать файл с входными данными
py gen <размер матрицы NxN> <максимальное рандомное значение ячейки матрицы>
# запуск скрипта
mpiexec -n 4 py solver.py
```
#### Пример запуска скрипта с MPI
```
mpiexec -n <количество процессов> py <название скрипта.py>
```
##### ВНИМАНИЕ! Перед запуском скрипта с MPI перейдите в директорию с самим скриптом