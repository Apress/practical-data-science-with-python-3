import numpy as np
import dask.array as da

def num_divisible(a, b, c):
    r = a % c
    if r == 0:
        start = a
    else:
        start = a + (c - r)

    if start > b:
        return 0
    else:
        return 1 + (b - start) // c
    
num_divisible_vect = np.vectorize(num_divisible)
x = da.asanyarray([(1, 100, 10), (16789, 445267839, 7), (34, 10**18, 3000), (3, 7, 9)])
x = x.rechunk(chunks=(2, -1))
y = x.map_blocks(lambda block: num_divisible_vect(*block.T), 
                 chunks=(-1,), 
                 drop_axis=1, 
                 dtype='i8')
print(y.compute())