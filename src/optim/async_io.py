import asyncio
import aiohttp
import os
import time
from tqdm.asyncio import tqdm

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"

async def download_month(session, year, month, dest_dir, semaphore):
    """Télécharge un fichier pour un mois donné avec gestion de concurrence."""
    url = BASE_URL.format(year=year, month=month)
    filename = os.path.join(dest_dir, f"yellow_tripdata_{year}-{month:02d}.parquet")
    
    async with semaphore: # Limite le nombre de téléchargements simultanés
        async with session.get(url) as response:
            if response.status == 200:
                # Lecture et écriture asynchrone par morceaux (chunks)
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024 * 1024) # 1MB
                        if not chunk:
                            break
                        f.write(chunk)
                return True
            else:
                print(f"❌ Erreur {response.status} pour le mois {month}")
                return False

async def download_year(year, dest_dir, concurrency=4):
    """Orchestre le téléchargement des 12 mois."""
    os.makedirs(dest_dir, exist_ok=True)
    semaphore = asyncio.Semaphore(concurrency)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for month in range(1, 13):
            tasks.append(download_month(session, year, month, dest_dir, semaphore))
        
        # 45. Bonus : Barre de progression tqdm
        results = await tqdm.gather(*tasks, desc=f"Téléchargement {year}")
        return results

if __name__ == "__main__":
    start = time.time()
    # On lance l'événement principal
    asyncio.run(download_year(2023, "data/raw", concurrency=4))
    print(f"⏱️ Temps total asynchrone : {time.time() - start:.2f}s")