from param_estim import optimize, optimize_continue
import os
import sys
import re
import warnings
import multiprocessing
warnings.filterwarnings('ignore')


def run_ga_continue(nth_paramset):
    if not os.path.isdir('./out/%d' % (nth_paramset)):
        os.mkdir('./out/%d' % (nth_paramset))
        optimize(nth_paramset)
    else:
        optimize_continue(nth_paramset)


if __name__ == '__main__':
    args = sys.argv
    if 'current_ipynb' in globals():
        nth_paramset = int(re.sub(r'\D', '', current_ipynb))
        run_ga_continue(nth_paramset)
    else:
        if len(args) == 2:
            run_ga_continue(int(args[1]))
        elif len(args) == 3:
            n_proc = max(1, multiprocessing.cpu_count() - 1)
            p = multiprocessing.Pool(processes=n_proc)
            p.map(run_ga_continue, range(int(args[1]), int(args[2])+1))
            p.close()
