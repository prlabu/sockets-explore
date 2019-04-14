import requests
import logging

# logging.basicConfig(level=logging.DEBUG)

req = requests.Session()
req.get('http://localhost:8080/flat.jpg')
req.get('http://localhost:8080/food.mp3')
req.get('http://localhost:8080/plainText.txt')

req.close()
