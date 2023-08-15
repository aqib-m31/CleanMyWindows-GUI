import argparse
from os import system


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        prog="Clean My Windows", description="Cleans junk files."
    )
    parser.add_argument("-i", "--install")
    args = parser.parse_args()

    # If install argument is provided, install requirements and provide instructions
    if args.install == "y":
        install_requirements()
        print("Requirements installed. To run the program, use: python run.py")
        return

    # Import and run the main program
    from cleaner.main import main

    main()


def install_requirements():
    """Install required packages from requirements.txt"""
    with open("requirements.txt") as file:
        for pkg in file.readlines():
            system(f"pip install -q {pkg.strip()}")


if __name__ == "__main__":
    main()
