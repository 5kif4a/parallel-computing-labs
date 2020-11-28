import numpy as np
from mpi4py import MPI

from utils import rank_from_row


def gauss(data, comm, n):
    """
    Inverse rows using Gauss-Jordan elimination
    :param data: list of rows, with row index as last element of row
    :param comm: communicator
    :param n: matrix dimension
    :return: inversed rows
    """

    def _eliminate(l, r, cur):
        """
        Do gauss elimination step
        :param l: left-side row
        :param r: right-side row
        :param cur: current processed index
        :return: None
        """
        for indx in indexes:
            if indx == cur:
                continue
            rhs[indx] -= r * lhs[indx, cur]
            lhs[indx] -= l * lhs[indx, cur]

    def _send(indx, rnk):
        """
        Send changed row to other process
        :param indx: index of changed row
        :param rnk: rank of process that change row
        :return: None
        """
        comm.Bcast([lhs[indx], MPI.DOUBLE], root=rnk)
        comm.Bcast([rhs[indx], MPI.DOUBLE], root=rnk)

        _eliminate(lhs[indx], rhs[indx], indx)

    def _receive(indx, rnk):
        """
        Receive changed row from current active process
        :param indx: index of changed row
        :param rnk: rank of process that change row
        :return: None
        """
        comm.Bcast([l_row, MPI.DOUBLE], root=rnk)
        comm.Bcast([r_row, MPI.DOUBLE], root=rnk)

        _eliminate(l_row, r_row, indx)

    indexes = []

    lhs = np.zeros((n, n))
    rhs = np.identity(n)

    for line in data:
        ind = int(line[-1])
        indexes.append(ind)
        lhs[ind] = line[:-1]

    l_row = np.zeros(n, dtype=np.float64)
    r_row = np.zeros(n, dtype=np.float64)

    for i in range(n):  # forward elimination
        rank = rank_from_row(n, comm.size, i)

        if i in indexes:
            rhs[i] /= lhs[i, i]
            lhs[i] /= lhs[i, i]
            _send(i, rank)

        else:
            _receive(i, rank)

        comm.Barrier()

    for i in range(n - 1, -1, -1):  # back substitution
        rank = rank_from_row(n, comm.size, i)

        if i in indexes:
            _send(i, rank)
        else:
            _receive(i, rank)

        comm.Barrier()

    return [rhs.tolist()[ind] + [ind] for ind in indexes]
