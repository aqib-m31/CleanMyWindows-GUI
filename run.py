from cleaner.main import App
import os, argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Clean My Windows", description="Cleans junk files."
    )
    parser.add_argument("-i", "--install")
    args = parser.parse_args()
    if args.install == "y":
        install_requirements()

    app = App()
    app.mainloop()


def install_requirements():
    with open("requirements.txt") as file:
        for pkg in file.readlines():
            os.system(f"pip install {pkg.strip()}")


if __name__ == "__main__":
    main()
