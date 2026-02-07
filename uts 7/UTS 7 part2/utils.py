import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk melanjutkan...")
    clear()
