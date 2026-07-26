import urllib.request
import urllib.error
import sys
import time
import os
import requests
import random
import socket
from urllib.parse import urlparse

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
except ImportError:
    print("\n[-] Biblioteca 'rich' nao encontrada. Instale usando: pip install rich\n")
    sys.exit(1)

console = Console()

RESET = "\033[0m"
G_BRIGHT = "\033[1;32m"
G_DARK = "\033[0;32m"
WHITE = "\033[1;37m"
RED = "\033[1;31m"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
]

def get_spoofed_headers():
    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Forwarded-For': fake_ip,
        'X-Real-IP': fake_ip,
        'X-Client-IP': fake_ip,
        'Via': f"1.1 fake-proxy-{random.randint(100,999)}",
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    return headers

def soquete(url, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.5)
    
    host = urlparse(url).netloc if url.startswith(('http://', 'https://')) else urlparse(f"http://{url}").netloc
    if ":" in host:
        host = host.split(":")

    try:
        ip = socket.gethostbyname(host)
        console.print(f" [bold white]* resolved ip:[/] [cyan]{ip}[/]")
        
        resultado = s.connect_ex((ip, port))
        if resultado == 0:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            data = s.recv(1024)
            text = data.decode('utf-8', errors='ignore').strip()
            
            lines = text.split("\n")
            banner_clean = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("server:")), "unknown")
            if banner_clean == "unknown" and lines:
                banner_clean = lines[0].strip()
                
            console.print(f" [bold white]* target port:[/] [green]{port} (open)[/]")
            console.print(f" [bold white]* socket banner:[/] [bold yellow]{banner_clean}[/]")
        else:
            console.print(f" [bold white]* target port:[/] [red]{port} (closed/filtered)[/]")
    except Exception as e:
        console.print(f" [bold white]* socket error:[/] [bold red]{e}[/]")
    finally:
        s.close()

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    sharingan = (
        "⠤⣤⣤⣤⣄⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⠤⠤⠴⠶⠶⠶⠶\n"
        "⢠⣤⣤⡄⣤⣤⣤⠄⣀⠉⣉⣙⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠘⣉⢡⣤⡤⠐⣶⡆⢶⠀⣶⣶⡦\n"
        "⣄⢻⣿⣧⠻⠇⠋⠀⠋⠀⢘⣿⢳⣦⣌⠳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠞⣡⣴⣧⠻⣄⢸⣿⣿⡟⢁⡻⣸⣿⡿⠁\n"
        "⠈⠃⠙⢿⣧⣙⠶⣿⣿⡷⢘⣡⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣷⣝⡳⠶⠶⠾⣛⣵⡿⠋⠀⠀\n"
        "⠀⠀⠀⠀⠉⠻⣿⣶⠂⠘⠛⠛⠛⢛⡛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠀⠉⠒⠛⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⢻⡁⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀ ⠀⠀⠀⠿"
    )
    
    text_sharingan = Text(sharingan, style="red")
    
    info_text = Text()
    info_text.append("\n⚡ SYSTEM PROFILE\n", style="bold cyan")
    info_text.append("─────────────────────\n", style="bright_black")
    info_text.append(" [!] project: ", style="bold white")
    info_text.append("CurseMark\n", style="bold red blink")
    info_text.append(" [v] version: ", style="bold white")
    info_text.append("1.0\n", style="bold green")
    info_text.append(" [+] coder:   ", style="bold white")
    info_text.append("cannabidi0lx\n", style="bold bright_blue")
    info_text.append(" [g] status:  ", style="bold white")
    info_text.append("github active", style="italic green")
    
    panel_info = Panel(info_text, border_style="bright_black", title="[bold red]CORE[/]", title_align="left")
    
    layout_table = Table.grid(padding=(0, 4))
    layout_table.add_column()
    layout_table.add_column()
    layout_table.add_row(text_sharingan, panel_info)
    
    console.print(layout_table)
    console.print()

