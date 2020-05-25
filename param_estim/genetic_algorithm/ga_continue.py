import sys
import time
import numpy as np

from .converter import *
from .undx_mgg import mgg_alternation
from .converging import converging
from .local_search import local_search
from param_estim.fitness import objective
from param_estim.set_search_param import get_region


def optimize_continue(nth_paramset):

    np.random.seed(
        time.time_ns()*nth_paramset % 2**32
    )

    search_region = get_region()

    max_generation = 10000
    n_population = int(5*search_region.shape[1])
    n_children = 50
    n_gene = search_region.shape[1]
    allowable_error = 0.25
    p0_bounds = [0.1, 10.0]  # [lower_bounds, upper bounds]

    (best_indiv, best_fitness) = ga_v2_continue(
        nth_paramset,
        max_generation,
        n_population,
        n_children,
        n_gene,
        allowable_error,
        search_region,
        p0_bounds
    )


def ga_v1_continue(nth_paramset, max_generation, n_population, n_children, n_gene,
                   allowable_error, search_region, p0_bounds):
    count_num = np.load(
        './out/%d/count_num.npy' % (nth_paramset)
    )
    best_generation = np.load(
        './out/%d/generation.npy' % (nth_paramset)
    )
    best_indiv = np.load(
        './out/%d/fit_param%d.npy' % (nth_paramset, int(best_generation))
    )
    best_fitness = objective(
        (np.log10(best_indiv) - search_region[0, :]) /
        (search_region[1, :] - search_region[0, :]), search_region
    )
    population = get_initial_population_continue(
        nth_paramset, n_population, n_gene, search_region, p0_bounds
    )
    if best_fitness < population[0, -1]:
        population[0, :n_gene] = (
            (np.log10(best_indiv) - search_region[0, :]) /
            (search_region[1, :] - search_region[0, :])
        )
        population[0, -1] = best_fitness
    else:
        best_indiv = decode_gene2variable(
            population[0, :n_gene], search_region)
        best_fitness = population[0, -1]
        np.save(
            './out/%d/fit_param%d.npy' % (
                nth_paramset, int(count_num) + 1
            ), best_indiv
        )
    with open('./out/%d/out.log' % (nth_paramset), mode='a') as f:
        f.write(
            '\n----------------------------------------\n\n' +
            'Generation%d: Best Fitness = %e\n' % (
                int(count_num) + 1, best_fitness)
        )
    print(
        '\n----------------------------------------\n\n' +
        'Generation%d: Best Fitness = %e' % (
            int(count_num) + 1, population[0, -1])
    )
    if population[0, -1] <= allowable_error:
        best_indiv = decode_gene2variable(
            population[0, :n_gene], search_region)
        best_fitness = population[0, -1]
        return best_indiv, best_fitness

    generation = 1
    while generation < max_generation:
        population = mgg_alternation(
            population, n_population, n_children, n_gene, search_region
        )
        print(
            'Generation%d: Best Fitness = %e' % (
                generation + int(count_num) + 1, population[0, -1]
            )
        )
        best_indiv = decode_gene2variable(
            population[0, :n_gene], search_region)

        if population[0, -1] < best_fitness:
            np.save(
                './out/%d/fit_param%d.npy' % (
                    nth_paramset, generation + int(count_num) + 1
                ), best_indiv
            )
            np.save(
                './out/%d/generation.npy' % (nth_paramset),
                generation + int(count_num) + 1
            )
            np.save(
                './out/%d/best_fitness' % (nth_paramset), best_fitness
            )
        best_fitness = population[0, -1]

        np.save(
            './out/%d/count_num.npy' % (nth_paramset), generation +
            int(count_num) + 1
        )
        with open('./out/%d/out.log' % (nth_paramset), mode='a') as f:
            f.write(
                'Generation%d: Best Fitness = %e\n' % (
                    generation + int(count_num) + 1, best_fitness
                )
            )
        if population[0, -1] <= allowable_error:
            best_indiv = decode_gene2variable(
                population[0, :n_gene], search_region)
            best_fitness = population[0, -1]
            return best_indiv, best_fitness

        generation += 1

    best_indiv = decode_gene2variable(population[0, :n_gene], search_region)
    best_fitness = population[0, -1]

    return best_indiv, best_fitness


