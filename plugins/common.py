import numpy as np

# Every hidden payload is MAGIC + 4-byte big-endian length + UTF-8 message,
# so decoders read exactly the message and can reject files that hold none.
MAGIC=b"STG1"
HEADER_BYTES=len(MAGIC)+4

def pack_message(message):
    data=message.encode('utf-8')
    return MAGIC+len(data).to_bytes(4,'big')+data

def capacity(slots):
    """Largest message, in UTF-8 bytes, that fits in the given number of hiding slots (one bit each)."""
    return max(slots//8-HEADER_BYTES,0)

def to_bits(data):
    return np.unpackbits(np.frombuffer(data,dtype=np.uint8))

def from_bits(bits):
    return np.packbits(np.asarray(bits,dtype=np.uint8)).tobytes()

def unpack_message(bits):
    """Returns the hidden message from a sequence of 0/1 values, or None if there isn't one."""
    header_bits=HEADER_BYTES*8
    if len(bits)<header_bits:
        return None
    header=from_bits(bits[:header_bits])
    if header[:len(MAGIC)]!=MAGIC:
        return None
    length=int.from_bytes(header[len(MAGIC):],'big')
    end=header_bits+length*8
    if end>len(bits):
        return None
    try:
        return from_bits(bits[header_bits:end]).decode('utf-8')
    except UnicodeDecodeError:
        return None
