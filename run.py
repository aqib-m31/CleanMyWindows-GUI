import argparse
from os import system


def main():
    parser = argparse.ArgumentParser(
        prog="Clean My Windows", description="Cleans junk files."
    )
    parser.add_argument("-i", "--install")
    args = parser.parse_args()

    if args.install == "y":
        install_requirements()
        
    from cleaner.main import App
    
    app = App()
    app.mainloop()


def install_requirements():
    with open("requirements.txt") as file:
        for pkg in file.readlines():
            system(f"pip install {pkg.strip()}")


if __name__ == "__main__":
    main()
