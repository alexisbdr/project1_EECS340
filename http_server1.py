import socket
import sys 
from urlparse import urlparse 

def enable_server(port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((socket.gethostname(), port))

	s.listen()



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

	

if __name__ == "__main__":
	main()