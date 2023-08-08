# Clean My Windows - GUI
[Clean My Windows](https://github.com/aqib-m31/clean-my-windows) with GUI.

**Cache Cleaner for Windows**

### This tool cleans following directories:
- `C:\Users\username\AppData\Local\Temp`
- `C:\Windows\Temp`
- `C:\Windows\Prefetch`
- `All directories with names cache or cache2 in C:\Users\username\AppData\Local`
---
### How to run
1. Clone the repository.
   
    ```bash
    git clone https://github.com/aqib-m31/CleanMyWindows-GUI
    ```
3. Change directory to Project the Directory.
   
    ```bash
    cd CleanMyWindows-GUI
    ```
3. Run the Script.
   
    ```bash
   python run.py
    ```
    
#### Run the Script with Command-Line Arguments for **first time.**
```bash
python run.py -i y
```
> **Note**: Command line arguments will instruct the script to install the required packages first

---
#### Building executable
`buil.py` script automates the process of installing `pyinstaller` and building the executable. Run
```bash
python build.py
```
If there were no errors, `dist\Clean My Windows\Clean My Windows.exe` will be the path of the executable.
