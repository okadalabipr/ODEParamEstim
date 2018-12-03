def myGAv2(n_generation,n_population,n_children,n_gene,allowable_error,SearchRegion):
    np.save('./FitParam/generation.npy',int(0))
    np.save('./FitParam/FitParam0.npy',SearchParam)
    N_iter = 1
    FIT    = np.random.rand(n_population)
    population = getInitialPopulation(n_population,n_gene,SearchRegion)
    FIT[0] = population[0,-1]
    print('Generation%d: Best Fitness = %e'%(1,population[0,-1]))
    X0 = decodeGene2Variable(population[0,:n_gene],SearchRegion)
    BestFitness = population[0,-1]
    np.save('./FitParam/generation.npy',int(1))
    np.save('./FitParam/FitParam1.npy',X0)
    if population[0,-1] <= allowable_error:
        X0 = decodeGene2Variable(population[0,:n_gene],SearchRegion)
        BestFitness = population[0,-1]
        return X0,BestFitness
    else:
        pass
    for i in range(1,n_generation):
        ip = np.random.choice(n_population,n_gene+2,replace=False)# m=n+2
        ip, population = Converging(ip,population,n_population,n_children,n_gene,SearchRegion)
        ip, population = LocalSearch(ip,population,n_population,n_children,n_gene,SearchRegion)
        for j in range(N_iter-1):
            ip = np.random.choice(n_population,n_gene+2,replace=False)
            ip,population = Converging(ip,population,n_population,n_children,n_gene,SearchRegion)
        if i%n_population == 0:
            FIT = np.random.rand(n_population)
        else:
            pass
        FIT[i%n_population] = population[0,-1]
        if FIT[0] == FIT[n_population-1]:
            N_iter *= 2
        else:
            N_iter = 1
        print('Generation%d: Best Fitness = %e'%(i+1,population[0,-1]))
        X0 = decodeGene2Variable(population[0,:n_gene],SearchRegion)
        if population[0,-1] < BestFitness:
            np.save('./FitParam/generation.npy',int(i+1))
            np.save('./FitParam/FitParam%d.npy'%(i+1),X0)
        BestFitness = population[0,-1]
        if population[0,-1] <= allowable_error:
            X0 = decodeGene2Variable(population[0,:n_gene],SearchRegion)
            BestFitness = population[0,-1]
            return X0,BestFitness
        else:
            pass
    X0 = decodeGene2Variable(population[0,:n_gene],SearchRegion)
    BestFitness = population[0,-1]
    return X0,BestFitness