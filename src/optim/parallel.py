import sys
import os
import time
from concurrent.futures import ProcessPoolExecutor

def init_worker(root_path):
    """Cette fonction sera exécutée au démarrage de CHAQUE nouveau processus."""
    if root_path not in sys.path:
        sys.path.insert(0, root_path)

def process_single_month(month_path):
    from src.pipeline.loaders import LoaderFactory
    from src.pipeline.profiling_test import compute_features_vectorized
    
    loader = LoaderFactory.create(month_path)
    df = loader.execute()
    df_processed = compute_features_vectorized(df)
    
    output_name = os.path.basename(month_path).replace(".parquet", "_proc.parquet")
    output_path = os.path.join("data", "processed", output_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_processed.to_parquet(output_path)
    return output_path

def process_months_parallel(month_paths, max_workers, root_path):
    # On utilise initializer pour préparer chaque processus enfant
    with ProcessPoolExecutor(
        max_workers=max_workers,
        initializer=init_worker,
        initargs=(root_path,)
    ) as executor:
        return list(executor.map(process_single_month, month_paths))

if __name__ == "__main__":
    # Définition du chemin racine
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    # On l'ajoute aussi au parent pour qu'il puisse lancer le premier test
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    test_files = ["data/raw/yellow_tripdata_2023-01.parquet"] * 4
    
    print(f"📂 Racine du projet : {project_root}")
    
    for w in [1, 2, 4]:
        start = time.time()
        print(f"🚀 Test avec {w} workers...")
        # On passe le project_root à l'orchestrateur
        process_months_parallel(test_files, w, project_root)
        print(f"⏱️  Temps : {time.time() - start:.2f}s")