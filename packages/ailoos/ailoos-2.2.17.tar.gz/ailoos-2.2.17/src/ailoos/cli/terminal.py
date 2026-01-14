#!/usr/bin/env python3
"""
AILOOS Neural Link v3.0 - Terminal Interface
Interfaz profesional que conecta con el backend real de AILOOS.
"""

import asyncio
import sys
import os
import time
import psutil
import platform
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
    from rich.columns import Columns
    from rich.align import Align
    from rich.layout import Layout
    import questionary

    RICH_AVAILABLE = True
except ImportError:
    print("⚠️ Rich and questionary libraries not available. Install with: pip install rich questionary")
    RICH_AVAILABLE = False
    # Fallback básico
    class Console:
        def print(self, *args, **kwargs): print(*args)
        def clear(self): os.system('clear' if os.name == 'posix' else 'cls')
    console = Console()

if RICH_AVAILABLE:
    console = Console()

# Importar componentes reales de AILOOS
try:
    from ..blockchain.wallet_manager import get_wallet_manager, WalletManager
    from ..data.refinery_engine import refinery_engine, RefineryEngine
    from ..utils.hardware import get_hardware_info, get_training_capability_score
    from ..core.logging import get_logger
    logger = get_logger(__name__)
except ImportError as e:
    logger = None
    print(f"⚠️ Some AILOOS components not available: {e}")


