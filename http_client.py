import socket
import sys
from urlparse import urlparse

CRLF = '\r\n\r\n'

def parse_url(url):

	parsed_url = urlparse(url)

	scheme = parsed_url.scheme
	path = str(parsed_url.path) if parsed_url.path else '/'
	port = parsed_url.port if parsed_url.port else 80
	port_string = ':'+str(parsed_url.port) if parsed_url.port else ''
	host = parsed_url.hostname if parsed_url.hostname else url

	url = host

	if scheme == 'https':
		sys.stderr.write('ERROR page requires encryption \n')
		sys.exit(1)

	if scheme == '':
		sys.stderr.write('ERROR url does not start with http:// \n')
		sys.exit(1)

	request_message = "GET " + path + " HTTP/1.1\r\nHost:" + host + port_string + "\r\n\r\n"
	
	return port, url, request_message

def receive_page_chunks(sock):

	CHUNK_SIZE = 1024

	chunks = []
	while True:
		chunk = sock.recv(CHUNK_SIZE)
		if chunk:
			chunks.append(chunk)
		else:
			break

	return ''.join(chunks)

def get_response_code(data):

	http_header = data.split(CRLF,1)[0]
	request = http_header.split('\n')[0]
	response_code = request.split()[1]

	return int(response_code)

def get_response_content_type(data):

	http_header = data.split(CRLF,1)[0].split('\n')
	print(http_header)
	for line in http_header:
		if len(line) > 12 and line[0:6] == 'Content':
			break
	content_type = line.split()[1].strip(';')

	return content_type == 'text/html'

def get_response_body(data):

	http_body = data.split(CRLF,1)[1]

	return http_body

def get_response_redirect_location(data):

	http_header = data.split(CRLF,1)[0].split('\n')
	for line in http_header:
		if line[0:8] == 'Location':
			break
	redirect_url = line.split()[1]

	return redirect_url

def GET_request(url):

	port, url, request_message = parse_url(url)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((url, port))

	s.send(request_message)

	chunks = receive_page_chunks(s)

	response_code = get_response_code(chunks)

	return response_code, chunks

def main():

	if len(sys.argv) < 2:
		sys.stderr.write("ERROR no URL provided \n")
		sys.exit(1)
	elif len(sys.argv) > 2:
		sys.stderr.write("ERROR more than one URL provided \n")
		sys.exit(1)

	url = str(sys.argv[1])
	num_redirect = 0
	while num_redirect < 10:

		response_code, chunks = GET_request(url)

		if response_code == 200:
			if get_response_content_type(chunks):
				sys.stdout.write(get_response_body(chunks))
			sys.exit(0)

		if response_code == 301 or response_code == 302:
			url = get_response_redirect_location(chunks)
			redirect_message = 'Redirected to: ' + str(url) + '\n'
			sys.stderr.write(redirect_message)
			num_redirect+=1
			continue

		if response_code >= 400:
			sys.stdout.write(chunks)
			sys.exit(1)

	sys.stderr.write("ERROR more than 10 redirects \n")
	sys.exit(1)

if __name__ == "__main__":
	main()
