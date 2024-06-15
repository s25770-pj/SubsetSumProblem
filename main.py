#!/usr/bin/env python
import sys
from subset_sum import *

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Użycie: python main.py <plik_z_liczbami> <algorytm> <szukana_suma> [opcje]")
        print("Dostępne algorytmy: random, brute_force, hill_climbing_classic, hill_climbing_random, subset_sum_tabu, genetic_algorithm")
        sys.exit(1)

    input_file = sys.argv[1]
    algorithm  = sys.argv[2]
    target_sum = int(sys.argv[3])

    tabu_size = 10
    population_size = 10
    mutation_rate = 0.01
    max_iterations = 1000

    crossover_method = 'one_point'
    mutation_method = 'flip_bit'
    termination_method = 'optimal_solution'

    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == "-population":
            try:
                population_size = int(sys.argv[i + 1])
                i += 2
            except (IndexError, ValueError):
                print("Nieprawidłowy argument dla -population")
                sys.exit(1)
        elif sys.argv[i] == "-mutation_rate":
            try:
                mutation_rate = float(sys.argv[i + 1])
                i += 2
            except (IndexError, ValueError):
                print("Nieprawidłowy argument dla -mutation_rate")
                sys.exit(1)
        elif sys.argv[i] == "-iter":
            try:
                max_iterations = int(sys.argv[i + 1])
                i += 2
            except (IndexError, ValueError):
                print("Nieprawidłowy argument dla -iter")
                sys.exit(1)
        elif sys.argv[i] == "-tabu_size":
            try:
                tabu_size = int(sys.argv[i + 1])
                i += 2
            except (IndexError, ValueError):
                print("Nieprawidłowy argument dla -tabu_size")
                sys.exit(1)
        elif sys.argv[i] == "-crossover_method":
            try:
                crossover_method = sys.argv[i + 1]
                i += 2
            except IndexError:
                print("Nieprawidłowy argument dla -crossover_method")
                sys.exit(1)
        elif sys.argv[i] == "-mutation_method":
            try:
                mutation_method = sys.argv[i + 1]
                i += 2
            except IndexError:
                print("Nieprawidłowy argument dla -mutation_method")
                sys.exit(1)
        elif sys.argv[i] == "-termination_method":
            try:
                termination_method = sys.argv[i + 1]
                i += 2
            except IndexError:
                print("Nieprawidłowy argument dla -termination_method")
                sys.exit(1)
        else:
            print("Nieznana opcja:", sys.argv[i])
            sys.exit(1)

    with open(input_file, 'r') as file:
        numbers = [int(line.strip()) for line in file]

    if algorithm == "random":
        solution = generate_random_solution(numbers)
    elif algorithm == "brute_force":
        solution = brute_force(numbers, target_sum)
    elif algorithm == "hill_climbing_classic":
        solution = hill_climbing_classic(numbers, target_sum, max_iterations)
    elif algorithm == "hill_climbing_random":
        solution = hill_climbing_random(numbers, target_sum, max_iterations)
    elif algorithm == "subset_sum_tabu":
        solution = subset_sum_tabu(numbers, target_sum, tabu_size, max_iterations)
    elif algorithm == "genetic_algorithm":
        solution = genetic_algorithm(numbers, target_sum, population_size, max_iterations, crossover_method, mutation_method, termination_method)
    else:
        print("Nieznany algorytm:", algorithm)
        sys.exit(1)

    if solution:
        print("Znalezione rozwiązanie:", solution)
        if type(solution) == list:
            print("Suma rozwiązania", sum(solution[0]))
    else:
        print("Nie znaleziono rozwiązania dla szukanej sumy", target_sum)