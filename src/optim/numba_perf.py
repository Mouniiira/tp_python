import numpy as np
import time
from numba import njit, prange

# --- 1. Version NumPy Vectorisée ---
def haversine_numpy(lat1, lon1, lat2, lon2):
    r = 6371
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    return 2 * r * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

# --- 2. Version Numba JIT ---
@njit
def haversine_numba(lat1, lon1, lat2, lon2):
    r = 6371
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = np.radians(lat2 - lat1)
    dl = np.radians(lon2 - lon1)
    a = np.sin(dp/2)**2 + np.cos(p1) * np.cos(p2) * np.sin(dl/2)**2
    return 2 * r * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

# --- 3. Version Numba Parallèle ---
@njit(parallel=True)
def haversine_numba_parallel(lats1, lons1, lats2, lons2):
    n = lats1.shape[0]
    res = np.empty(n, dtype=np.float64)
    for i in prange(n):
        r = 6371
        p1, p2 = np.radians(lats1[i]), np.radians(lats2[i])
        dp = np.radians(lats2[i] - lats1[i])
        dl = np.radians(lons2[i] - lons1[i])
        a = np.sin(dp/2)**2 + np.cos(p1) * np.cos(p2) * np.sin(dl/2)**2
        res[i] = 2 * r * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return res

if __name__ == "__main__":
    # Génération de 10 millions de points
    N = 10_000_000
    print(f"📊 Génération de {N:,} points...")
    lats1 = np.random.uniform(-90, 90, N)
    lons1 = np.random.uniform(-180, 180, N)
    lats2 = np.random.uniform(-90, 90, N)
    lons2 = np.random.uniform(-180, 180, N)

    print("\n🚀 Lancement du benchmark...")

    # Benchmark NumPy
    start = time.time()
    res_np = haversine_numpy(lats1, lons1, lats2, lons2)
    print(f"⏱️  NumPy Vectorisé : {time.time() - start:.4f}s")

    # Benchmark Numba (Premier appel inclut le temps de compilation)
    start = time.time()
    res_nb = haversine_numba(lats1, lons1, lats2, lons2)
    print(f"⏱️  Numba JIT (1er appel - avec compilation) : {time.time() - start:.4f}s")

    # Benchmark Numba (Deuxième appel - déjà compilé)
    start = time.time()
    res_nb = haversine_numba(lats1, lons1, lats2, lons2)
    print(f"⏱️  Numba JIT (2ème appel - optimisé) : {time.time() - start:.4f}s")

    # Benchmark Numba Parallel
    start = time.time()
    res_nb_p = haversine_numba_parallel(lats1, lons1, lats2, lons2)
    print(f"⏱️  Numba Parallel : {time.time() - start:.4f}s")