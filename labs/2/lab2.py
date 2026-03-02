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
    # i = the number of age groups used e.g. i = 7 
    num_age_group = len(m)
    # initialize the matrix with zeros 
    # it is n x n matrix
    L = np.zeros((num_age_group,num_age_group))
    
    ## columns: the number of baby rabbits
    for juv in range(num_age_group):
        # survival rate s_0 (because for juvie rabbits, it is always probability of survival at month 0 before growing up)
        # maternity rate m_i (gets reproduced in different numbers each month)
        L[0][juv] = s[0] * m[juv]
        
    ## rows: the number of adult rabbits
    for adult in range(num_age_group-1):
        # update survival rate into the matrix
        L[adult+1][adult] = s[adult+1]
        
    
    # update the last column with the survival rate at last input month
    L[num_age_group-1][num_age_group-1] = s[num_age_group]
    
    return L 

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
    # prepare leslie matrix for list of population estimates
    L = leslie_matrix(s,m)
    
    # output array size: 1 x n+1(the number of time stamps) and +1 because we need to estimate the future population, not just the current population
    estimate = np.zeros((1,n+1))
    
    
    # match the range
    for i in range(n+1):
        # because it is 2d array, and we are filling up the columns, set [0][i]
        # first element should be np.sum(p)
        # then, we add up L @ p to p
        estimate[0][i] = np.sum(p)
        p = L @ p

    return estimate    
    # estimate = np.zeros((len(m),1))
    # estimate[0] = np.sum(p)
    # for i in range(1,n):
    #     p = L @ p
    #     estimate[i] = np.sum(p)
    
    # return estimate

# print(population_estimates(np.array([1., 0.8, 0.7]), np.array([0., 0.75]), np.array([0., 1.]), 6))

# print(leslie_matrix(np.array([1., 0.8, 0.7]), np.array([0., 0.75])))

p = [0,20,50,30,20,10,0]
s = [0.4, 0.5, 0.6, 0.5, 0.6, 0.5, 0.3, 0.3]
s_4_modified = [0.4, 0.5, 0.6, 0.5, 1.0, 0.5, 0.3, 0.3]
s_3_modified = [0.4, 0.5, 0.6, 1.0, 0.6, 0.5, 0.3, 0.3]
s_2_modified = [0.4, 0.5, 1.0, 0.5, 0.6, 0.5, 0.3, 0.3]
s_1_modified = [0.4, 1.0, 0.6, 0.5, 0.6, 0.5, 0.3, 0.3]

s_stabilized = [0.4, 0.887, 0.6, 0.5, 0.6, 0.5, 0.3, 0.3]
m = [0,0,2,4,2,0.5,0]

# 1. control
populations = population_estimates(s,m,p,50)
plt.plot(range(len(populations[0])), populations[0], color="r", label="control")

# 2. s[4] = 1
s4_modified_pop = population_estimates(s_4_modified,m,p, 50)
plt.plot(range(len(s4_modified_pop[0])), s4_modified_pop[0], color="g",label="s[4] = 1")

#3. s[3] = 1  
s3_more_mod_pop = population_estimates(s_3_modified,m,p,50)
plt.plot(range(len(s3_more_mod_pop[0])), s3_more_mod_pop[0], color="b",label="s[3] = 1")

#4. s[2] = 1
s2_more_mod_pop = population_estimates(s_2_modified,m,p,50)
plt.plot(range(len(s2_more_mod_pop[0])), s2_more_mod_pop[0], color="y",label="s[2] = 1")

# 5. s[1] = 1
s1_more_mod_pop = population_estimates(s_1_modified,m,p,50)
plt.plot(range(len(s1_more_mod_pop[0])), s1_more_mod_pop[0], color="m",label="s[1] = 1")

# 6. s[1] stabilized
s_stabilized = population_estimates(s_stabilized,m,p,50)
plt.plot(range(len(s_stabilized[0])), s_stabilized[0], color="c",label="s[1] stable")


plt.xlabel("time")
plt.ylabel("population")
plt.title("Population Dynamics for Different Survival Rates")
plt.xlim(0, 50)
plt.ylim(0, 300)
plt.legend()
plt.show()

# Some hints for how to set things up:
# ------------------------------------

# plt.plot(x, y, color='b', label='control')
#p2, = plt.plot(x, y2, 'c', label='s[4] = 1')

# plt.title('Population Dynamics for Different Survival Rates')
# plt.xlabel('time')
# plt.ylabel('population')
# plt.xlim(50)
# plt.ylim(300)
# #plt.axis((0, 50, 0, 300))
# plt.legend()
# plt.show()
