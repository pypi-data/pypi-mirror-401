import os
import json
import datetime
import logging
from pathlib import Path
from typing import Optional
import importlib.resources

logger = logging.getLogger(__name__)

# Configuration par défaut à créer lors de l'installation
# Sera chargé depuis default_config.yaml (inclus dans le package)

class StorageError(Exception):
    """Raised when storage operations fail."""
    pass


class StorageManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(os.path.expanduser(base_dir))
        self.sessions_dir = self.base_dir / "sessions"
        self.memory_file = self.base_dir / "AI_CLI.md"
        self.config_file = self.base_dir / "config.yaml"
        
        try:
            self.sessions_dir.mkdir(parents=True, exist_ok=True)
            if not self.memory_file.exists():
                self.memory_file.write_text(
                    "# Mémoire de l'utilisateur\n\n"
                    "Informations sur l'utilisateur pour l'agent.\n"
                    "Utilisez `/memory add <info>` pour ajouter des informations.\n",
                    encoding="utf-8"
                )
            # Créer la config par défaut si elle n'existe pas
            self.ensure_default_config()
        except OSError as e:
            logger.error(f"Failed to initialize storage directories: {e}")
            raise StorageError(f"Impossible d'initialiser le stockage: {e}") from e

    def ensure_default_config(self) -> bool:
        """Crée le fichier config.yaml par défaut (copié du package) s'il n'existe pas."""
        if not self.config_file.exists():
            try:
                # Lire le fichier default_config.yaml inclus dans le package
                default_config = importlib.resources.files("ai_cli").joinpath("default_config.yaml").read_text(encoding="utf-8")
                
                self.config_file.write_text(default_config, encoding="utf-8")
                logger.info(f"Created default config at {self.config_file}")
                return True
            except (OSError, ImportError, FileNotFoundError) as e:
                logger.warning(f"Could not create default config: {e}")
                # Fallback minimal si jamais le fichier ressource est introuvable
                if not self.config_file.exists():
                     self.config_file.write_text("default_model: phi3.5\n", encoding="utf-8")
                return False
        return False

    def get_config_path(self) -> Optional[Path]:
        """Retourne le chemin du fichier de configuration s'il existe."""
        return self.config_file if self.config_file.exists() else None

    def save_session(self, messages: list, title: str) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(x for x in title if x.isalnum() or x in " -_").strip()
        if not safe_title:
            safe_title = "session"
        filename = f"{timestamp}_{safe_title}.json"
        filepath = self.sessions_dir / filename
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"title": title, "timestamp": timestamp, "messages": messages}, f, indent=4, ensure_ascii=False)
        except OSError as e:
            logger.error(f"Failed to save session {filename}: {e}")
            raise StorageError(f"Impossible de sauvegarder la session: {e}") from e
        return filename

    def list_sessions(self, limit: int = 10) -> list:
        try:
            files = sorted(self.sessions_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
        except OSError as e:
            logger.warning(f"Failed to list sessions: {e}")
            return []
        
        sessions = []
        for f in files[:limit]:
            try:
                with open(f, "r", encoding="utf-8") as src:
                    data = json.load(src)
                    sessions.append({
                        "file": f.name,
                        "title": data.get("title", "Sans titre"),
                        "time": data.get("timestamp", "Inconnu")
                    })
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Skipping corrupted session file {f.name}: {e}")
                continue
        return sessions

    def load_session(self, filename: str) -> dict:
        filepath = self.sessions_dir / filename
        if not filepath.exists():
            raise StorageError(f"Session {filename} introuvable.")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load session {filename}: {e}")
            raise StorageError(f"Impossible de charger la session: {e}") from e

    def delete_session(self, filename: str) -> bool:
        """Supprime une session de l'historique."""
        filepath = self.sessions_dir / filename
        if not filepath.exists():
            raise StorageError(f"Session {filename} introuvable.")
        
        try:
            filepath.unlink()
            return True
        except OSError as e:
            logger.error(f"Échec suppression session {filename}: {e}")
            raise StorageError(f"Impossible de supprimer la session: {e}") from e

    def save_memory(self, content: str, mode: str = "append"):
        try:
            if mode == "append":
                with open(self.memory_file, "a", encoding="utf-8") as f:
                    f.write(f"\n- {content}")
            else:
                self.memory_file.write_text(content, encoding="utf-8")
        except OSError as e:
            logger.error(f"Failed to save memory: {e}")
            raise StorageError(f"Impossible de sauvegarder la mémoire: {e}") from e

    def get_memory(self) -> str:
        try:
            return self.memory_file.read_text(encoding="utf-8")
        except OSError as e:
            logger.warning(f"Failed to read memory: {e}")
            return ""

    def get_memory_entries(self) -> list:
        """Retourne la liste des entrées de mémoire (lignes commençant par '- ')."""
        memory = self.get_memory()
        entries = []
        for line in memory.split('\n'):
            stripped = line.strip()
            if stripped.startswith('- '):
                entries.append(stripped[2:])  # Enlever le '- ' du début
        return entries

    def delete_memory_entry(self, index: int) -> bool:
        """Supprime une entrée de mémoire par son index (0-based). Retourne True si succès."""
        entries = self.get_memory_entries()
        if index < 0 or index >= len(entries):
            return False
        
        # Reconstruire le fichier sans l'entrée supprimée
        memory = self.get_memory()
        lines = memory.split('\n')
        new_lines = []
        entry_count = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- '):
                if entry_count == index:
                    entry_count += 1
                    continue  # Sauter cette ligne
                entry_count += 1
            new_lines.append(line)
        
        try:
            self.memory_file.write_text('\n'.join(new_lines), encoding="utf-8")
            return True
        except OSError as e:
            logger.error(f"Failed to delete memory entry: {e}")
            return False
