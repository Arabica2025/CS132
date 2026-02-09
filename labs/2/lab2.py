import numpy as np
import matplotlib.pyplot as plt

def leslie_matrix(s, m):
    """Constructs the Leslie matrix with given survival and maternity
    parameters.

    Parameters
    ----------
    s : numpy.ndarray
        1D ndarray with survival parameters, i.e., s[i] is the
        probability that an individual that is age i lives to age (i +
        1) and s[-1] is the probability that any individual with age N
        >= len(s) - 1 lives to age (N + 1)
    m : numpy.ndarray

        1D ndarray with maternity parameters, i.e., m[i] is the number
        of offspring an individual of age (i + 1) produces on average
        when they are age (i + 1) and m[-1] is the number of offspring
        that an individual of age N >= len(m) produces on average each
        time-step.  It must be that m.shape[0] == s.shape[0] - 1

    Returns
    -------
    numpy.ndarray
        2D ndarray representing the Leslie matrix for the given
        parameters, i.e., if p is a 1D ndarray with p[i] where p[i] is
        the number of individuals of age (i + 1), and the output of
        this function is the ndarray L, then (L @ p)[i] is the number
        of indivuals of age (i + 1) after 1 time-step has passed.

    Examples
    --------
    >>> leslie_matrix(np.array([1., 1., 1.]), np.array([0., 1.]))
    array([[0., 1.],
           [1., 1.]])

    >>> leslie_matrix(np.array([1., 0.8, 0.7]), np.array([0., 0.75]))
    array([[0.  , 0.75],
           [0.8 , 0.7 ]])

    """
    pass # TODO

def population_estimates(s, m, p, n):
    """Estimates the population for every time step from 0 to n - 1
    using the Leslie matrix.

    Parameters
    ----------
    s : ndarray
        1D ndarray with survival parameters (see above)
    m : ndarray
        1D ndarray with maternity parameters (see above)
    p : ndarray
        1D ndarray with initial populations, i.e., p[i] is the number
        of individuals of age (i + 1).  It must be that p.shape[0] ==
        s.shape[0] - 1

    Returns
    -------
    list

        list of population estimates based on the Leslie matrix, i.e.,
        if L is the Leslie matrix for parameters s and m, then the
        return value should be [np.sum(p), np.sum(L @ p), np.sum(L @
        (L @ p)),...]

    Examples
    --------
    >>> population_estimates(np.array([1., 1., 1.]), np.array([0., 1.]), np.array([0., 1.]), 6)
    [1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0]

    >>> population_estimates(np.array([1., 0.8, 0.7]), np.array([0., 0.75]), np.array([0., 1.]), 6)
    [1.0, 1.45, 1.615, 2.0004999999999997, 2.36935, 2.8588449999999996, 3.4228015]
    """
    pass # TODO


# Some hints for how to set things up:
# ------------------------------------

# p1, = plt.plot(x, y1, 'b', label='control')
# p2, = plt.plot(x, y2, 'c', label='s[4] = 1')

# plt.title('Population Dynamics for Different Survival Rates')
# plt.xlabel('time')
# plt.ylabel('population')
# plt.axis((0, 50, 0, 300))
# plt.legend(handles=[p1, p2])
# plt.show()
