import numpy as np
from matplotlib import pyplot as plt

from .observable import observable_names, num_observables, ExperimentalData

def timecourse(sim,n_file,viz_type,show_all,stdev,simulations_all):

    exp = ExperimentalData()
    
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.markersize'] = 10
#   plt.rcParams['font.family'] = 'Arial'
#   plt.rcParams['mathtext.fontset'] = 'custom'
#   plt.rcParams['mathtext.it'] = 'Arial:italic'

    cmap = plt.get_cmap('tab10')

    for i,title in enumerate(observable_names):

        plt.figure(figsize=(4,3))
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        if show_all:
            for j in range(n_file):
                for l in range(sim.condition):
                    plt.plot(
                        sim.t,simulations_all[i,j,:,l]/np.max(simulations_all[i,j,:,:]),
                        color=cmap(l),alpha=0.05
                    )

        if not viz_type == 'average':
            for l in range(sim.condition):
                plt.plot(
                    sim.t,sim.simulations[i,:,l]/np.max(sim.simulations[i]),
                    color=cmap(l)
                )
        else:
            normalized = np.empty((num_observables,n_file,len(sim.tspan),sim.condition))
            for j in range(n_file):
                for l in range(sim.condition):
                    normalized[i,j,:,l] = simulations_all[i,j,:,l]/np.max(simulations_all[i,j,:,:])
            for l in range(sim.condition):
                plt.plot(
                    sim.t,np.nanmean(normalized[i,:,:,l],axis=0),
                    color=cmap(l)
                )
            if stdev:
                for l in range(sim.condition):
                    mean = np.nanmean(normalized[i,:,:,l],axis=0)
                    yerr = [np.nanstd(normalized[i,:,k,l],ddof=1) for k,_ in enumerate(sim.t)]
                    plt.fill_between(
                        sim.t, mean - yerr, mean + yerr,
                        lw=0,color=cmap(l),alpha=0.1
                    )

        if exp.experiments[i] is not None:
            exp_t = exp.get_timepoint(i)
            keys = list(exp.experiments[i].keys())
            for l,key in enumerate(keys):
                plt.plot(
                    exp_t/60.,exp.experiments[i][key],'D',
                    markerfacecolor='None',
                    markeredgecolor=cmap(l),
                    clip_on=False
                )

        plt.xlim(0,90)
        plt.xticks([0,30,60,90])
        plt.yticks([0,0.2,0.4,0.6,0.8,1,1.2])
        plt.ylim(0,1.2)
        plt.xlabel('Time (min)')
        plt.title(title)

        plt.savefig('./figure/simulation_{0}_{1}.pdf'.
                    format(viz_type,title),bbox_inches='tight')
        plt.close()