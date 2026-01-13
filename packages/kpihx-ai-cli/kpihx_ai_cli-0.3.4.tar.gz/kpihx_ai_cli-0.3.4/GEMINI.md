# Gemini Context: ai-cli

## 1. 👤 Identité du Projet
- **Nom :** ai-cli
- **Version :** 0.3.0
- **Auteur :** KAMDEM POUOKAM Ivann Harold (@KpihX)
- **Objectif :** Fournir une interface CLI robuste, intelligente et hautement configurable pour interagir avec des modèles LLM locaux via Ollama.

## 2. 💻 Profil Technique & Architecture
- **Langage :** Python 3.11+
- **Gestionnaire de dépendances :** `uv` (utilisé pour l'initialisation, le packaging et les tests).
- **Stack logicielle :**
  - `typer` : Gestion de la CLI et des arguments.
  - `rich` : Rendu visuel (Markdown, Panels, Live, Tables).
  - `prompt_toolkit` : Saisie interactive avancée (auto-suggestions, historique, complétion Tab).
  - `requests` : Communication avec l'API REST d'Ollama.
  - `pyyaml` : Gestion de la configuration externalisée.
- **Structure Modulaire :**
  - `main.py` : Point d'entrée, boucle REPL et routage des commandes slash.
  - `storage.py` : Gestion de la persistance (JSON sessions et mémoire Markdown).
  - `ollama_client.py` : Abstraction de l'API Ollama avec méthodes séparées `chat_stream()` / `chat_sync()`.

## 3. ⚙️ Fonctionnalités Clés
- **Zéro Hardcoding :** Tous les prompts système (génération de titre, résumé, mémoire) sont dans `config.yaml`.
- **Gestion d'Historique :** Stockage automatique dans `~/.ai-cli/sessions/` au format JSON avec support UTF-8.
- **Mémoire Persistante :** Utilisation de `~/.ai-cli/AI_CLI.md` pour injecter des connaissances sur l'utilisateur dans chaque session.
- **Optimisation de Contexte :** Commande `/resume` pour compresser les anciens messages via un résumé LLM sans perdre le fil de la discussion.
- **Auto-gestion d'Ollama :** Détection automatique du serveur, démarrage si nécessaire, et téléchargement (`pull`) transparent des modèles manquants.
- **Gestion d'Erreurs Robuste :** Exceptions personnalisées (`OllamaConnectionError`, `StorageError`) avec logging approprié.
- **Options CLI avancées :** `-l` pour lister les modèles, `-d` pour changer le modèle par défaut, `-m` pour utiliser un modèle spécifique.

## 4. 🛠 Workflow de Développement
- **Installation :** `uv tool install .` ou `pipx install .`
- **Tests :** 46 tests unitaires avec `pytest` et `pytest-mock` situés dans le dossier `tests/`.
  - `test_main.py` : 12 tests (config, SessionState, slash commands)
  - `test_client.py` : 16 tests (stream, sync, erreurs réseau)
  - `test_storage.py` : 18 tests (CRUD, Delete, Unicode, edge cases)
- **Conventions :** Adhésion stricte aux standards de modularité et de séparation des préoccupations (SOC).

## 5. 🧠 Commandes Slash Supportées
- `/new` : Archive la session actuelle et en démarre une nouvelle.
- `/old` : Liste, charge ou supprime des discussions précédentes.
- `/save <info>` : Enregistre un fait dans `AI_CLI.md`.
- `/resume` : Résume l'historique au-delà du `summary_threshold`.
- `/settings` : Modifie les paramètres de session (modèle, température, etc.).
- `/clear` : Nettoie l'interface.
- `/help` : Affiche l'aide des commandes disponibles.
- `/exit` : Quitte proprement avec sauvegarde.

## 6. 🏗️ Architecture des Modules

### ollama_client.py
- `OllamaClient` : Classe principale avec méthodes :
  - `chat_stream()` : Générateur pour réponses en streaming
  - `chat_sync()` : Appel synchrone retournant la réponse complète
  - `chat()` : Wrapper backward-compatible
  - `generate_title()` / `summarize()` : Utilitaires LLM (titre amélioré avec multi-contexte)
  - `is_running()` / `list_models()` / `model_exists()` : Gestion modèles
- `OllamaConnectionError` : Exception personnalisée

### storage.py
- `StorageManager` : Gestion fichiers avec :
  - `save_session()` / `load_session()` / `list_sessions()` / `delete_session()`
  - `save_memory()` / `get_memory()`
  - `ensure_default_config()` / `get_config_path()`
  - Support UTF-8, gestion fichiers corrompus
- `StorageError` : Exception personnalisée

### main.py
- `SessionState` : État de la conversation avec paramètres modifiables
- `load_config()` : Chargement config YAML avec fallback
- `run_interactive()` : Boucle REPL principale avec Ctrl+C handling
- `handle_save_and_exit()` : Sauvegarde avec suggestion de titre améliorée
- `display_models_list()` / `update_default_model_in_config()` : Gestion modèles CLI
