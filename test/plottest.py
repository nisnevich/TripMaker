import matplotlib.pyplot as plt
import numpy as np

# if you want the vertical line _|
# plt.plot([0,2.3,2.3,5],[0,0,1,1])
#
# OR:
#                                       _
# if you don't want the vertical line _
#plt.plot([0,2.3],[0,0],[2.3,5],[1,1])

# now change the y axis so we can actually see the line
plt.hlines(range(1,3), range(4,6))
plt.show()
