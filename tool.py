import sys
import os
import detect
import importlib
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console=Console()

PLUGIN_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),'plugins')

def get_plugins():
    plugins={}
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and filename!="__init__.py":
            module_name=f"plugins.{filename[:-3]}"
            module=importlib.import_module(module_name)
            if hasattr(module,'file_type'):
                plugins[module.file_type]=module
    return plugins

def ask(question):
    # questionary returns None when the user presses Ctrl-C
    answer=question.ask()
    if answer is None:
        console.print("[dim]Exiting...[/dim]")
        sys.exit(0)
    return answer

def main():
    plugins=get_plugins()
    os.system('cls' if os.name=='nt' else 'clear')
    title=Text("🕵️ UNIVERSAL STEGANOGRAPHY TOOL", style="bold cyan")
    subtitle=Text("\nSecurely hide messages within files",style="dim italic")
    console.print(Panel(title+subtitle,border_style="bright_blue",padding=(1,2)))
    choice=ask(questionary.select("What would you like to do?",choices=["Hide a message (Encode)","Reveal a message (Decode)","Exit"],style=questionary.Style([('pointer', 'fg:cyan bold'),('selected', 'fg:cyan'),])))
    if choice=="Exit":
        console.print("[dim]Exiting...[/dim]")
        sys.exit(0)
    file=ask(questionary.path("📁 Enter file name:"))
    if not os.path.isfile(file):
        console.print("[bold red]❌ Error:[/bold red] File not found.", style="red")
        sys.exit(1)
    required_module=plugins.get(detect.file_type(file))
    if not required_module:
        console.print(f"[bold yellow]⚠️ Unidentified or unsupported file type[/bold yellow]")
        sys.exit(0)
    if "Hide" in choice:
        message=ask(questionary.text("💬 Enter the secret message:"))
        required_module.encode(file,message)
    else:
        required_module.decode(file)

if __name__=="__main__":
    main()
