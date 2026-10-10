import numpy as np
from PIL import Image
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

file_type="image"

console=Console()

def convert_to_bin(data):
    data_bytes=data.encode('latin-1')
    return ''.join(format(i,'08b') for i in data_bytes)

def encode(file,message):
    try:
        img=Image.open(file).convert("RGB") 
    except Exception as e:
        print("An error occured while opening file:", e)
        sys.exit(1)
    with console.status("[bold green]Encoding message...", spinner="dots"):
        message_bin=convert_to_bin(message)
        img=Image.open(file).convert("RGB")
        original_shape=np.array(img).shape
        pixel_array=np.array(img).flatten()
        j=0
        for i in message_bin:
            if i=='0':
                pixel_array[j]=pixel_array[j]&254
            else:
                pixel_array[j]=pixel_array[j]|1
            j+=1
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
        lsb_pixels=img_pixels&1
        if len(lsb_pixels)<8:
            print("No message was found.")
            sys.exit(0)
        no_of_bytes=len(lsb_pixels)//8
        lsb_pixels=lsb_pixels[:no_of_bytes*8]
        lsb_pixels_2d=lsb_pixels.reshape(-1,8)
        powers=2**np.arange(7,-1,-1)
        bytes_array=lsb_pixels_2d.dot(powers)
        bytes_object=bytes_array.astype(np.uint8).tobytes()
        message_bytes=bytearray()
        count=0
        for i in bytes_object:
            if i<=126 and i>=32:
                a=bytes([i])
                message_bytes.extend(a)
                count+=1
            else:
                break
    if count<5:
        console.print(Panel("❌ No hidden message detected in this file.", title="Scan Result", border_style="red"))
        sys.exit(0)
    else:
        message=message_bytes.decode('latin-1')
        result=Text()
        result.append("Success! Secret message found:\n\n", style="bold green")
        result.append(message, style="yellow italic")
        console.print(Panel(result, title="🔓 Decryption Complete", border_style="green", expand=False))