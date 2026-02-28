\# Media Quality Automation Tool (MP4 Checker)



\## Overview



The Media Quality Automation Tool is a Python-based desktop application designed to automate media file quality validation using FFmpeg.



This tool was created to reduce manual video review time by automatically detecting corrupted or problematic MP4 files before analyst review.



Business Impact:

\- Reduced manual media review time from approximately 2 hours to 15 minutes per day

\- Improved consistency and reliability of media quality checks

\- Enabled non-technical users through a simple GUI interface



---



\## Features



\- Automated MP4 file validation

\- FFmpeg-powered media analysis

\- Tkinter GUI for non-technical users

\- Batch processing support

\- Detection of corrupt or unreadable files

\- Executable packaging support (PyInstaller)



---



\## Tech Stack



\- Python

\- FFmpeg

\- Tkinter

\- PyInstaller (optional for packaging)



---



\## Project Structure



mp4\_Checker/



├── mp4\_checker.py  

├── requirements.txt  

├── README.md  

├── .gitignore  



├── ffmpeg/        (optional local ffmpeg folder - ignored in git)  

├── build/         (pyinstaller build output - ignored)  

└── dist/          (executable output - ignored)



---



\## Installation



\### 1. Clone the repository



git clone https://github.com/mark011062/media-quality-automation-tool.git  

cd media-quality-automation-tool



\### 2. Create a virtual environment (recommended)



Windows:



python -m venv venv  

venv\\Scripts\\activate



\### 3. Install dependencies



pip install -r requirements.txt



---



\## FFmpeg Setup (Required)



This tool relies on FFmpeg.



\### Option A — Install globally (recommended)



1\. Download FFmpeg from:  

https://ffmpeg.org/download.html



2\. Add FFmpeg to your system PATH.



3\. Verify installation:



ffmpeg -version



\### Option B — Local folder



Place ffmpeg.exe inside:



ffmpeg/



Note: this folder is ignored in GitHub to avoid large file issues.



---



\## Running the Application



python mp4\_checker.py



---



\## Building an Executable (Optional)



pyinstaller mp4\_checker.spec



Output will be generated in:



dist/



---



\## Use Case



This tool automates media quality assurance workflows by identifying problematic media files before manual review, reducing analyst workload and improving process reliability.



---



\## Future Improvements



\- Logging and reporting dashboard

\- Exportable quality reports

\- Parallel processing for large batches

\- CLI mode for automation pipelines



---



\## Author



Mark Young  

GitHub: https://github.com/mark011062

