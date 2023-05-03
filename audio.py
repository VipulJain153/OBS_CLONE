import pyaudio
import wave,keyboard

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1, 
    rate=44100,
    input=True,
    frames_per_buffer=1024
)
frames=[]
while True:
    data = stream.read(1024)
    frames.append(data)
    if keyboard.is_pressed('q'):
        stream.stop_stream()
        stream.close()
        audio.terminate()
        soundfile = wave.open("Recording.wav",'wb')
        soundfile.setnchannels(1)
        soundfile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        soundfile.setframerate(44100)
        soundfile.writeframes(b''.join(frames))
        soundfile.close()
        break