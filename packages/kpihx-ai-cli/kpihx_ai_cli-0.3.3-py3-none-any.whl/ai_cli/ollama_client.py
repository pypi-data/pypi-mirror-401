import requests
import json
from typing import Generator, Optional, Dict, Any, List


class OllamaConnectionError(Exception):
    """Raised when connection to Ollama fails."""
    pass


class OllamaClient:
    def __init__(self, url: str, prompts: dict, timeout: int = 30):
        self.url = url
        self.prompts = prompts
        self.timeout = timeout
        # Paramètres de génération par défaut
        self.options: Dict[str, Any] = {}

    def set_options(self, 
                    temperature: Optional[float] = None,
                    max_tokens: Optional[int] = None,
                    top_p: Optional[float] = None,
                    repeat_penalty: Optional[float] = None):
        """Configure les paramètres de génération."""
        if temperature is not None:
            self.options["temperature"] = temperature
        if max_tokens is not None and max_tokens > 0:
            self.options["num_predict"] = max_tokens
        if top_p is not None:
            self.options["top_p"] = top_p
        if repeat_penalty is not None:
            self.options["repeat_penalty"] = repeat_penalty

    def _build_payload(self, model: str, messages: list, stream: bool) -> dict:
        """Construit le payload pour l'API Ollama."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        if self.options:
            payload["options"] = self.options
        return payload

    def chat_stream(self, model: str, messages: list) -> Generator[str, None, None]:
        """Chat with streaming response - yields chunks of text."""
        payload = self._build_payload(model, messages, stream=True)
        try:
            response = requests.post(
                f"{self.url}/api/chat",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            yield chunk["message"].get("content", "")
                    except json.JSONDecodeError:
                        continue
        except requests.exceptions.ConnectionError as e:
            yield f"[Erreur] Impossible de se connecter à Ollama ({self.url}): {e}"
        except requests.exceptions.Timeout:
            yield f"[Erreur] Timeout lors de la connexion à Ollama."
        except requests.exceptions.RequestException as e:
            yield f"[Erreur] Requête Ollama échouée: {e}"

    def chat_sync(self, model: str, messages: list) -> str:
        """Chat with synchronous response - returns full text."""
        payload = self._build_payload(model, messages, stream=False)
        try:
            response = requests.post(
                f"{self.url}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError(f"Impossible de se connecter à Ollama: {e}") from e
        except requests.exceptions.Timeout:
            raise OllamaConnectionError("Timeout lors de la connexion à Ollama.")
        except (KeyError, json.JSONDecodeError) as e:
            raise OllamaConnectionError(f"Réponse Ollama invalide: {e}") from e
        except requests.exceptions.RequestException as e:
            raise OllamaConnectionError(f"Requête Ollama échouée: {e}") from e

    def chat(self, model: str, messages: list, stream: bool = True):
        """Backward-compatible chat method."""
        if stream:
            return self.chat_stream(model, messages)
        else:
            return self.chat_sync(model, messages)

    def list_models(self) -> List[Dict[str, Any]]:
        """Liste tous les modèles disponibles sur le serveur Ollama."""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [
                {
                    "name": m["name"],
                    "size": m.get("size", 0),
                    "modified": m.get("modified_at", "")
                }
                for m in models
            ]
        except requests.exceptions.RequestException:
            return []

    def model_exists(self, name: str) -> bool:
        """Vérifie si un modèle existe (match exact ou par préfixe)."""
        models = self.list_models()
        model_names = [m["name"] for m in models]
        # Match exact ou avec tag :latest ou autre
        return any(
            m == name or 
            m.startswith(f"{name}:") or 
            m.split(":")[0] == name
            for m in model_names
        )

    def get_model_full_name(self, name: str) -> Optional[str]:
        """Retourne le nom complet du modèle (avec tag) s'il existe."""
        models = self.list_models()
        for m in models:
            model_name = m["name"]
            if model_name == name or model_name.startswith(f"{name}:") or model_name.split(":")[0] == name:
                return model_name
        return None

    def generate_title(self, model: str, messages: list) -> str:
        if not messages:
            return "Nouvelle Discussion"
        prompt_template = self.prompts.get("title_generation", "{content}")
        # Prendre les 3 premiers messages user pour plus de contexte
        user_messages = [m for m in messages if m.get('role') == 'user']
        if user_messages:
            # Combiner les premiers messages pour un meilleur contexte
            content_parts = [m['content'][:200] for m in user_messages[:3]]
            content = "\n".join(content_parts)
        else:
            content = messages[0]['content'][:500]
        full_prompt = prompt_template.format(content=content[:800])
        try:
            result = self.chat_sync(model, [{"role": "user", "content": full_prompt}])
            # Nettoyer le résultat de façon approfondie
            title = result.strip()
            # Supprimer les guillemets
            title = title.strip('"\'«»')
            # Prendre seulement la première ligne
            title = title.split('\n')[0]
            # Supprimer les caractères indésirables
            for char in ['#', '*', ':', '-', '—']:
                title = title.lstrip(char).strip()
            # Limiter la longueur
            return title[:60] if title else "Nouvelle Discussion"
        except OllamaConnectionError:
            return "Nouvelle Discussion"

    def summarize(self, model: str, messages: list) -> str:
        prompt_template = self.prompts.get("summarization", "{content}")
        text_to_summarize = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        full_prompt = prompt_template.format(content=text_to_summarize)
        try:
            return self.chat_sync(model, [{"role": "user", "content": full_prompt}])
        except OllamaConnectionError as e:
            return f"[Erreur de résumé: {e}]"

    def is_running(self) -> bool:
        try:
            response = requests.get(self.url, timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
