import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(2048)
public_partner = None
hostname = socket.gethostname()
IP = '127.0.0.1'
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IP)

# Hosting or joining option
ask = int(input("Welcome to our chat! Do you want to start a chat(press 1 on your keyboard) or do you want to join a chat?(press 2 on your keyboard)"))

if ask == 1:
    print("You picked option 1!")
    print("Your friend should connect at IP: 10.25.104.69:8081")
    
    # Create the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, 9999)
    server.bind(server_address)
    
    print("Server is waiting for a connection...")
    server.listen(1)

    # Accept the connection from the client
    user, _ = server.accept()
    print("Connection established with the client.")

    # Send public key to the client
    user.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(user.recv(2048))
    
elif ask == 2:
    print("You picked option 2!")
    # Connect to the server
    user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user.connect((IP, 9999))
    
    public_partner = rsa.PublicKey.load_pkcs1(user.recv(2048))
    user.send(public_key.save_pkcs1("PEM"))
else:
    exit()

# Sending messages function
def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)

# Receiving messages function
def receiving_messages(c):
    while True:
        print("Them: " + rsa.decrypt(c.recv(1024), private_key).decode())

# Start threads for sending and receiving messages
threading.Thread(target=sending_messages, args=(user,)).start()
threading.Thread(target=receiving_messages, args=(user,)).start()
