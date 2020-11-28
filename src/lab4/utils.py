import time


def str_to_row(s):
    return [int(x) for x in s.split()][:-1]


def get_step_and_master_count(n, size):
    """
    Count number of rows per process
    :param n: matrix dimension
    :param size: number of process
    :return: number of rows for slave and for master
    """
    step = n / size
    return step, step + n % size


def rank_from_row(n, size, i):
    """
    Count rank of process that work with row
    :param n: matrix dimension
    :param size: number of process
    :param i: row index
    :return: process rank
    """
    step, master_count = get_step_and_master_count(n, size)

    if i < master_count:
        return 0

    i -= master_count
    return 1 + i // step


class Colors(object):
    HEADER = '\033[1;95m'
    OKBLUE = '\033[1;94m'
    OKGREEN = '\033[1;92m'
    WARNING = '\033[1;93m'
    FAIL = '\033[1;91m'
    CYAN = '\033[1;96m'
    ENDC = '\033[0m'


def formatting(rank, message):
    template = '${color} {name}{end_color}: {message}'

    return template.format(
        color=(Colors.FAIL if rank == 0 else Colors.OKGREEN),
        name=('master' if rank == 0 else 'proc{}'.format(rank)),
        end_color=Colors.ENDC,
        message=message
    )


def format_action(action, rows=None, x=None):
    template = '\t*{0}*\t'
    args = [action]
    if rows:
        template += '{1} rows'
        args.append(len(rows))
        if len(rows) < 4 and len(rows[0]) < 10:
            template += ': {2}'
            args.append([row[:-1] for row in rows])
    if x and len(x) < 10:
        template += '{1}x = {2}{3}'
        args += [Colors.OKBLUE, x, Colors.ENDC]
    return template.format(*args)


def write_matrix(matrix, out):
    out.write('{}\n'.format(len(matrix)))
    for row in matrix:
        out.write(('{:.3f}\t' * len(matrix) + '\n').format(*row))


class Timer(object):
    def __init__(self, message):
        self.message = message
        self.start = time.time()

    def finish(self):
        print("-" * 20 + "| {0}: {1:.3f} s |".format(self.message, (time.time() - self.start)) + "-" * 20)
