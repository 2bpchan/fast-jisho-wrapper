import re
from tkinter import StringVar, Tk, ttk
import MeCab
import requests
import whisper
import os


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# tk variable for the text area
display_text = StringVar()
# add a textarea to display the parsed text
text_area = ttk.Label(frm, textvariable=display_text).grid(column=0, row=1)
model = whisper.load_model("small")
# to keep track of parsed files

mecab = MeCab.Tagger()


def extract_terms(text):
    sentence = mecab.parse(text).splitlines()
    result = []
    for line in sentence:
        if line == "EOS":
            break
        entry = line.split("\t")
        if not entry[4].startswith("助詞") and not entry[4].startswith("助動詞"):
            result.append(entry[0])
    return result

def search_jisho(input):
    url = "https://jisho.org/api/v1/search/words"
    params = {"keyword": input}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        
        result_dict = {
            "jlpt": result["data"][0]["jlpt"][0][-1] if len(result["data"][0]["jlpt"]) > 0 else 0,
            "reading": result["data"][0]["japanese"][0]["reading"],
            "english_definitions": result["data"][0]["senses"][0]["english_definitions"]
        }
        return result_dict
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

parsed_files = {}
def parse_audio_files():
    filenames = os.listdir("output")
    # iterate through the files and print the name of each file
    for filename in filenames:
        if not filename.endswith("done.wav"):
            continue
        if filename in parsed_files:
            if os.access(f"output/{filename}", os.W_OK):
                os.remove(f"output/{filename}")
            continue
        print(filename)
        result = model.transcribe(f"output/{filename}")
        # add to parsed_files
        parsed_files[filename] = result["text"]
        # print(result["text"])
        # display_text.set(display_text.get() + "\n" + result["text"])
        terms = extract_terms(''.join(re.findall(r'[^\x00-\x7F]+', result["text"])))
        # display_text.set(display_text.get() + "\n" + ", ".join(terms))
        for term in terms:
            try:
                jisho_result = search_jisho(term)
                display_text.set(display_text.get() + f"\n{term} (JLPT N{jisho_result['jlpt']}): Reading: {jisho_result['reading']}, Definitions: {', '.join(jisho_result['english_definitions'])}")
            except Exception as e:
                display_text.set(display_text.get() + f"\n{term}: No results found")

        
        break
        # check if the file is not being used by another process
    root.after(100, parse_audio_files)



root.after(1000, parse_audio_files)
root.mainloop()

