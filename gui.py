import json
# from tkinter import *
# from tkinter import ttk
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

# def search_jisho(input):
#     url = "https://jisho.org/api/v1/search/words"
#     params = {"keyword": input}
    
#     response = requests.get(url, params=params)
    
#     if response.status_code == 200:
#         result = response.json()
        
#         result_dict = {
#             "jlpt": result["data"][0]["jlpt"][0][-1] if len(result["data"][0]["jlpt"]) > 0 else 0,
#             "reading": result["data"][0]["japanese"][0]["reading"],
#             "english_definitions": result["data"][0]["senses"][0]["english_definitions"]
#         }
#         return result_dict
#     else:
#         raise Exception(f"Request failed with status code {response.status_code}")
                                        
# print(search_jisho("鬱"))

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("Tkinter Treeview")

treeview = ttk.Treeview(columns=("Salary","Bonus"))

treeview.heading("#0", text="JLPT Level")
treeview.heading("Salary", text="Reading(s)")
treeview.heading("Bonus", text="Definition(s)")

# level1 = treeview.insert('', tk.END, text="San Jose")

treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

treeview.insert('', tk.END, text="John Doe", values=(f"${100000: ,}",f"${8000: ,}"))
treeview.insert('', tk.END, text="Jane Doe", values=(f"${120000: ,}",f"${9000: ,}"))

# Insert a new row at the top of the treeview
treeview.insert('', 0, text="Alice Smith", values=(f"${150000: ,}",f"${10000: ,}"))



root.mainloop()