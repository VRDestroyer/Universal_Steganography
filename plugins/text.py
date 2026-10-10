import numpy as np
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

file_type="text"

console=Console()

def encode(file,message):
    with console.status("[bold green]Encoding message...", spinner="dots"):
        message_bin=''.join(format(ord(i),'08b') for i in message)
        zero='\u200c'
        one='\u200d'
        try:
            with open(file,"r") as f:
                original=f.read()
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)
        with open("output_text.txt","w",encoding='utf-8') as f:
            f.write(original)
            for i in message_bin:
                if i=='0':
                    f.write(zero)
                else:
                    f.write(one)
    console.print(Panel("✅ [bold]Success![/bold] Saved as [cyan]output_text.txt[/cyan]", border_style="green"))

def decode(file):
    with console.status("[bold magenta]Analysing file...", spinner="dots") as status:
        with open(file,"r") as f:
            a=f.read()
        flag=0
        for i in a:
            if ord(i) not in range(256):
                flag=1
                index=a.index(i)
                break
        if flag==0:
            status.stop()
            console.print(Panel("❌ No hidden message detected in this file.", title="Scan Result", border_style="red"))
            sys.exit(0)
        zero='\u200c'
        one='\u200d'
        coded_message=a[index:]
        message_bin=np.array([])
        for i in coded_message:
            if i==zero:
                message_bin=np.append(message_bin,0)
            elif i==one:
                message_bin=np.append(message_bin,1)
        message_bin=message_bin.reshape(-1,8)
        powers=2**np.arange(7,-1,-1)
        bytes_array=message_bin.dot(powers)
        bytes_object=bytes_array.astype(np.uint8).tobytes()
        message=bytes_object.decode('latin-1')
    result=Text()
    result.append("Success! Secret message found:\n\n", style="bold green")
    result.append(message, style="yellow italic")
    console.print(Panel(result, title="🔓 Decryption Complete", border_style="green", expand=False))

