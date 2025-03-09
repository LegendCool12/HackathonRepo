from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
import rsa

app = FastAPI()

# Generate RSA keys (public and private)
public_key, private_key = rsa.newkeys(2048)

# Store connected clients (username -> websocket)
connected_clients = {}

# Serve the static index.html when accessed through the browser
@app.get("/")
async def get_index():
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()

    # Send public key to the newly connected client
    public_key_pem = public_key.save_pkcs1(format='PEM')
    await websocket.send_text(public_key_pem.decode())

    # Add client to the connected clients list
    connected_clients[username] = websocket

    print(f"New connection: {username}")

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)  # Parse the received message
            print(f"Received message from {message_data['username']}: {message_data['message']}")

            # Broadcast the message to all other connected clients
            for client_username, client_websocket in connected_clients.items():
                if client_username != username:
                    await client_websocket.send_text(json.dumps({
                        "username": message_data['username'],
                        "message": message_data['message']
                    }))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        del connected_clients[username]  # Remove user from the connected clients list
        await websocket.close()  # Close the WebSocket connection
        print(f"Connection closed: {username}")

# Make sure to run FastAPI server with: uvicorn server:app --host 0.0.0.0 --port 8000
