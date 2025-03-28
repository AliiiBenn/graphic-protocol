# Protocole de Communication Graphique

Ce projet vise à créer un nouveau protocole de communication graphique inspiré des QR codes, mais avec des fonctionnalités innovantes et une meilleure capacité de stockage.

## 🎯 Objectif

Développer un protocole de communication graphique capable de :
- Encoder des messages texte dans une matrice graphique
- Supporter différentes tailles de matrices
- Inclure des mécanismes de correction d'erreurs
- Être résistant aux distorsions et rotations
- Offrir des fonctionnalités innovantes (multi-couleurs, formes alternatives)

## 🚀 Pour Commencer

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd qr-code
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 📁 Structure du Projet

Le projet suit une architecture modulaire :

- `src/` : Code source du projet
  - `encoder/` : Modules d'encodage
  - `decoder/` : Modules de décodage
  - `utils/` : Utilitaires et configuration
- `tests/` : Tests unitaires et d'intégration
- `docs/` : Documentation du projet

## 📖 Documentation

- [Plan de Développement](docs/development_plan.md)
- [Spécifications Techniques](docs/technical_specs.md)
- [Guide Utilisateur](docs/user_guide.md)

## 🛠️ Développement

Pour contribuer au projet :

1. Consultez le [Plan de Développement](docs/development_plan.md)
2. Choisissez une tâche à implémenter
3. Créez une branche pour votre fonctionnalité
4. Développez et testez votre code
5. Soumettez une pull request

## 🧪 Tests

Pour exécuter les tests :

```bash
pytest tests/
```

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails. #   g r a p h i c - p r o t o c o l  
 