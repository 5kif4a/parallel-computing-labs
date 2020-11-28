#!/usr/bin/env python
"""
    usage: python gen.py {matrix_size} {max_element_value}
    return: A | b matrix, where rank A = {matrix_size}
"""

import random
import sys

try:
    n = int(sys.argv[1])
    m = int(sys.argv[2])
except (IndexError, ValueError) as e:
    print('Error!')
    print(__doc__)
    exit(1)

f = open('input.txt', 'w')
f.write(f'{n}\n')
for i in range(n):
    for j in range(n + 1):
        template = '{} ' if j != n else '{}\n'
        f.write(template.format(random.randint(1, m)))
f.close()
