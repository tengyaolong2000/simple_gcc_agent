import requests

prompt = "Tell me a joke"
response = requests.post("http://localhost:9000/generate", json={"prompt": prompt})
result = response.json()["response"]
print(result)

#ssh -L 9000:localhost:8000 2H100

