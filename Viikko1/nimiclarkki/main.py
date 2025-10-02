import time
from time import sleep
time.sleep(0.1) # Wait for USB to become ready

name = input("What is your name? ")

if name == "Clark Kent":
    print("You are the Superman!")
else:
    print("You are an ordinary person.")
