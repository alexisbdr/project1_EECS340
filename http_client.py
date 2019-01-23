import socket
import sys
from urlparse import urlparse

def main(): 

	url = str(sys.argv[1])

	parsed_url = urlparse(url)
	port = parsed_url.port if parsed_url.port else 80
	host = parsed_url.hostname if parsed_url.hostname else url

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	s.connect((url, port))

	request_message = "GET / HTTP/1.1\nHost:" + host + "\n\n"
	s.send(request_message)

	result = s.recv(4096)

	print(result)



if __name__ == "__main__": 
	main() 

