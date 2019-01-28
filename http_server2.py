import socket
import sys 
from urlparse import urlparse 
import os
import time
import signal
import select
import Queue


def signal_handler(sig, frame):

	sock.shutdown()


def get_last_modified_time(path):

	if platform.system() == 'Windows':

		return os.path.getctime(path)
	
	else:
	
		stat = os.stat(path)
	
		try:
	
			return stat.st_birthtime
	
		except AttributeError:
	
			return stat.st_mtime


def generate_http_header(code, path):
	
	responses = {
	200: '200 OK',
	403: '403 Forbidden',
	404: '404 Not Found'}

	http_header = 'HTTP/1.1 ' + responses[code] + '\n'
	
	current_date = 'Date: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + ' GMT\n'
	http_header += current_date

	'''
	Last modified stuff
	if code == 200: 
		last_modified_time = 'Last Modified: ' + get_last_modified_time(path) + ' GMT' 
	'''
	server_name = 'Server: http_server1 (Simple)\n'
	http_header += server_name

	if code == 200: 
		http_header += 'Content-Type: text/html; charset=UTF-8\n'

	CLRF = '\r\n\r\n'
	connection_close = 'Connection: Close' + CLRF
	http_header+=connection_close

	print(http_header)
	
	return http_header 


def generate_http_response(code, path):

	response_header = generate_http_header(code, path)

	if code == 200:
		try:
			file = open(path, 'r')
			response_body = file.read()
		except: 
			#If failure, 404 Not Found
			generate_http_response(404, path)
	
	elif code == 403: 
		
		response_body = "<html><body><p>Error 403: Forbidden</p>"
	
	elif code == 404:
		
		response_body = "<html><body><p>Error 404: Not Found</p>"

	response = response_header + response_body

	return response


def get_request_method(data):

	http_header = data.split('\n')[0].split()

	return str(http_header[0])


def get_file_name(data):

	http_header = data.split('\n')[0].split()

	file_name = http_header[1]

	if file_name == '/':
		return 'index.html'

	return file_name.strip('/')


def ends_with_(name):

	if name[-4:] == ".htm" or name[-4:] == "html": 
		return False


def check_command_input():

	if len(sys.argv) < 2: 
		sys.stderr.write("ERROR no port provided")
		sys.exit(1)
	elif len(sys.argv) > 2: 
		sys.stderr.write("ERROR more than one porrt provided")
		sys.exit(1)


class Socket:

	CHUNK = 1024

	def __init__(self): 

		check_command_input()

		self.host = ""
		self.port = int(sys.argv[1])

		if self.port < 1024:
			sys.stderr.write('ERROR - port number is below 1024, please try again')
			sys.exit(1)

		self.create_socket()


	def shutdown(self): 

		self.sock.shutdown(socket.SHUT_RDWR)

		sys.exit(1)


	def create_socket(self):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sock.setblocking(0)
		
		self.sock.bind((self.host, self.port))

		self.sock.listen(10)

		self.run_forever()


	def handle_request(self, data):

		if get_request_method(data) == "GET": 

			file_name = get_file_name(data) 
			
			#Empty file path or file does not exist - Error 404 Not Found
			if not file_name or not os.path.exists(file_name):
				http_response = generate_http_response(404, file_name)

			#Wrong file type - 403
			elif ends_with_(file_name): 
				http_response = generate_http_response(403, file_name)

			else: 
				http_response = generate_http_response(200, file_name)

			client_socket.send(http_response)

			client_socket.close()

		
	def run_forever(self):

		inputs = [ self.sock ]
		outputs = []
		message_queues = {}

		while inputs: 

			try:

				readable, writable, exceptional = select.select(inputs, outputs, inputs)
				for s in readable: 
					if s is self.sock:
						client_socket, client_address = s.accept()
						client_socket.setblocking(0)
						inputs.append(client_socket)
						message_queues[client_socket] = Queue.Queue()
					else: 
						data = s.recv(self.CHUNK)
						if data: 
							data = handle_request(data)
							message_queues[s].put(data)
							if s not in outputs:
								outputs.append(s)
						else: 
							if s in outputs:
								outputs.remove(s)
							inputs.remove(s)
							s.close()
							del message_queues[s]
					
					for s in writable: 
						try: 
							http_response = message_queues[s].get_nowait()
						except Queue.Empty:
							outputs.remove(s)
						else:
							s.send(http_response) 

					for s in exceptional: 
						inputs.remove(s)
						if s in outputs:
							outputs.remove(s)
						s.close()
						del message_queues[s]
				
			except (KeyboardInterrupt, SystemExit): 

				self.sock.shutdown(socket.SHUT_RDWR)

				sys.exit(1)


if __name__ == "__main__":
	Socket()