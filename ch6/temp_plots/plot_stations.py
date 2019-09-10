import matplotlib.pyplot as plt
import mplleaflet

def plot_stations(longitudes, latitudes, embedded = False):
    if embedded:
        plt.figure(figsize = (8, 8))
    plt.scatter(longitudes, latitudes, 
                c = 'b',
                marker = 'D',
                alpha = 0.7, 
                s = 200)
    return mplleaflet.display() if embedded else mplleaflet.show()
