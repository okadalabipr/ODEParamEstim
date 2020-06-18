import os
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from .name2idx import C, V
from .observable import observables, ExperimentalData

def timecourse(sim, n_file, viz_type, show_all, stdev, simulations_all):
    os.makedirs(
        '.figure/{}'.format(viz_type), exist_ok=True
    )
    exp = ExperimentalData()
    
    plt.rcParams['font.size'] = 20
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['xtick.major.width'] = 1.2
    plt.rcParams['ytick.major.width'] = 1.2
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.markersize'] = 12
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.it'] = 'Arial:italic'

    cmap = ['goldenrod', 'seagreen']
    shape = ['^', 'o']

    for i, obs_name in enumerate(observables):

        plt.figure(figsize=(4, 3))
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        if show_all:
            for j in range(n_file):
                for l, _ in enumerate(sim.conditions):
                    plt.plot(
                        sim.t, simulations_all[i, j, :, l] / np.max(simulations_all[i, j, :, :]), 
                        color=cmap[l], alpha=0.05
                    )
        if viz_type == 'average':
            normalized = np.empty_like(simulations_all)
            for j in range(n_file):
                for l, _ in enumerate(sim.conditions):
                    normalized[i, j, :, l] = (
                        simulations_all[i, j, :, l] / np.max(simulations_all[i, j, :, :])
                    )
            normalized[i,:,:,:] = normalized[i,:,:,:] / np.max(
                np.nanmean(normalized[i,:,:,:], axis=0)
            )
            for l, _ in enumerate(sim.conditions):
                plt.plot(
                    sim.t, np.nanmean(normalized[i, :, :, l], axis=0), 
                    color=cmap[l]
                )
            if stdev:
                for l, _ in enumerate(sim.conditions):
                    mean = np.nanmean(normalized[i, :, :, l], axis=0)
                    yerr = [
                        np.nanstd(normalized[i, :, k, l], ddof=1)
                        for k, _ in enumerate(sim.t)
                    ]
                    plt.fill_between(
                        sim.t, mean - yerr, mean + yerr, 
                        lw=0, color=cmap[l], alpha=0.1
                    )
        else:
            for l, _ in enumerate(sim.conditions):
                plt.plot(
                    sim.t, sim.simulations[i, :, l]/np.max(sim.simulations[i]), 
                    color=cmap[l]
                )
        if exp.experiments[i] is not None:
            exp_t = exp.get_timepoint(i)
            for l, condition in enumerate(sim.conditions):
                if condition in exp.experiments[i]:
                    plt.plot(
                        np.array(exp_t)/60., exp.experiments[i][condition], shape[l], 
                        markerfacecolor='None', markeredgecolor=cmap[l], clip_on=False
                    )

        if exp.experiments[i] is not None:
            exp_t = exp.get_timepoint(i)
            for l, condition in enumerate(sim.conditions):
                if condition in exp.experiments[i]:
                    plt.plot(
                        np.array(exp_t)/60., exp.experiments[i][condition], shape[l], 
                        markerfacecolor='None', markeredgecolor=cmap[l], clip_on=False
                    )

        plt.xlim(0, 90)
        plt.xticks([0, 30, 60, 90])
        plt.yticks([0, 0.3, 0.6, 0.9, 1.2])
        plt.ylim(0, 1.2)
        plt.xlabel('Time (min)')
        plt.ylabel(obs_name.replace('_', ' '))

        plt.savefig(
            './figure/{0}/{1}.pdf'.format(
                viz_type, obs_name
            ), bbox_inches='tight'
        )
        plt.close()
        
        
def param_range(search_idx, popt, portrait):
    
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['xtick.major.width'] = 1.2
    plt.rcParams['ytick.major.width'] = 1.2
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.it'] = 'Arial:italic'
    
    if portrait:
        if len(search_idx[0]) > 0:
            fig = plt.figure(figsize=(8, len(search_idx[0])/2.5))
            ax = sns.boxenplot(
                data=popt[:, :len(search_idx[0])], 
                orient='h', 
                linewidth=0.5, 
                palette='Set2'
            )
            sns.despine()
            ax.set_xlabel('Parameter value')
            ax.set_ylabel('')
            ax.set_yticklabels([C.NAMES[i] for i in search_idx[0]])
            ax.set_xscale('log')

            plt.savefig(
                './figure/param_range.pdf', bbox_inches='tight'
            )
            plt.close(fig)
        if len(search_idx[1]) > 0:
            fig = plt.figure(figsize=(8, len(search_idx[1])/2.5))
            ax = sns.boxenplot(
                data=popt[:, len(search_idx[0]):], 
                orient='h', 
                linewidth=0.5, 
                palette='Set2'
            )
            sns.despine()
            ax.set_xlabel('Initial value')
            ax.set_ylabel('')
            ax.set_yticklabels([V.NAMES[i] for i in search_idx[1]])
            ax.set_xscale('log')

            plt.savefig(
                './figure/initial_value_range.pdf', bbox_inches='tight'
            )
            plt.close(fig)
    else:
        if len(search_idx[0]) > 0:
            fig = plt.figure(figsize=(len(search_idx[0])/2.2, 6))
            ax = sns.boxenplot(
                data=popt[:, :len(search_idx[0])], 
                linewidth=0.5, 
                palette='Set2'
            )
            sns.despine()
            ax.set_xlabel('')
            ax.set_xticklabels([C.NAMES[i] for i in search_idx[0]], rotation=45)
            ax.set_ylabel('Parameter value')
            ax.set_yscale('log')

            plt.savefig(
                './figure/param_range_h.pdf', bbox_inches='tight'
            )
            plt.close(fig)
        if len(search_idx[1]) > 0:
            fig = plt.figure(figsize=(len(search_idx[1])/2.2, 6))
            ax = sns.boxenplot(
                data=popt[:, len(search_idx[0]):], 
                linewidth=0.5, 
                palette='Set2'
            )
            sns.despine()
            ax.set_xlabel('')
            ax.set_xticklabels([V.NAMES[i] for i in search_idx[1]], rotation=45)
            ax.set_ylabel('Initial value')
            ax.set_yscale('log')

            plt.savefig(
                './figure/initail_value_range_h.pdf', bbox_inches='tight'
            )
            plt.close(fig)