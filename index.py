from mpi4py import MPI

matrix = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [8, 3, 6, 8],
    [8, 3, 6, 8]
]

comm = MPI.COMM_WORLD
r = comm.Get_rank()
s = comm.Get_size()

if r == 0:
    per_rank = len(matrix)//s
    more = len(matrix)%s
    start = 0
    for dest in range(1,s):
        rows = 0
        if dest <= more:
            rows = per_rank + 1
        else:
            rows = per_rank
        comm.send({'rows':rows, 'start':start}, dest=dest)
        start += rows
else:
    m = comm.recv()
    print(f"Message received: Rows {m['rows']}, Start: {m['start']}")




print(f"Desde el rank {r}, size: {s}")