import pyaudio
import wave

import pyaudio
import wave


def record(record_active, frames):
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,  # 16-bit format for audio recording
        channels=1,  # Mono channel
        rate=44100,  # 44100 Hz -> standard sample rate for audio recording
        input=True,  # Input mode for recording audio (not sending data anywhere)
        frames_per_buffer=1024  # Record in chunks of 1024 frames
    )

    # While the recording flag is active, capture audio data
    while record_active.is_set():
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio data to a WAV file
    sound_file = wave.open("voices/voice_prompt.wav", mode="wb")  # Open file in write-binary mode
    sound_file.setnchannels(1)  # Set to mono
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))  # Set sample width based on format
    sound_file.setframerate(44100)  # Set the sample rate
    sound_file.writeframes(b''.join(frames))  # Write the collected audio data to the file
    sound_file.close()

