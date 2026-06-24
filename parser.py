import re
import tkinter as tk
from tkinter import ttk
import MeCab
import requests
import whisper
import os
import romkan2


root = tk.Tk()
root.title("Treeview")

treeview = ttk.Treeview(columns=("Reading","Definitions"))

treeview.heading("#0", text="JLPT Level")
treeview.heading("Reading", text="Reading(s)")
treeview.heading("Definitions", text="Definition(s)")
treeview.column("#0", width=80, anchor="center")
treeview.column("Reading", width=150)
treeview.column("Definitions", width=300)

treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


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
        if not entry[4].startswith("助詞") and not entry[4].startswith("助動詞") and not entry[0].startswith("、") and not entry[0].startswith("。"):
            result.append([entry[0], entry[1]])
            print(entry)

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
        for term_list in terms:
            try:
                # jisho_result = search_jisho(term_list[0])
                treeview.insert('', 0, text=f"JLPT N?", values=(f"{romkan2.to_roma(term_list[1])} - {term_list[1]}", ', '.join(term_list[0])))
                # add button?
            except Exception as e:
                print(f"Error occurred while searching for {term_list[0]}: {e}")
        
        break
        # check if the file is not being used by another process
    root.after(100, parse_audio_files)



root.after(1000, parse_audio_files)
root.mainloop()

