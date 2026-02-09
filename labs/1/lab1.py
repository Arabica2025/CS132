import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
import time

def is_consistent(a):
    a = sp.linalg.lu(a)[2]
    row = a[~np.all(a == 0, axis=1)][-1]
    return not np.allclose(row[:-1], 0) and not np.isclose(row[-1], 0)

def solve(aug):
    #Using NumPy slicing, write a wrapper for this function called solve which takes as an argument an augmented
    #matrix and calls scipy.linalg.solve on the appropriate inputs.
    
    ## scipy.linalg.solve: only computes coefficient matrix
    ## solving augmented matrix:
    ## separate the constants from the coefficient matrix
    coef = aug[:, :-1] # coefficient matrix
    const = aug[:, -1] # right-hand side constants
    try:
        return sp.linalg.solve(coef,const)
    except Exception: # if any errors occur (e.g. inconsistent system), return None.
        return None

def best_fit_cubic(x_axis, y_axis):
    coeff = np.linalg.lstsq(np.vstack(pow(x_axis, 3)), y_axis, rcond=None)[0][0]
    return coeff, coeff * pow(x_axis, 3)

def benchmark(n, step_size=10, low=-100, hi=100):
    # create a randon number generator
    rng = np.random.default_rng()

    x_axis = np.arange(1, n + 1) * step_size
    y_axis_con = np.zeros(n)
    y_axis_solve = np.zeros(n)
    y_axis_getrf = np.zeros(n)

    for i in range(n):
        x = x_axis[i]
        print(f'benchmarking: {x}')
        times_con = []
        times_solve = []
        times_getrf = []
        for _ in range(5):
            # create a random augmented matrix
            aug = (hi - low) * rng.random((x, x + 1)) + low
            augf = np.asfortranarray(aug)

            # time is_consistent
            start = time.time()
            is_consistent(aug)
            times_con.append(time.time() - start)

            # time solve
            start = time.time()
            solve(aug)
            times_solve.append(time.time() - start)

            # time getrf
            start = time.time()
            sp.linalg.lapack.get_lapack_funcs(('getrf',), (augf,))[0](augf)
            times_getrf.append(time.time() - start)

        # average the runs
        y_axis_con[i] = np.average(times_con)
        y_axis_solve[i] = np.average(times_solve)
        y_axis_getrf[i] = np.average(times_getrf)


    coeff, y_axis_cubic = best_fit_cubic(x_axis, y_axis_getrf)
    print(f'getrf running is approximately an^3 where a = {coeff}')
    print(f'the number of FLOPs per second performed by my CPU: {(2/3)*coeff} FLOPs per second')

    data_con, = plt.plot(x_axis, y_axis_con, 'ro', label='is_consistent')
    data_solve, = plt.plot(x_axis, y_axis_solve, 'g^', label='solve')
    data_getrf, = plt.plot(x_axis, y_axis_getrf, 'bo', label='getrf')
    cubic, = plt.plot(x_axis, y_axis_cubic, label='best fit cubic')
    plt.xlabel('# rows/cols')
    plt.ylabel('time (sec)')
    plt.legend(handles=[data_con, data_solve, data_getrf, cubic])
    plt.show()

benchmark(70)
