import numpy as np
import matplotlib.pyplot as plt

quartets = np.asarray([
    (
     [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0], 
     [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
    ), 
    (
     [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0], 
     [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
    ), 
    (
     [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0], 
     [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
    ), 
    (
     [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 19.0, 8.0, 8.0, 8.0],
     [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
    )
])
    
roman = ['I', 'II', 'III', 'IV']

fig = plt.figure(figsize = (12, 9))
fig.suptitle("Anscombe's Quartets", fontsize=16)
axes = fig.subplots(2, 2, sharex = True, sharey = True)

for quartet in range(quartets.shape[0]):
    x, y = quartets[quartet]
    coef = np.polyfit(x, y, 1)
    reg_line = np.poly1d(coef) 

    ax = axes[quartet // 2, quartet % 2]
    ax.plot(x, y, 'ro', x, reg_line(x), '--k')
    ax.set_title(roman[quartet])
    ax.set_xlim(3, 19.5)
    ax.set_ylim(2, 13)    
    
    # Print summary statistics for the current dataset
    print("Quartet:", roman[quartet])
    print("Mean X:", x.mean())
    print("Variance X:", x.var())
    print("Mean Y:", round(y.mean(), 2))
    print("Variance Y:", round(y.var(), 2))
    print("Pearson's correlation coef.:", round(np.corrcoef(x, y)[0][1], 2))
    print()

plt.show()