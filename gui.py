import json
from tkinter import *
from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()
import requests

import re

# text = "猿も木から落ちる。私は学some random Englishです。"
# # Find all non-ASCII blocks
# non_english = ''.join(re.findall(r'[^\x00-\x7F]+', text))
# print(non_english)

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
    
print(search_jisho("鬱"))