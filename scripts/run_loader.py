import sys
import os

# On remonte de 'scripts' à la racine 'tp_taxi'
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))

# On ajoute explicitement le dossier racine au chemin de recherche
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# TEST DE PRÉSENCE (pour le rapport de debug)
print(f"--- Debug ---")
print(f"Root: {root_path}")
print(f"Check src: {os.path.exists(os.path.join(root_path, 'src'))}")
print(f"Check loaders: {os.path.exists(os.path.join(root_path, 'src', 'pipeline', 'loaders.py'))}")
print(f"-------------\n")

try:
    from src.pipeline.loaders import LoaderFactory
    from src.core.config import Config
    print("✅ Imports réussis !")
except Exception as e:
    print(f"❌ Échec de l'import : {e}")
    sys.exit(1)