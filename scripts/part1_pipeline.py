import sys
import os

# Détection dynamique du dossier racine (tp_taxi)
current_script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_script_path))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Test de diagnostic avant l'import
orchestrator_path = os.path.join(project_root, "src", "pipeline", "orchestrator.py")
if not os.path.exists(orchestrator_path):
    print(f"❌ ERREUR CRITIQUE : Fichier introuvable à l'emplacement : {orchestrator_path}")
else:
    print(f"✅ Fichier trouvé : {orchestrator_path}")

try:
    from src.pipeline.orchestrator import Pipeline
    print("✅ Module orchestrator importé avec succès !")
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    sys.exit(1)
    
    # 2. Instanciation via Factory
    loader = LoaderFactory.create(raw_path)
    
    # 3. Attacher un Observer au loader
    loader.attach(LoggingObserver())
    loader.attach(MetricsObserver())
    
    # 4. Création du Pipeline (Orchestrateur)
    pipeline = Pipeline(steps=[loader])
    
    # 5. Exécution
    print("🚀 Lancement du Pipeline d'intégration...")
    final_df = pipeline.run()
    
    # 6. Persistance via le Mixin
    output_path = os.path.join(root_path, "data", "processed", "part1_result.pkl")
    pipeline.to_pickle(final_df, output_path)
    
    print("\n✅ Partie 1 terminée avec succès !")
    print(f"Shape finale : {final_df.shape}")

if __name__ == "__main__":
    main()