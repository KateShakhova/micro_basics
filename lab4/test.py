import requests


facade_url = "http://localhost:5000"


# Test POST request to facade-service
for i in range(10):
    msg = "Hello, my name is Kate {}".format(i)
    response = requests.post(facade_url, json={'msg': msg})
    print("POST request to facade-service:")
    print("Response:", response.json())

# Test GET request to facade-service
response = requests.get(facade_url)
print("\nGET request to facade-service:")
print("Response:", response.json())
