import random
import itertools
from collections import deque

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

def generate_random_neighbor(S, current_solution):
    neighbor_solution = current_solution[:]
    index = random.randint(0, len(S) - 1)
    neighbor_solution[index] = not neighbor_solution[index]
    return neighbor_solution

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

        if current_value == 0:
            return swap_bool_with_numbers(S, current_solution), current_value

        neighbors = generate_neighborhood(S, current_solution)
        best_neighbor = None
        best_neighbor_value = float('inf')

        for neighbor in neighbors:
            neighbor_value = objective_function(S, T, neighbor)
            if neighbor_value < best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value

        if best_neighbor is not None and best_neighbor_value < current_value:
            current_solution = best_neighbor
            current_value = best_neighbor_value
        else:
            break

    return swap_bool_with_numbers(S, current_solution), current_value

#########################################################################################################
# Algorytmy wspinaczkowy losowy
#########################################################################################################
def hill_climbing_random(S, T, max_iterations):
    current_solution = generate_random_solution(S)
    current_value = objective_function(S, T, current_solution)
    
    for iteration in range(max_iterations):
        print(f'Iteration: {iteration + 1}')

        if current_value == 0:
            return swap_bool_with_numbers(S, current_solution), current_value

        neighbor = generate_random_neighbor(S, current_solution)
        neighbor_value = objective_function(S, T, neighbor)
        if neighbor_value < current_value:
            current_solution = neighbor
            current_value = neighbor_value
    
    return swap_bool_with_numbers(S, current_solution), current_value

#########################################################################################################
# Algorytm tabu
#########################################################################################################
def subset_sum_tabu(S, T, tabu_size, max_iterations):
    tabu_list = deque(maxlen=tabu_size)

    current_solution = generate_random_solution(S)
    current_value  = objective_function(S, T, current_solution)

    best_solution = current_solution[:]
    best_value = current_value
    
    tabu_list.append(current_solution)

    for iteration in range(max_iterations):
        print(f'Iteration: {iteration+1}')

        neighbors = generate_neighborhood(S, current_solution)
        best_neighbor = None
        best_neighbor_value = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_value = objective_function(S, T, neighbor)
                if neighbor_value < best_neighbor_value:
                    best_neighbor = neighbor
                    best_neighbor_value = neighbor_value
        
        if best_neighbor is not None:
            current_solution = best_neighbor
            current_value = best_neighbor_value

            if current_value < best_value:
                best_solution = current_solution[:]
                best_value = current_value

            tabu_list.append(current_solution[:])
        else:
            if len(tabu_list) > 1:
                tabu_list.pop()
                current_solution = tabu_list[-1]
                current_value = objective_function(S, T, current_solution)

        if best_value == 0:
            break

    return swap_bool_with_numbers(S, best_solution), best_value

#########################################################################################################
# Algorytm genetyczny
#########################################################################################################
def crossover_one_point(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def crossover_two_point(parent1, parent2):
    point1 = random.randint(1, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

def mutation_flip_bit(solution):
    point = random.randint(0, len(solution) - 1)
    solution[point] = not solution[point]
    return solution

def mutation_swap_bits(solution):
    point1, point2 = random.sample(range(len(solution)), 2)
    solution[point1], solution[point2] = solution[point2], solution[point1]
    return solution

def select_parents(population, fitness, num_parents):
    parents = random.choices(population, weights=fitness, k=num_parents)
    return parents

def genetic_algorithm(S, T, pop_size, max_iterations, crossover_method, mutation_method, termination_condition):
    population = [generate_random_solution(S) for _ in range(pop_size)]
    fitness = [1 / (1 + objective_function(S, T, sol)) for sol in population]
    
    for iteration in range(max_iterations):
        print(f'Generation: {iteration + 1}')
        
        parents = select_parents(population, fitness, pop_size)
        
        next_population = []
        for i in range(0, pop_size, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1] if i + 1 < pop_size else parents[0]
            
            if crossover_method == 'one_point':
                child1, child2 = crossover_one_point(parent1, parent2)
            elif crossover_method == 'two_point':
                child1, child2 = crossover_two_point(parent1, parent2)
            else:
                raise ValueError
            
            if mutation_method == 'flip_bit':
                child1 = mutation_flip_bit(child1)
                child2 = mutation_flip_bit(child2)
            elif mutation_method == 'swap_bits':
                child1 = mutation_swap_bits(child1)
                child2 = mutation_swap_bits(child2)
            else:
                raise ValueError
            
            next_population.extend([child1, child2])
        
        population = next_population
        fitness = [1 / (1 + objective_function(S, T, sol)) for sol in population]
    
        if termination_condition == 'fixed_generations':
            if iteration + 1 >= max_iterations:
                break
        elif termination_condition == 'optimal_solution':
            if 0 in [objective_function(S, T, sol) for sol in population]:
                best_solution = min(population, key=lambda sol: objective_function(S, T, sol))
                best_value = objective_function(S, T, best_solution)
                return swap_bool_with_numbers(S, best_solution), best_value
