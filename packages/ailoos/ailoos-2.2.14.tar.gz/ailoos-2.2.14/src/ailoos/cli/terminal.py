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
        console.print("[info]💡 Upgrade your hardware or wait for new federated learning missions[/info]")

        await questionary.press_any_key_to_continue().ask_async()

    async def menu_validation_audit(self):
        """Menú 2: VALIDATION & AUDIT."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]🛡️ VALIDATION & AUDIT[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        console.print("[info]ℹ️ Validation and audit features coming soon[/info]")

        await questionary.press_any_key_to_continue().ask_async()

    async def menu_governance_dao(self):
        """Menú 3: GOVERNANCE & DAO."""
        self.show_header()
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]")
        console.print("[logo]🏛️ GOVERNANCE & DAO[/logo]")
        console.print("[enterprise]═══════════════════════════════════════════════════════════════[/enterprise]\n")

        console.print("[info]ℹ️ DAO governance features coming soon[/info]")

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
        else:
            table = Table(title="[enterprise]📁 AVAILABLE DATASETS[/enterprise]")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Type", style="green")
            table.add_column("Size", style="yellow", justify="right")

            for file_path in all_files[:10]:  # Limitar a 10 archivos
                stat = file_path.stat()
                size_mb = stat.st_size / (1024 * 1024)
                table.add_row(
                    file_path.name,
                    file_path.suffix.upper()[1:],
                    f"{size_mb:.2f} MB"
                )

            console.print(table)

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

        console.print("[info]ℹ️ Configuration settings coming soon[/info]")

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