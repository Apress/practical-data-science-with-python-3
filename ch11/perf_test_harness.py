import time

import numpy as np
import pandas as pd

def measure(f, num_repetitions=5):
    measurements = np.array([])
    for _ in range(num_repetitions):
        start = time.clock()
        f()
        measurements = np.append(measurements, time.clock() - start)
    return measurements.mean()

def execute(config):
    execution_times = {}

    for config_name in config['functions']:
        execution_times[config_name] = np.array([])
    
    for x in config['span']:
        for config_name in config['functions']:
            execution_times[config_name] = np.append(
                    execution_times[config_name], 
                    measure(lambda: config['functions'][config_name](x)))
    return execution_times

def attach_model(execution_times, config, function_name, model_name):
    model_vals = np.vectorize(config['models'][model_name])(config['span'])
    c = np.mean(execution_times[function_name] / model_vals)
    execution_times[model_name] = c * model_vals
 
def report(execution_times, x_vals, **plot_kwargs):
    df = pd.DataFrame(execution_times)
    df.index = x_vals
    ax = df.plot.line(
        figsize=(10, 8),
        title='Performance Test Report',
        grid=True, 
        **plot_kwargs
    )
    ax.set_xlabel('Span')
    ax.set_ylabel('Time [s]')
    return df

if __name__ == '__main__':
    import math
    
    from count_occurrences_digit_naive import count_occurrences_digit_naive
    import count_occurrences_digit as cog

    table_of_occurrences = cog.setup()
    config = {
        'functions': {
            'naive(k=0)': lambda n: count_occurrences_digit_naive(0, n),
            'fast(k=0)': lambda n: cog.count_occurrences_digit(0, n, table_of_occurrences)
        },
        'models': {
            'O(n)': lambda n: n,
            'O(log n)': lambda n: math.log(n)
        },
        'span': np.geomspace(10**2, 10**7, num=14, dtype=int)
    }
    execution_times = execute(config)
    attach_model(execution_times, config, 'naive(k=0)', 'O(n)')
    attach_model(execution_times, config, 'fast(k=0)', 'O(log n)')
    print(report(execution_times, config['span'], logx=True, style=['-ro', '-gs', ':r^', ':gv']))