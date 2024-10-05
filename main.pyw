from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askdirectory
from os import mkdir, path, listdir, startfile
from textwrap import shorten
from shutil import move as sort_into

root = Tk()
root.title("File Organizer")
root.geometry("700x550")
root.minsize(500, 300)
root.iconbitmap("icon.ico")

Label(root, text="File Organizer", font=("TkDefaultFont", 25, "bold")).pack(pady=2)
Label(root, text="Clean up that folder!").pack()

folders = []

folders_frame = Frame(root)
folders_frame.pack(expand=True)

label_frames = Frame(root)
label_frames.pack(side=BOTTOM, pady=25)

options_frame = LabelFrame(label_frames, text="Jobs", borderwidth=4)
options_frame.pack(side=LEFT, padx=5)

def get_folderInput():
    global result
    result = None
    temp_window = Tk()
    temp_window.title("New Folder")
    temp_window.iconbitmap("icon.ico")
    temp_window.focus_force()

    name_frame = Frame(temp_window)
    name_frame.pack(pady=10, fill=X, padx=2)
    Label(name_frame, text="Folder Name: ").pack(side=LEFT)
    name_entry = Entry(name_frame)
    name_entry.pack()

    type_frame = Frame(temp_window)
    type_frame.pack(fill=X, padx=2)
    Label(type_frame, text="Folder Type: ").pack(side=LEFT)
    def on_choose(e=None):
        name_entry.delete("0", END)
        name_entry.insert("0", folder_type.get())
    folder_type = StringVar(type_frame, value="Audio Files")
    on_choose()
    type_options = OptionMenu(type_frame, folder_type, "Audio Files", "Video Files", "Executables", "Compressed Files", "Image Files", "Documents", command=on_choose)
    type_options.pack()

    x = Frame(temp_window)
    x.pack(side=BOTTOM, pady=4)

    def close():
        temp_window.quit()
        temp_window.destroy()
        return None
    temp_window.protocol("WM_DELETE_WINDOW", close)
    def ok():
        global result
        folder_name, folder_Type = name_entry.get(), folder_type.get()
        print(folder_name, folder_Type)
        if not folder_name.strip(): return
        for folder in folders:
            if folder["Type"] == folder_Type:
                showerror("Error", "There's already a folder with the same type!")
                return
            elif folder["Name"] == folder_name:
                showerror("Error", "There's already a folder with the same name!")
                return
        result = folder_name, folder_Type
        print(result)
        temp_window.quit()
        temp_window.destroy()
        print(result)
        return result
    Button(x, text="OK", width=15, command=ok).pack(side=LEFT, padx=3)
    Button(x, text="Cancel", width=15, command=close).pack(side=LEFT)

    temp_window.resizable(False, False)
    temp_window.mainloop()

def add():
    global folders, folders_frame
    get_folderInput()
    if result is None:
        print("User canceled the job.")
        return
    folder_name, folder_type = result
    folder_frame = Frame(folders_frame, height=35, width=600, bg="#f1f1f1")
    folder_frame.propagate(False)
    folder_frame.pack(pady=2, padx=3)

    def remove():
        for folder in folders:
            if folder["Frame"] == folder_frame:
                folder["Frame"].destroy()
                folders.remove(folder)
    Button(folder_frame, cursor="hand2", text="×", font=("TkDefaultFont", 14, "bold"), width=0, height=0, command=remove).pack(side=LEFT, padx=3)
    Label(folder_frame, bg=folder_frame.cget("bg"), text=shorten(folder_name, 20, placeholder="..."), font=("TkDefaultFont", 16)).pack(side=LEFT, padx=12)
    Label(folder_frame, bg=folder_frame.cget("bg"), text=folder_type, font=("TkDefaultFont", 16)).pack(side=RIGHT, padx=15)

    folders.append({"Name": folder_name, "Type": folder_type, "Frame": folder_frame})

def go():
        dir_to_sort = askdirectory(title="Choose where your files are at.", initialdir=path.join(path.expanduser("~"), "Desktop"))
        if not dir_to_sort: return
        for folder in folders:
            try:
                mkdir(path.join(dir_to_sort, folder["Name"]))
            except FileExistsError: pass
            except Exception as e:
                print(f"Error: {e}")
                continue

            Path = path.join(dir_to_sort, folder["Name"])
            if folder["Type"] == "Audio Files":
                for file in listdir(dir_to_sort):
                    if not path.isfile(path.join(dir_to_sort, file)): continue
                    if not file.endswith((".mp3", ".wav", ".ogg")): continue
                    sort_into(path.join(dir_to_sort, file), Path)
            elif folder["Type"] == "Video Files":
                for file in listdir(dir_to_sort):
                    if not path.isfile(path.join(dir_to_sort, file)): continue
                    if not file.endswith((".mp4", ".avi", ".ogv", ".mpeg", ".mpg", ".webm", ".wmv", ".mov", ".m4v")): continue
                    sort_into(path.join(dir_to_sort, file), Path)
            elif folder["Type"] == "Executables":
                for file in listdir(dir_to_sort):
                    if not path.isfile(path.join(dir_to_sort, file)): continue
                    if not file.endswith((".exe", ".msi")): continue
                    sort_into(path.join(dir_to_sort, file), Path)
            elif folder["Type"] == "Compressed Files":
                for file in listdir(dir_to_sort):
                    if not path.isfile(path.join(dir_to_sort, file)): continue
                    if not file.endswith((".rar", ".zip")): continue
                    sort_into(path.join(dir_to_sort, file), Path)
            elif folder["Type"] == "Image Files":
                for file in listdir(dir_to_sort):
                    if not path.isfile(path.join(dir_to_sort, file)): continue
                    if not file.endswith((".png", ".bmp", ".jpg", ".jpeg", ".jfif", ".gif", ".webp", ".ico", ".icns")): continue
                    sort_into(path.join(dir_to_sort, file), Path)
            elif folder["Type"] == "Documents":
                for file in listdir(dir_to_sort):
                    if not path.isfile(path.join(dir_to_sort, file)): continue
                    if not file.endswith((".txt", ".pub", ".doc", ".docx", ".pdf", ".txt", ".odt", ".rtf", ".html", ".htm", ".epub", ".xls", ".xlsx", ".ppt", ".pptx", ".md", ".csv", ".xml", ".json", ".pages")): continue
                    sort_into(path.join(dir_to_sort, file), Path)
        if askyesno("Success!", "Files sorted! Would you like to open your folder?"): startfile(dir_to_sort)

new_folder_button = Button(options_frame, cursor="hand2", text="New Folder", bg="#fff", command=add, width=20)
new_folder_button.pack(pady=3, padx=2)

new_folder_button.bind("<Enter>", lambda e: new_folder_button.config(bg="#f0f0f0"))
new_folder_button.bind("<Leave>", lambda e: new_folder_button.config(bg="#fff"))

go_button = Button(options_frame, cursor="hand2", text="Go!", bg="#fff", command=go, width=20)
go_button.pack(padx=2)

go_button.bind("<Enter>", lambda e: go_button.config(bg="#f0f0f0"))
go_button.bind("<Leave>", lambda e: go_button.config(bg="#fff"))

mainloop()
