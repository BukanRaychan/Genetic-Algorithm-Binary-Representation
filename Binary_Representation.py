import math
import random
import os

def initializePopulation():
    population = []
    for _ in range(POPULATION_SIZE):
        chromosome = ""
        for _ in range(CHROMOSOME_LENGTH):
            chromosome += str(random.randint(0,1))
        population.append(chromosome)
    return population

def fitnessCalculation(decoded_population):
    fitness_of_population = []
    a = 0.000000001
    for individual in decoded_population:
        x1 = individual[0]
        x2 = individual[1]
        fitness_of_population.append(-1/(-(math.sin(x1) * - math.cos(x2) + (4/5) * math.exp(1 - (x1**2 + x2 ** 2) ** 0.5)) + a) )
    return fitness_of_population

def windowScaling(fitness_values):
    # Apply linear scaling to each fitness value
    scaled_fitness = [fitness - MIN_FITNESS_VALUE for fitness in fitness_values]
    
    return scaled_fitness

def parentSelection(fitness_of_population, population):

    # Fitness Prortionate Selection (FPS)
    # Stochastic Universal Sampling Algorithm

    pointers = []
    expectation_parent_value = []
    
    fitness_of_population = windowScaling(fitness_of_population) # Window Scaling

    max_fitness = sum(fitness_of_population)    
    spin_value = random.uniform(0,max_fitness)


    #Spin the wheel
    for i in range(1, POPULATION_SIZE + 1):
        pointers.append(((i * max_fitness/4) + spin_value) % max_fitness)
        expectation_parent_value.append(0) 


    #Count how many pointer which point to the each individual in  population
    for i in range(0, POPULATION_SIZE):
        for j in range(0, POPULATION_SIZE):
            if pointers[i] <= sum(fitness_of_population[0:(j + 1)]):
                expectation_parent_value[j] += 1
                break
    sorted_expectation_parent_value = sorted(expectation_parent_value)

    return(population[expectation_parent_value.index(sorted_expectation_parent_value[-1])] , population[expectation_parent_value.index(sorted_expectation_parent_value[-2])])

def decodeChromosomeToIndividual(population):
    alpha = 0.0
    beta_x1 = 0.0
    beta_x2 = 0.0

    decoded_population = []
    for chromosome in population:
        for i in range(CHROMOSOME_LENGTH // 2):
            alpha += 2**(-(i + 1))
            beta_x1 += int(chromosome[i]) * 2**(-(i + 1))
            beta_x2 += int(chromosome[i + CHROMOSOME_LENGTH//2 - 1]) * 2**(-(i + 1))
        decoded_population.append((LOWER_LIMIT + (UPPER_LIMIT - LOWER_LIMIT) / alpha * beta_x1, LOWER_LIMIT + (UPPER_LIMIT - LOWER_LIMIT) / alpha * beta_x2))
    
    return decoded_population

def recombination(parent1,parent2):
    
    #Uniform Crossover

    child1 = ""
    child2 = ""
    
    for i in range(CHROMOSOME_LENGTH):
        if random.uniform(0,1) < POSSIBLE_COMBINATION:
            child1 += parent1[i]
            child2 += parent2[i]
        else:
            child1 += parent2[i]
            child2 += parent1[i]
    
    return child1, child2

def mutation(child1, child2):

    # Mutasi Biner

    mutated_child_list = [list(child1), list(child2)] # Convert the strings to lists

    for iter_child in range(2):
        for iter_gen in range(CHROMOSOME_LENGTH):
            if random.uniform(0, 1) < POSSIBLE_MUTATION:
                # Flip the bit: 0 to 1 or 1 to 0
                mutated_child_list[iter_child][iter_gen] = str(int(mutated_child_list[iter_child][iter_gen]) ^ 1)

    # Convert the lists back to strings
    mutated_child1 = ''.join(mutated_child_list[0])
    mutated_child2 = ''.join(mutated_child_list[1])

    return mutated_child1, mutated_child2          

def exchangePopulation(population, fitness_of_population, child1, child2):

    #Steady State Model

    new_population = population
    new_generation = [child1, child2]
    fitness_of_new_generation = fitnessCalculation(decodeChromosomeToIndividual(new_generation))
    sorted_2_worst_fitness_of_old_generation = sorted(fitness_of_population)[0:2]

    for i in range(2):
        for j in range(2):
            if fitness_of_new_generation[i] > sorted_2_worst_fitness_of_old_generation[j]:
                new_population[fitness_of_population.index(sorted_2_worst_fitness_of_old_generation[j])] = new_generation[i]
                fitness_of_population[fitness_of_population.index(sorted_2_worst_fitness_of_old_generation[j])] = fitness_of_new_generation[i]
                sorted_2_worst_fitness_of_old_generation[j] = fitness_of_new_generation[i]
                sorted_2_worst_fitness_of_old_generation.sort()
                break

    return new_population

def main():
    global LOWER_LIMIT, UPPER_LIMIT, POPULATION_SIZE, CHROMOSOME_LENGTH, POSSIBLE_MUTATION, POSSIBLE_COMBINATION,  MIN_FITNESS_VALUE
    LOWER_LIMIT = -10
    UPPER_LIMIT = 10
    POPULATION_SIZE = 100
    CHROMOSOME_LENGTH = 50
    POSSIBLE_MUTATION = 1 / (POPULATION_SIZE * CHROMOSOME_LENGTH)
    POSSIBLE_COMBINATION =  0.6
    MIN_FITNESS_VALUE = 1.97

    limitation_of_change = 1000
    change_credit = 0
    generation = 0
    best_fitness = float('-inf')
    best_individual = ""

    population = initializePopulation()

    while change_credit <= limitation_of_change:
        # print(f'population: {population}\n')
        # Decode Cromosom to individual
        decoded_population = decodeChromosomeToIndividual(population)
        # print(f'decoded_population: {decoded_population}\n')
        
        # Fitness Calculation
        fitness_of_population = fitnessCalculation(decoded_population)
        # print(f'fitness_of_population: {fitness_of_population}\n')

        # Parent Selection
        parent1, parent2 = parentSelection(fitness_of_population, population)
        # print(f'parent1, parent2: {parent1, parent2}\n')

        # Recombination
        child1, child2 = recombination(parent1,parent2)
        # print(f'child1, child2: {child1, child2}\n')
        
        # permutation
        mutated_child1, mutated_child2 = mutation(child1, child2)
        # print(f'mutated_child1, mutated_child2: {mutated_child1, mutated_child2}\n')

        #Exchange Population
        population = exchangePopulation(population, fitness_of_population, mutated_child1, mutated_child2)
        # print(f'population: {population}\n')

        MIN_FITNESS_VALUE = min(fitness_of_population)

        if max(fitnessCalculation(decodeChromosomeToIndividual(population))) > best_fitness:
            best_fitness = max(fitnessCalculation(decodeChromosomeToIndividual(population)))
            best_individual = population[fitness_of_population.index(max(fitness_of_population))]
            change_credit = 0

        os.system("cls")
        
        print(f'Generation : {generation}\n')
        print(f'BEST INDIVIDUAL')
        print(f'x1 : {best_individual[:CHROMOSOME_LENGTH//2]}')
        print(f'x2 : {best_individual[CHROMOSOME_LENGTH//2:]}\n')
        print(f'BEST FITNESS: {best_fitness}\n')

        

        change_credit += 1
        generation += 1
    
    print("Finished")

main()

