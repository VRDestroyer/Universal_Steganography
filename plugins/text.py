import re
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from plugins.common import pack_message, to_bits, unpack_message

file_type="text"

console=Console()

zero='\u200c'
one='\u200d'

def encode(file,message):
    with console.status("[bold green]Encoding message...", spinner="dots"):
        message_bits=to_bits(pack_message(message))
        try:
            with open(file,"r",encoding='utf-8') as f:
                original=f.read()
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)
        with open("output_text.txt","w",encoding='utf-8') as f:
            # Drop any message already at the end, otherwise the new bits would merge into its run
            f.write(original.rstrip(zero+one))
            for i in message_bits:
                if i==0:
                    f.write(zero)
                else:
                    f.write(one)
    console.print(Panel("✅ [bold]Success![/bold] Saved as [cyan]output_text.txt[/cyan]", border_style="green"))

def decode(file):
    with console.status("[bold magenta]Analysing file...", spinner="dots") as status:
        try:
            with open(file,"r",encoding='utf-8') as f:
                a=f.read()
        except Exception as e:
            status.stop()
            print("An error occured while opening file:", e)
            sys.exit(1)
        # The message is a run of zero-width characters appended to the text. U+200D also joins
        # emoji (e.g. 👨‍👩‍👧), so check each run from the end and keep the first with a valid header.
        message=None
        for run in reversed(re.findall(f"[{zero}{one}]+",a)):
            message=unpack_message([0 if i==zero else 1 for i in run])
            if message is not None:
                break
        if message is None:
            status.stop()
            console.print(Panel("❌ No hidden message detected in this file.", title="Scan Result", border_style="red"))
            sys.exit(0)
    result=Text()
    result.append("Success! Secret message found:\n\n", style="bold green")
    result.append(message, style="yellow italic")
    console.print(Panel(result, title="🔓 Decryption Complete", border_style="green", expand=False))

