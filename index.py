from mpi4py import MPI

matriz = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [8, 3, 6, 8],
    [8, 3, 6, 8]
]

r = MPI.COMM_WORLD.Get_rank()
s = MPI.COMM_WORLD.Get_size()

if r == 0:
    for i in range(1,s+1):
        print(i)


print(f"Desde el rank {r}, size: {s}")