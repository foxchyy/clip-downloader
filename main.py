import youtube_dl
import ffmpeg
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog as fd

# Initialize the tk window
window = tk.Tk()
window.title('Twitch Clip Downloader')


# quiet stops ydl from spamming shit
ydl_opts = {
    'quiet': True
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

def vod_button_func():
    # if vod check is on show entries/labels for start & end also moves download button down
    if is_vod.get() == 1:
        start_entry.grid(column=1, row=3, sticky='ew')
        start_label.grid(column=0, row=3, sticky='ew')
        end_entry.grid(column=1, row=4, sticky='ew')
        end_label.grid(column=0, row=4, sticky='ew')
        download.grid(column=1, row=5, sticky='ew')
    # if it is 0 just remove all the entries/labels
    else:
        start_entry.grid_remove()
        end_entry.grid_remove()
        start_label.grid_remove()
        end_label.grid_remove()

# converts time hh:mm:s to seconds
def convert_to_seconds(time):
    split = time.split(':')
    hours = int(split[0]) * 60 * 60
    minutes = int(split[1]) * 60
    seconds = int(split[2])

    result = hours + minutes + seconds
    
    return result

# asks to open a folder & returns it's directory
def select_folder():
    folder = fd.askdirectory(
        title='Open a folder',
        initialdir='/',
        )
    return folder

def download_func():
    # gets the clip url and the name of the file from the entries
    clip_url = link_entry.get()
    name = name_entry.get()

    # sets folder equal to the selected directory
    folder = select_folder()

    # extracts info from the given link & gets only the url
    result = ydl.extract_info(clip_url, download=False)
    video_url = result['url']        

    # initialize ffmpeg input
    stream = ffmpeg.input(video_url)
    

    # if it is a vod get the start/end timestamps
    if is_vod.get() == 1: 
        start_timestmp = start_entry.get()
        end_timestmp = end_entry.get()
        
        # if the end timestamp is before the start timestamp initialize the ffmpeg input
        if convert_to_seconds(start_timestmp) < convert_to_seconds(end_timestmp):
            stream = ffmpeg.input(video_url, ss=start_timestmp, to=end_timestmp)
        # otherwise throw an error
        else:
            messagebox.showerror(title="ERROR", message="End time cannot be before start time.")
            return None

    try:
        # create the output from the input, with an ultrafast preset, fast decoding and loglevel quiet so it doesn't spam shit
        stream = ffmpeg.output(stream, preset='ultrafast', filename=f'{folder}/{name}.mp4', tune='fastdecode', loglevel='quiet')
        # run the output
        ffmpeg.run(stream)
        messagebox.showinfo(title="Done", message=f"'{name}' was downloaded.")
    
    except:
        messagebox.showerror(title="ERROR", message="An error occured. Please try again.")



# UI
greeting = ttk.Label(text="CHAMP'S TWITCH CLIP DOWNLOADER", font=('Bebas Neue', 24), foreground='Purple')
greeting.grid(column=1, row=0, sticky='ew')

link_label = ttk.Label(text="LINK", font=("Arial", 12, 'bold'))
link_label.grid(column=0,row=1, sticky='ew')
link_entry = ttk.Entry(width="50")
link_entry.grid(column=1, row=1, sticky='ew')

name_label = ttk.Label(text="NAME", font=("Arial", 12, 'bold'))
name_label.grid(column=0,row=2, sticky='ew')
name_entry = ttk.Entry(width="50")
name_entry.grid(column=1, row=2, sticky='ew')

start_entry = ttk.Entry(width="20")
start_label = ttk.Label(text="START TIME (hh:mm:s)", font=('Arial', 12, 'bold'))
end_entry = ttk.Entry(width="20")
end_label = ttk.Label(text="END TIME (hh:mm:s)", font=('Arial', 12, 'bold'))

is_vod = tk.IntVar()
vod_check = ttk.Checkbutton(window, text="VOD", variable=is_vod, onvalue=1, offvalue=0, command=vod_button_func)
vod_check.grid(column=2, row=1, sticky='ew')

download = ttk.Button(text='DOWNLOAD', width="40", command=download_func)
download.grid(column=1, row=3, pady=4, sticky='ew')

window.mainloop()