def request_url(url, path):
    try:
        headers = get_spoofed_headers()
        rq = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(rq, timeout=2.5) as resp:
            if resp.status == 200:
                print(f"{G_BRIGHT}[+] exploited | endpoint found: /{path} ({resp.status}){RESET}")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"{G_DARK}[!] restrict  | page found: /{path} ({e.code}){RESET}")
    except Exception:
        pass

def req(target_url):
    try:
        headers = get_spoofed_headers()
        r = requests.head(target_url, headers=headers, allow_redirects=True, timeout=2.5)
        res_headers = r.headers

        console.print("[bold green][>] TARGET SCOPE DATA[/]")
        table = Table(show_header=False, border_style="bright_black")
        table.add_column("Key", style="bold white")
        table.add_column("Value", style="cyan")

        table.add_row("* status code", str(r.status_code))
        table.add_row("* size", res_headers.get('Content-Length', 'unknown'))
        table.add_row("* server", res_headers.get('Server', 'not exposed'))
        table.add_row("* powered by", res_headers.get('X-Powered-By', 'not exposed'))
        table.add_row("* redirect to", res_headers.get('Location', 'nothing'))
        table.add_row("* cors origin", res_headers.get('Access-Control-Allow-Origin', 'standard'))
        
        waf_status = "[bold red]cloudflare[/]" if "CF-Ray" in res_headers else "[green]unknown[/]"
        table.add_row("* waf indicator", waf_status)
        
        hsts_status = "[green]true[/]" if 'Strict-Transport-Security' in res_headers else "[red]false[/]"
        table.add_row("* get hsts", hsts_status)
        
        csp_status = "[green]true[/]" if 'Security-Policy' in res_headers else "[red]false[/]"
        table.add_row("* get csp", csp_status)

        console.print(table)
        
        porta_alvo = 443 if target_url.startswith("https") else 80
        soquete(target_url, porta_alvo)
        print()

    except Exception as e:
        console.print(f"[bold red][-] unexpected error gathering host data: {e}[/]\n")

def fun_base():
    show_banner()

    console.print(f"[bold green][>] configuration interface[/]")
    console.print(f"[bright_black]--------------------------------------------------[/]")
    u_base = console.input(f"[bold white]---> target url...:[/] ").strip()
    w = console.input(f"[bold white]---> wordlist......:[/] ").strip()
    console.print(f"[bright_black]--------------------------------------------------[/]\n")

    if not u_base.startswith(('http://', 'https://')):
        u_base = 'http://' + u_base

    if not u_base.endswith("/"):
        u_base += "/"

    req(u_base)

    console.print(f"[bold bright_blue][*] initializing core modules...[/]")
    time.sleep(0.5)
    console.print(f"[bold yellow][*] brute-force attack in progress! (ctrl+c to abort)[/]\n")
    console.print(f"[bright_black]==================================================[/]\n")

    extensions = ["", ".php", ".html", ".txt", ".json", "/"]
    env_files = [".env", ".env.local", ".env.production", ".env.bak", ".env.old", "local.env"]

    console.print(f"[bold bright_black][~] scanning root environment targets...[/]")
    for env in env_files:
        request_url(u_base + env, env)

    console.print(f"\n[bold bright_black][~] launching main wordlist sequence...[/]")
    try:
        with open(w, 'r', encoding='utf-8', errors='ignore') as arqv:
            for lines in arqv:
                delines = lines.strip()
                if not delines or delines.startswith("#"):
                    continue

                for ext in extensions:
                    current_path = delines + ext
                    if current_path.endswith("//"):
                        current_path = current_path[:-1]
                    request_url(u_base + current_path, current_path)

                for env in env_files:
                    current_path = f"{delines}/{env}"
                    request_url(u_base + current_path, current_path)

    except FileNotFoundError:
        console.print(f"\n[bold red][--> error: wordlist file not found! :([/]")
    except KeyboardInterrupt:
        console.print(f"\n\n[bold red][*] interrupted by keyboarding [teclado] aborting... :D[/]")
    except Exception as error:
        console.print(f"[bold red]\n[-] unexpected error: {error}[/]")

if __name__ == "__main__":
    fun_base()
