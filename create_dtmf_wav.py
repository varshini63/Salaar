#!/usr/bin/env python3
"""
Script to create the Layer 3 DTMF WAV challenge file
Encodes a message as DTMF tones in a WAV file
"""

import numpy as np
import wave
import struct

# DTMF frequencies for each digit
DTMF_TABLE = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477),
}

def generate_dtmf_tone(digit, duration=0.2, sample_rate=44100):
    """Generate DTMF tone for a single digit"""
    if digit not in DTMF_TABLE:
        # Return silence for invalid digits
        return np.zeros(int(duration * sample_rate))
    
    low_freq, high_freq = DTMF_TABLE[digit]
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate the two frequency components
    tone = np.sin(2 * np.pi * low_freq * t) + np.sin(2 * np.pi * high_freq * t)
    
    # Normalize
    tone = tone / np.max(np.abs(tone))
    
    return tone

def text_to_ascii_digits(text):
    """Convert text to space-separated ASCII codes"""
    return ''.join(str(ord(c)) for c in text)

def create_dtmf_wav(message, output_file, tone_duration=0.2, silence_duration=0.05):
    """Create WAV file with DTMF-encoded message"""
    
    # Convert message to ASCII codes
    ascii_sequence = text_to_ascii_digits(message)
    print(f"[*] Message: {message}")
    print(f"[*] ASCII sequence: {ascii_sequence}")
    print(f"[*] Length: {len(ascii_sequence)} digits")
    
    sample_rate = 44100
    audio_data = np.array([])
    
    # Generate DTMF for each digit
    for i, digit in enumerate(ascii_sequence):
        if i % 10 == 0:
            print(f"[*] Encoding digit {i+1}/{len(ascii_sequence)}")
        
        # Generate tone
        tone = generate_dtmf_tone(digit, tone_duration, sample_rate)
        
        # Add silence between tones
        silence = np.zeros(int(silence_duration * sample_rate))
        
        audio_data = np.concatenate([audio_data, tone, silence])
    
    # Normalize final audio
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"[+] WAV file created: {output_file}")
    print(f"[+] Duration: {len(audio_data) / sample_rate:.2f} seconds")
    print(f"[+] File size: {len(audio_data.tobytes())} bytes")

def main():
    print("[*] Creating Layer 3 DTMF WAV Challenge")
    
    # The message to encode
    message = "CTFlean{CRYPTOGRAPHY}"
    
    # Create challenges directory
    import os
    os.makedirs('challenges', exist_ok=True)
    
    # Create WAV file
    output_file = 'challenges/khansaar_transmission.wav'
    create_dtmf_wav(message, output_file)
    
    print("\n[*] Challenge file created successfully!")
    print("[*] To solve:")
    print("    1. Download khansaar_transmission.wav")
    print("    2. Use DTMF decoder (online or tools like dtmf.py, multimon-ng)")
    print(f"    3. Decode to get: {text_to_ascii_digits(message)}")
    print("    4. Convert ASCII codes to text")
    print(f"    5. Submit: {message}")

if __name__ == '__main__':
    main()