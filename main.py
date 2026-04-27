import whisper
import requests
import json
import MeCab

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
    
mecab = MeCab.Tagger()

model = whisper.load_model("small")
result = model.transcribe("audio.m4a")
print(result["text"])

print(mecab.parse(result["text"]))

# search_jisho(result["text"])
