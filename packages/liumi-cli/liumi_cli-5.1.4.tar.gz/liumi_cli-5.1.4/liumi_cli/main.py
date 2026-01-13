import typer
import os
import sys
import json
import shutil
import requests
import pyfiglet
import stat
import errno
import re
import subprocess
import webbrowser
import socketserver
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google import genai
from github import Github
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown

# --- APP INITIALIZATION ---
app = typer.Typer(help="Liumi Interface Utility (LIU) - DevOps Edition", add_completion=False)
console = Console()
CONFIG_FILE = os.path.expanduser("~/.liu_config.json")

# --- GITHUB CONFIGURATION ---
GITHUB_CLIENT_ID = "Ov23liebLvUVClQaH15j"
GITHUB_CLIENT_SECRET = "e348ca8b8a1a4d3b0cfe27b3e64dd26e43baa17f"

# --- PROVIDER CONFIGURATIONS ---
PROVIDERS = {
    "LIUMI": { 
        "url": "https://api.liumi.cloud/v1/chat/completions", 
        "model": "liumix-2o", 
        "env_prefix": "lum_" 
    },
    "GOOGLE": { 
        "url": "https://generativelanguage.googleapis.com", 
        "model": "gemini-2.5-pro",
        "sdk": True 
    },
    "OPENAI": { 
        "url": "https://api.openai.com/v1/chat/completions", 
        "model": "gpt-4o" 
    },
    "GROQ": { 
        "url": "https://api.groq.com/openai/v1/chat/completions", 
        "model": "qwen/qwen3-32b" 
    },
    "OPENROUTER": { 
        "url": "https://openrouter.ai/api/v1/chat/completions", 
        "model": "xiaomi/mimo-v2-flash:free" 
    }
}

# --- OAUTH SERVER ---
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "/callback" in self.path:
            query = urlparse(self.path).query
            params = parse_qs(query)
            if "code" in params:
                self.server.auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body style='background:#000;color:#00F0FF;text-align:center;padding-top:100px;'><h1>LIU CONNECTED</h1><script>window.close()</script></body></html>")
            else:
                self.server.auth_code = None
                self.send_response(400)

# --- UTILITIES ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"provider": None, "keys": {}, "models": {}, "github_token": None}

def save_config(config):
    with open(CONFIG_FILE, "w") as f: json.dump(config, f, indent=2)

def show_logo():
    try:
        ascii_art = pyfiglet.figlet_format("> LIU - CLI", font="ansi_shadow")
    except:
        ascii_art = "> LIU - CLI"
    console.print("\n")
    console.print(ascii_art, style="bold #00F0FF")
    console.print("[dim]   [ Liumi Interface Utility v5.1.3 ]   [/dim]\n")

def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else: raise

# --- BRAIN (FIXED FOR OPENROUTER/PARASAIL) ---
def call_brain(system_prompt, user_prompt, json_mode=False):
    config = load_config()
    provider = config.get("provider")
    
    if not provider or provider not in config.get("keys", {}):
        console.print("[bold yellow]⚠ AI Provider Not Configured. Running setup...[/bold yellow]")
        setup()
        config = load_config()
        provider = config.get("provider")

    api_key = config["keys"][provider]
    
    # DETERMINE MODEL
    default_model = PROVIDERS[provider]["model"]
    user_models = config.get("models", {})
    selected_model = user_models.get(provider, default_model)

    # --- GOOGLE HANDLING ---
    if provider == "GOOGLE":
        try:
            client = genai.Client(api_key=api_key)
            full_prompt = f"{system_prompt}\n\nUser Request: {user_prompt}"
            response = client.models.generate_content(model=selected_model, contents=full_prompt)
            return response.text
        except Exception as e: return f"AI Error: {str(e)}"
    
    # --- REST API HANDLING ---
    else:
        info = PROVIDERS[provider]
        headers = { "Authorization": f"Bearer {api_key}", "Content-Type": "application/json" }
        if provider in ["OPENROUTER", "LIUMI"]: 
            headers["HTTP-Referer"] = "https://liumi.cloud"
            headers["X-Title"] = "Liumi CLI"
        
        # --- THE FIX: HANDLE MESSAGE FORMATTING ---
        # Some OpenRouter/Parasail models CRASH if you send "system" role.
        # We merge system prompt into user prompt to be safe for everyone.
        if provider == "OPENROUTER":
            messages_payload = [
                {"role": "user", "content": f"SYSTEM INSTRUCTIONS:\n{system_prompt}\n\nUSER TASK:\n{user_prompt}"}
            ]
        else:
            # Standard formatting for OpenAI, Groq, Liumi
            messages_payload = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

        payload = {
            "model": selected_model,
            "messages": messages_payload,
            # Removed temperature for OpenRouter to avoid Molmo validation errors
            # "temperature": 0.2 if json_mode else 0.7 
        }
        
        # Only add temperature if NOT OpenRouter (some Molmo models hate temp)
        if provider != "OPENROUTER":
             payload["temperature"] = 0.2 if json_mode else 0.7

        if json_mode and provider in ["OPENAI", "GROQ"]: payload["response_format"] = {"type": "json_object"}
        
        try:
            response = requests.post(info["url"], headers=headers, json=payload, timeout=60)
            if response.status_code != 200: 
                # Better Error Reporting
                return f"Error {response.status_code}: {response.text}"
            
            return response.json()['choices'][0]['message']['content']
        except Exception as e: return f"Connection Failed: {str(e)}"

