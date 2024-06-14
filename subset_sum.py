import random
import itertools

#########################################################################################################
# General utilities
#########################################################################################################
def generate_random_solution(numbers):
    return [random.choice([True, False]) for _ in numbers]

def objective_function(S, T, subset):
    subset_sum = sum(S[i] for i in range(len(S)) if subset[i])
    return abs(T - subset_sum)

def generate_neighborhood(S, current_solution):
    neighbors = []
    for i in range(len(S)):
        neighbor_solution = current_solution[:]
        neighbor_solution[i] = not neighbor_solution[i]
        neighbors.append(neighbor_solution)
    return neighbors

def swap_bool_with_numbers(S, current_solution):
    return [S[i] for i in range(len(S)) if current_solution[i]]

#########################################################################################################
# Algorytm brute force
#########################################################################################################
def brute_force(S, T):
    n = len(S)
    best_subset = None
    best_subset_sum = float('inf')
    
    for subset_size in range(1, n + 1):
        for subset in itertools.combinations(S, subset_size):
            subset_sum = sum(subset)
            if subset_sum == T:
                return subset
            elif abs(T - subset_sum) < best_subset_sum:
                best_subset = list(subset)
                best_subset_sum = abs(T - subset_sum)
    
    return best_subset

#########################################################################################################
# Algorytmy wspinaczkowy klasyczny
#########################################################################################################
def hill_climbing_classic(S, T, max_iterations):
    current_solution = generate_random_solution(S)
    current_value = objective_function(S, T, current_solution)
    
    for iteration in range(max_iterations):
        print(f'Iteration: {iteration + 1}')
        neighbors = generate_neighborhood(S, current_solution)
        
        best_neighbor = None
        best_value = current_value
        for neighbor in neighbors:
            neighbor_value = objective_function(S, T, neighbor)
            if neighbor_value < best_value:
                best_value = neighbor_value
                best_neighbor = neighbor
        
        if best_neighbor is None:
            break
        
        current_solution = best_neighbor
        current_value = best_value
    
    best_subset = swap_bool_with_numbers(S, current_solution)
    best_value = objective_function(S, T, current_solution)
    
    return best_subset, T - best_value
