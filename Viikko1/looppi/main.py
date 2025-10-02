import time
from time import sleep
time.sleep(0.1) # Wait for USB to become ready

print("Ready to go!")

for i in range(10):
  print(f"Loop number {i}")
  sleep(0.1)
  if i == 9:
    print ("Loop Finished")
