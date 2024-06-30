import time
import matplotlib.pyplot as plt
from subset_sum import *

def clear_output_file():
    with open("output_file", 'w') as file:
        file.write("")

def run_experiment(S, T, max_iterations, tabu_size):
    clear_output_file()
    results = {}
    times = {}
    histories = {}
    best_params = {
        'Hill Climbing Classic': (None, None),
        'Hill Climbing Random': (None, None),
        'Tabu Search': (None, None)
    }
    best_results = {
        'Hill Climbing Classic': (None, float('inf')),
        'Hill Climbing Random': (None, float('inf')),
        'Tabu Search': (None, float('inf'))
    }
    best_time = {
        'Hill Climbing Classic': float('inf'),
        'Hill Climbing Random': float('inf'),
        'Tabu Search': float('inf')
    }
    best_convergence = {
        'Hill Climbing Classic': None,
        'Hill Climbing Random': None,
        'Tabu Search': None
    }

    # Hill Climbing Classic
    start_time_hc = time.time()
    solution, value, history = hill_climbing_classic(S, T, max_iterations)
    end_time_hc = time.time()
    exec_time_hc = end_time_hc - start_time_hc
    times['Hill Climbing Classic'] = exec_time_hc
    histories['Hill Climbing Classic'] = history
    if exec_time_hc < best_time['Hill Climbing Classic']:
        best_time['Hill Climbing Classic'] = exec_time_hc
        best_params['Hill Climbing Classic'] = (max_iterations, tabu_size)
        best_results['Hill Climbing Classic'] = (solution, value)
        best_convergence['Hill Climbing Classic'] = history

    # Hill Climbing Random
    start_time_hr = time.time()
    solution, value, history = hill_climbing_random(S, T, max_iterations)
    end_time_hr = time.time()
    exec_time_hr = end_time_hr - start_time_hr
    times['Hill Climbing Random'] = exec_time_hr
    histories['Hill Climbing Random'] = history
    if exec_time_hr < best_time['Hill Climbing Random']:
        best_time['Hill Climbing Random'] = exec_time_hr
        best_params['Hill Climbing Random'] = (max_iterations, tabu_size)
        best_results['Hill Climbing Random'] = (solution, value)
        best_convergence['Hill Climbing Random'] = history

    # Tabu
    start_time_ts = time.time()
    solution, value, history = subset_sum_tabu(S, T, tabu_size, max_iterations)
    end_time_ts = time.time()
    exec_time_ts = end_time_ts - start_time_ts
    times['Tabu Search'] = exec_time_ts
    histories['Tabu Search'] = history
    if exec_time_ts < best_time['Tabu Search']:
        best_time['Tabu Search'] = exec_time_ts
        best_params['Tabu Search'] = (max_iterations, tabu_size)
        best_results['Tabu Search'] = (solution, value)
        best_convergence['Tabu Search'] = history

    solution = True

    return solution, times, histories, best_params, best_results, best_time, best_convergence

def plot_convergence(best_convergence):
    plt.figure(figsize=(10, 6))
    
    for method, history in best_convergence.items():
        if history is not None:
            plt.plot(history, label=method)
    
    plt.title('Convergence Plot')
    plt.xlabel('Iteration')
    plt.ylabel('Objective Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()