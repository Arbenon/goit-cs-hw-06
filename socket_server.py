import socket
import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Підключення до MongoDB
try:
    client = MongoClient('mongodb', 27017)  # 'mongodb' якщо використовується Docker Compose
    db = client.webapp
    collection = db.messages
    print("Connected to MongoDB")
except ServerSelectionTimeoutError as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit(1)

# Налаштування TCP серверу
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(5)
print("Socket server listening on port 5000...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data = client_socket.recv(1024)
    if not data:
        print("No data received, closing connection.")
        client_socket.close()
        continue
    
    try:
        message_data = json.loads(data)
        message_data['date'] = datetime.now().isoformat()
        print("Received data:", message_data)
        collection.insert_one(message_data)
        print("Message inserted into MongoDB")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    client_socket.close()
