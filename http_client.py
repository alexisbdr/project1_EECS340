import socket
import sys
from urlparse import urlparse

def parse_url(url):

	parsed_url = urlparse(url)

	scheme = parsed_url.scheme	
	port = parsed_url.port if parsed_url.port else 80
	host = parsed_url.hostname if parsed_url.hostname else url

	if scheme == 'https': 
		sys.stderr.write('ERROR page requires encryption')
		sys.exit(1)

	if scheme == '': 
		sys.stderr.write('ERROR url does not start with http://')
		sys.exit(1)

	if port != 80 : 
		request_message = "GET / HTTP/1.1\nHost:" + host + ":" + str(port) + "\n\n"
	else: 
		request_message = "GET / HTTP/1.1\nHost:" + host + "\n\n"

	return port, host, request_message


def main(): 

	url = str(sys.argv[1])

	port, host, request_message = parse_url(url)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((host, port))
	
	s.send(request_message)

	result = s.recv(4096)

	print(result)



if __name__ == "__main__": 
	main() 

