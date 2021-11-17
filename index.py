from mpi4py import MPI
import numpy as np

matrix_a = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [8, 3, 6, 8],
    [8, 3, 6, 8]
]

matrix_b = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [8, 3, 6, 8],
    [8, 3, 6, 8]
]

comm = MPI.COMM_WORLD
r = comm.Get_rank()
s = comm.Get_size()

workers = s - 1

if r == 0:
    per_rank = len(matrix_a)//workers
    more = len(matrix_a)%workers
    start = 0
    for dest in range(1,workers+1):
        rows = 0
        if dest <= more:
            rows = per_rank + 1
        else:
            rows = per_rank
        comm.send({'rows':rows, 'start':start}, dest=dest)
        start += rows
    
    matrix_c = []
    for source in range(1,workers+1):
        m = comm.recv(source=source)
        for r in m:
            matrix_c.append(r)
    print(f"Final result: {matrix_c}")
else:
    m = comm.recv()
    start_row = m['start']
    b_cols = len(matrix_b[0])
    a_rows = m['rows']
    a_cols = len(matrix_a[0])
    res = np.zeros( (a_rows, b_cols) )

    for i in range(b_cols):
        for j in range(a_rows):
            for k in range(a_cols):
                res[j][i] += matrix_a[start_row + j][k] * matrix_b[k][i]

    comm.send(res, dest=0)