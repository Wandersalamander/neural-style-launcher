from tkinter import *
import tkinter.messagebox as box
from os import listdir
import os
import subprocess
from natsort import natsorted


def only_name(path):
    '''Removes path and file ending from file'''
    path = path.replace("\\", "/")
    name = path.split("/")[-1]
    name = name[:name.index(".")]
    return name


def resized_path(file):
    '''Makes resized copy of image and returns location'''
    file_old = str(file)
    if file.count(".") != 1:
        raise Exception("File has more than one points:" + str(file))
    file = file.replace(".", "_%dpx." % SIZE)
    file != file_old
    resize = ["convert", file_old, "-resize", str(SIZE), file]
    subprocess.check_output(resize)
    return file


def run_nstf(content, style, output, checkpoint_output):
    '''Runs neural style transfer

    Notes
    -----
    if output file already exists, its renamed to *_old.*
    and used as initial guess
    '''
    content = resized_path(content)
    style = resized_path(style)
    output = str(output)
    commands = [
        PYTHONPATH,
        NEURAL_PATH + "neural_style.py",
        "--content", content,
        "--styles", style,
        "--output", output,
        "--checkpoint-output", str(checkpoint_output),
        "--checkpoint-iterations", "100",
        "--network", NEURAL_PATH + "imagenet-vgg-verydeep-19.mat"
    ]
    if os.path.isfile(output):
        assert output.count(".") == 1
        initial_guess = output.replace(".", "_old.")
        os.rename(output, initial_guess)
        commands.append("--initial")
        commands.append(initial_guess)
    for cmd in commands:
        print(cmd)
    print()
    print(subprocess.check_output(commands, env={"PATH": NEURAL_PATH}))
    os.remove(content)
    os.remove(style)

PYTHONPATH = "/home/simon/anaconda3/bin/python"
NEURAL_PATH = "/home/simon/Git/neural-style/"
SIZE = 600  # resolution of images
path = str(os.getcwd()) + "/"
dir_content = path + "content/"
dir_styles = path + "styles/"

window = Tk()
window.title('Run neural-style resolution' + str(SIZE))

frame = Frame(window)

listbox_content = Listbox(frame, exportselection=0)
for name in natsorted(listdir(dir_content)):
    if name != ".keep":
        listbox_content.insert('end', name)

listbox_style = Listbox(frame, exportselection=0)
for name in natsorted(listdir(dir_styles)):
    if name != ".keep":
        listbox_style.insert('end', name)


def dialog():
    entry_content = listbox_content.get(listbox_content.curselection())
    entry_style = listbox_style.get(listbox_style.curselection())
    name1 = only_name(entry_content)
    name2 = only_name(entry_style)
    output_name = path + "output/%s_%s.jpg" % (name1, name2)
    content = entry_content
    style = entry_style
    output = output_name
    box.showinfo('Selection', 'Running Job: ' + output_name)
    checkpoint_output = output_name.replace(
        ".", r"_{}.").replace("/output/", "/checkpoints/")
    run_nstf(dir_content + content, dir_styles +
             style, output, checkpoint_output)
    box.showinfo('Selection', 'Completed Job: ' + output_name)


btn = Button(frame, text='Run', command=dialog)

btn.pack(side=RIGHT, padx=5)
listbox_content.pack(side=LEFT)
listbox_style.pack(side=LEFT)
frame.pack(padx=30, pady=30)

if __name__ == "__main__":
    window.mainloop()
