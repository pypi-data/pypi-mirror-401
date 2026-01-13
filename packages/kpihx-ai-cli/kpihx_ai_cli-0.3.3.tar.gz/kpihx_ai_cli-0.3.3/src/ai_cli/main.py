import os
import sys
import time
import signal
import yaml
import requests
import subprocess
import typer
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML

from .storage import StorageManager
from .ollama_client import OllamaClient

app = typer.Typer()
console = Console()

# ═══════════════════════════════════════════════════════════════════════════════
#                              CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    "default_model": "phi3.5",
    "ollama_url": "http://localhost:11434",
    "summary_threshold": 5,
    "history_dir": "~/.ai-cli",
    "request_timeout": 60,
    "temperature": 0.7,
    "max_output_length": 2048,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
    "prompts": {
        "title_generation": "Génère un titre court (3-5 mots) pour: {content}",
        "summarization": "Résume les points clés: {content}",
        "memory_prefix": "Contexte utilisateur: {memory}",
        "welcome_message": "🤖 Bienvenue dans AI-CLI !",
        "interactive_info": "Mode Interactif • Modèle: {model} • /help pour l'aide",
        "goodbye_message": "👋 À bientôt !"
    },
    "user_style": {"border_color": "cyan", "title": "👤 Vous"},
    "ai_style": {"border_color": "green", "title_template": "🤖 {model}"}
}


def load_config() -> Dict[str, Any]:
    """Charge la configuration depuis config.yaml ou utilise les valeurs par défaut."""
    paths = [
        os.path.join(os.getcwd(), "config.yaml"),
        os.path.expanduser("~/.ai-cli/config.yaml")
    ]
    config = DEFAULT_CONFIG.copy()
    
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}
                    # Merge profond
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in config:
                            config[key].update(value)
                        else:
                            config[key] = value
                    break
            except (yaml.YAMLError, OSError):
                continue
    
    return config


# ═══════════════════════════════════════════════════════════════════════════════
#                              ÉTAT DE SESSION
# ═══════════════════════════════════════════════════════════════════════════════

class SessionState:
    def __init__(self, model: str, config: Dict[str, Any]):
        self.model = model
        self.messages = []
        self.title = "Nouvelle Discussion"
        self.config = config
        # Paramètres modifiables en cours de session
        self.temperature = config.get("temperature", 0.7)
        self.max_output_length = config.get("max_output_length", 2048)
        self.top_p = config.get("top_p", 0.9)
        self.repeat_penalty = config.get("repeat_penalty", 1.1)
        # Gestion interruption
        self.interrupted = False
        self.last_interrupt_time = 0


# ═══════════════════════════════════════════════════════════════════════════════
#                         SLASH COMMANDS COMPLETION
# ═══════════════════════════════════════════════════════════════════════════════

SLASH_COMMANDS = [
    '/help', '/new', '/old', '/memory', '/resume', 
    '/clear', '/settings', '/exit'
]

def get_slash_completer():
    """Retourne un completer pour les commandes slash."""
    return WordCompleter(
        SLASH_COMMANDS,
        ignore_case=True,
        sentence=True,
        match_middle=False
    )


# ═══════════════════════════════════════════════════════════════════════════════
#                              AFFICHAGE
# ═══════════════════════════════════════════════════════════════════════════════

def display_welcome(storage: StorageManager, config: Dict[str, Any]):
    """Affiche le message de bienvenue et les sessions récentes."""
    sessions = storage.list_sessions(5)
    welcome_msg = config.get("prompts", {}).get("welcome_message", "Bienvenue")
    
    console.print()
    console.print(Panel(
        f"[bold green]{welcome_msg}[/bold green]",
        border_style="green",
        padding=(0, 2)
    ))
    
    if sessions:
        table = Table(
            title="📚 Discussions Récentes",
            show_header=True,
            header_style="bold magenta",
            border_style="dim"
        )
        table.add_column("", style="dim", width=3)
        table.add_column("Titre", style="white")
        table.add_column("Date", style="dim")
        
        for i, s in enumerate(sessions):
            table.add_row(str(i+1), s['title'], s['time'])
        
        console.print(table)
        console.print("[dim]💡 Utilisez /old pour charger une ancienne discussion.[/dim]\n")


