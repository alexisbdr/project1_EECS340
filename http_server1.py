import socket
import sys 
from urlparse import urlparse 


def check_command_input():

	if len(sys.argv) < 2: 
		sys.stderr.write("ERROR no port provided")
		sys.exit(1)
	elif len(sys.argv) > 2: 
		sys.stderr.write("ERROR more than one porrt provided")
		sys.exit(1)


class Socket:


	def __init__(self): 

		check_command_input()

		self.host = socket.gethostname if socket.gethostname else ''
		self.port = sys.argv[1]

		if self.port < 1024:
			sys.stderr.write('ERROR - port number is below 1024, please try again')
			sys.exit(1)

		create_socket()


	def create_socket(self):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.sock.bind((self.host, self.port))
	
		self
	def run_forever():

		while True: 

			sock.listen(1)

			(client_socket, client_address) = sock.accept()

			sock.recv(CHUNK)


def main(): 

	if len(sys.argv) < 2: 
		sys.stderr.write("ERROR no port provided")
		sys.exit(1)
	elif len(sys.argv) > 2: 
		sys.stderr.write("ERROR more than one porrt provided")
		sys.exit(1)

	port = int(sys.argv[1])

	if port < 1024: 
		sys.stderr.write('ERROR - port number must be above 1024')

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((socket.gethostname(), port))

	run_forever(s)



if __name__ == "__main__":
	Socket()