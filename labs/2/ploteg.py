import matplotlib.pyplot as plt
import numpy as np

# # set x and y
# x = np.arange(10)
# y = x**2

# #plot x and y
# plt.plot(x,y)


# # labels
# plt.xlabel("time")
# plt.ylabel("population")
# plt.title("example line plot")

# # show the plot
# plt.show()

# create new figure
plt.figure()

x = np.arange(10)
y1 = x**7
y2 = x**3
y3 = x**2

X_LIMIT = 10
Y_LIMIT = 1000

plt.plot(x, y1, color = 'r', label="control group")
plt.plot(x, y2, color = 'g', label="s[4] = 1")
plt.plot(x, y3, color = 'b', label="s[3] = 1")

plt.xlabel("time")
plt.ylabel("population")
plt.title("Population dynamics")

# axis limit
plt.xlim(0, X_LIMIT)
plt.ylim(0,Y_LIMIT)

plt.legend()

plt.show()