def display_user_message(content: str, config: Dict[str, Any]):
    """Affiche le message de l'utilisateur (sans panel pour éviter duplication)."""
    # Pas de Panel pour éviter duplication visuelle avec le prompt
    pass  # Le message est déjà affiché dans le prompt, pas besoin de le ré-afficher


def display_settings_menu(state: SessionState, client: OllamaClient):
    """Affiche et permet de modifier les paramètres."""
    console.print()
    console.print(Panel(
        "[bold]⚙️ Paramètres de Session[/bold]",
        border_style="yellow"
    ))
    
    # Afficher les paramètres actuels
    table = Table(show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("Paramètre", style="white")
    table.add_column("Valeur Actuelle", style="green")
    table.add_column("Description", style="dim")
    
    table.add_row("1. Modèle", state.model, "LLM utilisé")
    table.add_row("2. Température", str(state.temperature), "0.0=déterministe, 2.0=créatif")
    table.add_row("3. Max Output", str(state.max_output_length), "Tokens max en sortie")
    table.add_row("4. Top-P", str(state.top_p), "Nucleus sampling")
    table.add_row("5. Repeat Penalty", str(state.repeat_penalty), "Pénalité répétition")
    
    console.print(table)
    console.print("\n[dim]Entrez le numéro du paramètre à modifier (0 pour annuler):[/dim]")
    
    try:
        choice = IntPrompt.ask("Choix", default=0)
        
        if choice == 1:
            # Changer de modèle
            models = client.list_models()
            if not models:
                console.print("[red]Aucun modèle disponible.[/red]")
                return
            
            console.print("\n[bold]Modèles disponibles:[/bold]")
            for i, m in enumerate(models):
                size_mb = m.get("size", 0) / (1024 * 1024 * 1024)
                current = "✓ " if m["name"].startswith(state.model) else "  "
                console.print(f"  {current}[cyan]{i+1}.[/cyan] {m['name']} [dim]({size_mb:.1f} GB)[/dim]")
            
            idx = IntPrompt.ask("\nNuméro du modèle", default=1)
            if 1 <= idx <= len(models):
                state.model = models[idx-1]["name"]
                console.print(f"[green]Modèle changé en: {state.model}[/green]")
        
        elif choice == 2:
            new_temp = Prompt.ask("Nouvelle température (0.0-2.0)", default=str(state.temperature))
            state.temperature = max(0.0, min(2.0, float(new_temp)))
            console.print(f"[green]Température: {state.temperature}[/green]")
        
        elif choice == 3:
            new_max = IntPrompt.ask("Max output length (0=illimité)", default=state.max_output_length)
            state.max_output_length = max(0, new_max)
            console.print(f"[green]Max output: {state.max_output_length}[/green]")
        
        elif choice == 4:
            new_top_p = Prompt.ask("Top-P (0.0-1.0)", default=str(state.top_p))
            state.top_p = max(0.0, min(1.0, float(new_top_p)))
            console.print(f"[green]Top-P: {state.top_p}[/green]")
        
        elif choice == 5:
            new_rp = Prompt.ask("Repeat penalty (1.0=off)", default=str(state.repeat_penalty))
            state.repeat_penalty = max(1.0, float(new_rp))
            console.print(f"[green]Repeat penalty: {state.repeat_penalty}[/green]")
            
    except (ValueError, KeyboardInterrupt):
        console.print("[dim]Annulé.[/dim]")


def display_help():
    """Affiche l'aide des commandes."""
    help_text = """
[bold cyan]Commandes disponibles:[/bold cyan]

  [green]/help[/green]     📚 Affiche cette aide
  [green]/new[/green]      🆕 Sauvegarder et démarrer une nouvelle discussion
  [green]/old[/green]      📂 Charger ou supprimer une discussion
  [green]/memory[/green]   🧠 Gérer la mémoire (voir, ajouter, supprimer)
  [green]/resume[/green]   📝 Résumer l'historique pour libérer du contexte
  [green]/settings[/green] ⚙️  Modifier les paramètres (modèle, température...)
  [green]/clear[/green]    🧹 Effacer l'écran
  [green]/exit[/green]     👋 Sauvegarder et quitter

[dim]Raccourcis: Ctrl+D = /exit, Ctrl+C (x2 rapide) = exit forcé[/dim]
"""
    console.print(Panel(help_text.strip(), title="Aide", border_style="cyan"))


# ═══════════════════════════════════════════════════════════════════════════════
#                         GESTION SAUVEGARDE & EXIT
# ═══════════════════════════════════════════════════════════════════════════════

def handle_save_only(state: SessionState, storage: StorageManager, client: OllamaClient) -> Optional[str]:
    """Sauvegarde la session sans quitter. Retourne le titre si sauvegardé, None sinon."""
    if not state.messages:
        return None
    
    suggested_title = client.generate_title(state.model, state.messages)
    console.print(f"\n[yellow]💾 Sauvegarde de la discussion...[/yellow]")
    console.print(f"Proposition de titre: [dim]{suggested_title}[/dim]")
    
    history = InMemoryHistory()
    history.append_string(suggested_title)
    
    try:
        user_title = pt_prompt(
            "Titre (Tab=accepter, Entrée=valider): ",
            auto_suggest=AutoSuggestFromHistory(),
            history=history
        )
    except (EOFError, KeyboardInterrupt):
        user_title = suggested_title

    final_title = user_title.strip() or suggested_title
    storage.save_session(state.messages, final_title)
    console.print(f"[green]✓ Session enregistrée: {final_title}[/green]")
    return final_title


def handle_save_and_exit(state: SessionState, storage: StorageManager, client: OllamaClient, config: Dict[str, Any]):
    """Sauvegarde la session et quitte proprement."""
    goodbye_msg = config.get("prompts", {}).get("goodbye_message", "À bientôt !")
    
    if not state.messages:
        console.print(f"\n[green]{goodbye_msg}[/green]")
        sys.exit(0)
    
    handle_save_only(state, storage, client)
    console.print(f"[green]{goodbye_msg}[/green]")
    sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════════════
#                              BOUCLE INTERACTIVE
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive(state: SessionState, storage: StorageManager, client: OllamaClient, config: Dict[str, Any]):
    """Boucle REPL principale avec gestion Ctrl+C améliorée."""
    
    # Afficher info mode interactif
    info_msg = config.get("prompts", {}).get("interactive_info", "Mode Interactif")
    console.print(f"[dim]{info_msg.format(model=state.model)}[/dim]\n")
    
    # Completer pour les commandes slash
    slash_completer = get_slash_completer()
    
    while True:
        try:
            # Reset flag interruption
            state.interrupted = False
            
            # Prompt avec auto-complétion
            user_input = pt_prompt(
                HTML('<ansigreen><b>Vous</b></ansigreen> <ansicyan>❯</ansicyan> '),
                completer=slash_completer,
                complete_while_typing=False,
                auto_suggest=AutoSuggestFromHistory()
            ).strip()
            
        except EOFError:
            # Ctrl+D
            handle_save_and_exit(state, storage, client, config)
            break
        except KeyboardInterrupt:
            # Ctrl+C pendant l'input
            now = time.time()
            if now - state.last_interrupt_time < 1.5:
                # Double Ctrl+C rapide = exit forcé
                console.print("\n[yellow]Exit forcé...[/yellow]")
                handle_save_and_exit(state, storage, client, config)
                break
            state.last_interrupt_time = now
            console.print("\n[dim]Ctrl+C détecté. Appuyez encore une fois rapidement pour quitter.[/dim]")
            continue

        if not user_input:
            continue

        # ─────────────────────────────────────────────────────────────────────
        #                         COMMANDES SLASH
        # ─────────────────────────────────────────────────────────────────────
        if user_input.startswith("/"):
            cmd_parts = user_input.split(maxsplit=1)
            cmd = cmd_parts[0].lower()
            args = cmd_parts[1] if len(cmd_parts) > 1 else ""
            
            if cmd == "/exit":
                handle_save_and_exit(state, storage, client, config)
                break
            
            elif cmd == "/clear":
                console.clear()
                continue
            
            elif cmd == "/help":
                display_help()
                continue
            
            elif cmd == "/new":
                if state.messages:
                    handle_save_only(state, storage, client)
                state.messages = []
                state.title = "Nouvelle Discussion"
                console.clear()
                console.print(Panel(
                    "[bold green]🆕 Nouvelle discussion démarrée.[/bold green]",
                    border_style="green"
                ))
                continue
            
            elif cmd == "/old":
                sessions = storage.list_sessions(20)
                if not sessions:
                    console.print("[red]Aucun historique trouvé.[/red]")
                    continue
                
                console.print("\n[bold]📂 Sessions disponibles:[/bold]")
                table = Table(show_header=True, header_style="bold cyan", border_style="dim")
                table.add_column("#", style="cyan", width=3)
                table.add_column("Titre", style="white")
                table.add_column("Date", style="dim")
                
                for i, s in enumerate(sessions):
                    table.add_row(str(i+1), s['title'], s['time'])
                
                console.print(table)
                console.print("\n[dim]Actions: [cyan]numéro[/cyan]=charger, [red]d numéro[/red]=supprimer, [yellow]0[/yellow]=annuler[/dim]")
                
                try:
                    action = Prompt.ask("Action", default="0")
                    action = action.strip().lower()
                    
                    if action == "0" or not action:
                        console.print("[dim]Annulé.[/dim]")
                        continue
                    
                    # Supprimer une session
                    if action.startswith("d ") or action.startswith("d"):
                        parts = action.split()
                        if len(parts) >= 2:
                            try:
                                idx = int(parts[1])
                            except ValueError:
                                console.print("[red]Numéro invalide.[/red]")
                                continue
                        else:
                            idx = IntPrompt.ask("Numéro de la session à supprimer")
                        
                        if 1 <= idx <= len(sessions):
                            session = sessions[idx-1]
                            if Confirm.ask(f"[red]Supprimer définitivement[/red] '{session['title']}' ?", default=False):
                                try:
                                    storage.delete_session(session['file'])
                                    console.print(f"[green]✓ Session '{session['title']}' supprimée.[/green]")
                                except Exception as e:
                                    console.print(f"[red]Erreur: {e}[/red]")
                        else:
                            console.print("[red]Numéro invalide.[/red]")
                        continue
                    
                    # Charger une session
                    try:
                        idx = int(action)
                    except ValueError:
                        console.print("[red]Action non reconnue.[/red]")
                        continue
                    
                    if 1 <= idx <= len(sessions):
                        data = storage.load_session(sessions[idx-1]['file'])
                        state.messages = data['messages']
                        state.title = data['title']
                        console.clear()
                        console.print(Panel(f"📂 Session chargée: [bold]{state.title}[/bold]", border_style="green"))
                        
                        # Afficher l'historique
                        for m in state.messages:
                            if m['role'] == 'user':
                                display_user_message(m['content'], config)
                            elif m['role'] == 'assistant':
                                ai_style = config.get("ai_style", {})
                                console.print(Panel(
                                    Markdown(m['content']),
                                    title=ai_style.get("title_template", "🤖 {model}").format(model=state.model),
                                    border_style=ai_style.get("border_color", "green")
                                ))
                    else:
                        console.print("[red]Numéro invalide.[/red]")
                except (ValueError, KeyboardInterrupt):
                    console.print("[dim]Annulé.[/dim]")
                continue
            
            elif cmd == "/memory":
                # Gestion de la mémoire avec sous-commandes
                parts = args.split(maxsplit=1) if args else []
                subcmd = parts[0].lower() if parts else ""
                subargs = parts[1] if len(parts) > 1 else ""
                
                if subcmd == "add" and subargs:
                    storage.save_memory(subargs)
                    console.print(f"[green]🧠 Mémorisé: {subargs}[/green]")
                
                elif subcmd == "delete" or subcmd == "del":
                    entries = storage.get_memory_entries()
                    if not entries:
                        console.print("[dim]La mémoire est vide.[/dim]")
                        continue
                    
                    console.print("\n[bold]🧠 Entrées de mémoire:[/bold]")
                    for i, entry in enumerate(entries):
                        console.print(f"  [cyan]{i+1}.[/cyan] {entry}")
                    
                    try:
                        if subargs:
                            idx = int(subargs)
                        else:
                            idx = IntPrompt.ask("\nNuméro à supprimer")
                        
                        if 1 <= idx <= len(entries):
                            if storage.delete_memory_entry(idx - 1):
                                console.print(f"[green]✓ Entrée supprimée.[/green]")
                            else:
                                console.print("[red]Erreur lors de la suppression.[/red]")
                        else:
                            console.print("[red]Numéro invalide.[/red]")
                    except (ValueError, KeyboardInterrupt):
                        console.print("[dim]Annulé.[/dim]")
                
                else:
                    # Par défaut: afficher la mémoire
                    entries = storage.get_memory_entries()
                    if not entries:
                        console.print("[dim]La mémoire est vide. Utilisez [cyan]/memory add <info>[/cyan] pour ajouter.[/dim]")
                    else:
                        console.print("\n[bold]🧠 Mémoire de l'utilisateur:[/bold]")
                        for i, entry in enumerate(entries):
                            console.print(f"  [cyan]{i+1}.[/cyan] {entry}")
                        console.print("\n[dim]Actions: [cyan]/memory add <info>[/cyan] | [cyan]/memory delete[/cyan][/dim]")
                continue
            
            elif cmd == "/resume":
                threshold = config.get("summary_threshold", 5)
                if len(state.messages) > threshold:
                    to_summarize = [m for m in state.messages if m['role'] != 'system']
                    summary = client.summarize(state.model, to_summarize)
                    state.messages = [{"role": "system", "content": f"Contexte résumé: {summary}"}] + state.messages[-threshold:]
                    console.print("[cyan]📝 Historique résumé avec succès.[/cyan]")
                else:
                    console.print("[dim]Pas assez de messages pour résumer.[/dim]")
                continue
            
            elif cmd == "/settings":
                display_settings_menu(state, client)
                # Mettre à jour les options du client
                client.set_options(
                    temperature=state.temperature,
                    max_tokens=state.max_output_length,
                    top_p=state.top_p,
                    repeat_penalty=state.repeat_penalty
                )
                continue
            
            else:
                console.print(f"[red]❌ Commande inconnue: {cmd}[/red]")
                console.print("[dim]Tapez /help pour voir les commandes disponibles.[/dim]")
                continue

        # ─────────────────────────────────────────────────────────────────────
        #                         CHAT NORMAL
        # ─────────────────────────────────────────────────────────────────────
        
        # Afficher le message utilisateur avec style
        display_user_message(user_input, config)
        
        # Détection mémoire naturelle
        lower_input = user_input.lower()
        memory_triggers = ["retiens que ", "souviens-toi que ", "note que ", "enregistre que ", "enregistre dans ta memoire que ", "sache que "]
        
        # Vérifier si l'input contient une commande de mémoire
        trigger_found = next((t for t in memory_triggers if t in lower_input), None)
        
        if trigger_found:
            # Extraire l'information (tout ce qui suit le trigger)
            try:
                start_index = lower_input.find(trigger_found) + len(trigger_found)
                info = user_input[start_index:].strip()
                if info:
                    storage.save_memory(info)
                    console.print(f"[green]🧠 (Auto-Memory) J'ai noté: {info}[/green]")
            except Exception as e:
                logger.error(f"Erreur extraction mémoire: {e}")

        # Mise à jour dynamique du prompt système avec la mémoire
        # On le fait à chaque tour pour inclure la mémoire fraîchement ajoutée
        memory = storage.get_memory()
        if memory.strip():
            memory_prompt = config.get("prompts", {}).get("memory_prefix", "{memory}").format(memory=memory)
            
            # Si le premier message est un prompt système, on le met à jour
            if state.messages and state.messages[0].get("role") == "system":
                # Vérifier si c'est notre prompt mémoire (simple heuristique)
                if "[CONTEXTE]" in state.messages[0]["content"]:
                     state.messages[0]["content"] = memory_prompt
                else:
                    # Sinon, on ne touche pas au prompt système existant s'il est différent, 
                    # mais on pourrait vouloir concaténer. Ici on insère si pas de contexte mémoire.
                    if "[CONTEXTE]" not in state.messages[0]["content"]:
                         state.messages.insert(0, {"role": "system", "content": memory_prompt})
            
            # Si pas de messages ou pas de système au début, on insère
            elif not state.messages or state.messages[0].get("role") != "system":
                state.messages.insert(0, {"role": "system", "content": memory_prompt})
        
        
        state.messages.append({"role": "user", "content": user_input})
        
        # Configurer les options avant chaque requête
        client.set_options(
            temperature=state.temperature,
            max_tokens=state.max_output_length,
            top_p=state.top_p,
            repeat_penalty=state.repeat_penalty
        )
        
        # Streaming de la réponse avec gestion Ctrl+C
        full_response = ""
        ai_style = config.get("ai_style", {})
        ai_title = ai_style.get("title_template", "🤖 {model}").format(model=state.model)
        
        try:
            with Live(console=console, refresh_per_second=10, transient=True) as live:
                for chunk in client.chat(state.model, state.messages):
                    if state.interrupted:
                        break
                    full_response += chunk
                    live.update(Panel(
                        Markdown(full_response + "▌"),
                        title=ai_title,
                        border_style=ai_style.get("border_color", "green"),
                        padding=(0, 1)
                    ))
        except KeyboardInterrupt:
            # Ctrl+C pendant le streaming = stop réponse
            console.print("\n[dim]Génération interrompue.[/dim]")
            state.interrupted = True
        
        # Afficher la réponse finale (sans curseur)
        if full_response:
            console.print(Panel(
                Markdown(full_response),
                title=ai_title,
                border_style=ai_style.get("border_color", "green"),
                padding=(0, 1)
            ))
            state.messages.append({"role": "assistant", "content": full_response})
        
        console.print()  # Ligne vide pour aérer


# ═══════════════════════════════════════════════════════════════════════════════
#                              POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

def update_default_model_in_config(new_model: str, storage: StorageManager) -> bool:
    """Met à jour le modèle par défaut dans le fichier config.yaml."""
    config_path = storage.get_config_path()
    if not config_path:
        console.print("[red]Fichier config.yaml non trouvé.[/red]")
        return False
    
    try:
        content = config_path.read_text(encoding="utf-8")
        import re
        # Remplacer default_model: xxx par default_model: new_model
        new_content = re.sub(
            r'^(default_model:\s*).*$',
            f'\\1{new_model}',
            content,
            flags=re.MULTILINE
        )
        config_path.write_text(new_content, encoding="utf-8")
        return True
    except (OSError, Exception) as e:
        console.print(f"[red]Erreur mise à jour config: {e}[/red]")
        return False


def display_models_list(client: OllamaClient, current_default: str):
    """Affiche la liste des modèles disponibles."""
    models = client.list_models()
    if not models:
        console.print("[yellow]Aucun modèle trouvé. Est-ce qu'Ollama est en cours d'exécution?[/yellow]")
        return
    
    console.print()
    table = Table(
        title="🦙 Modèles Ollama Disponibles",
        show_header=True,
        header_style="bold cyan",
        border_style="dim"
    )
    table.add_column("", width=2)
    table.add_column("Nom", style="white")
    table.add_column("Taille", style="dim", justify="right")
    table.add_column("Modifié", style="dim")
    
    for m in models:
        is_default = "✓" if m['name'].startswith(current_default) or m['name'].split(":")[0] == current_default else ""
        size_gb = m.get("size", 0) / (1024 ** 3)
        modified = m.get("modified", "")[:10] if m.get("modified") else ""
        table.add_row(is_default, m['name'], f"{size_gb:.1f} GB", modified)
    
    console.print(table)
    console.print(f"\n[dim]Modèle par défaut: [cyan]{current_default}[/cyan][/dim]")
    console.print("[dim]Utilisez [cyan]-d/--default-model <nom>[/cyan] pour changer le défaut.[/dim]")


@app.command()
def main(
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p", help="Question rapide (one-shot)"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Mode interactif"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Modèle à utiliser pour cette session"),
    list_models: bool = typer.Option(False, "--list-models", "-l", help="Lister les modèles disponibles"),
    default_model: Optional[str] = typer.Option(None, "--default-model", "-d", help="Définir le modèle par défaut")
):
    """AI-CLI - Client CLI intelligent pour Ollama."""
    
    config = load_config()
    storage = StorageManager(config.get("history_dir", "~/.ai-cli"))
    client = OllamaClient(
        config.get("ollama_url", "http://localhost:11434"),
        config.get("prompts", {}),
        timeout=config.get("request_timeout", 60)
    )
    
    # Configurer les options par défaut
    client.set_options(
        temperature=config.get("temperature", 0.7),
        max_tokens=config.get("max_output_length", 2048),
        top_p=config.get("top_p", 0.9),
        repeat_penalty=config.get("repeat_penalty", 1.1)
    )
    
    current_default = config.get("default_model", "phi3.5")
    
    # Mode: Lister les modèles
    if list_models:
        # Vérifier qu'Ollama est en cours d'exécution
        if not client.is_running():
            console.print("[red]❌ Ollama n'est pas en cours d'exécution.[/red]")
            return
        display_models_list(client, current_default)
        return
    
    # Mode: Changer le modèle par défaut
    if default_model:
        # Vérifier qu'Ollama est en cours d'exécution pour valider le modèle
        if not client.is_running():
            console.print("[yellow]⚠ Ollama n'est pas en cours d'exécution. Mise à jour sans validation.[/yellow]")
        elif not client.model_exists(default_model):
            console.print(f"[yellow]⚠ Modèle '{default_model}' non trouvé sur Ollama. Mise à jour quand même.[/yellow]")
        
        if update_default_model_in_config(default_model, storage):
            console.print(f"[green]✓ Modèle par défaut changé: [bold]{current_default}[/bold] → [bold]{default_model}[/bold][/green]")
        return
    
    selected_model = model or current_default
    
    # Vérifier qu'Ollama est en cours d'exécution
    if not client.is_running():
        try:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            console.print("[yellow]⏳ Démarrage d'Ollama...[/yellow]")
            for _ in range(10):
                time.sleep(1)
                if client.is_running():
                    console.print("[green]✓ Ollama démarré.[/green]")
                    break
            else:
                console.print("[red]❌ Impossible de démarrer Ollama.[/red]")
                return
        except FileNotFoundError:
            console.print("[red]❌ Ollama n'est pas installé. Visitez https://ollama.ai[/red]")
            return

    # Vérification du modèle avec match intelligent
    if not client.model_exists(selected_model):
        console.print(f"[yellow]📥 Modèle '{selected_model}' non trouvé. Téléchargement...[/yellow]")
        try:
            with requests.post(
                f"{client.url}/api/pull",
                json={"name": selected_model},
                stream=True,
                timeout=600
            ) as r:
                for line in r.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            status = data.get("status", "")
                            if "pulling" in status or "downloading" in status:
                                console.print(".", end="", style="dim")
                        except json.JSONDecodeError:
                            pass
            console.print(f"\n[green]✓ Modèle '{selected_model}' prêt.[/green]")
        except Exception as e:
            console.print(f"\n[red]❌ Erreur téléchargement: {e}[/red]")
            return
    else:
        # Utiliser le nom complet du modèle
        full_name = client.get_model_full_name(selected_model)
        if full_name:
            selected_model = full_name

    state = SessionState(selected_model, config)
    
    if interactive:
        display_welcome(storage, config)
        run_interactive(state, storage, client, config)
    elif prompt:
        # Mode one-shot
        console.print()
        full_response = ""
        ai_style = config.get("ai_style", {})
        
        try:
            with Live(console=console, refresh_per_second=10, transient=True) as live:
                for chunk in client.chat(selected_model, [{"role": "user", "content": prompt}]):
                    full_response += chunk
                    live.update(Panel(
                        Markdown(full_response + "▌"),
                        title=ai_style.get("title_template", "🤖 {model}").format(model=selected_model),
                        border_style=ai_style.get("border_color", "green")
                    ))
        except KeyboardInterrupt:
            console.print("\n[dim]Interrompu.[/dim]")
        
        if full_response:
            console.print(Panel(
                Markdown(full_response),
                title=ai_style.get("title_template", "🤖 {model}").format(model=selected_model),
                border_style=ai_style.get("border_color", "green")
            ))
    else:
        # Afficher l'aide si aucune option
        console.print("[bold cyan]AI-CLI[/bold cyan] - Client CLI intelligent pour Ollama\n")
        console.print("[yellow]Usage:[/yellow]")
        console.print("  ai-cli [cyan]-i[/cyan]              Mode interactif")
        console.print("  ai-cli [cyan]-p[/cyan] \"question\"   Question rapide")
        console.print("  ai-cli [cyan]-l[/cyan]              Lister les modèles")
        console.print("  ai-cli [cyan]-d[/cyan] <modèle>     Changer modèle par défaut")
        console.print("  ai-cli [cyan]-m[/cyan] <modèle> -i  Utiliser un modèle spécifique")
        console.print("\n[dim]Utilisez --help pour plus d'informations.[/dim]")


# Import json pour le pull
import json

if __name__ == "__main__":
    app()