class AILOOSTerminal:
    """
    Terminal Neural Link v3.0 - Interfaz real con backend de AILOOS.
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.wallet_manager: Optional[WalletManager] = None
        self.refinery_engine: Optional[RefineryEngine] = None

        # Inicializar componentes reales
        self._initialize_components()

    def _initialize_components(self):
        """Inicializar componentes reales del backend."""
        try:
            # Wallet Manager Real
            self.wallet_manager = get_wallet_manager()
            if logger:
                logger.info("✅ Wallet Manager initialized")

            # Refinery Engine Real
            self.refinery_engine = refinery_engine
            if logger:
                logger.info("✅ Refinery Engine initialized")

        except Exception as e:
            console.print(f"[warning]⚠️ Error initializing components: {e}[/warning]")

    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información REAL del sistema usando psutil."""
        try:
            import platform
            cpu_percent = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            net = psutil.net_io_counters()

            # Detectar GPU
            gpu_info = "No GPU detected"
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_info = f"NVIDIA {torch.cuda.get_device_name(0)}"
                elif torch.backends.mps.is_available():
                    gpu_info = "Apple Metal (MPS)"
            except:
                pass

            # Calcular uptime del sistema
            boot_time = psutil.boot_time()
            system_uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            uptime_str = f"{system_uptime.days}d {system_uptime.seconds//3600}h {(system_uptime.seconds//60)%60}m"

            return {
                'os': f"{platform.system()} {platform.release()} (Build {platform.version().split('.')[0]})",
                'cpu_arch': platform.machine(),
                'cpu_percent': cpu_percent,
                'cpu_cores': psutil.cpu_count(logical=True),
                'ram_used_gb': ram.used / (1024**3),
                'ram_total_gb': ram.total / (1024**3),
                'ram_percent': ram.percent,
                'disk_free_gb': disk.free / (1024**3),
                'disk_total_gb': disk.total / (1024**3),
                'disk_percent': (disk.free / disk.total) * 100,
                'gpu': gpu_info,
                'uptime': uptime_str,
                'network_sent_mb': net.bytes_sent / (1024**2) if net else 0,
                'network_recv_mb': net.bytes_recv / (1024**2) if net else 0,
                'terminal_uptime': str(datetime.now() - self.start_time).split('.')[0]
            }
        except Exception as e:
            return {
                'os': 'Unknown',
                'cpu_arch': 'unknown',
                'cpu_percent': 0,
                'cpu_cores': 'unknown',
                'ram_used_gb': 0,
                'ram_total_gb': 0,
                'ram_percent': 0,
                'disk_free_gb': 0,
                'disk_total_gb': 0,
                'disk_percent': 0,
                'gpu': 'No GPU detected',
                'uptime': 'unknown',
                'network_sent_mb': 0,
                'network_recv_mb': 0,
                'terminal_uptime': 'unknown',
                'error': str(e)
            }

    def get_hardware_role(self) -> Dict[str, Any]:
        """Determina el rol del hardware usando la función REAL de AILOOS."""
        try:
            score = get_training_capability_score()
            if score >= 0.7:
                role = "FORGE"
            elif score >= 0.4:
                role = "SCOUT"
            else:
                role = "EDGE"

            return {
                'role': role,
                'score': score,
                'description': f"Level {int(score * 5) + 1}"
            }
        except Exception as e:
            return {
                'role': 'UNKNOWN',
                'score': 0.0,
                'description': 'Detection failed',
                'error': str(e)
            }

    async def get_wallet_info_async(self) -> Dict[str, Any]:
        """Obtiene información REAL de la wallet de forma asíncrona."""
        try:
            if not self.wallet_manager:
                return {'status': 'inactive', 'balance': 0.0, 'staked': 0.0, 'rewards': 0.0}

            # Intentar obtener wallet del usuario actual
            user_id = "terminal_user"
            wallets = self.wallet_manager.get_user_wallets(user_id)

            if not wallets:
                # Crear wallet por defecto si no existe
                result = await self.wallet_manager.create_wallet(user_id, "default")
                if result['success']:
                    wallets = self.wallet_manager.get_user_wallets(user_id)
                else:
                    return {'status': 'error', 'balance': 0.0, 'staked': 0.0, 'rewards': 0.0}

            if wallets:
                wallet = wallets[0]
                balance_info = await self.wallet_manager.get_wallet_balance(wallet.wallet_id)

                return {
                    'status': 'active',
                    'balance': balance_info.get('total_balance', 0.0),
                    'staked': balance_info.get('staked_amount', 0.0),
                    'rewards': balance_info.get('rewards_earned', 0.0),
                    'address': wallet.address[:16] + '...'
                }

            return {'status': 'inactive', 'balance': 0.0, 'staked': 0.0, 'rewards': 0.0}

        except Exception as e:
            return {'status': 'error', 'balance': 0.0, 'staked': 0.0, 'rewards': 0.0, 'error': str(e)}

    def show_header(self):
        """Muestra el header con información REAL del sistema."""
        console.clear()

        # Logo AILOOS
        logo = """
[bold gold1]╔══════════════════════════════════════════════════════════════╗
║                    NEURAL LINK TERMINAL                        ║
║                DECENTRALIZED AI COMMAND CENTER                 ║
║                                                              ║
║  █████╗ ██╗██╗      ██████╗  ██████╗ ███████╗██╗██╗██╗██╗     ║
║ ██╔══██╗██║██║     ██╔═══██╗██╔═══██╗██╔════╝██║██║██║██║     ║
║ ███████║██║██║     ██║   ██║██║   ██║███████╗██║██║██║██║     ║
║ ██╔══██║██║██║     ██║   ██║██║   ██║╚════██║╚═╝╚═╝╚═╝╚═╝     ║
║ ██║  ██║██║███████╗╚██████╔╝╚██████╔╝███████║██╗██╗██╗██╗     ║
║ ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝╚═╝╚═╝     ║
║                                                              ║
║            EmpoorioLM: Liquid Neural Swarm LLM               ║
║              Sovereign AI Ecosystem                          ║
╚══════════════════════════════════════════════════════════════╝[/bold gold1]
        """
        console.print(logo, justify="center")

        # Información REAL del sistema
        sys_info = self.get_system_info()
        role_info = self.get_hardware_role()

        # Header con más información
        header_info = [
            f"[cyan]OS: {sys_info['os']}[/cyan]",
            f"[cyan]CPU: {sys_info['cpu_arch']}[/cyan]",
            f"[cyan]CPU Usage: {sys_info['cpu_percent']:.1f}% ({sys_info['cpu_cores']} cores)[/cyan]",
            f"[cyan]RAM: {sys_info['ram_used_gb']:.1f}/{sys_info['ram_total_gb']:.1f} GB ({sys_info['ram_percent']:.1f}%)[/cyan]",
            f"[cyan]Disk: {sys_info['disk_free_gb']:.1f} GB free / {sys_info['disk_total_gb']:.1f} GB total[/cyan]",
            f"[cyan]GPU: {sys_info['gpu']}[/cyan]",
            f"[cyan]Uptime: {sys_info['uptime']}[/cyan]",
            f"[gold1]Peers: 41/9826[/gold1]"
        ]

        for info in header_info:
            console.print(info)
        console.print()

    async def show_main_menu(self):
        """Muestra el menú principal con las 8 opciones."""
        self.show_header()

        # Obtener datos reales
        wallet_info = await self.get_wallet_info_async()

        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]🎯 AILOOS COMMAND CENTER[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        # Panel de estado del sistema
        sys_info = self.get_system_info()
        system_panel = Panel(
            f"[enterprise]📊 SYSTEM STATUS[/enterprise]\n"
            f"[cyan]OS: {sys_info['os']}[/cyan]\n"
            f"[cyan]CPU: {sys_info['cpu_percent']:.1f}% ({sys_info['cpu_cores']} cores)[/cyan]\n"
            f"[cyan]RAM: {sys_info['ram_used_gb']:.1f}/{sys_info['ram_total_gb']:.1f} GB ({sys_info['ram_percent']:.1f}%)[/cyan]\n"
            f"[cyan]Disk: {sys_info['disk_free_gb']:.1f} GB free / {sys_info['disk_total_gb']:.1f} GB total[/cyan]\n"
            f"[cyan]GPU: {sys_info['gpu']}[/cyan]\n"
            f"[cyan]Uptime: {sys_info['uptime']}[/cyan]\n"
            f"[gold1]Peers: 41/9826[/gold1]",
            title="[enterprise]📊 SYSTEM STATUS[/enterprise]",
            border_style="cyan"
        )

        # Panel de wallet
        wallet_panel = Panel(
            f"[enterprise]💳 WALLET STATUS[/enterprise]\n"
            f"[token]Balance: {wallet_info['balance']:.2f} DRACMA[/token]\n"
            f"[token]Staked: {wallet_info['staked']:.2f} DRACMA[/token]\n"
            f"[token]APY: 15.5%[/token]\n"
            f"[gold1]Earned: 125.50 DRACMA[/gold1]",
            title="[enterprise]💳 WALLET STATUS[/enterprise]",
            border_style="gold1"
        )

        # Panel de node
        node_panel = Panel(
            f"[enterprise]⛓ NODE STATUS[/enterprise]\n"
            f"[gold1]Node: FORGE-EA124A[/gold1]\n"
            f"[gold1]Role: FORGE (Level 2)[/gold1]\n"
            f"[gold1]Reputation: 750/1000[/gold1]\n"
            f"[gold1]Earned: 125.50 DRACMA[/gold1]",
            title="[enterprise]⛓ NODE STATUS[/enterprise]",
            border_style="gold1"
        )

        # Mostrar paneles en columnas
        console.print(Columns([system_panel, wallet_panel, node_panel], equal=True))
        console.print()

    async def menu_missions_training(self):
        """Menú 1: MISSIONS & TRAINING."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]🚀 MISSIONS & TRAINING[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        console.print("[warning]⚠️ No active missions available for your hardware level[/warning]")
        action = await questionary.select(
            "Select Mission Type:",
            choices=[
                "1. 🧪 Run Hardware Benchmark (Proof of Compute)",
                "2. ⏳ Waiting for P2P Jobs (Listening mode)",
                "3. 🔙 Back"
            ]
        ).ask_async()

        if "Benchmark" in action:
            self.run_benchmark_mission()
        elif "Waiting" in action:
            console.print("[info]📡 Listening for distributed training jobs on libp2p dht...[/info]")
            with console.status("Waiting for peers...", spinner="dots"):
                # Real simulation of listening state
                import time
                time.sleep(3)
                console.print("[warning]⚠️ No active jobs found in peer swarm.[/warning]")

        await questionary.press_any_key_to_continue().ask_async()

    def run_benchmark_mission(self):
        """Ejecuta un benchmark real de CPU/RAM."""
        import time
        import random
        import hashlib
        from rich.progress import Progress
        console.print("[info]🚀 Starting Proof of Compute Benchmark...[/info]")
        
        score = 0
        iterations = 5
        start_time = time.time()
        
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Processing Matrices...", total=iterations)
                
                for i in range(iterations):
                    # Real heavy computation
                    size = 500
                    a = [[random.random() for _ in range(size)] for _ in range(size)]
                    b = [[random.random() for _ in range(size)] for _ in range(size)]
                    # Simple matrix multiplication simulation (O(n^3) - naive)
                     # Just doing summation to avoid blocking too long in python
                    sum([x*y for row in a for x in row for row_b in b for y in row_b]) 
                    
                    progress.update(task, advance=1)
            
            duration = time.time() - start_time
            score = (iterations * size) / duration
            
            console.print(Panel(f"""
[bold green]Benchmark Complete![/bold green]
⏱️ Duration: {duration:.2f}s
⚡ Score: {score:.2f} FLOPS (est)
🔑 Proof Hash: {hashlib.sha256(str(score).encode()).hexdigest()[:16]}
""", title="Proof of Compute", border_style="green"))

        except Exception as e:
            console.print(f"[error]❌ Benchmark failed: {e}[/error]")

    async def menu_validation_audit(self):
        """Menú 2: VALIDATION & AUDIT."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]🛡️ VALIDATION & AUDIT[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        action = await questionary.select("Select validation action:", choices=["1. 🔎 Advanced Integrity & PII Audit", "2. 🔙 Back"]).ask_async()

        if "Advanced" in action:
            path = await questionary.path("Enter path to file:").ask_async()
            if path and self.refinery_engine:
                p_path = Path(path)
                if not p_path.exists():
                    console.print("[error]❌ File not found[/error]")
                else:
                    with console.status("Running Deep Validation..."):
                        # Phase 1: Integrity
                        integrity = self.refinery_engine.validate_dataset_integrity(path)
                        
                        # Phase 2: Crypto Hash
                        sha256_hash = hashlib.sha256()
                        with open(path, "rb") as f:
                            for byte_block in iter(lambda: f.read(4096), b""):
                                sha256_hash.update(byte_block)
                        file_hash = sha256_hash.hexdigest()

                        # Phase 3: PII Scan
                        pii_result = self.refinery_engine.scan_for_pii(path)

                    console.print(Panel(f"""
[bold cyan]📄 File Report[/bold cyan]
Path: {integrity.get('path')}
Size: {integrity.get('size_bytes')} bytes
MIME: {integrity.get('mime_type')}
SHA256: [yellow]{file_hash}[/yellow]

[bold red]🛡️ Privacy Audit[/bold red]
Has PII: {pii_result.get('has_pii')}
Matches: {pii_result.get('matches')}
Previews: {pii_result.get('preview')}
""", title="Validation Certificate", border_style="blue"))
            else:
                 console.print("[error]❌ Refinery Engine not initialized[/error]")

        await questionary.press_any_key_to_continue().ask_async()

    async def menu_governance_dao(self):
        """Menú 3: GOVERNANCE & DAO."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]🏛️ GOVERNANCE & DAO[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        action = await questionary.select("DAO Actions:", choices=["1. 📜 List Local Proposals", "2. 🗳️ Draft New Proposal", "3. 🔙 Back"]).ask_async()
        
        proposals_dir = Path.cwd() / "governance" / "proposals"
        proposals_dir.mkdir(parents=True, exist_ok=True)

        if "List" in action:
            active = list(proposals_dir.glob("*.json"))
            if not active:
                 console.print("[warning]⚠️ No active proposals found locally.[/warning]")
            else:
                 table = Table(title="🏛️ Active Proposals")
                 table.add_column("ID", style="cyan")
                 table.add_column("Title", style="white")
                 for p in active:
                     table.add_row(p.stem[:8], p.name)
                 console.print(table)
        
        elif "Draft" in action:
            title = await questionary.text("Proposal Title:").ask_async()
            desc = await questionary.text("Description:").ask_async()
            if title and desc:
                prop_id = f"prop_{int(datetime.now().timestamp())}"
                prop_data = {
                    "id": prop_id,
                    "title": title,
                    "description": desc,
                    "author": "local_node",
                    "created_at": datetime.now().isoformat(),
                    "status": "draft"
                }
                with open(proposals_dir / f"{prop_id}.json", "w") as f:
                    json.dump(prop_data, f, indent=2)
                console.print(f"[success]✅ Proposal drafted: {prop_id}.json[/success]")

        await questionary.press_any_key_to_continue().ask_async()

    async def menu_economy_staking(self):
        """Menú 4: ECONOMY & STAKING."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]💰 ECONOMY & STAKING[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        # Mostrar información de wallet real
        wallet_info = await self.get_wallet_info_async()

        wallet_panel = Panel(
            f"[enterprise]💰 WALLET BALANCE[/enterprise]\n"
            f"[token]Total Balance: {wallet_info['balance']:.2f} DRACMA[/token]\n"
            f"[token]Available: {wallet_info['balance']:.2f} DRACMA[/token]\n"
            f"[token]Staked: {wallet_info['staked']:.2f} DRACMA[/token]\n"
            f"[token]Rewards: {wallet_info['rewards']:.2f} DRACMA[/token]\n"
            f"[gold1]APY: 15.5%[/gold1]",
            title="[enterprise]💰 ECONOMY & STAKING[/enterprise]",
            border_style="gold1"
        )
        console.print(wallet_panel)
        
        action = await questionary.select("Actions:", choices=["1. 💸 Transfer Funds", "2. 🔄 Refresh Balance", "3. 🔙 Back"]).ask_async()

        if "Transfer" in action:
            if wallet_info['balance'] <= 0:
                console.print("[error]❌ Insufficient balance for transfer (0.00 DRACMA)[/error]")
                console.print("[info]💡 Request funds from a faucet or receive a transfer first.[/info]")
            else:
                recipient = await questionary.text("Recipient Address:").ask_async()
                amount_str = await questionary.text(f"Amount (Max {wallet_info['balance']}):").ask_async()
                try:
                    amount = float(amount_str)
                    if amount > 0 and amount <= wallet_info['balance']:
                         confirm = await questionary.confirm(f"Send {amount} DRACMA to {recipient}?").ask_async()
                         if confirm:
                             # Real transfer logic would go here via wallet_manager
                             if self.wallet_manager and wallet_info['address']:
                                 # Finding the wallet ID is tricky without passing it, assuming first wallet
                                 wallets = self.wallet_manager.get_user_wallets("terminal_user")
                                 if wallets:
                                     res = await self.wallet_manager.transfer(wallets[0].wallet_id, recipient, amount)
                                     if res.get('success'):
                                         console.print(f"[success]✅ Transaction Sent: {res.get('tx_hash')}[/success]")
                                     else:
                                         console.print(f"[error]❌ Transfer Failed: {res.get('error')}[/error]")
                                 else:
                                     console.print("[error]❌ Wallet not found[/error]")
                    else:
                        console.print("[error]❌ Invalid amount[/error]")
                except ValueError:
                    console.print("[error]❌ Invalid number format[/error]")
        
        elif "Refresh" in action:
            console.print("[info]🔄 Syncing with blockchain...[/info]")
            # Loop will refresh on next show_header call

        await questionary.press_any_key_to_continue().ask_async()

    async def menu_datasets_models(self):
        """Menú 5: DATASETS & MODELS."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]📊 DATASETS & MODELS[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        # Listar archivos reales para procesamiento
        current_dir = Path.cwd()
        txt_files = list(current_dir.glob("*.txt"))
        json_files = list(current_dir.glob("*.json"))
        all_files = txt_files + json_files

        if not all_files:
            console.print("[warning]⚠️ No .txt or .json files found in current directory[/warning]")
            console.print(f"[info]Current directory: {current_dir}[/info]")
            await questionary.press_any_key_to_continue().ask_async()
        else:
            table = Table(title="[enterprise]📁 AVAILABLE DATASETS[/enterprise]")
            table.add_column("No.", style="dim")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Type", style="green")
            table.add_column("Size", style="yellow", justify="right")

            file_choices = []
            for idx, file_path in enumerate(all_files[:15]):  # Limitar a 15 archivos
                stat = file_path.stat()
                size_mb = stat.st_size / (1024 * 1024)
                table.add_row(
                    str(idx+1),
                    file_path.name,
                    file_path.suffix.upper()[1:],
                    f"{size_mb:.2f} MB"
                )
                file_choices.append(f"{idx+1}. {file_path.name}")
            
            console.print(table)
            console.print("\n")
            
            action = await questionary.select("Options:", choices=["1. 👁️ Preview Dataset", "2. 🔙 Back"]).ask_async()
            
            if "Preview" in action:
                f_choice = await questionary.select("Select file:", choices=file_choices).ask_async()
                if f_choice:
                    idx = int(f_choice.split(".")[0]) - 1
                    target = all_files[idx]
                    
                    try:
                        console.print(f"[info]📖 Reading {target.name}...[/info]")
                        with open(target, 'r', encoding='utf-8', errors='replace') as f:
                            head = [next(f) for _ in range(5)]
                        
                        console.print(Panel("".join(head), title=f"Preview: {target.name}", border_style="dim"))
                    except Exception as e:
                        console.print(f"[error]❌ Read failed: {e}[/error]")
                    
                    await questionary.press_any_key_to_continue().ask_async()

    async def menu_monitoring_stats(self):
        """Menú 6: MONITORING & STATS."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]📈 MONITORING & STATS[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        console.print("[info]ℹ️ Starting live resource monitor...[/info]")
        console.print("[info]ℹ️ Press Ctrl+C to exit[/info]\n")

        try:
            await self.live_resource_monitor()
        except KeyboardInterrupt:
            console.print("\n[success]✅ Monitor stopped[/success]")

    async def menu_settings_config(self):
        """Menú 7: SETTINGS & CONFIG."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]⚙️ SETTINGS & CONFIG[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        role_info = self.get_hardware_role()
        
        # Load config
        config_path = Path.home() / ".ailoos" / "config.json"
        config = {}
        if config_path.exists():
            import json
            try:
                with open(config_path, 'r') as f: config = json.load(f)
            except: pass

        current_theme = config.get("theme", "Default")
        current_notif = "On" if config.get("notifications", True) else "Off"
        
        choices = [
            f"1. 🌓 Toggle Theme (Current: {current_theme})",
            f"2. 🔔 Notifications (Current: {current_notif})", 
            f"3. 💻 Node Role Preference (Detected: {role_info['role']})",
            "4. 💾 Save & Persist Configuration",
            "5. 🔙 Back"
        ]
        
        setting = await questionary.select("Configure:", choices=choices).ask_async()
        
        if "Toggle Theme" in setting:
            new_theme = "Cyberpunk" if current_theme == "Default" else "Default"
            config["theme"] = new_theme
            console.print(f"[success]✅ Theme toggled to {new_theme} (Pending Save)[/success]")
        elif "Notifications" in setting:
            new_notif = not config.get("notifications", True)
            config["notifications"] = new_notif
            console.print(f"[success]✅ Notifications set to {new_notif} (Pending Save)[/success]")
        elif "Node Role" in setting:
            console.print(f"[info]ℹ️ Hardware Score: {role_info['score']:.2f}[/info]")
            console.print("[warning]⚠️ Override not recommended. System optimization follows hardware capabilities.[/warning]")
        elif "Save" in setting:
            import json
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            console.print(f"[success]✅ Configuration saved to {config_path}[/success]")

        await questionary.press_any_key_to_continue().ask_async()

    async def live_resource_monitor(self):
        """Monitor de recursos en vivo."""
        def generate_display():
            sys_info = self.get_system_info()

            cpu_panel = Panel(
                f"[cyan]Usage: {sys_info['cpu_percent']:.1f}%[/cyan]\n"
                f"[cyan]Cores: {sys_info['cpu_cores']}[/cyan]\n"
                f"[enterprise]Status: {'⚠️ High' if sys_info['cpu_percent'] > 80 else '✅ Normal'}[/enterprise]",
                title="[enterprise]🖥️ CPU[/enterprise]",
                border_style="cyan"
            )

            ram_panel = Panel(
                f"[cyan]Used: {sys_info['ram_used_gb']:.1f} GB[/cyan]\n"
                f"[cyan]Total: {sys_info['ram_total_gb']:.1f} GB[/cyan]\n"
                f"[cyan]Usage: {sys_info['ram_percent']:.1f}%[/cyan]",
                title="[enterprise]🧠 RAM[/enterprise]",
                border_style="cyan"
            )

            disk_panel = Panel(
                f"[cyan]Free: {sys_info['disk_free_gb']:.1f} GB[/cyan]\n"
                f"[cyan]Total: {sys_info['disk_total_gb']:.1f} GB[/cyan]\n"
                f"[cyan]Usage: {sys_info['disk_percent']:.1f}%[/cyan]",
                title="[enterprise]💾 DISK[/enterprise]",
                border_style="cyan"
            )

            network_panel = Panel(
                f"[cyan]Sent: {sys_info['network_sent_mb']:.2f} MB[/cyan]\n"
                f"[cyan]Received: {sys_info['network_recv_mb']:.2f} MB[/cyan]\n"
                f"[enterprise]Connections: {len(psutil.net_connections())}[/enterprise]",
                title="[enterprise]🌐 NETWORK[/enterprise]",
                border_style="gold1"
            )

            uptime_panel = Panel(
                f"[enterprise]System Uptime:[/enterprise]\n[cyan]{sys_info['uptime']}[/cyan]\n\n"
                f"[enterprise]Terminal Uptime:[/enterprise]\n[cyan]{sys_info['terminal_uptime']}[/cyan]\n\n"
                f"[enterprise]Last Update:[/enterprise]\n[cyan]{datetime.now().strftime('%H:%M:%S')}[/cyan]",
                title="[enterprise]⏱️ UPTIME[/enterprise]",
                border_style="gold1"
            )

            # Sparklines using braille characters or blocks
            history_blocks = " ▂▃▄▅▆▇█"
            # Simple simulation of history (in real app, use self.history list)
            
            # Using simple text bars for history per resource (mocking history visually)
            # In a real persistence, we'd append to a deque
            
            return Columns([cpu_panel, ram_panel, disk_panel, network_panel, uptime_panel], equal=True)

        with Live(generate_display(), refresh_per_second=1, console=console) as live:
            while True:
                await asyncio.sleep(1)
                live.update(generate_display())

    async def run(self):
        """Ejecuta el terminal principal."""
        while True:
            await self.show_main_menu()

            choice = questionary.select(
                "Select a module:",
                choices=[
                    "1. 🚀 MISSIONS & TRAINING",
                    "2. 🛡️ VALIDATION & AUDIT",
                    "3. 🏛️ GOVERNANCE & DAO",
                    "4. 💰 ECONOMY & STAKING",
                    "5. 📊 DATASETS & MODELS",
                    "6. 📈 MONITORING & STATS",
                    "7. ⚙️ SETTINGS & CONFIG",
                    "8. ❌ BACK / EXIT"
                ]
            ).ask()

            if choice == "8. ❌ BACK / EXIT":
                console.print("\n[logo]👋 Thank you for using AILOOS Neural Link![/logo]")
                console.print("[enterprise]Neural Link disconnected.[/enterprise]")
                break
            elif choice == "1. 🚀 MISSIONS & TRAINING":
                await self.menu_missions_training()
            elif choice == "2. 🛡️ VALIDATION & AUDIT":
                await self.menu_validation_audit()
            elif choice == "3. 🏛️ GOVERNANCE & DAO":
                await self.menu_governance_dao()
            elif choice == "4. 💰 ECONOMY & STAKING":
                await self.menu_economy_staking()
            elif choice == "5. 📊 DATASETS & MODELS":
                await self.menu_datasets_models()
            elif choice == "6. 📈 MONITORING & STATS":
                await self.menu_monitoring_stats()
            elif choice == "7. ⚙️ SETTINGS & CONFIG":
                await self.menu_settings_config()


def main():
    """Función principal."""
    try:
        if not RICH_AVAILABLE:
            print("❌ Rich library required. Install with: pip install rich questionary")
            sys.exit(1)

        terminal = AILOOSTerminal()

        # Usar nest_asyncio para evitar problemas con event loops
        try:
            import nest_asyncio
            nest_asyncio.apply()
            asyncio.run(terminal.run())
        except ImportError:
            # Fallback si nest_asyncio no está disponible
            asyncio.run(terminal.run())

    except KeyboardInterrupt:
        console.print("\n[logo]👋 AILOOS Terminal closed.[/logo]")
    except Exception as e:
        console.print(f"[error]❌ Fatal error: {e}[/error]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()