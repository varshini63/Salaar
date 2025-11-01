#!/usr/bin/env python3
"""
Fixed DTMF WAV Generator for Layer 3
Creates a WAV file without requiring numpy
"""

import wave
import math
import struct
import os

# DTMF frequencies for each digit
DTMF_TABLE = {
    '0': (941, 1336), '1': (697, 1209), '2': (697, 1336),
    '3': (697, 1477), '4': (770, 1209), '5': (770, 1336),
    '6': (770, 1477), '7': (852, 1209), '8': (852, 1336),
    '9': (852, 1477), '*': (941, 1209), '#': (941, 1477),
}

def generate_dtmf_tone(digit, duration=0.2, sample_rate=44100):
    """Generate DTMF tone for a single digit"""
    if digit not in DTMF_TABLE:
        # Return silence for invalid digits
        return [0] * int(duration * sample_rate)
    
    low_freq, high_freq = DTMF_TABLE[digit]
    samples = []
    
    for i in range(int(sample_rate * duration)):
        t = i / sample_rate
        # Generate two sine waves and add them
        sample = math.sin(2 * math.pi * low_freq * t) + math.sin(2 * math.pi * high_freq * t)
        # Normalize and convert to 16-bit integer
        sample = int((sample / 2.0) * 32767)
        samples.append(sample)
    
    return samples

def text_to_ascii_digits(text):
    """Convert text to ASCII digit sequence"""
    return ''.join(str(ord(c)) for c in text)

def create_dtmf_wav(message, output_file, tone_duration=0.2, silence_duration=0.05):
    """Create WAV file with DTMF-encoded message"""
    
    # Convert message to ASCII codes
    ascii_sequence = text_to_ascii_digits(message)
    print(f"[*] Message: {message}")
    print(f"[*] ASCII sequence: {ascii_sequence}")
    print(f"[*] Length: {len(ascii_sequence)} digits")
    
    sample_rate = 44100
    all_samples = []
    
    # Generate DTMF for each digit
    for i, digit in enumerate(ascii_sequence):
        if (i + 1) % 10 == 0:
            print(f"[*] Encoding digit {i+1}/{len(ascii_sequence)}")
        
        # Generate tone
        tone_samples = generate_dtmf_tone(digit, tone_duration, sample_rate)
        
        # Add silence between tones
        silence_samples = [0] * int(silence_duration * sample_rate)
        
        all_samples.extend(tone_samples)
        all_samples.extend(silence_samples)
    
    # Write WAV file
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Pack samples as 16-bit integers
        packed_samples = struct.pack('<' + 'h' * len(all_samples), *all_samples)
        wav_file.writeframes(packed_samples)
    
    file_size = os.path.getsize(output_file)
    duration = len(all_samples) / sample_rate
    
    print(f"[+] WAV file created: {output_file}")
    print(f"[+] Duration: {duration:.2f} seconds")
    print(f"[+] File size: {file_size} bytes ({file_size/1024:.1f} KB)")

def main():
    print("=" * 60)
    print("[*] Creating Layer 3 DTMF WAV Challenge")
    print("=" * 60)
    print()
    
    # The message to encode
    message = "CTF{CRYPTOGRAPHY}"
    
    # Create challenges directory if it doesn't exist
    os.makedirs('challenges', exist_ok=True)
    
    # Create WAV file
    output_file = 'challenges/khansaar_transmission.wav'
    create_dtmf_wav(message, output_file)
    
    print()
    print("=" * 60)
    print("[+] Challenge file created successfully!")
    print("=" * 60)
    print()
    print("To solve this challenge:")
    print("  1. Download khansaar_transmission.wav")
    print("  2. Use DTMF decoder tool")
    print(f"  3. Decode to get: {text_to_ascii_digits(message)}")
    print("  4. Convert ASCII codes to text")
    print(f"  5. Submit: {message}")
    print()

if __name__ == '__main__':
    main()