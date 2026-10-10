import wave
import numpy as np
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

file_type="audio"

console=Console()

def convert_to_bin(data):
    data_bytes=data.encode('latin-1')
    return ''.join(format(i,'08b') for i in data_bytes)

def encode(file,message):
    with console.status("[bold green]Encoding message...", spinner="dots"):
        try:
            with wave.open(file,"rb") as f:
                params=f.getparams()
                no_of_frames=f.getnframes()
                audio_bytes=f.readframes(no_of_frames)
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)
        audio_bytesarray=bytearray(audio_bytes)
        message_bin=convert_to_bin(message)
        j=0
        for i in message_bin:
            if i=='0':
                audio_bytesarray[j]=audio_bytesarray[j]&254
            else:
                audio_bytesarray[j]=audio_bytesarray[j]|1
            j+=1
        modified_bytes=bytes(audio_bytesarray)
        with wave.open("output_audio.wav","wb") as f:
            f.setparams(params)
            f.writeframes(modified_bytes)
    console.print(Panel("✅ [bold]Success![/bold] Saved as [cyan]output_audio.wav[/cyan]", border_style="green"))
    
def decode(file):
    with console.status("[bold magenta]Analysing file...", spinner="dots"):
        try:
            with wave.open(file,"rb") as f:
                no_of_frames=f.getnframes()
                audio_bytes=f.readframes(no_of_frames)
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)        
        audio_bytes_array=np.frombuffer(audio_bytes,dtype=np.uint8)
        lsb=audio_bytes_array&1
        if len(lsb)<8:
            print("No message was found.")
            sys.exit(0)
        no_of_bytes=len(lsb)//8
        lsb=lsb[:(no_of_bytes*8)]
        lsb_array=lsb.reshape(-1,8)
        powers=2**np.arange(7,-1,-1)
        lsb_bytes=lsb_array.dot(powers)
        bytes_object=lsb_bytes.astype(np.uint8).tobytes()
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