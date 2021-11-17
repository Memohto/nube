from mpi4py import MPI

r = MPI.COMM_WORLD.Get_rank()
n = MPI.Get_processor_name()

print(f"Desde el rank {r}  en {n}")