import socket
import sys
from urlparse import urlparse

def parse_url(url):

	parsed_url = urlparse(url)

	scheme = parsed_url.scheme
	path = str(parsed_url.path)
	port = parsed_url.port if parsed_url.port else 80
	port_string = ':'+str(parsed_url.port) if parsed_url.port else ''
	host = parsed_url.hostname if parsed_url.hostname else url

	url = host

	if scheme == 'https': 
		sys.stderr.write('ERROR page requires encryption')
		sys.exit(1)

	if scheme == '': 
		sys.stderr.write('ERROR url does not start with http://')
		sys.exit(1)

	request_message = "GET " + path + " HTTP/1.1\r\nHost:" + host + port_string + "\r\n\r\n"

	return port, url, request_message


def main(): 

	url = str(sys.argv[1])

	port, url, request_message = parse_url(url)
	print(port, url, request_message)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((url, port))
	
	s.send(request_message)

	result = s.recv(4096)

	print(result)



if __name__ == "__main__": 
	main() 

