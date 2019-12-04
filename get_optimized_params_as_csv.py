import os
import re
import csv
import numpy as np

import model
from param_estim.search_parameter import search_parameter_index

n_file = 0
fitparam_files = os.listdir('./out')
for file in fitparam_files:
    if re.match(r'\d',file):
        n_file += 1
        
search_idx = search_parameter_index()
optimized_params = np.empty((len(search_idx[0])+2,n_file+1), dtype='<U21')

for i,param_index in enumerate(search_idx[0]):
    for j in range(n_file):
        
        generation = np.load('./out/%d/generation.npy'%(j+1))
        best_indiv = np.load('./out/%d/fit_param%d.npy'%(j+1,int(generation)))
        error = np.load('./out/%d/best_fitness.npy'%(j+1))

        
        optimized_params[0,0] = ''
        optimized_params[1,0] = '*Error*'
        optimized_params[i+2,0] = model.C.param_names[param_index]    
        optimized_params[0,j+1] = str(j+1)
        optimized_params[1,j+1] = '%8.3e'%(error) 
        optimized_params[i+2,j+1] = '%8.3e'%(best_indiv[i])
        
with open('optimized_params.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(optimized_params)
        
