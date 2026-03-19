import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt



def solve(a: np.ndarray, bs: np.ndarray)-> np.ndarray:
    # uses numpy.linalg.solve to solve each matrix equation
    return np.linalg.solve(a,bs)

def lu_solve(a: np.ndarray, bs: np.ndarray)-> np.ndarray:
    # uses the function scipy.linalg.lu_factor to LU factor a, and then
    # uses scipy.linalg.lu_solve to solve each matrix equation
    # *this should only factor once
    # 1. LU Factorization to create two different matrices of Lower and Upper 
    lu, pivot = sp.linalg.lu_factor(a)
    return sp.linalg.lu_solve((lu, pivot), bs)

def inv_solve(a: np.ndarray,bs: np.ndarray)-> np.ndarray:
    # uses numpy.linalg.inv to invert a, and then uses
    # matrix-vector multiplication(@) to solve each matrix equation
    # *this should only invert once
    inv = np.linalg.inv(a)
    return inv @ bs



def benchmark_random(num_exp: int, step_size: int, num_eqs: int, process, low=-100, hi=100):
    """Benchmark a process using random matrix equations.

    Parameters
    ----------
    num_exp : int
        The number of experiments to be run.
    step_size : int
        This value dictates the size of each experiment to run.  For
        example, if experiments with step size `10`, then the i-th
        experiment should use a matrix of size `(10 * i)` by `(10 * i)`
    num_eqs : int
        This value dictates the number of experiments that `process`
        needs to solve, if `num_eqs` is `100`, then the length of the
        vectors `bs` passed into `process` should be `100`.
    process
        The function to benchmark.  In this lab, it will be `solve`,
        `lu_solve`, or `inv_solve`, as defined in the lab spec.
    low : int, default=100
        The lowest value that should appear in a random matrix/vector
    high : int, default=100
        The highest value that should appear in a random matrix/vector

    Returns
    -------
    tuple[np.ndarray, np.ndarry]
        The output `x_axis, y_axis` should be the `x_axis` of the
        experiment, which should be of the form:
            `np.array([1 * step_size, 2 * step_size,..., num_exp * step_size])`
        and `y_axis` should be the times it takes to run each experiment.

    Notes
    -----
    An experiment is comprised of the following:

    * Generate a random matrix `a` of the appropriate size with values
      between `low` and `high`.

    * Generate a list of vectors `bs` of the appropriate size, of
      length `num_eqs`.

    * Time `process(a, bs)`.  Be careful not to include the matrix
      generation as part of the timing.

    """
    rng = np.random.default_rng() # random number generator
    # matrix A: i-th experiment should use a matrix of size `(step_size * i)` by `(step_size * i)`
    ## i: the number of experiments so should be num_exp
    
    x_axis = []
    y_axis = []
    for i in range(num_exp):
        n = step_size * i
        a = (hi-low) * rng.random((n, n))+low
        bs = (hi - low) * rng.random((n, num_eqs))+ low
        
        start = time.time()
        process(a, bs)
        end = time.time() - start
        
        x_axis.append(n)
        y_axis.append(end)
    return np.array(x_axis), np.array(y_axis)
    # if process is 'solve':
    #     start = time.time()
    #     for i in range(num_exp):
    #         x_process = solve(A[i], bs[i])
    #     t_solve = time.time() - start
        
    # elif process is 'lu_solve':
    #     start = time.time()
    #     for i in range(num_exp):
    #         x_lu = lu_solve(A[i],bs[i])
    #     t_lu = time.time() - start
        
    # elif process is 'inv_solve':
    #     start = time.time()
    #     for i in range(num_exp):
    #         x_inv = inv_solve(A,bs)
    #     t_inv = time.time() - start
    


