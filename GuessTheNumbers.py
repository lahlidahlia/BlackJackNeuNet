import Genetics
import random

""" This program use a genetic algorithm in order to guess a set of number efficiently """

def get_fitness_score(subject, goal):
    """
    In this case, subject and goal is a list of 5 numbers.
    Return a score that is the total difference between the subject and the goal.
    """
    total = 0
    for i in range(len(subject)):
        total += abs(goal[i] - subject[i])
    return total

def score_all(subject_list, goal):
    """
    Subject_list can either be a normal list or a tuple list.
    Return a dictionary of each subject as a tuple list paired up with its score.
    """
    if type(subject_list[0]) is list:
        subject_list = tuple(tuple(subject) for subject in subject_list)   

    ret = {}
    for subject in subject_list:
        ret[subject] = 1/float(get_fitness_score(subject, goal)+1) * 10000
        # ret[subject] = float(get_fitness_score(subject, goal)) 
        
    return ret

def find_average_score(generation):
    """
    Generation is a dictionary with the subjects and score.
    Returns the average score of that generation
    """
    sum = 0
    for score in generation.values():
        sum += score
    return sum/len(generation.values())

POPULATION = 50
AMOUNT_OF_NUMBERS = 5
gen = Genetics.Genetics(crossover_chance=0.3, individual_crossover_chance=0.3, mutation_chance=1, mutation_range_flat=0.1, mutation_range_percent=0, elite_amount=1)
goal = [random.randrange(1000) for _ in range(AMOUNT_OF_NUMBERS)]

first_generation = score_all([[random.randrange(1000) for _ in range(AMOUNT_OF_NUMBERS)] for _ in range(POPULATION)], goal)
next_generation = score_all(gen.generate_generation(first_generation, POPULATION), goal)
print find_average_score(first_generation)
print find_average_score(next_generation)
count = 0
last_gen_best = 0
while True:
    gen_best = gen.generate_generation(next_generation, POPULATION)
    print gen_best[0]
    if gen_best[0] != last_gen_best:
        for _ in range(100):
            print("DETHRONED!")
        last_gen_best = gen_best[0]
    next_generation = score_all(gen_best, goal)
    print find_average_score(next_generation)
    count += 1
    # if count > 1000:
    #     break