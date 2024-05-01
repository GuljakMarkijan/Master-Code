from tkinter import *
import ctypes
import re 
import os 

def execute(event=None):
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    os.system('start cmd /K "python run.py"')

def changes(event=None):
    global previousText
    if editArea.get('1.0', END) ==previousText:
        return
    
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0","end")

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)
            i+=1

    previousText = editArea.get('1.0', END)

def search_re(pattern, text):
    matches = []
    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
    
    return matches


def rgb(rgb):
    return "#%02x%02x%02x" % rgb

ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
root.geometry('700x500')
root.title('Master Code')
previousText = ''

normal = rgb((0, 209, 7))
keywords = rgb((228, 232, 0))
comments = rgb((135, 135, 134))
string = rgb((13, 0, 255))
function = rgb((0, 255, 255))
background = rgb((0, 0, 0))
font = 'Consolas 15'

repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\".*?\"', string],
    ['#.*?$', comments],
]

editArea = Text(
    root, background=background, foreground=normal, insertbackground=normal,relief=FLAT, borderwidth=30, font=font
)

editArea.pack(fill=BOTH, expand=1)

editArea.insert('1.0', """""")

editArea.bind('<KeyRelease>', changes)

root.bind('<Control-r>', execute)

changes()

root.mainloop()