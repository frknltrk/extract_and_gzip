import tkinter as tk
from tkinter import filedialog
import subprocess
import os
#import winsound

# Program metadata
AUTHOR = "Furkan Ünlütürk"
YEAR = 2024
VERSION = "1.0"

# def play_sound():
#     winsound.PlaySound("audio.wav", winsound.SND_FILENAME)

def browse_7zip_folder():
    seven_zip_folder = filedialog.askdirectory(title="Select 7-Zip folder", initialdir="C:/Program Files/7-Zip")
    seven_zip_folder_entry.delete(0, tk.END)
    seven_zip_folder_entry.insert(0, seven_zip_folder)
    
def browse_input_files():
    input_files = filedialog.askopenfilenames(title="Select input files", filetypes=[("Archive files", "*.7z;*.zip")])
    input_files_entry.delete(0, tk.END)
    input_files_entry.insert(0, " ".join(input_files))

def browse_output_directory():
    output_directory = filedialog.askdirectory(title="Select output directory")
    output_directory_entry.delete(0, tk.END)
    output_directory_entry.insert(0, output_directory)
    
def extract_and_compress():
    input_files = input_files_entry.get()
    output_directory = output_directory_entry.get()
    seven_zip_folder = seven_zip_folder_entry.get()

    if not input_files or not output_directory:
        result_label.config(text="Please select input files and output directory.")
        return
        
    # Set the system PATH to include the 7-Zip folder
    os.environ["PATH"] = seven_zip_folder + ";" + os.environ["PATH"]

    input_files_list = input_files.split()
    
    for input_file in input_files_list:
        # Extract *.xml files from each *.7z file
        subprocess.run(["7z", "x", "-o" + output_directory, input_file])

        # Gzip each extracted *.xml file separately
        for root, dirs, files in os.walk(output_directory):
            for file in files:
                if not file.endswith(".gz"):
                    file_path = os.path.join(root, file)
                    subprocess.run(["7z", "a", "-tgzip", f"{file_path}.gz", file_path])
                    os.remove(file_path)

    result_label.config(text="Extraction and compression completed.")

# GUI setup
root = tk.Tk()
root.title("Extract and gzip")

# Set the icon
# root.iconbitmap("icon.ico")

# Play frog sound on launch
# play_sound()

# 7-Zip Folder
seven_zip_folder_label = tk.Label(root, text="7-Zip Folder:")
seven_zip_folder_label.grid(row=0, column=0, padx=10, pady=5)

seven_zip_folder_entry = tk.Entry(root, width=50)
seven_zip_folder_entry.grid(row=0, column=1, padx=10, pady=5)
seven_zip_folder_entry.insert(0, "C:/Program Files/7-Zip")

browse_seven_zip_folder_button = tk.Button(root, text="Browse", command=browse_7zip_folder)
browse_seven_zip_folder_button.grid(row=0, column=2, padx=10, pady=5)

# Input Files
input_files_label = tk.Label(root, text="Input Files:")
input_files_label.grid(row=1, column=0, padx=10, pady=5)

input_files_entry = tk.Entry(root, width=50)
input_files_entry.grid(row=1, column=1, padx=10, pady=5)

browse_input_files_button = tk.Button(root, text="Browse", command=browse_input_files)
browse_input_files_button.grid(row=1, column=2, padx=10, pady=5)

# Output Directory
output_directory_label = tk.Label(root, text="Output Directory:")
output_directory_label.grid(row=2, column=0, padx=10, pady=5)

output_directory_entry = tk.Entry(root, width=50)
output_directory_entry.grid(row=2, column=1, padx=10, pady=5)

browse_output_directory_button = tk.Button(root, text="Browse", command=browse_output_directory)
browse_output_directory_button.grid(row=2, column=2, padx=10, pady=5)

# Extract and Compress Button
extract_button = tk.Button(root, text="Extract and GZIP", command=extract_and_compress)
extract_button.grid(row=3, column=0, columnspan=3, pady=10)

# Result Label
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=3, pady=10)

# About Section
about_frame = tk.Frame(root)
about_frame.grid(row=5, column=0, columnspan=3, pady=10)

about_label = tk.Label(about_frame, text=f"{AUTHOR} - {YEAR} - {VERSION}")
about_label.pack()

root.mainloop()
