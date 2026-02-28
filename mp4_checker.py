import os
import subprocess
import csv
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- Find FFmpeg ---
def find_ffmpeg():
    exe_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Look in 'ffmpeg' subfolder
    ffmpeg_in_subfolder = os.path.join(exe_dir, "ffmpeg", "ffmpeg.exe")
    if os.path.isfile(ffmpeg_in_subfolder):
        return ffmpeg_in_subfolder

    # 2. Look in same folder as script/exe
    ffmpeg_local = os.path.join(exe_dir, "ffmpeg.exe")
    if os.path.isfile(ffmpeg_local):
        return ffmpeg_local

    # 3. Look in system PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path

    # 4. Not found
    return None

FFMPEG_PATH = find_ffmpeg()

# --- Global variable for CSV output ---
csv_file_path = "video_check_report.csv"

# --- Video Check Function ---
def check_mp4_ffmpeg(file_path):
    """Check MP4 using ffmpeg only."""
    if not FFMPEG_PATH:
        messagebox.showerror(
            "FFmpeg Error",
            "FFmpeg was not found.\n\nPlease place ffmpeg.exe inside a folder named 'ffmpeg' next to this program, "
            "or in the same folder as this program, or install FFmpeg."
        )
        return False, "FFmpeg not found"

    cmd = [FFMPEG_PATH, "-v", "error", "-i", file_path, "-f", "null", "-"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        return False, result.stderr.decode(errors="ignore").strip()
    return True, "Passed FFmpeg check"

# --- Scan Function ---
def scan_videos(root_folder):
    """Recursively scan 'video' folder for MP4s with progress bar."""
    global csv_file_path

    video_folder = os.path.join(root_folder, "video")
    if not os.path.exists(video_folder):
        messagebox.showerror("Error", f"No 'video' folder found in {root_folder}")
        return

    # Collect all MP4 files
    mp4_files = []
    for dirpath, _, filenames in os.walk(video_folder):
        for f in filenames:
            if f.lower().endswith(".mp4"):
                mp4_files.append(os.path.join(dirpath, f))

    total_files = len(mp4_files)
    if total_files == 0:
        messagebox.showinfo("No Files", "No MP4 files found in the video folder.")
        return

    results = []

    # Configure progress bar
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0
    root.update_idletasks()

    # Scan each file
    for idx, file_path in enumerate(mp4_files, start=1):
        status, message = check_mp4_ffmpeg(file_path)
        results.append([file_path, "OK" if status else "Corrupt", message])

        # Update progress bar
        progress_bar["value"] = idx
        progress_label.config(text=f"Checking file {idx} of {total_files}")
        root.update_idletasks()

    # Save report
    try:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Path", "Status", "Notes"])
            writer.writerows(results)
        messagebox.showinfo("Done", f"Scan complete. Report saved to:\n{csv_file_path}")
    except PermissionError:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "video_check_report.csv")
        with open(desktop_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Path", "Status", "Notes"])
            writer.writerows(results)
        messagebox.showwarning(
            "Permission Error",
            f"Could not save to {csv_file_path}.\nReport saved to Desktop instead:\n{desktop_path}"
        )

    progress_label.config(text="Scan complete.")

# --- GUI Functions ---
def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)

def save_csv_location():
    global csv_file_path
    file_selected = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        initialfile="video_check_report.csv"
    )
    if file_selected:
        csv_file_path = file_selected

def run_scan():
    folder = folder_path_var.get()
    if not folder:
        messagebox.showwarning("Input Needed", "Please select a folder.")
        return
    scan_videos(folder)

# --- GUI Setup ---
root = tk.Tk()
root.title("MP4 Video Checker")

folder_path_var = tk.StringVar()

tk.Label(root, text="Folder containing 'video' subfolder:").pack(pady=5)
tk.Entry(root, textvariable=folder_path_var, width=50).pack(padx=10)
tk.Button(root, text="Browse Folder...", command=browse_folder).pack(pady=5)

tk.Button(root, text="Select CSV Output Location", command=save_csv_location).pack(pady=5)
tk.Button(root, text="Check Videos", command=run_scan).pack(pady=10)

# Progress bar
progress_label = tk.Label(root, text="")
progress_label.pack()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

root.mainloop()
