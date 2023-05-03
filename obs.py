# Import
import pyaudio
import wave
import cv2
import moviepy.editor as mpe
import pyautogui
import numpy as np
import keyboard
import threading

# Coding the Classes to Record AUDIO and VIDEO with the help of Threads
def merge(vidname = "Recording.mp4", audname = "Recording.wav", outname = "Recording1.mp4", FPS = 60):
        "Merges a Audio File with Video File"
        myFile = mpe.VideoFileClip(vidname)
        myAudio = mpe.AudioFileClip(audname)
        FinalFile = myFile.set_audio(myAudio)
        FinalFile.write_videofile(outname, fps = FPS)

class VideoCapture():
    """This class Captures Video"""

    cap = cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,180) # 320,180
    resolution = (1920, 1080)
    size = int(cap.get(3)),int(cap.get(4))
    codec = cv2.VideoWriter_fourcc(*"mp4v")#or*"MJPG"
    fps = 30.0
    filename="Recording.mp4"
    out = cv2.VideoWriter(filename, codec, fps, resolution)

    @classmethod
    def run(cls):
        "Records The Video File"
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

        # Resize this window
        cv2.resizeWindow("Live", 480, 640)
        while True:
            key = (yield)
            _, img = cls.cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = pyautogui.screenshot()
            frame = np.array(frame)
            frame[:180,:320] = img
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cls.out.write(frame)
            cv2.imshow('Live', frame)
            cv2.waitKey(1)
            if key=="q":
                cls.out.release()
                cls.cap.release()
                break

class AudioCapture():
    """This class Captures Audio"""

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1, 
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    frames = []

    filename = "Recording.wav"

    @classmethod
    def run(cls):
        "Records The Audio File"
        while True:
            key = (yield)
            data = cls.stream.read(1024)
            cls.frames.append(data)
            if key=='q':
                cls.save()
                break

    @classmethod
    def save(cls):
        "Saves The Audio File"
        cls.stream.stop_stream()
        cls.stream.close()
        cls.audio.terminate()
        soundfile = wave.open("Recording.wav",'wb')
        soundfile.setnchannels(1)
        soundfile.setsampwidth(cls.audio.get_sample_size(pyaudio.paInt16))
        soundfile.setframerate(44100)
        soundfile.writeframes(b''.join(cls.frames))
        soundfile.close()

# Coding the MAIN to EXCEUTE THE CODE

def Runner(obj):
    running = obj.run()
    next(running)
    while True:
        try:
            if keyboard.is_pressed('q'):
                running.send('q')
                break
            else:
                running.send(None)
        except StopIteration:
            break


def main():
    video = VideoCapture()
    audio = AudioCapture()
    VideoThread = threading.Thread(target = Runner, args = (video,))
    AudioThread = threading.Thread(target = Runner, args = (audio,))
    VideoThread.start()
    AudioThread.start()
    VideoThread.join()
    AudioThread.join()
    merge()

# CALLING THE MAIN FUNCTION FOR EXCEUTION

if __name__ == "__main__":
    main()