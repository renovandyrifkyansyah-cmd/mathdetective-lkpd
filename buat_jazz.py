import numpy as np
import wave

def generate_jazz_backsound(filename="backsound.wav"):
    sample_rate = 22050
    duration = 16.0  # Durasi 16 detik (otomatis mengulang/loop)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    bpm = 80
    beat_dur = 60.0 / bpm
    audio = np.zeros_like(t)
    
    # 1. Component: Walking Bassline
    bass_notes = [43.65, 58.27, 49.00, 51.91, 43.65, 65.41, 61.74, 65.41]
    for i, freq in enumerate(t):
        current_beat = int((i / sample_rate) / beat_dur)
        note_freq = bass_notes[current_beat % len(bass_notes)]
        val = 0.6 * np.sin(2 * np.pi * note_freq * (i / sample_rate))
        val += 0.2 * np.sin(2 * np.pi * note_freq * 2 * (i / sample_rate))
        beat_pos = ((i / sample_rate) % beat_dur) / beat_dur
        env = np.exp(-3.0 * beat_pos)
        audio[i] += val * env * 0.4

    # 2. Component: Soft Jazz Piano Chords
    chords = [
        [174.61, 207.65, 261.63, 311.13], # Fm7
        [116.54, 138.59, 174.61, 207.65], # Bbm7
        [155.56, 196.00, 233.08, 277.18], # Eb7
        [207.65, 261.63, 311.13, 392.00]  # Abmaj7
    ]
    
    for i, freq in enumerate(t):
        chord_idx = int((i / sample_rate) / (beat_dur * 4)) % len(chords)
        chord = chords[chord_idx]
        beat_pos = ((i / sample_rate) % (beat_dur * 2)) / (beat_dur * 2)
        if beat_pos < 0.8:
            env = np.exp(-2.0 * beat_pos)
            chord_val = sum(np.sin(2 * np.pi * f * (i / sample_rate)) for f in chord)
            audio[i] += chord_val * env * 0.08

    # Normalisasi Audio
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.7

    # Simpan ke format WAV
    audio_int16 = (audio * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())
    print(f"✅ File audio berhasil dibuat: {filename}")

if __name__ == "__main__":
    generate_jazz_backsound("backsound.wav")