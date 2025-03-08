import socket #allow to you to establis network connections over various network protocols such as TCP and UDP to send and recive data
import threading #allows you to have different parts of your process run concurrently

import rsa #it supports encryption and decryption, signing and veifying signatures

public_key, private_key = rsa.newkeys(2048)
public_partner = None
hostname = socket.gethostname()
IP = '10.25.104.69'
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IP)

# Hosting or joining option


ask = int(input("Welcome to our chat! Do you want to start a chat(press 1 on your keyboard) or do you want to join a chat?(press 2 on your keyboard)"))

if ask == 1:
    print("you picked option 1!")   
    print("your friend should connect at _ip_addess_:8080")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, 8081)
    try:
        server.bind(server_address)
        server.listen(1)
    except:
        exit()

    user, _ = server.accept()
    user.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(user.recv(2048))
elif ask == 2:
    print("you picked option 2!")
    user = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    user.connect((IP, 8081))
    public_partner = rsa.PublicKey.load_pkcs1(user.recv(2048))
    user.send(public_key.save_pkcs1("PEM"))
else:
    exit()
    
def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print(("You: ") + message)
    

def receiving_messages(c):
    while True:
        print(("Them: ") + rsa.decrypt(c.recv(1024), private_key).decode())
        

threading.Thread(target=sending_messages, args=(user,)).start()
threading.Thread(target=receiving_messages, args=(user,)).start()
        

