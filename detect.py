import magic
import os

def file_type(file):
    mime_type=magic.from_file(file,mime=True)
    if '/' in mime_type:
        primary_type, sub_type=mime_type.split('/', 1)
    else:
        primary_type=mime_type 
    if primary_type in ('image', 'video', 'audio', 'text'):
        return primary_type