def banded_matrix(k):
    n = 2 * k
    # print("n after n = 2 * k:",n)
    d = 4 * np.eye(n) # np.eye(): create identity matrix
    # print()
    # print("d after 4 * np.eye(n):")
    # print(d)
    d -= np.eye(n, k=2) + np.eye(n, k=-2)
    # print()
    # print("d after d -= np.eye(n, k=2) + np.eye(n, k=-2):")
    # print(d)
    a = [-1 * (n % 2) for n in range(1, n)]
    # print()
    # print("a after a = [-1 * (n % 2) for n in range(1, n)]:")
    # print(a)
    d += np.diag(a, k=-1) + np.diag(a, k=1)
    # print("d after d += np.diag(a, k=-1) + np.diag(a, k=1):")
    # print(d)
    # print()
    # print("final result")
    # print(d)
    return d

def benchmark_banded(num_exp, step_size, num_eqs, process, low=-100, hi=100):
    """Benchmake a process using a banded matrix equation.

    This function is *identical* to `benchmark_random` except that `a`
    in the experiment described above, should be replaced with the
    output of `banded_matrix` on the appropriate argument

    Note that `banded_matrix` takes a parameter `k` and produces a
    matrix with shape `(2 * k, 2 * k)`, so be careful about what
    parameter you use.

    """
    rng = np.random.default_rng() # random number generator
    # matrix A: i-th experiment should use a matrix of size `(step_size * i)` by `(step_size * i)`
    ## i: the number of experiments so should be num_exp
    
    # x_axis, y_axis prep
    x_axis = []
    y_axis = []
    # iteration for the number of experiments
    for i in range(num_exp):
        n = step_size * i # the size of each experiment to run; i-th experiment should use a matrix of size step_size * i(current iteration)
        a = banded_matrix(n) # create banded_matrix of size n
        bs = (hi - low) * rng.random((a.shape[0], num_eqs)) + low # bs is random vector used for calculation
        print("a.shape:", a.shape)
        print("bs.shape:", bs.shape)
        
        start = time.time()# set timer only for the process
        process(a,bs) 
        end = time.time()-start
        
        # store the result in x_axis and y_axis
        x_axis.append(a.shape[0]) # np.array([1 * step_size, 2 * step_size,..., num_exp * step_size])
        y_axis.append(end) # time to execute the process
        
    return np.array(x_axis), np.array(y_axis)

# banded_matrix(3)

def plotting(num_exp, step_size, num_eqs, process1, process2, benchmark):
    plt.figure() # create new figure for plotting
    
    # call x_axis and y_axis from the process
    ## 1. first process benchmark
    x_cmp1, y_cmp1 = benchmark(num_exp, step_size, num_eqs, process1)
    ## 2. second process benchmark
    x_cmp2, y_cmp2 = benchmark(num_exp, step_size, num_eqs, process2)
    
    plt.xlabel("matrix size in i-th experiment")
    plt.ylabel("Runtime")
    plt.title(f"Runtime comparison: {process1.__name__} vs. {process2.__name__}")
    plt.plot(x_cmp1, y_cmp1, label=process1.__name__)
    plt.plot(x_cmp2, y_cmp2, label=process2.__name__)
    
    plt.legend()
    plt.show()
    
    

    

if __name__ == "__main__":
    #print(banded_matrix(3))
    # print("-----------benchmark_random unit test------------")
    # print("benchmark_random solve:",benchmark_random(10,5,5,solve))
    # print("benchmark_random lu_solve:", benchmark_random(10,5,5,lu_solve))
    # print("benchmark_random inv_solve:", benchmark_random(10,5,5,inv_solve))
    
    
    # print()
    # print("-----------benchmark_banded unit test------------")
    # print("benchmark_banded solve:",benchmark_banded(10,5,5,solve))
    # print("benchmark_baned lu_solve:", benchmark_banded(10,5,5,lu_solve))
    print("benchmark_banded inv_solve:", benchmark_banded(10,5,5,inv_solve))
    
    #plotting(100,10,100,solve, lu_solve, benchmark_random)
    #plotting(250, 10, 100, inv_solve, lu_solve, benchmark_random)
    #plotting(8, 1000, 100, inv_solve, lu_solve, benchmark_banded)
