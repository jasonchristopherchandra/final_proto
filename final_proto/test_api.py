import requests

url = 'http://127.0.0.1:5000/translate_view'
data = {
"author": "test author",
"message": 'test_message',
}
response = requests.post(url, json=data)
print(response.json())