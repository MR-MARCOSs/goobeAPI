import requests

url = "https://goobeapi.onrender.com/goobe/query"
#url = "https://44.226.145.213:10000/goobe/query"
params = {'query': 'summarize what was said in this video: https://www.youtube.com/watch?v=QMbx0dTWJIQ&pp=ygUSaG93IHRvIHByb2dyYW1taW5n'}
response = requests.get(url, params=params)

# Verificar o conteúdo da resposta
print("Status Code:", response.status_code)
print("Response Text:", response.text)