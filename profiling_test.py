import pandas as pd
import numpy as np
import math
import time
import os

# Le décorateur @profile est injecté par kernprof au runtime.
# Si vous lancez avec 'python', il faut définir un décorateur vide pour éviter une NameError.
if 'profile' not in __builtins__:
    def profile(func): return func

@profile
def compute_features_naive(df):
    results = []
    for index, row in df.iterrows():
        # 1. Calcul de la durée en minutes
        duration = (row['tpep_dropoff_datetime'] - row['tpep_pickup_datetime']).total_seconds() / 60
        
        # 2. Calcul de la vitesse (mph)
        speed = row['trip_distance'] / (duration / 60) if duration > 0 else 0
        
        # 3. Calcul de la pénalité
        penalty = 0.5 * (row['trip_distance'] ** 2) + math.log(abs(row['fare_amount']) + 1)
        
        results.append({
            'duration': duration,
            'speed': speed,
            'penalty': penalty
        })

    # SORTIE DE LA BOUCLE : Le return doit être aligné avec le 'for'
    return pd.DataFrame(results)

def compute_features_vectorized(df):
    """Version vectorisée exploitant NumPy et les Series Pandas."""
    # 1. Durée (vectorisée)
    duration = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # 2. Vitesse (vectorisée)
    speed = df['trip_distance'] / (duration / 60)
    speed = speed.replace([np.inf, -np.inf], 0).fillna(0)
    
    # 3. Pénalité (vectorisée avec np.log1p)
    penalty = 0.5 * (df['trip_distance'] ** 2) + np.log1p(df['fare_amount'].abs())
    
    return pd.DataFrame({
        'duration': duration,
        'speed': speed,
        'penalty': penalty
    })

if __name__ == "__main__":
    # --- 1. Chargement des données ---
    path = "data/raw/yellow_tripdata_2023-01.parquet"
    
    if os.path.exists(path):
        print(f"📂 Chargement de {path}...")
        # On limite à 20 000 lignes pour que le profilage naïf ne soit pas trop long
        df_sample = pd.read_parquet(path).head(20000)
        
        # --- 2. Profilage ligne par ligne (kernprof) ---
        print("🚀 Lancement du profilage de la fonction naïve...")
        compute_features_naive(df_sample)
        
        # --- 3. Benchmark de comparaison (Speedup) ---
        print("\n--- Benchmark de performance ---")
        
        # Chrono Naïf
        start_n = time.time()
        _ = compute_features_naive(df_sample)
        time_naive = time.time() - start_n
        
        # Chrono Vectorisé
        start_v = time.time()
        _ = compute_features_vectorized(df_sample)
        time_vectorized = time.time() - start_v
        
        print(f"⏱️  Temps Naïf (iterrows) : {time_naive:.4f}s")
        print(f"⏱️  Temps Vectorisé (Pandas) : {time_vectorized:.4f}s")
        
        if time_vectorized > 0:
            speedup = time_naive / time_vectorized
            print(f"🚀 Speedup : {speedup:.1f}x")
        
        print("\n✅ Test terminé.")
    else:
        print(f"❌ Erreur : Le fichier {path} est introuvable. Vérifiez le chemin.")