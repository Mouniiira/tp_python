import numpy as np
import pandas as pd
import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# PARTIE 40 : CPU-BOUND (Calcul Intensif)
def cpu_task(n=5_000_000):
    """Calcul de la somme des sinus pour occuper le CPU."""
    return np.sum(np.sin(np.arange(n)))

def run_cpu_benchmark():
    n_tasks = 8
    print(f"\n Benchmark CPU-Bound ({n_tasks} tâches) ")
    
    # Test Threading
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, [5_000_000]*n_tasks))
    print(f"Threading (GIL présent) : {time.time() - start:.2f}s")
    
    # Test Multiprocessing
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, [5_000_000]*n_tasks))
    print(f"Multiprocessing (GIL contourné) : {time.time() - start:.2f}s")

# PARTIE 41 : I/O-BOUND (Lecture de fichiers)
def io_task(path):
    """Lecture d'un fichier Parquet (attente disque)."""
    if os.path.exists(path):
        return pd.read_parquet(path).shape
    return None

def run_io_benchmark():
    file_path = "data/raw/yellow_tripdata_2023-01.parquet"
    files = [file_path] * 10
    
    print(f"\n Benchmark I/O-Bound (10 lectures de fichiers)")
    
    # Test Séquentiel
    start = time.time()
    for f in files:
        io_task(f)
    print(f"Séquentiel : {time.time() - start:.2f}s")
    
    # Test Threading
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(io_task, files))
    print(f"Threading (Concurrence I/O) : {time.time() - start:.2f}s")

if __name__ == "__main__":
    run_cpu_benchmark()
    run_io_benchmark()