
import random

# ==========================================
# 1. INITIALIZATION
# ==========================================

# Initial number of vehicles on each road
traffic = {
    "North": 50,
    "South": 30,
    "East": 80,
    "West": 20
}

roads = list(traffic.keys())

TOTAL_TIME = 120
MIN_GREEN = 10
MAX_GREEN = 60

POPULATION_SIZE = 30
GENERATIONS = 50
MUTATION_RATE = 0.20
CROSSOVER_RATE = 0.80

# Vehicles that can pass per second of green signal
SERVICE_RATE = 0.5


# ==========================================
# 2. CREATE INITIAL POPULATION
# ==========================================

def create_individual():

    timings = [MIN_GREEN] * 4
    remaining = TOTAL_TIME - sum(timings)

    while remaining > 0:
        i = random.randint(0, 3)

        if timings[i] < MAX_GREEN:
            timings[i] += 1
            remaining -= 1

    return timings


def create_population():

    return [
        create_individual()
        for _ in range(POPULATION_SIZE)
    ]


# ==========================================
# 3. TRAFFIC SIMULATION
# ==========================================

def simulate_traffic(individual):

    cars_left = {}

    for i, road in enumerate(roads):

        green_time = individual[i]

        vehicles = traffic[road]

        # Calculate vehicles that can pass
        vehicles_passed = int(
            green_time * SERVICE_RATE
        )

        # Calculate remaining vehicles
        remaining = max(
            0, vehicles - vehicles_passed
        )

        cars_left[road] = remaining

    return cars_left


# ==========================================
# 4. FITNESS EVALUATION
# ==========================================

def fitness(individual):

    result = simulate_traffic(individual)

    total_cars_left = sum(result.values())

    # Fewer remaining vehicles = Higher fitness
    return 1000 / (total_cars_left + 1)


# ==========================================
# 5. SELECTION
# ==========================================

def selection(population):

    # Select the best 30% of the population
    ranked = sorted(
        population,
        key=fitness,
        reverse=True
    )

    parent_pool = ranked[:max(2, int(
        POPULATION_SIZE * 0.30
    ))]

    return random.choice(parent_pool)


# ==========================================
# 6. REPAIR TIMINGS
# ==========================================

def repair(child):

    # Ensure minimum and maximum limits
    child = [
        max(MIN_GREEN, min(MAX_GREEN, int(x)))
        for x in child
    ]

    # Adjust timings to maintain 120 seconds
    while sum(child) != TOTAL_TIME:

        if sum(child) < TOTAL_TIME:

            possible = [
                i for i in range(4)
                if child[i] < MAX_GREEN
            ]

            if not possible:
                break

            child[random.choice(possible)] += 1

        else:

            possible = [
                i for i in range(4)
                if child[i] > MIN_GREEN
            ]

            if not possible:
                break

            child[random.choice(possible)] -= 1

    return child


# ==========================================
# 7. CROSSOVER
# ==========================================

def crossover(parent1, parent2):

    if random.random() < CROSSOVER_RATE:

        point = random.randint(1, 3)

        child = (
            parent1[:point] +
            parent2[point:]
        )

        return repair(child)

    return parent1[:]


# ==========================================
# 8. MUTATION
# ==========================================

def mutation(individual):

    if random.random() < MUTATION_RATE:

        # Select two different roads
        i, j = random.sample(range(4), 2)

        # Transfer a few seconds between roads
        amount = random.randint(1, 5)

        if (
            individual[i] - amount >= MIN_GREEN
            and individual[j] + amount <= MAX_GREEN
        ):

            individual[i] -= amount
            individual[j] += amount

        elif (
            individual[j] - amount >= MIN_GREEN
            and individual[i] + amount <= MAX_GREEN
        ):

            individual[j] -= amount
            individual[i] += amount

    return individual


# ==========================================
# 9. GENETIC ALGORITHM
# ==========================================

def genetic_algorithm():

    population = create_population()

    best_solution = None
    best_fitness = 0

    print("SMART TRAFFIC SIGNAL OPTIMIZATION")
    print("----------------------------------")

    for generation in range(GENERATIONS):

        # Evaluate population
        ranked = sorted(
            population,
            key=fitness,
            reverse=True
        )

        current_best = ranked[0]
        current_fitness = fitness(current_best)

        if current_fitness > best_fitness:

            best_fitness = current_fitness
            best_solution = current_best[:]

        print(
            f"Generation {generation + 1}: "
            f"Best Fitness = {best_fitness:.2f}"
        )

        # Keep the best individual (Elitism)
        next_population = [best_solution[:]]

        # Generate next generation
        while len(next_population) < POPULATION_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)

            child = mutation(child)

            next_population.append(child)

        population = next_population

    # ======================================
    # 10. FINAL RESULT
    # ======================================

    print("\n========== OPTIMIZED RESULTS ==========")

    final_result = simulate_traffic(best_solution)

    total_remaining = 0

    for i, road in enumerate(roads):

        print(
            f"{road:6} | "
            f"Vehicles: {traffic[road]:3} | "
            f"Green Time: {best_solution[i]:3} sec | "
            f"Cars Left: {final_result[road]:3}"
        )

        total_remaining += final_result[road]

    print("--------------------------------------")
    print("Total Cycle Time:", sum(best_solution), "seconds")
    print("Total Cars Remaining:", total_remaining)
    print("Best Fitness:", round(best_fitness, 2))

    print("\nOptimization Completed!")


# Run the Genetic Algorithm
random.seed(42)
genetic_algorithm()
