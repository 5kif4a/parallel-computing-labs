import sys

from numpy import linalg as la

from gauss import *
from utils import formatting, str_to_row, format_action, get_step_and_master_count, Timer, write_matrix

inp = open('input.txt', 'r')
out = open('output.txt', 'w')


def _do_inversion(com, rws):
    """
    Print formatting messages and call gauss elimination
    :param com: communicator
    :param rws: rows
    :return: inversed rows
    """
    print(formatting(com.rank, format_action('receive', rows=rws)))

    inv = gauss(np.array(rws, dtype=np.float64), com, n)

    print(formatting(com.rank, format_action('inverse', rows=inv)))

    return inv


comm = MPI.COMM_WORLD
master = 0
A, b, rows = [], [], []

if comm.rank == master:
    t = Timer('TOTAL')
    n = int(inp.readline())

    for line in inp:
        A.append(str_to_row(line))
        b.append(int(line[-2:-1]))

    a = np.array(A, dtype=np.float64)
    det = la.det(np.array(A))

    t_inv = Timer('inversion')

    if not det:
        print(formatting(comm.rank, 'ERROR! det A = {} - there is no inversion'.format(det)))
        comm.bcast(0, root=master)
        sys.exit()

    comm.bcast(n, root=master)

    step, master_count = get_step_and_master_count(n, comm.size)

    rows = [A[i] + [i] for i in range(int(master_count))]

    cur = int(master_count)
    for proc in range(1, comm.size):
        for i in range(int(step)):
            comm.send(A[int(cur) + i] + [int(cur) + i], dest=proc)  # send row with index as last element
        cur += int(step)

    inversed = _do_inversion(comm, rows)

    A_inv = inversed

    for proc in range(1, comm.size):
        A_inv += comm.recv(source=proc)

    A_inv.sort(key=lambda row: row[-1])
    A_inv = np.delete(A_inv, -1, 1)
    print(formatting(comm.rank, format_action('merge results')))
    t_inv.finish()
    write_matrix(A_inv, out)

    x = np.dot(A_inv, b)
    print(formatting(comm.rank, format_action('product A_inv on b', x=x.tolist())))
    out.write(('{}\n' + '{:.3f}\t' * len(x)).format(1, *x))

    t.finish()
else:
    t = Timer('proc{}'.format(comm.rank))
    n = comm.bcast(None, root=master)
    step = int(n / comm.size)

    if not step:
        sys.exit()

    for i in range(step):
        rows.append(comm.recv(source=master))

    inversed = _do_inversion(comm, rows)

    comm.send(inversed, dest=master)
    t.finish()
