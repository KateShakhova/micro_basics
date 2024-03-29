import requests
import json

facade_url = "http://localhost:5000"
logging_url = "http://localhost:5001"
messages_url = "http://localhost:5002"

# Test POST request to facade-service
msg = "Hello, my name is Kate"
response = requests.post(facade_url, json={'msg': msg})
print("POST request to facade-service:")
print("Response:", response.json())

# Test GET request to facade-service
response = requests.get(facade_url)
print("\nGET request to facade-service:")
print("Response:", response.json())

# Test GET request to logging-service
response = requests.get(logging_url)
print("\nGET request to logging-service:")
print("Response:", response.json())

# Test GET request to messages-service
response = requests.get(messages_url)
print("\nGET request to messages-service:")
print("Response:", response.text)