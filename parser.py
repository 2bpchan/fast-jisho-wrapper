from tkinter import StringVar, Tk, ttk
import MeCab
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

print(mecab.parse("猿も木から落ちる").splitlines().map(lambda x: x.split("\t")[0] if "\t" in x else x))
# TODO figure out how to map over a list of strings in python, the above code is not working

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
        print(result["text"])
        display_text.set(display_text.get() + "\n" + result["text"])
        
        break
        # check if the file is not being used by another process
    root.after(100, parse_audio_files)



root.after(1000, parse_audio_files)
root.mainloop()

