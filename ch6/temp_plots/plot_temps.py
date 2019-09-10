from matplotlib.ticker import MultipleLocator

def plot_temps(df, min_temp, max_temp, extreme_low_temps, extreme_high_temps):
    ax1 = df.plot.line(y = ['TMAX', 'TMIN'], 
            figsize = (12, 9),
            ylim = (1.3 * min_temp, 1.3 * max_temp),
            rot = 45, fontsize = 12, style = ['-r', '-b'], linewidth = 0.6,
            legend = False,
            x_compat = True)
    ax1.lines[0].set_label('Max. temperature')
    ax1.lines[-1].set_label('Min. temperature')
    ax1.set_title('Low and High Temperatures in January 2010\nNorth Dakota, United States', 
                  fontsize = 20, y = 1.06)
    ax1.set_xlabel('Date', fontsize = 14, labelpad = 15)
    ax1.set_ylabel('Temperature [\u2103]', fontsize = 14)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax1.fill_between(df.index, df['TMAX'], df['TMIN'], 
                     facecolor = 'lightgray', alpha = 0.25)

    def fahrenheit_to_celisus(temp):
        return 1.8 * temp + 32

    ax2 = ax1.twinx()
    y_min, y_max = ax1.get_ylim()
    ax2.set_ylim(fahrenheit_to_celisus(y_min), fahrenheit_to_celisus(y_max))
    ax2.set_ylabel('Temperature [\u2109]', fontsize = 14, labelpad = 15)
    ax2.spines['top'].set_visible(False)
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    for label in ax2.get_yticklabels():
        label.set_fontsize(12)
    
    ax1.scatter(extreme_low_temps.index, extreme_low_temps, 
                color = 'blue', marker = 'v', s = 100, 
                label = 'Unusually low temperatures')
    ax1.scatter(extreme_high_temps.index, extreme_high_temps, 
                color = 'red', marker = '^', s = 100, 
                label = 'Unusually high temperatures')
    ax1.legend(loc = 4, frameon = False, title = 'Legend')
