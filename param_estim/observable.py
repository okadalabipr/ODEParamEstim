import numpy as np
from scipy.integrate import ode

from .model.name2idx import parameters as C
from .model.name2idx import variables as V
from .model.differential_equation import diffeq
    
observable_names = [
    'Phosphorylated_MEKc',
    'Phosphorylated_ERKc',
    'Phosphorylated_RSKw',
    'Phosphorylated_CREBw',
    'dusp_mRNA',
    'cfos_mRNA',
    'cFos_Protein',
    'Phosphorylated_cFos'\
]

num_observables = len(observable_names)
species = dict(zip(observable_names,range(num_observables)))


def diff_sim_and_exp(
    sim_matrix,exp_dict,exp_timepoint,num_condition,
    norm_max_sim=1,norm_max_exp=1
    ):
        
    return (
        np.r_[
            [sim_matrix[exp_timepoint,i] for i in range(num_condition)]
        ].flatten()/norm_max_sim,
        np.r_[
            list(exp_dict.values())
        ].flatten()/norm_max_exp
    )
    

def solveode(diffeq,y0,tspan,args):
    sol = ode(diffeq)
    sol.set_integrator('vode',method='bdf',min_step=1e-8,with_jacobian=True)
    sol.set_initial_value(y0,tspan[0])
    sol.set_f_params(args)

    T = [tspan[0]]
    Y = [y0]

    while sol.successful() and sol.t < tspan[-1]:
        sol.integrate(sol.t+1.)
        T.append(sol.t)
        Y.append(sol.y)

    return np.array(T),np.array(Y)


class NumericalSimulation(object):
    
    def _solveode(self,diffeq,y0,tspan,args):
        sol = ode(diffeq)
        sol.set_integrator('vode',method='bdf',min_step=1e-8,with_jacobian=True)
        sol.set_initial_value(y0,tspan[0])
        sol.set_f_params(args)

        T = [tspan[0]]
        Y = [y0]

        while sol.successful() and sol.t < tspan[-1]:
            sol.integrate(sol.t+1.)
            T.append(sol.t)
            Y.append(sol.y)

        return np.array(T),np.array(Y)

    tspan = range(5401) # Unit time: 1 sec.
    condition = 2

    t = np.array(tspan)/60. # sec. -> min. (plot_func.py)
    
    simulations = np.empty((num_observables,len(tspan),condition))

    def simulate(self,x,y0):

        for i in range(self.condition):
            if i==0:
                x[C.Ligand] = x[C.EGF]
            elif i==1:
                x[C.Ligand] = x[C.HRG]

            (T,Y) = self._solveode(diffeq,y0,self.tspan,tuple(x))

            if T[-1] < self.tspan[-1]:
                return False
            else:
                self.simulations[species['Phosphorylated_MEKc'],:,i] = \
                    Y[:,V.ppMEKc]
                    
                self.simulations[species['Phosphorylated_ERKc'],:,i] = \
                    Y[:,V.pERKc] + Y[:,V.ppERKc]
                    
                self.simulations[species['Phosphorylated_RSKw'],:,i] = \
                    Y[:,V.pRSKc] + Y[:,V.pRSKn]*(x[C.Vn]/x[C.Vc])
                    
                self.simulations[species['Phosphorylated_CREBw'],:,i] = \
                    Y[:,V.pCREBn]*(x[C.Vn]/x[C.Vc])
                    
                self.simulations[species['dusp_mRNA'],:,i] = \
                    Y[:,V.duspmRNAc]
                    
                self.simulations[species['cfos_mRNA'],:,i] = \
                    Y[:,V.cfosmRNAc]
                    
                self.simulations[species['cFos_Protein'],:,i] = \
                    (Y[:,V.pcFOSn] + Y[:,V.cFOSn])*(x[C.Vn]/x[C.Vc]) + Y[:,V.cFOSc] + Y[:,V.pcFOSc]
                    
                self.simulations[species['Phosphorylated_cFos'],:,i] = \
                    Y[:,V.pcFOSn]*(x[C.Vn]/x[C.Vc]) + Y[:,V.pcFOSc]
                    
                    
class ExperimentalData(object):

    t2 = np.array([0, 300, 600, 900, 1800, 2700, 3600, 5400])
    
    experiments = [None]*num_observables
    
    experiments[species['Phosphorylated_MEKc']] = {
        'EGF':np.array([0.000,0.773,0.439,0.252,0.130,0.087,0.080,0.066]),
        'HRG':np.array([0.000,0.865,1.000,0.837,0.884,0.920,0.875,0.789])
    }

    experiments[species['Phosphorylated_ERKc']] = {
        'EGF':np.array([0.000,0.867,0.799,0.494,0.313,0.266,0.200,0.194]),
        'HRG':np.array([0.000,0.848,1.000,0.971,0.950,0.812,0.747,0.595])
    }

    experiments[species['Phosphorylated_RSKw']] = {
        'EGF':np.array([0,0.814,0.812,0.450,0.151,0.059,0.038,0.030]),
        'HRG':np.array([0,0.953,1.000,0.844,0.935,0.868,0.779,0.558])
    }

    experiments[species['Phosphorylated_cFos']] = {
        'EGF':np.array([0,0.060,0.109,0.083,0.068,0.049,0.027,0.017]),
        'HRG':np.array([0,0.145,0.177,0.158,0.598,1.000,0.852,0.431])
    }

    # ==========================================================================
    t3 = np.array([0, 600, 1800, 3600, 5400])

    experiments[species['Phosphorylated_CREBw']] = {
        'EGF':np.array([0,0.446,0.030,0.000,0.000]),
        'HRG':np.array([0,1.000,0.668,0.460,0.340])
    }
    
    # ==========================================================================
    t4 = np.array([0,600,1200,1800,2700,3600,5400])
    
    experiments[species['cfos_mRNA']] = {
        'EGF':np.array([0,0.181,0.476,0.518,0.174,0.026,0.000]),
        'HRG':np.array([0,0.353,0.861,1.000,0.637,0.300,0.059])
    }

    # ==========================================================================
    t5 = np.array([0,900,1800,2700,3600,5400])
    
    experiments[species['cFos_Protein']] = {
        'EGF':np.array([0,0.078,0.216,0.240,0.320,0.235]),
        'HRG':np.array([0,0.089,0.552,0.861,1.000,0.698])
    }

    experiments[species['dusp_mRNA']] = {
        'EGF':np.array([0.000,0.177,0.331,0.214,0.177,0.231]),
        'HRG':np.array([0.000,0.221,0.750,1.000,0.960,0.934])
    }
    
    
    def get_timepoint(self,observable):
        if observable in [
            species['Phosphorylated_MEKc'],
            species['Phosphorylated_ERKc'],
            species['Phosphorylated_RSKw'],
            species['Phosphorylated_cFos']
            ]:
            exp_t = self.t2
            
        elif observable == species['Phosphorylated_CREBw']:
            exp_t = self.t3
            
        elif observable == species['cfos_mRNA']:
            exp_t = self.t4
            
        elif observable in [
            species['cFos_Protein'],
            species['dusp_mRNA']
            ]: 
            exp_t = self.t5
            
        return exp_t