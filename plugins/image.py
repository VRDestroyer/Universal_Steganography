import numpy as np
from PIL import Image
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from plugins.common import capacity, pack_message, to_bits, unpack_message

file_type="image"

console=Console()

def encode(file,message):
    try:
        img=Image.open(file).convert("RGB") 
    except Exception as e:
        print("An error occured while opening file:", e)
        sys.exit(1)
    message_bits=to_bits(pack_message(message))
    original_shape=np.array(img).shape
    pixel_array=np.array(img).flatten()
    if len(message_bits)>len(pixel_array):
        needed=len(message.encode('utf-8'))
        console.print(Panel(f"❌ Message too long: it needs {needed} bytes, but this file can hold at most {capacity(len(pixel_array))} bytes.", border_style="red"))
        sys.exit(1)
    with console.status("[bold green]Encoding message...", spinner="dots"):
        n=len(message_bits)
        pixel_array[:n]=(pixel_array[:n]&254)|message_bits
        pixel_array=pixel_array.reshape(original_shape).astype(np.uint8)
        output_img=Image.fromarray(pixel_array)
        output_img.save("output_image.png")
    console.print(Panel("✅ [bold]Success![/bold] Saved as [cyan]output_image.png[/cyan]", border_style="green"))

def decode(file):
    try:
        img=Image.open(file).convert("RGB")
    except Exception as e:
        print("An error occured while opening file:", e)
        sys.exit(1)
    with console.status("[bold magenta]Analysing file...", spinner="dots"):
        img_pixels=np.array(img).flatten()
        message=unpack_message(img_pixels&1)
    if message is None:
        console.print(Panel("❌ No hidden message detected in this file.", title="Scan Result", border_style="red"))
        sys.exit(0)
    else:
        result=Text()
        result.append("Success! Secret message found:\n\n", style="bold green")
        result.append(message, style="yellow italic")
        console.print(Panel(result, title="🔓 Decryption Complete", border_style="green", expand=False))