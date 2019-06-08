# [ga_v2] ENDX + MGG(best&random)
def converging(
    ip,
    population,
    n_population,
    n_gene,
    search_idx,
    search_region
    ):
    n_children = 10
    children = np.empty((n_children,n_gene+1))

    for i in range(n_children):
        ip[2:] = np.random.choice(n_population,n_gene,replace=False)
        children[i,:] = xover(population[ip,:],n_gene)

    family = np.empty((n_children+2,n_gene+1))
    family[:n_children,:] = children
    family[n_children,:] = population[ip[0],:]
    family[n_children+1,:] = population[ip[1],:]

    family = family[np.argsort(family[:,-1]),:]

    population[ip[0],:] = family[0,:] # Best, either of parents
    population[ip[1],:] = family[np.random.randint(low=1,high=n_children+2,dtype=np.int),:] # Random

    if np.isinf(population[ip[1],-1]):
        population[ip[1],-1] = get_fitness(population[ip[1],:n_gene],search_idx,search_region)

    population = population[np.argsort(population[:,-1]),:]

    return ip, population


def xover(parents,n_gene):
    MAXITER = np.iinfo(np.int8).max

    in_range = False
    for i in range(MAXITER):
        child = endx(parents,n_gene)
        if 0. <= np.min(child[:n_gene]) and np.max(child[:n_gene]) <= 1.:
            in_range = True
            break

    if not in_range:
        child[:n_gene] = np.clip(child[:n_gene],0.,1.)

    child[-1] = np.inf

    return child


# Extended Normal Distribution Xover
def endx(parents,n_gene):
    ALPHA = (1.-2*0.35**2)**0.5/2.
    BETA = 0.35/(n_gene-1)**0.5

    child = np.empty(n_gene+1)

    t1 = (parents[1,:n_gene]-parents[0,:n_gene])/2.
    t2 = np.random.normal(scale=ALPHA)*(parents[1,:n_gene]-parents[0,:n_gene])
    t3 = np.sum(
        np.random.normal(scale=BETA,size=n_gene)[:,None]
        *(parents[2:,:n_gene]-(np.sum(parents[2:,:n_gene],axis=0)/n_gene)),
        axis=0
    )

    child[:n_gene] = t1 + t2 + t3

    return child
