import requests

url = "https://goobeapi.onrender.com/goobe/query"
params = {'query': 'Hello, i am Maria, who are you?'}
response = requests.get(url, params=params)

# Verificar o conteúdo da resposta
print("Status Code:", response.status_code)
print("Response Text:", response.text)