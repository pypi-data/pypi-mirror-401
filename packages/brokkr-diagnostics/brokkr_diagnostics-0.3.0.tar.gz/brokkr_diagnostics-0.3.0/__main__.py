"""
Entry point for brokkr-diagnostics binary
"""

from brokkr_diagnostics.drivers import run_driver_diagnostics
from brokkr_diagnostics.hardware import run_gpu_hardware_diagnostics, run_lspci_diagnostics
from brokkr_diagnostics.services import run_nvidia_services_diagnostics
from brokkr_diagnostics.system import run_kernel_logs_diagnostics, run_proc_diagnostics
from brokkr_diagnostics.ib import run_ib_diagnostics
from brokkr_diagnostics.tests.gpu_tests import run_cuda_diagnostics
from brokkr_diagnostics.troubleshoot import run_gpu_reset
from brokkr_diagnostics.cc import toggle_cc_mode
import asyncio
from termcolor import cprint
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import os


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║                          ⟨⟨═══════════════════⟩⟩                          ║
    ║                       ⟨⟨     ╱◖ ◗╲   ╱◖ ◗╲   ╱◖ ◗╲    ⟩⟩                  ║
    ║                     ⟨⟨      ╱ ◉ ◉ ╲ ╱ ◉ ◉ ╲ ╱ ◉ ◉ ╲    ⟩⟩                 ║
    ║                    ⟨⟨      ╱   ▼   ╲   ▼   ╲   ▼   ╲   ⟩⟩                ║
    ║                   ⟨⟨       │ ╲═══╱ │ ╲═══╱ │ ╲═══╱ │   ⟩⟩                ║
    ║                   ⟨⟨        ╲     ╱ ╲     ╱ ╲     ╱    ⟩⟩                 ║
    ║                   ⟨⟨         ╲___╱   ╲___╱   ╲___╱     ⟩⟩                 ║
    ║                   ⟨⟨          ╲│      │╲      │╱        ⟩⟩                 ║
    ║                   ⟨⟨           ╲╲    ╱│╲╲    ╱╱         ⟩⟩                 ║
    ║                    ⟨⟨           ╲╲__╱ │ ╲╲__╱╱         ⟩⟩                  ║
    ║                     ⟨⟨           ╲╲___│___╱╱          ⟩⟩                   ║
    ║                       ⟨⟨          ╲╲__│__╱╱          ⟩⟩                    ║
    ║                          ⟨⟨═════════╲│╱═════════⟩⟩                        ║
    ║                                                                            ║
    ║                  ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗  ██╗██████╗        ║
    ║                  ██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██║ ██╔╝██╔══██╗       ║
    ║                  ██████╔╝██████╔╝██║   ██║█████╔╝ █████╔╝ ██████╔╝       ║
    ║                  ██╔══██╗██╔══██╗██║   ██║██╔═██╗ ██╔═██╗ ██╔══██╗       ║
    ║                  ██████╔╝██║  ██║╚██████╔╝██║  ██╗██║  ██╗██║  ██║       ║
    ║                  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝       ║
    ║                                                                            ║
    ║                       NVIDIA GPU DIAGNOSTICS TOOLKIT                      ║
    ║                         Hardware • Drivers • Kernel                       ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """
    cprint(banner, "cyan", attrs=["bold"])


def print_help():
    """Print available commands"""
    cprint("\nAvailable Commands:", "cyan", attrs=["bold"])
    cprint("-" * 80, "cyan")
    cprint("  driver      - NVIDIA driver version & installation checks", "white")
    cprint("  gpu         - GPU hardware state & identification", "white")
    cprint("  lspci       - PCIe bus topology & link status", "white")
    cprint("  pcie        - Alias for 'lspci'", "white")
    cprint("  services    - SystemD service status (suspend/resume/persistence)", "white")
    cprint("  kernel      - Kernel messages & error detection", "white")
    cprint("  logs        - Alias for 'kernel'", "white")
    cprint("  system      - System information (/proc files, NUMA)", "white")
    cprint("  proc        - Alias for 'system'", "white")
    cprint("  ib          - InfiniBand diagnostics", "white")
    cprint("  cuda        - CUDA diagnostics", "white")
    cprint("  all         - Run all diagnostics", "white")
    cprint("  reset       - Reset all GPUs (unloads modules, resets hardware)", "yellow")
    cprint("  cc <mode>   - Toggle Confidential Compute mode (on|off)", "yellow")
    cprint("  help        - Show this help message", "white")
    cprint("  quit/exit   - Exit the program", "white")
    cprint("  clear       - Clear the screen", "yellow")
    cprint("  cc          - Confidential Compute diagnostics", "yellow")
    cprint("-" * 80, "cyan")


def run_all_diagnostics():
    """Run all diagnostic modules"""
    cprint("\n" + "=" * 80, "cyan")
    cprint("RUNNING ALL DIAGNOSTICS", "cyan", attrs=["bold"])
    cprint("=" * 80 + "\n", "cyan")
    
    diagnostics = [
        ("Driver Version & Installation", run_driver_diagnostics),
        ("PCIe Bus & Hardware", run_lspci_diagnostics),
        ("GPU Hardware State", run_gpu_hardware_diagnostics),
        ("System Information", run_proc_diagnostics),
        ("NVIDIA Services", run_nvidia_services_diagnostics),
        ("Kernel Messages", run_kernel_logs_diagnostics),
        ("InfiniBand", run_ib_diagnostics),
        ("CUDA", run_cuda_diagnostics),
        # GPU Reset excluded from "all" - must be run explicitly
    ]
    
    for name, func in diagnostics:
        cprint(f"\n{'=' * 80}", "cyan")
        cprint(f"Running: {name}", "yellow", attrs=["bold"])
        cprint("=" * 80, "cyan")
        try:
            asyncio.run(func())
        except Exception as e:
            cprint(f"\nERROR running {name}: {e}", "red", attrs=["bold"])
        cprint("\n", "white")


def main():
    """Main entry point"""
    print_banner()
    print_help()
    
    # Setup prompt_toolkit with autocomplete
    commands = [
        'driver', 'gpu', 'lspci', 'pcie', 'services', 'kernel', 'logs',
        'system', 'proc', 'ib', 'cuda', 'cuda-tests', 'all', 'reset',
        'cc on', 'cc off',
        'help', 'h', '?', 'quit', 'exit', 'q', 'clear'
    ]
    completer = WordCompleter(commands, ignore_case=True, sentence=True)
    
    # Custom style for the prompt
    style = Style.from_dict({
        'prompt': '#00aa00 bold',  # Green bold
    })
    
    # Create prompt session with history
    session = PromptSession(
        completer=completer,
        style=style,
        complete_while_typing=True,
    )
    
    while True:
        try:
            choice = session.prompt(
                HTML('<prompt>brokkr-diagnostics> </prompt>')
            ).strip().lower()
            
            if not choice:
                continue
            
            # Handle cc command with argument
            if choice.startswith("cc "):
                # check if not sudo 
                is_sudo = os.geteuid() == 0
                if not is_sudo:
                    cprint("\nPlease run as root", "red")
                    continue
                parts = choice.split()
                if len(parts) == 2:
                    mode = parts[1].lower()
                    if mode in ["on", "off"]:
                        toggle_cc_mode(mode)
                    else:
                        cprint(f"\nInvalid CC mode: '{mode}'", "red")
                        cprint("Valid modes: on, off", "yellow")
                else:
                    cprint("\nUsage: cc <mode>", "red")
                    cprint("Example: cc on", "yellow")
                continue
            
            match choice:
                case "driver":
                    asyncio.run(run_driver_diagnostics())
                
                case "gpu":
                    asyncio.run(run_gpu_hardware_diagnostics())
                
                case "lspci" | "pcie":
                    asyncio.run(run_lspci_diagnostics())
                
                case "services":
                    asyncio.run(run_nvidia_services_diagnostics())
                
                case "kernel" | "logs":
                    asyncio.run(run_kernel_logs_diagnostics())
                
                case "system" | "proc":
                    asyncio.run(run_proc_diagnostics())
                
                case "ib":
                    asyncio.run(run_ib_diagnostics())
                
                case "cuda" | "cuda-tests":
                    asyncio.run(run_cuda_diagnostics())
                
                case "reset":
                    asyncio.run(run_gpu_reset())
                
                case "all":
                    run_all_diagnostics()
                
                case "help" | "h" | "?":
                    print_help()
                
                case "clear":
                    os.system('clear')

                case "quit" | "exit" | "q":
                    cprint("\nExiting Brokkr Host Manager Diagnostics...", "red")
                    break
                
                case _:
                    cprint(f"\nUnknown command: '{choice}'", "red")
                    cprint("Type 'help' to see available commands.", "yellow")
        
        except KeyboardInterrupt:
            cprint("\n\nExiting Brokkr Host Manager Diagnostics...", "red")
            break
        except EOFError:
            cprint("\n\nExiting Brokkr Host Manager Diagnostics...", "red")
            break


if __name__ == "__main__":
    main()

