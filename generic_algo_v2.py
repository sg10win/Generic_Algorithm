import random


# What are the x, y, z that will give us 2223
def target_function(x, y, z):
    return 34 * x ** 5 + 12 * y ** 7 + 90 * z ** 2 - 2223


# fitness function
def fitness(x, y, z):
    ans = target_function(x, y, z)
    if ans == 0:
        return 9999999
    else:
        return abs(1 / ans)


# Randomly combine elements from two parents to form a new solution
def crossover(parent1, parent2):
    child_x = random.choice([parent1[0], parent2[0]])
    child_y = random.choice([parent1[1], parent2[1]])
    child_z = random.choice([parent1[2], parent2[2]])
    return child_x, child_y, child_z


if __name__ == '__main__':

    population_size = 1000
    max_generations = 10000
    solution_fitness_break = 99999

    solutions = []
    for s in range(population_size):
        first_x = random.uniform(0, 100)
        first_y = random.uniform(0, 100)
        first_z = random.uniform(0, 100)
        solutions.append((first_x, first_y, first_z))

    for i in range(max_generations):
        ranked_solutions = []
        for s in solutions:
            ranked_solutions.append((fitness(s[0], s[1], s[2]), s))
        ranked_solutions.sort(reverse=True)
        if i % 10 == 0:
            print(f"################ Gen {i} best solution ##################")
            print(ranked_solutions[0])
            diff_from_solution = target_function(ranked_solutions[0][1][0], ranked_solutions[0][1][1],
                                                 ranked_solutions[0][1][2])
            print(f'''DELTA FROM OBJECTIVE = {format(diff_from_solution, '.20f')}''')

        # Stop condition
        if ranked_solutions[0][0] > solution_fitness_break:
            diff_from_solution = target_function(ranked_solutions[0][1][0], ranked_solutions[0][1][1], ranked_solutions[0][1][2])
            print(f'''DELTA FROM OBJECTIVE = {format(diff_from_solution, '.20f')}''')
            break

        # Keep the top 10 solutions without a change
        best_solutions = [s[1] for s in ranked_solutions[:10]]

        # Use the top 100 solutions to create the next generation
        best_solutions_for_breeding = [s[1] for s in ranked_solutions[:100]]

        # Generate the new population
        new_gen = best_solutions[:]  # Start with the elites

        # Mutation
        mutation_range = 1.0 / (i + 1)

        while len(new_gen) < population_size:
            # Randomly selects two parents from the best solutions
            parent1 = random.choice(best_solutions_for_breeding)
            parent2 = random.choice(best_solutions_for_breeding)

            # Crossover to create a child
            child = crossover(parent1, parent2)

            # Mutation
            mutated_child = (
                child[0] + random.uniform(-mutation_range, mutation_range),
                child[1] + random.uniform(-mutation_range, mutation_range),
                child[2] + random.uniform(-mutation_range, mutation_range)
            )

            new_gen.append(mutated_child)

        solutions = new_gen

