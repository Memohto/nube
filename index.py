# https://gist.github.com/kmkurn/39ca673bb37946055b38

from mpi4py import MPI
import numpy as np
import pyrebase

config = {
  "apiKey": "AIzaSyB33WNvEv9-SBciuOZK2A8ZUbRO14fwc5k",
  "authDomain": "nubes-e8905.firebaseapp.com",
  "databaseURL": "https://nubes-e8905-default-rtdb.firebaseio.com",
  "storageBucket": "nubes-e8905.appspot.com"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
user = auth.sign_in_with_email_and_password('test@mail.com', 'Nubes1234')

db = firebase.database()

def solve(matrix_a, matrix_b):
    comm = MPI.COMM_WORLD
    r = comm.Get_rank()
    s = comm.Get_size()

    workers = s - 1

    if r == 0:
        start_time = MPI.Wtime()

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

        end_time = MPI.Wtime()
        total_time = end_time - start_time
        return {
            'matrix': matrix_c,
            'time': total_time
        }
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

def stream_handler(message):
    matrix = message["data"]
    if matrix != None:
        result = solve(matrix, matrix)
        print(f"Result: {result['matrix']}, in {result['time']}")
        db.child("output").set(result)
        

my_stream = db.child("input").stream(stream_handler)