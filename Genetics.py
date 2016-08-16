import random

class Genetics:
    def __init__(self, crossover_chance=0.85, individual_crossover_chance=0.3, mutation_chance=0.1, mutation_range_flat=0.1,
                 mutation_range_percent=0.1, elite_amount=0):
        self.crossover_chance = crossover_chance  # Chance for crossover to trigger.
        self.individual_crossover_chance = individual_crossover_chance # If crossover is triggered, chance for individual chromosome value to exchange between two parents.
        self.mutation_chance = mutation_chance  # Chance for each chrom_value to mutate.
        self.mutation_range_flat = mutation_range_flat  # The value will be added or subtracted by this amount.
        self.mutation_range_percent = mutation_range_percent  # The value will be added or subtracted by a chrom_value*randrange(MUTATION_RANGE) amount.
        self.elite_amount = elite_amount  # The amount of best chromosomes that will be carried toward the next generation.


    def select_chrom(self, chrom_dict):
        """
        Select a chromosome using roulette wheel algorithm. 
        chrom_dict: dictionary that follows the format {chromosome : score, ...}, with chromosome being a tuple list of weights.
        Returns the selected chromosome.
        """
    
        # Sum fitness score together.
        sum_fitness = 0
        for score in chrom_dict.values():
            sum_fitness += score

        # Roulette wheel selection algorithm
        r = random.uniform(0, sum_fitness)
        s = 0
        for chrom, score in chrom_dict.iteritems():
            s += score
            if s > r:
                return chrom
            
    def crossover(self, parent_1, parent_2):
        """
        Perform a chromosome cross over between two parents and produce two offsprings.
        Has a CROSSOVER_CHANCE of running successfully. If not successful, simply return the parents.
        The crossover method is uniform crossover
        
        parents: chromosomes in a form of a list that follows the format of [value, ...]. Both parents must have the same lengths.
        returns either the parents or crossovered siblings.        
        """
        
        if random.random() > self.crossover_chance:
            # Failure
            return (parent_1, parent_2)
        
        # Success, iterate through the chromosomes and randomly swap them.
        for i in range(len(parent_1)):
            if random.random() > self.individual_crossover_chance:
                # Failure, continue to next value.
                continue
            # Success, swap the values.
            temp = parent_1[i]
            parent_1[i] = parent_2[i]
            parent_2[i] = temp
            
        return (parent_1, parent_2)
            
    def mutate(self, chrom):
        """
        For each chromosome value, have a chance to mutate by MUTATION_RANGE percent.
        For example if the range is 0.05 (5%) and the value is 100, then the final will be random between 95 and 105.
        
        chrom: A chromosome in the format of a list that has the structure of [value, ...].
        Returns the mutated chromosome.
        """
    
        for i in range(len(chrom)):
            if random.random() > self.mutation_chance:
                # Failure, continue to the next value.
                continue
            # Success, mutate the value by a small amount
            chrom[i] += random.uniform(-self.mutation_range_flat, self.mutation_range_flat)
            chrom[i] = random.uniform(chrom[i] - chrom[i]*self.mutation_range_percent, chrom[i] + chrom[i]*self.mutation_range_percent)
        return chrom
    
    def choose_elites(self, chrom_dict):
        """
        Return a predefined amount of chromsoomes with the best score in the generation.
        
        chrom_dict: a dictionary that has the format of {chromosome : fitness_score, ...}, where chromosome is a tuple list.
        Returns a tuple list of the elite chromosomes.
        """
        if self.elite_amount == 0:
            return ()  # That's an empty tuple, folks.
        
        # Check if dictionary is large enough for specified elite amount. If not, return all the chromosomes.
        if len(chrom_dict) <= self.elite_amount:
            return tuple(chrom_dict.keys())
        
        # Get a list of sorted chromosome from best performing to worst.
        sorted_chrom = sorted(chrom_dict, key=chrom_dict.get, reverse=True)
        # Grab the top elite_amount chromosomes and return it.
        elites = [sorted_chrom[x] for x in range(self.elite_amount)]
        return tuple(elites)
    
    
    def generate_generation(self, chrom_dict, population):
        """
        Create a new generation using a dictionary previous generation's chromosomes that also contains their fitness scores.
        Population must be higher than elite amount, otherwise an error is raised.
        
        chrom_dict: a dictionary that has the format of {chromosome : fitness_score, ...}, where chromosome is a tuple list.
        population: the population of the returned next generation.
        Returns a tuple list of the new generation's chromosome.
        """
        if population < self.elite_amount:
            raise Exception("Population must be higher than elite_amount")
        
        population_ls = []
        population_ls.extend(self.choose_elites(chrom_dict))
        population -= self.elite_amount
        for _ in range(0, population, 2):
            parent_1 = self.select_chrom(chrom_dict)
            parent_2 = self.select_chrom(chrom_dict)
            sibling_1, sibling_2 = self.crossover(list(parent_1), list(parent_2))
            sibling_1 = self.mutate(sibling_1)
            sibling_2 = self.mutate(sibling_2)
            population_ls.append(tuple(sibling_1))
            population_ls.append(tuple(sibling_2))
        if population % 2 != 0:
            # If population is an odd number then remove one chromosome from the pool because the above loop will always output an even number.
            population_ls.pop()
        assert len(population_ls) == population + self.elite_amount
        return tuple(population_ls)

if __name__ == "__main__":
    gen = Genetics(crossover_chance=0.85, individual_crossover_chance=0.3, mutation_chance=0.1, mutation_range_flat=0.1, mutation_range_percent=0.1)
    
    # # Overall Test
    # chrom_dict = {(1,1,1,1,1) : 10, (0,0,0,0,0) : 10}
    # sibling_ls = gen.generate_generation(chrom_dict, 10)
    # print sibling_ls
    
    # # select_chrom
    # d = {1:1, 2:1, 3:1}
    # ls = []
    # for _ in range(10000):
    #     ls.append(gen.select_chrom(d))
    #   # Generally want these numbers really close to each other.
    # print ls.count(1)
    # print ls.count(2)
    # print ls.count(3)
    
    # # Crossover
    # chrom1 = [1,1,1,1,1]
    # chrom2 = [2,2,2,2,2]
    # print gen.crossover(chrom1, chrom2)
    
    # # Mutate
    # chrom1 = [0.1,1,10.5,50,100]
    # print gen.mutate(chrom1)
    
    # # choose_elites
    # gen = Genetics(elite_amount=2)
    # d = {2:2, 1:1, 4:4, 3:3, 5:5}
    # print gen.choose_elites(d) == (5,4)
    # gen = Genetics(elite_amount=6)
    # print gen.choose_elites(d) == tuple(d.keys())
    # gen = Genetics(elite_amount=2)
    # d = {(1,1):1, (2,2):2, (3,3):3, (4,4):4, (5,5):5}
    # next_gen = gen.generate_generation(d, 10)
    # print next_gen[0] == (5,5) and next_gen[1] == (4,4)
    
    
