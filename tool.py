import sys
import os
import detect
import importlib
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console=Console()

def get_plugins():
    plugins={}
    for filename in os.listdir('plugins'):
        if filename.endswith(".py") and filename!="__init__.py":
            module_name=f"plugins.{filename[:-3]}"
            module=importlib.import_module(module_name)
            if hasattr(module,'file_type'):
                plugins[module.file_type]=module
    return plugins

def main():
    plugins=get_plugins()
    os.system('cls' if os.name=='nt' else 'clear')
    title=Text("🕵️ UNIVERSAL STEGANOGRAPHY TOOL", style="bold cyan")
    subtitle=Text("\nSecurely hide messages within files",style="dim italic")
    console.print(Panel(title+subtitle,border_style="bright_blue",padding=(1,2)))
    file=questionary.path("📁 Enter file name:").ask()
    if not os.path.exists(file):
        console.print("[bold red]❌ Error:[/bold red] File not found.", style="red")
        sys.exit(1)
    if not detect.file_type(file):
        console.print(f"[bold yellow]⚠️ Unidentified or unsupported file type[/bold yellow]")
        sys.exit(0)
    choice=questionary.select("What would you like to do?",choices=["Hide a message (Encode)","Reveal a message (Decode)","Exit"],style=questionary.Style([('pointer', 'fg:cyan bold'),('selected', 'fg:cyan'),])).ask()
    file_type=detect.file_type(file)
    required_module=plugins.get(file_type)
    if not required_module:
        console.print(f"[bold yellow]⚠️ Unidentified or unsupported file type[/bold yellow]")
        sys.exit(0)
    if "Hide" in choice:
        message=questionary.text("💬 Enter the secret message:").ask()
        required_module.encode(file,message)
    elif "Reveal" in choice:
        required_module.decode(file)
    else:
        console.print("[dim]Exiting...[/dim]")

if __name__=="__main__":
    main()
