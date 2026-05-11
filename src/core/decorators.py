import time
import logging
import functools
import pandas as pd
from collections import OrderedDict

# 18. @timeit - Gère @timeit et @timeit(unit="ms")
def timeit(func=None, *, unit="s"):
    if func is None:
        return lambda f: timeit(f, unit=unit)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        if unit == "ms":
            print(f"⏱️  {func.__name__} exécuté en {duration * 1000:.2f} ms")
        else:
            print(f"⏱️  {func.__name__} exécuté en {duration:.4f} s")
        return result
    return wrapper

# 19. @log_calls
def log_calls(level="INFO", log_args=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("pipeline")
            if log_args:
                msg = f"📞 Appel à {func.__name__} | Args: {args} Kwargs: {kwargs}"
            else:
                msg = f"📞 Appel à {func.__name__}"
            
            logger.log(getattr(logging, level.upper()), msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 20. @retry avec délai exponentiel
def retry(max_attempts=3, backoff=2.0, exceptions=(IOError,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = 1.0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise e
                    print(f"🔄 Tentative {attempt}/{max_attempts} échouée pour {func.__name__}. "
                          f"Nouvel essai dans {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

# 21. @memoize_dataframe (Cache LRU basé sur le contenu du DF)
def memoize_dataframe(maxsize=4):
    cache = OrderedDict()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # On cherche les dataframes dans les arguments pour le hash
            df_args = [a for a in args if isinstance(a, pd.DataFrame)]
            if not df_args:
                return func(*args, **kwargs)
            
            # Hashage du contenu du DataFrame
            df_hash = hash(tuple(pd.util.hash_pandas_object(df_args[0]).values))
            
            if df_hash in cache:
                print(f"🧠 Cache HIT pour {func.__name__}")
                return cache[df_hash]
            
            result = func(*args, **kwargs)
            
            # Gestion LRU
            if len(cache) >= maxsize:
                cache.popitem(last=False)
            cache[df_hash] = result
            return result
        return wrapper
    return decorator

# Demo du chainage
# Configuration minimale du logging pour le test
logging.basicConfig(level=logging.INFO)

@retry(max_attempts=2, exceptions=(ValueError,))
@timeit(unit="ms")
@log_calls(log_args=True)
def load_month(year, month):
    print(f"--- Simulation du chargement de {year}-{month:02d} ---")
    # Simule un échec aléatoire pour tester le retry
    if time.time() % 2 > 1:
        raise ValueError("Erreur réseau fictive")
    return pd.DataFrame({"trip_id": [1, 2, 3]})

if __name__ == "__main__":
    try:
        df = load_month(2023, 1)
        print("✅ Résultat obtenu")
    except Exception as e:
        print(f"❌ Échec final : {e}")