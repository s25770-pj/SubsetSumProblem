#!/usr/bin/env python
import sys
from subset_sum import *

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Użycie: python main.py <plik_z_liczbami> <algorytm> <szukana_suma> [opcje]")
        print("Dostępne algorytmy: random, brute_force, hill_climbing_classic")
        sys.exit(1)

    input_file = sys.argv[1]
    algorithm  = sys.argv[2]
    target_sum = int(sys.argv[3])

    max_iterations = 1000

    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == "-iter":
            try:
                max_iterations = int(sys.argv[i + 1])
                i += 2
            except (IndexError, ValueError):
                print("Nieprawidłowy argument dla -iter")
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
    else:
        print("Nieznany algorytm:", algorithm)
        sys.exit(1)

    if solution:
        print("Znalezione rozwiązanie:", solution)
        print("Suma rozwiązania", sum(solution[0]))
    else:
        print("Nie znaleziono rozwiązania dla szukanej sumy", target_sum)