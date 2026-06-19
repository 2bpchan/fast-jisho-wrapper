import asyncio
import os
# TODO try using pyaudio and manually record and handle parsing instead of using whisper_mic 
import whisper
import requests
import json
import MeCab
import wave
import sys
import pyaudio
from whisper_mic import WhisperMic

def search_jisho(input, filename="result.json"):
    url = "https://jisho.org/api/v1/search/words"
    params = {"keyword": input}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Save to file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

# search_jisho(result["text"])


# async def main():
#     mic = WhisperMic(dynamic_energy=True,energy=0)
#     async for result in mic.listen_loop_async(dictate=False, phrase_time_limit=2):
#         print(result)

# asyncio.run(main())

# mic = WhisperMic()
# result = mic.record(duration=5)
# print(result)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5
INDEX = 0

while True:
    filename = f"output/output_{INDEX}.wav"
    with wave.open(filename, 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')

        stream.close()
        p.terminate()
    # after the file is recorded, we rename it to include a done suffix to indicate that it is ready for parsing
    os.rename(filename, f"output/output_{INDEX}_done.wav")
    INDEX += 1



# TODO: add in jisho search, make more graceful start/stop, GUI, etc.