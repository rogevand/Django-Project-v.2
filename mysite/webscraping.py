import requests
from bs4 import BeautifulSoup


page = requests.get('http://10.1.85.29/161111.1236/status.cgi')


soup = BeautifulSoup(page.content, 'html.parser')

print(soup.prettify()
)