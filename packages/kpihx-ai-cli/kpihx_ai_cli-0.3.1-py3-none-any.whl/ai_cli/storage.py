import os
import json
import datetime
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Configuration par défaut à créer lors de l'installation
DEFAULT_CONFIG_CONTENT = """# ═══════════════════════════════════════════════════════════════════════════════
#                              AI-CLI CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# Fichier généré automatiquement. Modifiez selon vos préférences.
# Documentation: https://github.com/KpihX/ai-cli

# ─────────────────────────────────────────────────────────────────────────────────
#                                 MODÈLE & API
# ─────────────────────────────────────────────────────────────────────────────────

default_model: phi3.5
ollama_url: http://localhost:11434
request_timeout: 60

# ─────────────────────────────────────────────────────────────────────────────────
#                           PARAMÈTRES DE GÉNÉRATION
# ─────────────────────────────────────────────────────────────────────────────────

temperature: 0.7          # 0.0 = déterministe, 2.0 = très créatif
max_output_length: 2048   # Tokens max en sortie (0 = illimité)
top_p: 0.9                # Nucleus sampling
repeat_penalty: 1.1       # Pénalité répétition (1.0 = désactivé)

# ─────────────────────────────────────────────────────────────────────────────────
#                              GESTION DU CONTEXTE
# ─────────────────────────────────────────────────────────────────────────────────

summary_threshold: 5      # Messages avant résumé automatique
history_dir: ~/.ai-cli

# ─────────────────────────────────────────────────────────────────────────────────
#                           PROMPTS SYSTÈME
# ─────────────────────────────────────────────────────────────────────────────────

prompts:
  title_generation: |
    Génère UN SEUL titre de 3-5 mots pour cette discussion.
    Réponds uniquement avec le titre, sans guillemets.
    Discussion: {content}

  summarization: |
    Résume de façon concise les points clés de cet échange:
    {content}

  memory_prefix: |
    [CONTEXTE] Informations sur l'utilisateur:
    {memory}

  welcome_message: "🤖 Bienvenue dans AI-CLI !"
  interactive_info: "Mode Interactif • Modèle: {model} • /help pour l'aide"
  goodbye_message: "👋 À bientôt !"

# ─────────────────────────────────────────────────────────────────────────────────
#                                 INTERFACE
# ─────────────────────────────────────────────────────────────────────────────────

user_style:
  border_color: cyan
  title: "👤 Vous"

ai_style:
  border_color: green
  title_template: "🤖 {model}"
"""


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
                    "Utilisez `/save <info>` pour ajouter des informations.\n",
                    encoding="utf-8"
                )
            # Créer la config par défaut si elle n'existe pas
            self.ensure_default_config()
        except OSError as e:
            logger.error(f"Failed to initialize storage directories: {e}")
            raise StorageError(f"Impossible d'initialiser le stockage: {e}") from e

    def ensure_default_config(self) -> bool:
        """Crée le fichier config.yaml par défaut s'il n'existe pas."""
        if not self.config_file.exists():
            try:
                self.config_file.write_text(DEFAULT_CONFIG_CONTENT, encoding="utf-8")
                logger.info(f"Created default config at {self.config_file}")
                return True
            except OSError as e:
                logger.warning(f"Could not create default config: {e}")
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
            raise StorageError(f"Session introuvable: {filename}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise StorageError(f"Session corrompue: {filename}") from e
        except OSError as e:
            raise StorageError(f"Erreur de lecture: {e}") from e

    def delete_session(self, filename: str) -> bool:
        """Supprime une session de l'historique.
        
        Args:
            filename: Le nom du fichier de session à supprimer.
            
        Returns:
            True si la suppression a réussi, False sinon.
            
        Raises:
            StorageError: Si la session n'existe pas ou si la suppression échoue.
        """
        filepath = self.sessions_dir / filename
        if not filepath.exists():
            raise StorageError(f"Session introuvable: {filename}")
        try:
            filepath.unlink()
            logger.info(f"Session supprimée: {filename}")
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


