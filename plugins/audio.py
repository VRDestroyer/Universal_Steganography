import wave
import numpy as np
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from plugins.common import capacity, pack_message, to_bits, unpack_message

file_type="audio"

console=Console()

def encode(file,message):
    with console.status("[bold green]Encoding message...", spinner="dots"):
        try:
            with wave.open(file,"rb") as f:
                params=f.getparams()
                no_of_frames=f.getnframes()
                audio_bytes=f.readframes(no_of_frames)
        except wave.Error:
            console.print(Panel("❌ Only WAV audio files are supported.", border_style="red"))
            sys.exit(1)
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)
        audio_bytes_array=np.frombuffer(audio_bytes,dtype=np.uint8).copy()
        # WAV samples are little-endian, so the first byte of each sample is its least significant one
        low_bytes=audio_bytes_array[::params.sampwidth]
        message_bits=to_bits(pack_message(message))
        if len(message_bits)>len(low_bytes):
            needed=len(message.encode('utf-8'))
            console.print(Panel(f"❌ Message too long: it needs {needed} bytes, but this file can hold at most {capacity(len(low_bytes))} bytes.", border_style="red"))
            sys.exit(1)
        n=len(message_bits)
        low_bytes[:n]=(low_bytes[:n]&254)|message_bits
        audio_bytes_array[::params.sampwidth]=low_bytes
        modified_bytes=audio_bytes_array.tobytes()
        with wave.open("output_audio.wav","wb") as f:
            f.setparams(params)
            f.writeframes(modified_bytes)
    console.print(Panel("✅ [bold]Success![/bold] Saved as [cyan]output_audio.wav[/cyan]", border_style="green"))
    
def decode(file):
    with console.status("[bold magenta]Analysing file...", spinner="dots"):
        try:
            with wave.open(file,"rb") as f:
                sample_width=f.getsampwidth()
                no_of_frames=f.getnframes()
                audio_bytes=f.readframes(no_of_frames)
        except wave.Error:
            console.print(Panel("❌ Only WAV audio files are supported.", border_style="red"))
            sys.exit(1)
        except Exception as e:
            print("An error occured while opening file:", e)
            sys.exit(1)        
        audio_bytes_array=np.frombuffer(audio_bytes,dtype=np.uint8)
        message=unpack_message(audio_bytes_array[::sample_width]&1)
    if message is None:
        console.print(Panel("❌ No hidden message detected in this file.", title="Scan Result", border_style="red"))
        sys.exit(0)
    else:
        result=Text()
        result.append("Success! Secret message found:\n\n", style="bold green")
        result.append(message, style="yellow italic")
        console.print(Panel(result, title="🔓 Decryption Complete", border_style="green", expand=False))