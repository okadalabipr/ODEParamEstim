import sys
import numpy as np

from .transformation import decode_gene2variable
from .undx_mgg import mgg_variant
from .converging import converging
from .local_search import local_search
from param_estim.fitness import get_fitness
from param_estim.search_parameter import search_parameter_index
from param_estim.search_parameter import get_search_region

def parameter_estimation_continue(nth_paramset):

    search_idx = search_parameter_index()
    search_region = get_search_region()

    n_generation = 10000
    n_population = int(5*search_region.shape[1])
    n_children = 50
    n_gene = search_region.shape[1]
    allowable_error = 0.25
    p0_bounds = [0.1,10.0]  # [lower_bounds, upper bounds]

    (best_indiv,best_fitness) = ga_v2_continue(
        nth_paramset,
        n_generation,
        n_population,
        n_children,
        n_gene,
        allowable_error,
        search_idx,
        search_region,
        p0_bounds
    )


def ga_v1_continue(
    nth_paramset,
    n_generation,
    n_population,
    n_children,
    n_gene,
    allowable_error,
    search_idx,
    search_region,
    p0_bounds
    ):
    count_num = np.load('../FitParam/%d/count_num.npy'%(nth_paramset))
    generation = np.load('../FitParam/%d/generation.npy'%(nth_paramset))
    best_indiv = np.load('../FitParam/%d/FitParam%d.npy'%(nth_paramset,int(generation)))
    best_fitness = get_fitness(
        (np.log10(best_indiv) - search_region[0,:])/(search_region[1,:] - search_region[0,:]),
        search_idx,
        search_region
    )

    population = get_initial_population_continue(nth_paramset,n_population,n_gene,search_idx,search_region,p0_bounds)

    if best_fitness < population[0,-1]:
        population[0,:n_gene] = (np.log10(best_indiv) - search_region[0,:])/(search_region[1,:] - search_region[0,:])
        population[0,-1] = best_fitness
    else:
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
        best_fitness = population[0,-1]
        np.save('../FitParam/%d/FitParam%d.npy'%(nth_paramset,int(count_num)+1),best_indiv)

    print('Generation%d: Best Fitness = %e'%(int(count_num)+1,population[0,-1]))

    if population[0,-1] <= allowable_error:
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
        best_fitness = population[0,-1]
        return best_indiv,best_fitness
    else:
        pass

    for i in range(1,n_generation):
        population = mgg_variant(population,n_population,n_children,n_gene,search_idx,search_region)
        print('Generation%d: Best Fitness = %e'%(i+int(count_num)+1,population[0,-1]))
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

        if population[0,-1] < best_fitness:
            np.save('../FitParam/%d/FitParam%d.npy'%(nth_paramset,i+int(count_num)+1),best_indiv)
            np.save('../FitParam/%d/generation.npy'%(nth_paramset),i+int(count_num)+1)
        best_fitness = population[0,-1]

        if population[0,-1] <= allowable_error:
            best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
            best_fitness = population[0,-1]
            return best_indiv,best_fitness
        else:
            pass

        np.save('../FitParam/%d/count_num.npy'%(nth_paramset),i+int(count_num)+1)

    best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

    best_fitness = population[0,-1]

    return best_indiv,best_fitness


def ga_v2_continue(
    nth_paramset,
    n_generation,
    n_population,
    n_children,
    n_gene,
    allowable_error,
    search_idx,
    search_region,
    p0_bounds
    ):
    n_iter = 1
    n0 = np.zeros(2*n_population)

    count_num = np.load('../FitParam/%d/count_num.npy'%(nth_paramset))
    generation = np.load('../FitParam/%d/generation.npy'%(nth_paramset))
    best_indiv = np.load('../FitParam/%d/FitParam%d.npy'%(nth_paramset,int(generation)))
    best_fitness = get_fitness(
        (np.log10(best_indiv) - search_region[0,:])/(search_region[1,:] - search_region[0,:]),
        search_idx,
        search_region
    )

    population = get_initial_population_continue(nth_paramset,n_population,n_gene,search_idx,search_region,p0_bounds)

    if best_fitness < population[0,-1]:
        population[0,:n_gene] = (np.log10(best_indiv) - search_region[0,:])/(search_region[1,:] - search_region[0,:])
        population[0,-1] = best_fitness
    else:
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
        best_fitness = population[0,-1]
        np.save('../FitParam/%d/FitParam%d.npy'%(nth_paramset,int(count_num)+1),best_indiv)

    n0[0] = population[0,-1]

    print('Generation%d: Best Fitness = %e'%(int(count_num)+1,population[0,-1]))

    if population[0,-1] <= allowable_error:
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
        best_fitness = population[0,-1]
        return best_indiv,best_fitness
    else:
        pass

    for i in range(1,n_generation):
        ip = np.random.choice(n_population,n_gene+2,replace=False) # m=n+2
        ip, population = converging(ip,population,n_population,n_gene,search_idx,search_region)
        ip, population = local_search(ip,population,n_population,n_children,n_gene,search_idx,search_region)
        for j in range(n_iter-1):
            ip = np.random.choice(n_population,n_gene+2,replace=False)
            ip,population = converging(ip,population,n_population,n_gene,search_idx,search_region)
        if i%len(n0) == 0:
            n0 = np.zeros(len(n0))
        else:
            pass

        n0[i%len(n0)] = population[0,-1]

        if i%(len(n0)-1) == 0:
            if n0[0] == n0[len(n0)-1]:
                n_iter *= 2
            else:
                n_iter = 1

        print('Generation%d: Best Fitness = %e'%(i+int(count_num)+1,population[0,-1]))
        best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

        if population[0,-1] < best_fitness:
            np.save('../FitParam/%d/generation.npy'%(nth_paramset),i+int(count_num)+1)
            np.save('../FitParam/%d/FitParam%d.npy'%(nth_paramset,i+int(count_num)+1),best_indiv)
        best_fitness = population[0,-1]

        if population[0,-1] <= allowable_error:
            best_indiv = decode_gene2variable(population[0,:n_gene],search_region)
            best_fitness = population[0,-1]
            return best_indiv,best_fitness
        else:
            pass

        np.save('../FitParam/%d/count_num.npy'%(nth_paramset),i+int(count_num)+1)

    best_indiv = decode_gene2variable(population[0,:n_gene],search_region)

    best_fitness = population[0,-1]

    return best_indiv,best_fitness


def get_initial_population_continue(nth_paramset,n_population,n_gene,search_idx,search_region,p0_bounds):
    generation = np.load('../FitParam/%d/generation.npy'%(nth_paramset))
    best_indiv = np.load('../FitParam/%d/FitParam%d.npy'%(nth_paramset,int(generation)))

    population = np.inf*np.ones((n_population,n_gene+1))

    print('initpop')
    for i in range(n_population):
        while np.isinf(population[i,-1]) or np.isnan(population[i,-1]):
            population[i,:n_gene] = (
                np.log10(
                    best_indiv*10**(
                        np.random.rand(len(best_indiv))*np.log10(p0_bounds[1]/p0_bounds[0])+np.log10(p0_bounds[0])
                    )
                ) - search_region[0,:]
            )/(search_region[1,:] - search_region[0,:])
            population[i,:n_gene] = np.clip(population[i,:n_gene],0.,1.)
            population[i,-1] = get_fitness(population[i,:n_gene],search_idx,search_region)
        sys.stdout.write('\r%d/%d'%(i+1,n_population))
    sys.stdout.write('\n')

    population = population[np.argsort(population[:,-1]),:]

    return population