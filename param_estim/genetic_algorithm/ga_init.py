import sys
import numpy as np

from .converter import decode_gene2variable
from .undx_mgg import mgg_alternation
from .converging import converging
from .local_search import local_search
from param_estim.fitness import objective
from param_estim.search_parameter import search_parameter_index
from param_estim.search_parameter import get_search_region

def parameter_estimation(nth_paramset):

    search_idx = search_parameter_index()
    search_region = get_search_region()

    n_generation = 10000
    n_population = int(5*search_region.shape[1])
    n_children = 50
    n_gene = search_region.shape[1]
    allowable_error = 0.5

    (best_indiv,best_fitness) = ga_v2(
        nth_paramset,
        n_generation,
        n_population,
        n_children,
        n_gene,
        allowable_error,
        search_idx,
        search_region
    )


def ga_v1(
    nth_paramset,
    n_generation,
    n_population,
    n_children,
    n_gene,
    allowable_error,
    search_idx,
    search_region
    ):
    population = get_initial_population(n_population,n_gene,search_idx,search_region)
    print('Generation%d: Best Fitness = %e'%(1,population[0,-1]))
    with open('../FitParam/%d/out.txt'%(nth_paramset), mode='w') as f:
            f.write(
                'Generation1: Best Fitness = %e\n'%(population[0,-1])
            )
    best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

    best_fitness = population[0,-1]

    np.save('../FitParam/%d/generation.npy'%(nth_paramset),1)
    np.save('../FitParam/%d/FitParam1'%(nth_paramset),best_indiv)
    np.save('../FitParam/%d/BestFitness.npy'%(nth_paramset),best_fitness)

    if population[0,-1] <= allowable_error:
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
        best_fitness = population[0,-1]
        return best_indiv,best_fitness

    for i in range(1,n_generation):
        population = mgg_alternation(population,n_population,n_children,n_gene,search_idx,search_region)
        print('Generation%d: Best Fitness = %e'%(i+1,population[0,-1]))
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

        if population[0,-1] < best_fitness:
            np.save('../FitParam/%d/generation.npy'%(nth_paramset),i+1)
            np.save('../FitParam/%d/FitParam%d.npy'%(nth_paramset,i+1),best_indiv)
        best_fitness = population[0,-1]
        np.save('../FitParam/%d/BestFitness.npy'%(nth_paramset),best_fitness)

        if population[0,-1] <= allowable_error:
            best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
            best_fitness = population[0,-1]
            return best_indiv,best_fitness

        np.save('../FitParam/%d/count_num.npy'%(nth_paramset),i+1)
        
        with open('../FitParam/%d/out.txt'%(nth_paramset), mode='a') as f:
            f.write(
                'Generation%d: Best Fitness = %e\n'%(i+1, best_fitness)
            )

    best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

    best_fitness = population[0,-1]

    return best_indiv,best_fitness


def ga_v2(
    nth_paramset,
    n_generation,
    n_population,
    n_children,
    n_gene,
    allowable_error,
    search_idx,
    search_region
    ):
    if n_population < n_gene+2:
        print('n_population must be larger than %d'%(n_gene+2))
        sys.exit()
        
    n_iter = 1
    n0 = np.zeros(2*n_population)

    population = get_initial_population(n_population,n_gene,search_idx,search_region)
    n0[0] = population[0,-1]
    print('Generation%d: Best Fitness = %e'%(1,population[0,-1]))
    with open('../FitParam/%d/out.txt'%(nth_paramset), mode='w') as f:
            f.write(
                'Generation1: Best Fitness = %e\n'%(population[0,-1])
            )
    best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
    best_fitness = population[0,-1]

    np.save('../FitParam/%d/generation.npy'%(nth_paramset),1)
    np.save('../FitParam/%d/FitParam1.npy'%(nth_paramset),best_indiv)
    np.save('../FitParam/%d/BestFitness.npy'%(nth_paramset),best_fitness)

    if population[0,-1] <= allowable_error:
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
        best_fitness = population[0,-1]
        return best_indiv,best_fitness

    for i in range(1,n_generation):
        ip = np.random.choice(n_population,n_gene+2,replace=False) # m=n+2
        ip, population = converging(ip,population,n_population,n_gene,search_idx,search_region)
        ip, population = local_search(ip,population,n_population,n_children,n_gene,search_idx,search_region)
        for j in range(n_iter-1):
            ip = np.random.choice(n_population,n_gene+2,replace=False)
            ip,population = converging(ip,population,n_population,n_gene,search_idx,search_region)
        if i%len(n0) == 0:
            n0 = np.zeros(len(n0))

        n0[i%len(n0)] = population[0,-1]

        if i%(len(n0)-1) == 0:
            if n0[0] == n0[len(n0)-1]:
                n_iter *= 2
            else:
                n_iter = 1

        print('Generation%d: Best Fitness = %e'%(i+1,population[0,-1]))
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

        if population[0,-1] < best_fitness:
            np.save('../FitParam/%d/generation.npy'%(nth_paramset),i+1)
            np.save('../FitParam/%d/FitParam%d.npy'%(nth_paramset,i+1),best_indiv)
        best_fitness = population[0,-1]
        np.save('../FitParam/%d/BestFitness.npy'%(nth_paramset),best_fitness)

        if population[0,-1] <= allowable_error:
            best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
            best_fitness = population[0,-1]
            return best_indiv,best_fitness

        np.save('../FitParam/%d/count_num.npy'%(nth_paramset),i+1)
        
        with open('../FitParam/%d/out.txt'%(nth_paramset), mode='a') as f:
            f.write(
                'Generation%d: Best Fitness = %e\n'%(i+1, best_fitness)
            )

    best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

    best_fitness = population[0,-1]

    return best_indiv,best_fitness


def get_initial_population(n_population,n_gene,search_idx,search_region):
    population = np.inf*np.ones((n_population,n_gene+1))

    print('initpop')
    for i in range(n_population):
        while np.isinf(population[i,-1]) or np.isnan(population[i,-1]):
            population[i,:n_gene] = np.random.rand(n_gene)
            population[i,-1] = objective(population[i,:n_gene],search_idx,search_region)
        sys.stdout.write('\r%d/%d'%(i+1,n_population))
    sys.stdout.write('\n')

    population = population[np.argsort(population[:,-1]),:]

    return population