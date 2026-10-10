import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

file_type="video"

console=Console()

def encode(file,message):
    with console.status("[bold green]Encoding message...", spinner="dots"):
        try:
            with open(file,"rb") as f:
                print("Creating new video with hidden message... ")
                existing_data=f.read()
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)
        message_bytes=message.encode('latin-1')
        with open("output_video.mp4","wb") as f:
            f.write(existing_data)
            f.write(message_bytes)
    console.print(Panel("✅ [bold]Success![/bold] Saved as [cyan]output_video.mp4[/cyan]", border_style="green"))

def decode(file_path):
    with console.status("[bold magenta]Analysing file...", spinner="dots"):
        file_size=os.path.getsize(file_path)
        last_valid_end=0
        with open(file_path,'rb') as f:
            while f.tell()<file_size:
                cur_pos=f.tell()
                header=f.read(8)
                if len(header)<8: 
                    break
                size=int.from_bytes(header[:4], 'big')
                if cur_pos+size>file_size or size<8:
                    break
                f.seek(cur_pos+size)
                last_valid_end=f.tell()
        extra_size=file_size-last_valid_end
    if extra_size>0:
        with open(file_path,'rb') as f:
            f.seek(last_valid_end)
            message=f.read().decode('latin-1')
        result=Text()
        result.append("Success! Secret message found:\n\n", style="bold green")
        result.append(message, style="yellow italic")
        console.print(Panel(result, title="🔓 Decryption Complete", border_style="green", expand=False))
    else:
        console.print(Panel("❌ No hidden message detected in this file.", title="Scan Result", border_style="red"))
        sys.exit(0)