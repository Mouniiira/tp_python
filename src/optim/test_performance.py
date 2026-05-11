import time
import numpy as np
from src.optim.numba_perf import haversine_numba, haversine_numba_parallel
# On n'importe Cython que s'il est compilé
try:
    from src.optim.cython_ext.haversine_cython import haversine_cython_array
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False

def run_benchmarks():
    # 1. Préparation des données (10^7 points)
    N = 10_000_000
    lats1 = np.random.uniform(-90, 90, N)
    # ... (autres lats/lons)

    # 2. Test Numba
    start = time.time()
    haversine_numba(lats1, lons1, lats2, lons2)
    print(f"Numba JIT: {time.time() - start:.4f}s")

    # 3. Test Cython
    if CYTHON_AVAILABLE:
        start = time.time()
        haversine_cython_array(lats1, lons1, lats2, lons2)
        print(f"Cython AOT: {time.time() - start:.4f}s")
    else:
        print("Cython non compilé, passage au test suivant.")

if __name__ == "__main__":
    run_benchmarks()