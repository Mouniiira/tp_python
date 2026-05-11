import time
import psutil
import tracemalloc
import pandas as pd
from contextlib import contextmanager
from contextlib import ExitStack

# 23. Version Classe : Timer
class Timer:
    def __init__(self, description="Opération"):
        self.description = description

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (time.perf_counter() - self.start) * 1000
        print(f"[Timer] {self.description} : {duration:.2f} ms")

# 24. Version Classe : MemoryGuard
class MemoryGuard:
    def __init__(self, threshold_mb=2000):
        self.threshold = threshold_mb
        self.process = psutil.Process()

    def __enter__(self):
        self.initial_mem = self.process.memory_info().rss / (1024 * 1024)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_mem = self.process.memory_info().rss / (1024 * 1024)
        consumed = current_mem - self.initial_mem
        
        print(f"📊 Mémoire consommée dans le bloc : {consumed:.2f} MB")
        if current_mem > self.threshold:
            raise MemoryError(f"Seuil de {self.threshold}MB dépassé ({current_mem:.2f}MB)")

# 25. Version Générateur : temp_dtypes
@contextmanager
def temp_dtypes(df: pd.DataFrame, mapping: dict):
    """Change temporairement les types de colonnes pour une opération spécifique."""
    # Sauvegarde des types originaux
    original_dtypes = {col: df[col].dtype for col in mapping.keys() if col in df.columns}
    
    try:
        # Application des types temporaires
        print(f"🔄 Conversion temporaire : {list(mapping.keys())}")
        for col, new_dtype in mapping.items():
            if col in df.columns:
                df[col] = df[col].astype(new_dtype)
        yield df
    finally:
        # Restauration systématique, même en cas d'erreur dans le bloc with
        print("⏪ Restauration des types originaux...")
        for col, old_dtype in original_dtypes.items():
            df[col] = df[col].astype(old_dtype)

# Démonstration : Stack de contextes et cumul

def process_taxi_data(path):
    df = pd.read_parquet(path)
    
    # On utilise ExitStack pour gérer plusieurs contextes proprement
    with ExitStack() as stack:
        # 1. Surveiller le temps
        stack.enter_context(Timer("Traitement lourd"))
        
        # 2. Surveiller la mémoire (ex: seuil à 1 Go pour le test)
        stack.enter_context(MemoryGuard(threshold_mb=1000))
        
        # 3. Optimisation temporaire des types pour économiser de la RAM
        # On passe PULocationID en int16 au lieu de int64
        mapping = {"PULocationID": "int16", "DOLocationID": "int16"}
        stack.enter_context(temp_dtypes(df, mapping))
        
        # --- Corps de l'opération ---
        print(f"Type actuel de PULocationID : {df['PULocationID'].dtype}")
        # Simulation d'un calcul
        _ = df.groupby("PULocationID")["total_amount"].mean()

    # À la sortie du bloc, les types originaux sont restaurés automatiquement
    print(f"Type après restauration : {df['PULocationID'].dtype}")

if __name__ == "__main__":
    # Test avec un DataFrame fictif
    dummy_df = pd.DataFrame({
        "PULocationID": [1, 2, 3], 
        "DOLocationID": [4, 5, 6],
        "total_amount": [10.0, 15.0, 20.0]
    })
    
    # Pour le test, on simule l'appel
    with ExitStack() as stack:
        stack.enter_context(Timer("Démo globale"))
        # ... vos opérations ici