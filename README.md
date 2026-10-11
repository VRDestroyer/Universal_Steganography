# Universal Steganography Tool

An interactive command-line tool that hides secret text messages inside images, audio, text and video files, and reveals them again.

## Setup

Requires Python 3.9+ and the `libmagic` system library (used to detect file types).

```bash
# macOS
brew install libmagic
# Debian / Ubuntu
sudo apt install libmagic1

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, install `python-magic-bin` instead of `python-magic`, since it bundles libmagic.

## Usage

```bash
python tool.py
```

1. Choose **Hide a message (Encode)**, **Reveal a message (Decode)** or **Exit**.
2. Enter the path to the file.
3. When encoding, type the secret message.

The result is written to the current directory as `output_image.png`, `output_audio.wav`, `output_text.txt` or `output_video.mp4`. These files overwrite earlier output of the same type. Press Ctrl-C at any prompt to quit.

## How it works

The file type is detected from the file's contents with libmagic (`detect.py`), and the matching plugin in `plugins/` does the work.

| File type | Supported input | Technique |
|---|---|---|
| Image | Any format Pillow opens (PNG, JPEG, BMP, ...) | Least-significant-bit (LSB) hiding in the RGB channel values. Always saved as PNG, because lossy formats like JPEG would destroy the hidden bits. |
| Audio | Uncompressed (PCM) WAV only | LSB hiding in the least significant byte of each sample, so each sample changes by at most 1. |
| Text | UTF-8 text files | Message bits added to the end of the text as invisible zero-width characters (U+200C = 0, U+200D = 1). |
| Video | MP4 | Message bytes appended after the end of the MP4 file, where players ignore them. |

For images, audio and text, the hidden data is laid out as:

```
"STG1" (4 bytes) | message length (4 bytes, big-endian) | message (UTF-8)
```

The marker and length let the decoder read exactly the message, support any Unicode text, and report "no hidden message" for files that don't contain one. The helpers for this are in `plugins/common.py`.

### Capacity

| File type | Maximum message size |
|---|---|
| Image | `width × height × 3 / 8 − 8` bytes (about 33 KB for a 300×300 image) |
| Audio | `samples × channels / 8 − 8` bytes (about 5.5 KB per second of mono 44.1 kHz audio, 11 KB for stereo) |
| Text and video | No practical limit |

If a message doesn't fit, the tool reports the maximum size and writes nothing.

## Limitations

- **Messages are not encrypted.** Anyone who knows the technique can read them.
- **Video:** the message sits in plain bytes after the end of the file, so a hex editor shows it immediately. Only the MP4 structure is understood: other video formats are saved as `.mp4` anyway and may not decode.
- **Images:** the hidden bits are destroyed if the output is re-saved as JPEG, resized or edited.
- **Text:** some editors, websites and chat apps strip zero-width characters.
- Files hidden with versions before the `STG1` format can't be decoded.

## Adding a file type

Create `plugins/<name>.py` with a module-level `file_type` string (the primary MIME type, such as `"image"`) and `encode(file, message)` and `decode(file)` functions. `tool.py` loads it automatically. `detect.py` only reports `image`, `video`, `audio` and `text`, so a new type also needs adding there.