def ga_v2_continue(nth_paramset, max_generation, n_population, n_children, n_gene,
                   allowable_error, search_region, p0_bounds):
    if n_population < n_gene+2:
        raise ValueError(
            'n_population must be larger than %d' % (
                n_gene + 2
            )
        )
    n_iter = 1
    n0 = np.empty(3*n_population)

    count_num = np.load(
        './out/%d/count_num.npy' % (nth_paramset)
    )
    best_generation = np.load(
        './out/%d/generation.npy' % (nth_paramset)
    )
    best_indiv = np.load(
        './out/%d/fit_param%d.npy' % (nth_paramset, int(best_generation))
    )
    best_fitness = objective(
        (np.log10(best_indiv) - search_region[0, :]) /
        (search_region[1, :] - search_region[0, :]), search_region
    )
    population = get_initial_population_continue(
        nth_paramset, n_population, n_gene, search_region, p0_bounds
    )
    if best_fitness < population[0, -1]:
        population[0, :n_gene] = (
            (np.log10(best_indiv) - search_region[0, :]) /
            (search_region[1, :] - search_region[0, :])
        )
        population[0, -1] = best_fitness
    else:
        best_indiv = decode_gene2variable(
            population[0, :n_gene], search_region)
        best_fitness = population[0, -1]
        np.save(
            './out/%d/fit_param%d.npy' % (
                nth_paramset, int(count_num) + 1
            ), best_indiv
        )
    with open('./out/%d/out.log' % (nth_paramset), mode='a') as f:
        f.write(
            '\n----------------------------------------\n\n' +
            'Generation%d: Best Fitness = %e\n' % (
                int(count_num) + 1, best_fitness
            )
        )
    n0[0] = population[0, -1]

    print(
        '\n----------------------------------------\n\n' +
        'Generation%d: Best Fitness = %e' % (
            int(count_num) + 1, population[0, -1]
        )
    )
    if population[0, -1] <= allowable_error:
        best_indiv = decode_gene2variable(
            population[0, :n_gene], search_region)
        best_fitness = population[0, -1]
        return best_indiv, best_fitness

    generation = 1
    while generation < max_generation:
        ip = np.random.choice(n_population, n_gene+2, replace=False)
        ip, population = converging(
            ip, population, n_population, n_gene, search_region
        )
        ip, population = local_search(
            ip, population, n_population, n_children, n_gene, search_region
        )
        for _ in range(n_iter-1):
            ip = np.random.choice(n_population, n_gene+2, replace=False)
            ip, population = converging(
                ip, population, n_population, n_gene, search_region
            )
        if generation % len(n0) == len(n0) - 1:
            n0[-1] = population[0, -1]
            if n0[0] == n0[-1]:
                n_iter *= 2
            else:
                n_iter = 1
        else:
            n0[generation % len(n0)] = population[0, -1]

        print(
            'Generation%d: Best Fitness = %e' % (
                generation + int(count_num) + 1, population[0, -1]
            )
        )
        best_indiv = decode_gene2variable(
            population[0, :n_gene], search_region)

        if population[0, -1] < best_fitness:
            np.save(
                './out/%d/generation.npy' % (nth_paramset),
                generation + int(count_num) + 1
            )
            np.save(
                './out/%d/fit_param%d.npy' % (
                    nth_paramset, generation + int(count_num) + 1
                ), best_indiv
            )
            np.save(
                './out/%d/best_fitness' % (nth_paramset), best_fitness
            )
        best_fitness = population[0, -1]

        np.save(
            './out/%d/count_num.npy' % (nth_paramset), generation +
            int(count_num) + 1
        )
        with open('./out/%d/out.log' % (nth_paramset), mode='a') as f:
            f.write(
                'Generation%d: Best Fitness = %e\n' % (
                    generation + int(count_num) + 1, best_fitness
                )
            )
        if population[0, -1] <= allowable_error:
            best_indiv = decode_gene2variable(
                population[0, :n_gene], search_region
            )
            best_fitness = population[0, -1]
            return best_indiv, best_fitness

        generation += 1

    best_indiv = decode_gene2variable(population[0, :n_gene], search_region)
    best_fitness = population[0, -1]

    return best_indiv, best_fitness


def get_initial_population_continue(nth_paramset, n_population, n_gene,
                                    search_region, p0_bounds):
    best_generation = np.load(
        './out/%d/generation.npy' % (nth_paramset)
    )
    best_indiv = np.load(
        './out/%d/fit_param%d.npy' % (nth_paramset, int(best_generation))
    )
    population = np.full(
        (n_population, n_gene+1), np.inf
    )
    print('Generating the initial population. . .')
    for i in range(n_population):
        while np.isinf(population[i, -1]) or np.isnan(population[i, -1]):
            population[i, :n_gene] = encode_bestindiv2randgene(
                best_indiv, search_region, p0_bounds
            )
            population[i, :n_gene] = np.clip(population[i, :n_gene], 0., 1.)
            population[i, -1] = objective(
                population[i, :n_gene], search_region
            )
        sys.stdout.write('\r%d/%d' % (i+1, n_population))
    sys.stdout.write('\n')

    population = population[np.argsort(population[:, -1]), :]

    return population
