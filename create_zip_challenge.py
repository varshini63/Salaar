#!/usr/bin/env python3
"""
Script to create the Layer 2 ZIP challenge files
Creates 14 small ZIP files with CRC-crackable content
"""

import zipfile
import os
import shutil

# The flag to be split across 14 files
FLAG = "CTF{Salaar_devaratha_raisaar}"

# Split flag into 14 parts (approximately equal)
def split_flag(flag, parts=14):
    """Split flag into equal parts"""
    chunk_size = len(flag) // parts
    remainder = len(flag) % parts
    
    chunks = []
    start = 0
    
    for i in range(parts):
        # Add 1 extra char to first 'remainder' chunks
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(flag[start:end])
        start = end
    
    return chunks

def create_small_zip(content, filename, password=None):
    """Create a small ZIP file with given content"""
    # Create a temporary text file
    temp_file = "temp_flag.txt"
    with open(temp_file, 'w') as f:
        f.write(content)
    
    # Create ZIP with password protection
    with zipfile.ZipFile(filename, 'w') as zf:
        if password:
            zf.setpassword(password.encode())
            zf.write(temp_file, os.path.basename(temp_file.replace('.txt', '')))
        else:
            zf.write(temp_file, os.path.basename(temp_file.replace('.txt', '')))
    
    # Remove temp file
    os.remove(temp_file)

def main():
    print("[*] Creating Layer 2 ZIP Challenge Files")
    print(f"[*] Flag: {FLAG}")
    
    # Create challenges directory
    os.makedirs('challenges/flag_parts', exist_ok=True)
    
    # Split the flag
    parts = split_flag(FLAG, 14)
    print(f"[*] Split into {len(parts)} parts")
    
    # Create individual ZIP files
    for i, part in enumerate(parts):
        zip_name = f'challenges/flag_parts/flag{i:02d}.zip'
        
        # Create small text file and zip it
        flag_filename = f'flag{i:02d}'
        
        # Write small file
        with open(f'challenges/flag_parts/{flag_filename}', 'w') as f:
            f.write(part)
        
        # Create ZIP without password (makes it CRC-crackable)
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(f'challenges/flag_parts/{flag_filename}', flag_filename)
        
        # Remove the unzipped file
        os.remove(f'challenges/flag_parts/{flag_filename}')
        
        print(f"[+] Created {zip_name} with content: '{part}'")
    
    # Create master ZIP containing all flag ZIPs
    print("[*] Creating master flag_parts.zip")
    with zipfile.ZipFile('challenges/flag_parts.zip', 'w') as master_zip:
        for i in range(14):
            zip_name = f'flag_parts/flag{i:02d}.zip'
            master_zip.write(f'challenges/{zip_name}', zip_name)
    
    print("[+] Master ZIP created: challenges/flag_parts.zip")
    print(f"[+] Total size: {os.path.getsize('challenges/flag_parts.zip')} bytes")
    
    # Clean up individual ZIPs from flag_parts directory (keep only in master)
    # Comment this out if you want to keep them for testing
    # shutil.rmtree('challenges/flag_parts')
    
    print("\n[*] Challenge files created successfully!")
    print("[*] To solve:")
    print("    1. Extract flag_parts.zip")
    print("    2. Each flag##.zip contains a small file (4 chars)")
    print("    3. Use CRC collision tools to extract content")
    print("    4. Concatenate all parts in order")
    print(f"    5. Submit: {FLAG}")

if __name__ == '__main__':
    main()