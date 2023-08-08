from os import system, popen
from re import search, IGNORECASE


def main():
    # Install Pyinstaller
    pyinstaller = popen("pip show pyinstaller").read()
    if not search(r"Name:\spyinstaller", pyinstaller, IGNORECASE):
        system("pip install pyinstaller")

    # Get path of customtkinter folder
    ctk = popen("pip show customtkinter").read()

    # Build if location of customtkinter folder found
    if matches := search(r"Location:\s(.+site-packages)", ctk, IGNORECASE):
        path = matches.group(1)
        system(
            f'pyinstaller --noconfirm --onedir --windowed --add-data {path}\\customtkinter;customtkinter/  run.py --name "Clean My Windows"'
        )
        print("Check dist\Clean My Windows\Clean My Windows.exe")
        return

    print("ERROR!")


if __name__ == "__main__":
    main()
