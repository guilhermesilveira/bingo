import numpy as np
from multiprocessing import Pool
import numpy as np


def run_multiple(f, parameters):
    with Pool(processes=7) as pool:
        r = pool.map(f, parameters)
        if (not isinstance(r[0], list)) or np.isscalar(r[0]):
            return zip(parameters, r)
        results = []
        for i in range(len(parameters)):
            results.append([parameters[i], *r[i]])
        return results