# --- GIT UTILS ---
def get_git_diff():
    try:
        if not os.path.exists(".git"): return None
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
        return result.stdout
    except: return None

# --- COMMANDS ---

@app.command()
def setup():
    """Configure Provider & Model."""
    show_logo()
    choices = list(PROVIDERS.keys())
    console.print("[cyan]Select AI Platform:[/cyan]")
    for i, p in enumerate(choices, 1): console.print(f"{i}. {p}")
    
    c = Prompt.ask("Selection", choices=[str(i) for i in range(1, len(choices)+1)])
    provider = choices[int(c)-1]
    
    default_model = PROVIDERS[provider]["model"]
    console.print(f"\n[dim]Default Model: {default_model}[/dim]")
    user_model = Prompt.ask("Enter Model Name", default=default_model)
    key = Prompt.ask("API Key", password=True).strip()
    
    config = load_config()
    config["provider"] = provider
    if "keys" not in config: config["keys"] = {}
    config["keys"][provider] = key
    if "models" not in config: config["models"] = {}
    config["models"][provider] = user_model
    
    save_config(config)
    console.print(f"[green]✔ Connected to {provider} using {user_model}.[/green]")

@app.command()
def gh_connect():
    """Connect GitHub."""
    show_logo()
    if "YOUR_CLIENT_ID" in GITHUB_CLIENT_ID:
        console.print("[red]⚠ Developer Error: Missing GITHUB_CLIENT_ID in code.[/red]")
        return
    
    try:
        server = socketserver.TCPServer(("localhost", 9999), OAuthHandler)
    except: return console.print("[red]Port 9999 blocked.[/red]")

    console.print("[yellow]Opening GitHub...[/yellow]")
    webbrowser.open(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=repo,user,workflow")
    
    with console.status("[cyan]Waiting for auth...[/cyan]"): server.handle_request()
    auth_code = getattr(server, "auth_code", None)
    server.server_close()
    
    if not auth_code: return console.print("[red]Auth failed.[/red]")

    token_res = requests.post("https://github.com/login/oauth/access_token", 
                              json={"client_id":GITHUB_CLIENT_ID, "client_secret":GITHUB_CLIENT_SECRET, "code":auth_code},
                              headers={"Accept":"application/json"})
    token = token_res.json().get("access_token")
    if token:
        user = Github(token).get_user()
        config = load_config()
        config["github_token"] = token
        save_config(config)
        console.print(f"[green]✔ Connected as {user.login}[/green]")
    else: console.print("[red]Token exchange failed.[/red]")

@app.command()
def create_repo(name: str, private: bool = False):
    """Create GitHub Repo."""
    config = load_config()
    if not config.get("github_token"): return console.print("[red]Run 'liu gh-connect' first.[/red]")
    try:
        user = Github(config["github_token"]).get_user()
        with Progress(SpinnerColumn("dots"), TextColumn("Creating..."), transient=True) as p:
            p.add_task("", total=None)
            repo = user.create_repo(name, private=private)
        if not os.path.exists(".git"): os.system("git init")
        os.system("git branch -M main")
        os.system(f"git remote add origin {repo.clone_url}")
        console.print(f"[green]✔ Repo created & linked: {repo.html_url}[/green]")
    except Exception as e: console.print(f"[red]Error: {e}[/red]")

@app.command()
def ship():
    """Auto-Commit & Push."""
    show_logo()
    if not os.path.exists(".git"): return console.print("[red]Not a git repo.[/red]")
    
    with Progress(SpinnerColumn("dots"), TextColumn("Checking changes..."), transient=True) as p:
        p.add_task("", total=None)
        diff = get_git_diff()
    
    if not diff: return console.print("[yellow]No changes found.[/yellow]")
    
    with Progress(SpinnerColumn("aesthetic"), TextColumn("AI Writing Commit..."), transient=True) as p:
        p.add_task("", total=None)
        msg = call_brain("You are a Senior DevOps Engineer. Write a concise semantic commit message for this diff. Return ONLY the message.", f"Diff: {diff}").strip().replace('"','').replace('`','')
    
    console.print(f"\n[dim]Message:[/dim] [bold white]“{msg}”[/bold white]\n")
    if Confirm.ask("[green]Ship it?[/green]"):
        os.system(f'git commit -m "{msg}"')
        res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
        if res.returncode == 0: console.print("[bold green]✔ Shipped![/bold green]")
        elif "upstream" in res.stderr: os.system("git push --set-upstream origin master")
        else: console.print(f"[red]{res.stderr}[/red]")

@app.command()
def do(task: str):
    """Agent Mode."""
    show_logo()
    files = ", ".join([f for f in os.listdir('.') if not f.startswith('.')][:30])
    system = """You are LIU. Modify files. Return JSON wrapped in ```json``` blocks.
    Schema: { "actions": [ { "type": "CREATE", "path": "file", "content": "code" }, { "type": "UPDATE", "path": "file", "content": "code" }, { "type": "DELETE", "path": "file" } ] }"""
    
    with Progress(SpinnerColumn("dots"), TextColumn("[cyan]Architecting...[/cyan]"), transient=True) as p:
        p.add_task("", total=None)
        res = call_brain(system, f"Files: {files}\nTask: {task}", json_mode=True)
    
    execute_agent_plan(res)

def execute_agent_plan(res):
    try:
        match = re.search(r'```json\s*([\s\S]*?)\s*```', res)
        plan = json.loads(match.group(1) if match else res)
    except: return console.print("[red]Invalid JSON Plan[/red]")
    
    actions = plan.get("actions", [])
    console.print(f"\n[bold white]🤖 Plan:[/bold white]")
    for a in actions: console.print(f"[green] {a['type']}:[/green] {a['path']}")
    if not Confirm.ask("\n[bold cyan]Proceed?[/bold cyan]"): return
    
    for a in actions:
        try:
            if a['type'] in ["CREATE", "UPDATE"]:
                os.makedirs(os.path.dirname(a['path']) or ".", exist_ok=True)
                with open(a['path'], "w", encoding="utf-8") as f: f.write(a['content'])
            elif a['type'] == "DELETE" and os.path.exists(a['path']):
                if os.path.isdir(a['path']): shutil.rmtree(a['path'], onerror=handle_remove_readonly)
                else: os.remove(a['path'])
            console.print(f"[green]✔ Done:[/green] {a['path']}")
        except Exception as e: console.print(f"[red]Error:[/red] {e}")

@app.command()
def audit():
    """Security Scan."""
    show_logo()
    code = ""
    for r, d, f in os.walk("."):
        if any(x in r for x in [".git", "venv", "node_modules"]): continue
        for file in f:
            if file.endswith(('.py', '.js', '.ts')): 
                try: 
                    with open(os.path.join(r, file), "r", encoding="utf-8") as o: code += f"\n--- {file} ---\n{o.read()[:5000]}\n"
                except: pass
    
    system = "Analyze code. Return JSON: { 'score': 'A-F', 'issues': [ { 'severity': 'HIGH/MED', 'file': 'name', 'desc': 'issue' } ], 'summary': 'text' }"
    with Progress(SpinnerColumn("aesthetic"), TextColumn("[red]Auditing...[/red]"), transient=True) as p:
        p.add_task("", total=None)
        res = call_brain(system, code, json_mode=True)
    
    try:
        data = json.loads(re.search(r'```json\s*([\s\S]*?)\s*```', res).group(1))
        console.print(Panel(f"[bold]Grade: {data['score']}[/bold]\n{data['summary']}", title="AUDIT REPORT", border_style="#00F0FF"))
    except: console.print(Panel(res))

@app.command()
def ignite():
    """Auto-Start."""
    show_logo()
    files = ", ".join([f for f in os.listdir('.') if not f.startswith('.')][:15])
    with Progress(SpinnerColumn("dots"), TextColumn("Igniting..."), transient=True) as p:
        p.add_task("", total=None)
        cmd = call_brain("Return ONLY shell start command.", f"Files: {files}").strip().replace('`', '')
    if Confirm.ask(f"Run [green]{cmd}[/green]?"): os.system(cmd)

@app.command()
def ghost(action: str):
    """Safe Mode: start | revert | keep"""
    show_logo()
    GHOST_DIR = ".liu_ghost"
    ignore = shutil.ignore_patterns('node_modules', '.git', 'venv', '__pycache__', 'dist')
    if action == "start":
        if os.path.exists(GHOST_DIR): return console.print("[red]Active.[/red]")
        shutil.copytree('.', GHOST_DIR, ignore=ignore)
        console.print("[green]✔ Snapshot saved.[/green]")
    elif action == "revert":
        if not os.path.exists(GHOST_DIR): return console.print("[red]No snapshot.[/red]")
        if Confirm.ask("[red]Revert?[/red]"):
            for i in os.listdir('.'):
                if i != GHOST_DIR and i != '.git':
                    if os.path.isdir(i): shutil.rmtree(i, onerror=handle_remove_readonly)
                    else: os.remove(i)
            shutil.copytree(GHOST_DIR, '.', dirs_exist_ok=True)
            shutil.rmtree(GHOST_DIR, onerror=handle_remove_readonly)
            console.print("[green]✔ Restored.[/green]")
    elif action == "keep":
        if os.path.exists(GHOST_DIR): shutil.rmtree(GHOST_DIR, onerror=handle_remove_readonly)
        console.print("[green]✔ Saved.[/green]")

@app.command()
def resume():
    """Project Summary."""
    show_logo()
    files = [f for f in os.listdir('.') if not f.startswith('.')]
    if not files: files = ["(Empty Folder)"]
    file_list = ", ".join(files[:25])
    
    system = """
    You are LIU. Analyze project state.
    Output format:
    TYPE: <Stack>
    SUMMARY: <Sarcastic summary>
    CMD: <Next command>
    """
    
    with Progress(SpinnerColumn("aesthetic"), TextColumn("[cyan]Reading Memory...[/cyan]"), transient=True) as p:
        p.add_task("", total=None)
        res = call_brain(system, f"Files in folder: {file_list}")

    p_type, msg, cmd = "Unknown", "Welcome back.", "ls"
    if "Error" in res: return console.print(f"[red]{res}[/red]")

    for line in res.split('\n'):
        if "TYPE:" in line: p_type = line.split("TYPE:")[1].strip()
        if "SUMMARY:" in line: msg = line.split("SUMMARY:")[1].strip()
        if "CMD:" in line: cmd = line.split("CMD:")[1].strip()

    content = f"[bold white]🧠 Neural Context[/bold white]\n[cyan]• Stack:[/cyan] {p_type}\n[cyan]• Insight:[/cyan] [white]\"{msg}\"[/white]\n[cyan]• Suggested:[/cyan] [bold green]{cmd}[/bold green]"
    console.print(Panel(content, title="[bold cyan]LIUMI INTELLIGENCE[/bold cyan]", border_style="#00F0FF"))

def entry():
    if len(sys.argv) == 1: resume() 
    else: app()

if __name__ == "__main__":
    entry()