import random
import time

def initial_population(pop_size, target_length):
	population = []
	for i in range(pop_size):
		string = []
		for j in range(target_length):
			string.append(chr(random.randint(32, 126)))
		population.append(string)
	return(population)

def main():
	pop_size = 200
	#target = "Two households, both alike in dignity, In fair Verona, where we lay our scene, From ancient grudge break to new mutiny, Where civil blood makes civil hands unclean.From forth the fatal loins of these two foes. A pair of star-cross'd lovers take their life; Whose misadventured piteous overthrows. Do with their death bury their parents' strife. The fearful passage of their death-mark'd love, And the continuance of their parents' rage, Which, but their children's end, nought could remove, Is now the two hours' traffic of our stage; The which if you with patient ears attend, What here shall miss, our toil shall strive to mend."
	target = 'cats and dogs and other things to make this longer'
	#target = 'cats and dogs and other things to make this longer and try and break it'
	mutation_rate = 1/len(target)
	#mutation_rate = 0.01
	power = len(target)
	#power = 10

	target_length = len(target)
	population = initial_population(pop_size, target_length)
	#print(population)
	generation_count = 0
	current_best = None
	current_best_fitness = 0
	while(True):
		fitness, fitness_without_power = fitness_calc(population, target, power)

		if ''.join(population[fitness.index(max(fitness))]) == target:
			#print('success, we found {}'.format(population[fitness.index(max(fitness))]))
			break

		normalised_fitness = normalise_fitness(fitness)
		population = crossover(population, target, normalised_fitness)
		#print('population pre mutate {}'.format(population))
		population = mutate(population, target, mutation_rate)

		#mutation_rate = 1/(sum(fitness_without_power)/pop_size*len(target))
		#print(mutation_rate)
		#time.sleep(1)

		#print('mutation_rate is {}'.format(mutation_rate))
		#for i in range(len(population)):
			#print(''.join(population[i]))

		if max(fitness)>current_best_fitness:
			current_best_fitness = max(fitness)
			current_best = ''.join(population[fitness.index(max(fitness))])
			print('We are at generation {}, the current best is {}'.format(generation_count, current_best))
		#print('We are at generation {}, the current best is {}'.format(generation_count, current_best))
		#print('population post mutate {}'.format(population))
		#print('We are at generation {}, our current population is {}'. format(generation_count, population))
		generation_count += 1
	return(generation_count)

def mutate(population, target, mutation_rate):
	new_population = []
	target_length = len(target)
	for i in range(len(population)):
		new_DNA = []
		for j in range(target_length):
			seed = random.random()
			if seed < mutation_rate:
				new_DNA.append(chr(random.randint(32, 126)))
			else:
				new_DNA.append(population[i][j])
		new_population.append(new_DNA)
	return(new_population)


def crossover(population, target, normalised_fitness):
	target_length = len(target)
	new_population = []
	for i in range(len(population)):
		seed = random.random()
		for j in range(len(normalised_fitness)):
			seed -= normalised_fitness[j]
			if seed < 0:
				DNA_1 = population[j]
				break
		seed = random.random()
		for j in range(len(normalised_fitness)):
			seed -= normalised_fitness[j]
			if seed < 0:
				DNA_2 = population[j]
				break
		new_DNA = []
		element_index = 0
		while(len(new_DNA)<len(target)):
			seed = random.random()
			if seed > 0.5:
				new_DNA.append(DNA_1[element_index])
			else:
				new_DNA.append(DNA_2[element_index])
			element_index += 1
		new_population.append(new_DNA)
	return(new_population)


def normalise_fitness(fitness):
	normalised_fitness = []
	sum_fitness = sum(fitness)
	if sum_fitness == 0:
		sum_fitness = 1
	for i in range(len(fitness)):
		normalised_fitness.append(fitness[i]/sum_fitness)
	return(normalised_fitness)

def fitness_calc(population, target, power):
	fitness = []
	fitness_without_power = []
	target_list = list(target)
	for i in range(len(population)):
		fitness_score = 0
		for j in range(len(target)):
			if population[i][j] == target_list[j]:
				fitness_score += 1
		fitness.append(fitness_score**power)
		fitness_without_power.append(fitness_score)

	if max(fitness) == 0:
		for i in range(len(fitness)):
			fitness[i] = 1

	return(fitness, fitness_without_power)


def test():
	number_of_times = 0
	total_gen_count = 0
	times_to_run = 10
	start_time = time.time()
	while(number_of_times<times_to_run):
		gen = main()
		#print(gen)
		total_gen_count += gen
		number_of_times += 1
		print(gen)
	print('total gen count is {}, this is an average of {} generations, and took {} seconds'.format(total_gen_count, int(total_gen_count/times_to_run), time.time()-start_time))


test()

#main()