import socket
from bs4 import BeautifulSoup

HOST = '127.0.0.1'
PORT = 8080


def request_data(page_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    request_server = f"GET {page_path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client.send(request_server.encode('utf-8'))

    response_data = b''
    while True:
        chunk = client.recv(1024)
        if not chunk:
            break
        response_data += chunk

    return response_data.decode('utf-8')


pages = ["/", "/about", "/contact", "/products"]
parsed_pages = []
product_links = []
products_info = []

for path in pages:
    response = request_data(path)
    header, body = response.split('\n\n', 1)

    if path == "/products":
        soup = BeautifulSoup(response, 'html.parser')
        link_tags = soup.find_all('a', href=True)
        product_links = [link['href'] for link in link_tags]
        continue

    parsed_pages.append(body.strip())

for link in product_links:
    response = request_data(link)
    soup = BeautifulSoup(response, 'html.parser')
    product_info = {}

    for i in soup.find_all('tr'):
        header = i.find('th')
        data = i.find('td')

        if not (header and data):
            continue

        header = header.text.strip()
        data = data.text.strip()
        product_info[header] = data

    products_info.append(product_info)

print("Pages content:")
for i in parsed_pages:
    print(i)

print("\nProducts info:")
for i in products_info:
    print(i)

