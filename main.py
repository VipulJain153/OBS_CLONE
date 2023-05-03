import pyaudio
import wave
import cv2
import moviepy.editor as mpe
import pyautogui
import numpy as np
import keyboard

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1, 
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

frames = []

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,180) # 320,180
resolution = (1920, 1080)
size = int(cap.get(3)),int(cap.get(4))
codec = cv2.VideoWriter_fourcc(*"XVID")#or*"MJPG"
fps = 10.0
filename="Recording.avi"

out = cv2.VideoWriter(filename, codec, fps, resolution)

cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# Resize this window
cv2.resizeWindow("Live", 480, 640)

while True:
    success, img = cap.read()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    frame = pyautogui.screenshot()
    frame = np.array(frame)
    frame[:180,:320] = img
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    out.write(frame)
    cv2.imshow('Live', frame)
    data = stream.read(1024)
    frames.append(data)

    if (cv2.waitKey(1) and 0xFF == ord('q')) or keyboard.is_pressed('q'):
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

out.release()
cap.release()
cv2.destroyAllWindows()

myFile = mpe.VideoFileClip(filename)
myAudio = mpe.AudioFileClip("Recording.wav")
FinalFile = myFile.set_audio(myAudio)
FinalFile.write_videofile("main.mp4",fps=fps)
